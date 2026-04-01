---
date: "2026-04-01T11:37:18+05:30"
title: "I Rebuilt Traceroute in Rust and It Was Simpler Than I Expected"
description:
  "I never understood how traceroute discovers each hop. Turns out it's a clever
  TTL trick, and about 80 lines of Rust."
tags:
  - "rust"
  - "networking"
  - "traceroute"
  - "systems-programming"
cover:
  image: "/images/posts/traceroute/concept.png"
  alt:
    "Sequence diagram showing how traceroute discovers network hops using
    incrementing TTL values and ICMP replies"
---

Previously, I wrote about [setting up a Tailscale exit node][tailscale] and
appreciated how traffic gets wired to my home network. I wanted to understand
`traceroute` a bit. I've never contemplated how it works, and now feels like as
good a time as any to do just that. I mean, now's the time to rewrite it in
Rust.

## What _does_ traceroute do?

I've just used traceroute to investigate how my query is travelling from my
computer to my router and to the internet, finally reaching the end server.

```text
$ traceroute -m 15 -w 2 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 15 hops max, 40 byte packets
 1  <tailscale-gw> (<tailscale-ip>)  6.553 ms  5.323 ms  5.384 ms
 2  <home-router> (<router-ip>)  7.183 ms  6.271 ms  4.607 ms
 3  * <isp-gateway> (<isp-gateway-ip>)  7.189 ms *
 4  * * *
 5  * * *
 6  * * *
 7  <isp-hop-1> (<isp-hop-1-ip>)  284.000 ms  229.201 ms  257.805 ms
 8  72.14.223.26 (72.14.223.26)  11.642 ms  12.643 ms  12.868 ms
 9  * * *
10  dns.google (8.8.8.8)  12.268 ms  11.907 ms  11.766 ms
```

At a cursory level, it looks like it's asking "where is this IP" at each level,
and I'm not sure how it does that.

Traceroute doesn't actually ask this "where is this IP." It uses a TTL trick.

But to understand it, let's write some code.

1. Every IP packet has a TTL (Time To Live) field - a counter that starts at
   some value (usually 64)
2. Every router that forwards the packet decrements TTL by 1.
3. When a router decrements TTL to 0, it drops the packet and sends back an ICMP
   "Time Exceeded" message to the sender.
4. That ICMP message contains the router's IP address.

So if we send packets with TTL=1, the first router replies. TTL=2, the second
router replies. And so on, until we reach the destination. That's traceroute.

{{< tip title="The core idea" >}} Traceroute is just sending packets that are
designed to die at each hop, then listening for the error messages. {{< /tip >}}

## The first probe

Let's start with a single function that sends one UDP packet at a given TTL and
listens for the ICMP reply. Why UDP? Because these are throwaway packets
designed to die in transit. We don't need TCP's handshake or delivery
guarantees. We just fire bytes at a port and wait for routers to tell us they
dropped them.

```rust
use socket2::{Domain, Protocol, SockAddr, Socket, Type};
use std::mem::MaybeUninit;
use std::net::{Ipv4Addr, SocketAddrV4};
use std::time::Duration;

fn probe(target: Ipv4Addr, ttl: u32) -> std::io::Result<Option<Ipv4Addr>> {
    // UDP socket to send the probe
    let send_sock = Socket::new(Domain::IPV4, Type::DGRAM, Some(Protocol::UDP))?;
    send_sock.set_ttl_v4(ttl)?;

    // Raw ICMP socket to catch Time Exceeded replies
    let recv_sock = Socket::new(
        Domain::IPV4,
        Type::from(libc::SOCK_RAW),
        Some(Protocol::ICMPV4),
    )?;
    recv_sock.set_read_timeout(Some(Duration::from_secs(2)))?;

    // Send UDP packet to high port (33434)
    let dest = SockAddr::from(SocketAddrV4::new(target, 33434));
    send_sock.send_to(&[0u8; 32], &dest)?;

    // Listen for ICMP reply
    let mut buf = [MaybeUninit::<u8>::uninit(); 512];
    match recv_sock.recv(&mut buf) {
        Ok(n) => {
            // Safety: recv wrote n bytes into buf
            let buf: &[u8] = unsafe {
                std::slice::from_raw_parts(buf.as_ptr() as *const u8, n)
            };
            // IP header is first 20 bytes, source IP is at bytes 12-16
            if buf.len() >= 20 {
                let ip = Ipv4Addr::new(buf[12], buf[13], buf[14], buf[15]);
                Ok(Some(ip))
            } else {
                Ok(None)
            }
        }
        Err(_) => Ok(None), // timeout = no reply (*)
    }
}

fn main() -> std::io::Result<()> {
    let target = Ipv4Addr::new(8, 8, 8, 8); // Google DNS
    for ttl in 1..=15 {
        let hop = probe(target, ttl)?;
        match hop {
            Some(ip) => println!("{:>2}  {}", ttl, ip),
            None => println!("{:>2}  *", ttl),
        }
        if hop == Some(target) {
            break;
        }
    }
    Ok(())
}
```

Let's walk through this.

**Lines 7-9**: We create a regular UDP socket and set its TTL. This is the key
trick; we're deliberately setting a low TTL so the packet dies before reaching
the destination.

**Lines 12-17**: A second socket, this time a raw ICMP socket. This one listens
for _all_ ICMP packets arriving at our machine, including the "Time Exceeded"
replies from routers that dropped our short-lived UDP packet. We need
`libc::SOCK_RAW` here because `socket2` doesn't expose raw socket types
directly, and we need root/sudo to open it.

**Lines 20-21**: We send 32 bytes of zeros to port 33434 on the target. The
content doesn't matter. Port 33434 is the traditional traceroute port; nothing
listens there, so when our packet finally _does_ reach the destination, the
target responds with ICMP "Port Unreachable" instead of "Time Exceeded," which
is how we know we've arrived.

**Lines 24-38**: We read from the raw ICMP socket. The reply is a raw IP packet;
the first 20 bytes are the IP header, and bytes 12-15 contain the source address
of whoever sent the ICMP reply (that's the router that dropped our packet). We
use `MaybeUninit` because Rust won't let us read uninitialized memory; the
`unsafe` block is safe here since `recv` tells us exactly how many bytes it
wrote.

**Lines 42-55**: The main loop. We increment TTL from 1 to 15, printing each
hop. When the responding IP matches our target, we've reached the destination
and break out.

This needs `sudo` to run because of the raw ICMP socket.

```text
$ sudo cargo run
 1  <tailscale-ip>
 2  <router-ip>
 3  <isp-gateway-ip>
 4  *
 5  *
 6  *
 7  <isp-hop-1-ip>
 8  72.14.223.26
 9  *
10  8.8.8.8
```

It works! We can see our Tailscale gateway, home router, ISP, and Google's
network. But there are two problems: it doesn't know when to stop (it runs all
the way to hop 15), and we only get one probe per TTL with no timing
information.

## Some Simplifications

- Traceroute increments the port for each probe, but conventionally, the
  original traceroute by Van Jacobson used 33434. Incrementing the port for each
  probe helps match replies to specific probes, since the original UDP header is
  embedded inside the ICMP Time Exceeded reply.

- Traceroute also _does_ support a TCP mode with `-T`, to account for networks
  where firewalls block UDP but allow TCP through. The principle, however, is
  the same. Set a low TTL, let the packet die, and read the ICMP error.

## What is ICMP?

ICMP stands for Internet Control Message Protocol. It's the error reporting
protocol for the internet, not a data transport. I've _seen_ ICMP errors before
without realizing it. `ping`'s "Destination Host Unreachable" is ICMP type 3.
Similarly, "Time Exceeded" is ICMP Type 11, and this is what we rely on.

I think of it this way: if I mail a letter and the recipient writes back "I
don't know what this is about," that's an HTTP error. If the postal service
returns the letter stamped "address doesn't exist," that's ICMP.

Here's what the ICMP reply packet looks like when we receive it on the raw
socket:

![ICMP packet layout showing IP header, ICMP message, and embedded original packet](/images/posts/traceroute/packet-layout.png)

The IP header comes first (bytes 0-19), then the ICMP message starts at byte 20.
The ICMP payload also contains our original packet's headers, which is how real
traceroute matches replies to specific probes.

Looking at our code, this is the part where we parse the ICMP reply:

```rust
let buf: &[u8] = unsafe {
    std::slice::from_raw_parts(buf.as_ptr() as *const u8, n)
};
// IP header is first 20 bytes, source IP is at bytes 12-16
if buf.len() >= 20 {
    let ip = Ipv4Addr::new(buf[12], buf[13], buf[14], buf[15]);
    Ok(Some(ip))
}
```

Right now we only read the source IP from the IP header. But the ICMP message
itself starts at byte 20, and its first byte is the **type**. We're ignoring it
completely, which is why our traceroute doesn't know when to stop. If we checked
`buf[20]`, we could distinguish between Type 11 (Time Exceeded, meaning a router
along the way) and Type 3 (Destination Unreachable, meaning we've arrived).

This raw byte parsing is a bit of an unnecessary hard mode. The `pnet_packet`
crate handles all of this idiomatically, but I wanted to understand what's
actually in the packet.

## Knowing when to stop

Let's fix our traceroute so it knows when it's arrived. First, we replace the
`Option<Ipv4Addr>` return type with an enum that captures the three possible
outcomes:

```rust
enum ProbeResult {
    Hop(Ipv4Addr),     // Type 11 - Time Exceeded
    Reached(Ipv4Addr), // Type 3 - Destination Unreachable
    Timeout,           // No reply
}
```

Then we check `buf[20]` (the ICMP type byte) after extracting the source IP:

```rust
if buf.len() >= 21 {
    let ip = Ipv4Addr::new(buf[12], buf[13], buf[14], buf[15]);
    match buf[20] {
        11 => Ok(ProbeResult::Hop(ip)),
        3  => Ok(ProbeResult::Reached(ip)),
        _  => Ok(ProbeResult::Timeout),
    }
}
```

And the main loop can now break when we get `Reached`:

```rust
match hop {
    ProbeResult::Hop(ip) => println!("{:>2}  {}", ttl, ip),
    ProbeResult::Reached(ip) => {
        println!("{:>2}  {}", ttl, ip);
        break;
    }
    ProbeResult::Timeout => println!("{:>2}  *", ttl),
}
```

Funnily enough, while running this, I discovered a bug with the typecheck. It is
too naive and trusting. What we need to do, is to say we have "reached" only if
the ip is equal to the target IP. Otherwise, we get this when running the code.

```text
$ sudo cargo run
 1 <tailscale-ip>
 2 <router-ip>
 3 192.168.0.1
```

```rust
match buf[20] {
  11 => Ok(ProbeResult::Hop(ip)),
  3 if ip == target => Ok(ProbeResult::Reached(ip)),
  3 => Ok(ProbeResult::Hop(ip)),
  _ => Ok(ProbeResult::Timeout),
}
```

With this fix, our traceroute correctly stops at `8.8.8.8`:

```text
$ sudo cargo run
 1  <tailscale-ip>
 2  <router-ip>
 3  <isp-gateway-ip>
 4  *
 5  *
 6  *
 7  <isp-hop-1-ip>
 8  72.14.223.26
 9  *
10  8.8.8.8
```

## Adding timing

Our output is missing timing. Real traceroute shows round-trip time for each
probe. The fix is straightforward: `Instant::now()` before send, `elapsed()`
after recv. We update the enum to carry the duration:

```rust
use std::time::Instant;

enum ProbeResult {
    Hop(Ipv4Addr, Duration),
    Reached(Ipv4Addr, Duration),
    Timeout,
}
```

Then in `probe`, we wrap the send/recv in a timer:

```rust
let start = Instant::now();
send_sock.send_to(&[0u8; 32], &dest)?;

// ... recv logic ...
let elapsed = start.elapsed();
// return ProbeResult::Hop(ip, elapsed) etc.
```

And print it in milliseconds:

```rust
ProbeResult::Hop(ip, rtt) => {
    println!("{:>2}  {}  {:.3} ms", ttl, ip, rtt.as_secs_f64() * 1000.0)
}
```

```text
$ sudo cargo run
 1  <tailscale-ip>  6.091 ms
 2  <router-ip>  4.907 ms
 3  <isp-gateway-ip>  6.363 ms
 4  *
 5  *
 6  *
 7  <isp-hop-1-ip>  12.652 ms
 8  72.14.223.26  12.196 ms
 9  *
10  8.8.8.8  12.197 ms
```

Now we can see latency at each hop. The jump from ~6 ms (local ISP) to ~12 ms at
hop 7 is where our traffic leaves the local network and enters Google's.

## Three probes per hop

Traceroute sends three probes at each TTL. That's why we see 3 timing values per
hop in the original output:

```text
8 72.14.223.26 11.642 ms 12.643 ms 12.868 ms
```

I wondered what this was, but traceroute does this for three reasons:

- Variance: Network latency fluctuates. One measurement could be an outlier.
  Three gives a feel for consistency.
- Reliability: If one probe times out but the other two get replies, we still
  see the hop. A single `*` among real times means "flaky" not "dead".
- Load balancer detection - If different probes hit different IPs at the same
  TTL, we know there is a load balancer. In fact, when I originally started this
  blogpost, I used `github.com` as a destination and I kept hitting the load
  balancer.

In code, it's just wrapping the existing `probe()` call in a small inner loop.
We track the last IP seen and only print it when it changes, so the output stays
clean:

```rust
let mut reached = false;
let mut last_ip: Option<Ipv4Addr> = None;
print!("{:>2}  ", ttl);
for _ in 0..3 {
    match probe(target, ttl)? {
        ProbeResult::Hop(ip, rtt) => {
            if last_ip != Some(ip) {
                print!("{}  ", ip);
                last_ip = Some(ip);
            }
            print!("{:.3} ms  ", rtt.as_secs_f64() * 1000.0);
        }
        ProbeResult::Reached(ip, rtt) => {
            if last_ip != Some(ip) {
                print!("{}  ", ip);
                last_ip = Some(ip);
            }
            print!("{:.3} ms  ", rtt.as_secs_f64() * 1000.0);
            reached = true;
        }
        ProbeResult::Timeout => print!("*  "),
    }
}
println!();
if reached { break; }
```

```text
$ sudo cargo run
 1  <tailscale-ip>  5.713 ms  4.993 ms  4.739 ms
 2  <router-ip>  5.355 ms  5.082 ms  4.998 ms
 3  *  *  *
 4  *  *  *
 5  *  *  *
 6  *  *  *
 7  <isp-hop-1-ip>  15.658 ms  12.088 ms  11.362 ms
 8  72.14.223.26  11.978 ms  12.555 ms  12.344 ms
 9  *  *  *
10  8.8.8.8  14.246 ms  13.244 ms  12.892 ms
```

That's starting to look like the real thing.

## Comparing with real traceroute

At this point, I was happy. I understood more about traceroute than I ever knew.
But I wanted to figure out what my implementation was lacking.

| Feature                     | Real traceroute         | Ours             |
| --------------------------- | ----------------------- | ---------------- |
| TTL incrementing            | Yes                     | Yes              |
| ICMP type checking          | Yes                     | Yes              |
| Timing (RTT)                | Yes                     | Yes              |
| 3 probes per hop            | Yes                     | Yes              |
| DNS reverse lookup          | Yes (e.g. `dns.google`) | No               |
| Port incrementing per probe | Yes (33434, 33435...)   | No (fixed 33434) |
| ICMP Echo mode (`-I`)       | Yes                     | No (UDP only)    |
| TCP mode (`-T`)             | Yes                     | No               |
| IPv6 support                | Yes (`traceroute6`)     | No               |

## What traceroute doesn't show

While building this, I realized that traceroute's output looks like a map of the
network, but it's more of a sketch. There are things happening that it can't
reveal:

1. Asymmetric return paths : the ICMP reply from each router takes its own route
   back, which might be completely different from the forward path. The output
   shows forward-path routers but there's no way to know how the replies got
   back.
2. MPLS tunnels: packets can traverse multiple routers inside a label-switched
   path but traceroute shows it as one hop or none.
3. Load balancer path splitting: consecutive probes at the same TTL can hit
   different routers. The "path" we see is not a single actual path any packet
   took. I experienced this with the `github.com` attempt.
4. ICMP rate limiting: Those `* * *` hops aren't necessarily dead routers. Many
   routers deprioritize or drop ICMP to save CPU. The packets pass through fine;
   the router just doesn't bother replying.

## Why Do We See `*`?

After all this, I was still a little confused why we would see `* * *` rows. In
our code, we print this when we get a timeout, but we don't `break` the loop.
Can we get stuck in a `*` limbo if we didn't limit our hops?

We see `*` because:

1. ICMP Rate Limiting: the router is healthy and forwarding packets fine, but it
   deprioritizes generating ICMP Time Exceeded replies to save CPU. This is the
   most common reason.
2. Firewall blocking: the router or a firewall in front of it drops ICMP
   outright. Corporate and cloud firewalls do this aggressively.
3. Firewall blocking UDP on port 33434: the router drops our probe before it
   even gets a chance to decrement TTL. The packet never dies naturally.
4. Read timeout: the router did reply, but the reply took longer than our
   2-second timeout to arrive (rare on modern networks).
5. Reply routed elsewhere: The ICMP reply was generated but got lost or routed
   to a different path and never reached us.

`*` means "we didn't get a reply," not "there's nothing there." Our traceroute
output proves this - the hops 3-6 are all `*` but hop `7` still shows up,
meaning packets are passing through those silent routers just fine.

## Why does this need sudo?

I kept having to type `sudo cargo run` every time, and it bugged me. Regular
`traceroute` doesn't need that. So I looked into it.

Our code opens a `SOCK_RAW` ICMP socket to read replies directly. Raw sockets
are a privileged operation because they can sniff arbitrary network traffic, so
the kernel requires root.

System `traceroute` gets around this because it's installed with the **setuid
bit** set. Running `ls -la $(which traceroute)` shows something like
`-r-xr-sr-x` with the `s` flag, which means the binary runs with elevated
privileges regardless of who calls it.

On macOS, there's a third option: ICMP datagram sockets (`SOCK_DGRAM` with
`IPPROTO_ICMP`) that the kernel allows for unprivileged users. More restricted
than raw sockets, but enough for basic ping and traceroute.

## Wrapping up

I started this exercise as I was thinking deeply about [Tailscale][tailscale].
This is part of a larger effort I'm on: spending several evenings trying to
understand more of the modern internet. I'm reading the [WireGuard][wireguard]
whitepapers next, and digging deeper into how Tailscale's control plane works.
There's a lot happening in this space that's exciting to me, from a distributed
systems perspective and from a programming one.

I call this an evening well spent. One of my previous companies blocked `ping`
and it messed up my mental model all the time when I was there. I'm glad I can
write my own traceroute and debug things if a future company chooses to somehow
prevent it as well.

The code for this post is on [GitHub][repo]. Here's the final version:

```rust
use socket2::{Domain, Protocol, SockAddr, Socket, Type};
use std::mem::MaybeUninit;
use std::net::{Ipv4Addr, SocketAddrV4};
use std::time::{Duration, Instant};

enum ProbeResult {
    Hop(Ipv4Addr, Duration),     // Type 11 - Time Exceeded
    Reached(Ipv4Addr, Duration), // Type 3 - Destination Unreachable
    Timeout,                     // No reply
}

fn probe(target: Ipv4Addr, ttl: u32) -> std::io::Result<ProbeResult> {
    let send_sock = Socket::new(Domain::IPV4, Type::DGRAM, Some(Protocol::UDP))?;
    send_sock.set_ttl_v4(ttl)?;

    let recv_sock = Socket::new(
        Domain::IPV4,
        Type::from(libc::SOCK_RAW),
        Some(Protocol::ICMPV4),
    )?;
    recv_sock.set_read_timeout(Some(Duration::from_secs(2)))?;

    let dest = SockAddr::from(SocketAddrV4::new(target, 33434));
    let start = Instant::now();
    send_sock.send_to(&[0u8; 32], &dest)?;

    let mut buf = [MaybeUninit::<u8>::uninit(); 512];
    match recv_sock.recv(&mut buf) {
        Ok(n) => {
            let buf: &[u8] =
                unsafe { std::slice::from_raw_parts(buf.as_ptr() as *const u8, n) };
            if buf.len() >= 21 {
                let ip = Ipv4Addr::new(buf[12], buf[13], buf[14], buf[15]);
                let elapsed = start.elapsed();
                match buf[20] {
                    11 => Ok(ProbeResult::Hop(ip, elapsed)),
                    3 if ip == target => Ok(ProbeResult::Reached(ip, elapsed)),
                    3 => Ok(ProbeResult::Hop(ip, elapsed)),
                    _ => Ok(ProbeResult::Timeout),
                }
            } else {
                Ok(ProbeResult::Timeout)
            }
        }
        Err(_) => Ok(ProbeResult::Timeout),
    }
}

fn main() -> std::io::Result<()> {
    let target = Ipv4Addr::new(8, 8, 8, 8);
    for ttl in 1..=15 {
        let mut reached = false;
        let mut last_ip: Option<Ipv4Addr> = None;
        print!("{:>2}  ", ttl);
        for _ in 0..3 {
            match probe(target, ttl)? {
                ProbeResult::Hop(ip, rtt) => {
                    if last_ip != Some(ip) {
                        print!("{}  ", ip);
                        last_ip = Some(ip);
                    }
                    print!("{:.3} ms  ", rtt.as_secs_f64() * 1000.0);
                }
                ProbeResult::Reached(ip, rtt) => {
                    if last_ip != Some(ip) {
                        print!("{}  ", ip);
                        last_ip = Some(ip);
                    }
                    print!("{:.3} ms  ", rtt.as_secs_f64() * 1000.0);
                    reached = true;
                }
                ProbeResult::Timeout => print!("*  "),
            }
        }
        println!();
        if reached {
            break;
        }
    }
    Ok(())
}
```

## References

- [My previous post on Tailscale exit nodes][tailscale]
- [WireGuard whitepaper][wireguard]
- [traceroute-rs source code][repo]
- [Van Jacobson's original traceroute][vj-traceroute]
- [RFC 792: ICMP][rfc-icmp]
- [socket2 crate documentation][socket2]
- [pnet crate documentation][pnet]

<!-- prettier-ignore-start -->
[tailscale]: {{< ref "/posts/2026/tailscale-exit-nodes" >}}
[wireguard]: https://www.wireguard.com/papers/wireguard.pdf
[repo]: https://github.com/stonecharioteer/traceroute-rs
[vj-traceroute]: https://ee.lbl.gov/papers/traceroute.pdf
[rfc-icmp]: https://datatracker.ietf.org/doc/html/rfc792
[socket2]: https://docs.rs/socket2/latest/socket2/
[pnet]: https://docs.rs/pnet/latest/pnet/
<!-- prettier-ignore-end -->
