---
date: "2026-04-01T11:37:18+05:30"
draft: true
title: "I Rebuilt Traceroute in Rust and It Was Simpler Than I Expected"
description: "I built traceroute from scratch in Rust and was surprised how simple the core idea is: send packets designed to die at each hop and listen for the error replies."
tags:
  - "rust"
  - "networking"
  - "traceroute"
  - "systems-programming"
---

Previously, I wrote about setting up a tailscale exit node and appreciated how
traffic gets wired to my home network. I wanted to understand `traceroute` a
bit. I've never contemplated how it works, and now feels like as good a time as
any to do just that. I mean, now's the time to rewrite it in Rust.

## What _does_ traceroute do?

I've just used traceroute to investigate how my query is travelling from my
computer to my router and to the internet, finally reaching the end server.

```text
$ traceroute -m 15 -w 2 github.com
traceroute to github.com (20.207.73.82), 15 hops max, 40 byte packets
 1  <tailscale-gw> (<tailscale-ip>)  4.605 ms  5.259 ms  4.703 ms
 2  <home-router> (<router-ip>)  4.475 ms  4.677 ms  4.354 ms
 3  <isp-gateway> (<isp-gateway-ip>)  6.695 ms *  6.774 ms
 4  * * *
 5  * * *
 6  * * *
 7  <isp-hop-1> (<isp-hop-1-ip>)  11.893 ms  11.645 ms  12.189 ms
 8  * <isp-hop-2> (<isp-hop-2-ip>)  41.558 ms *
 9  * * *
10  51.10.23.169 (51.10.23.169)  59.356 ms
    51.10.23.171 (51.10.23.171)  31.347 ms  31.517 ms
11  * 51.10.36.17 (51.10.36.17)  211.263 ms
    51.10.26.236 (51.10.26.236)  34.690 ms
12  * * *
13  ae102-0.rwa02.pnq21.ntwk.msn.net (104.44.11.234)  30.532 ms *
    ae106-0.rwa04.pnq21.ntwk.msn.net (104.44.20.68)  26.723 ms
14  * ae124-0.rwa03.pnq21.ntwk.msn.net (104.44.21.22)  31.501 ms *
15  * * *
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

## The first probe

Let's start with a single function that sends one UDP packet at a given TTL and
listens for the ICMP reply.

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
    let target = Ipv4Addr::new(20, 207, 73, 82); // github.com
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
for *all* ICMP packets arriving at our machine, including the "Time Exceeded"
replies from routers that dropped our short-lived UDP packet. We need
`libc::SOCK_RAW` here because `socket2` doesn't expose raw socket types
directly, and we need root/sudo to open it.

**Lines 20-21**: We send 32 bytes of zeros to port 33434 on the target. The
content doesn't matter. Port 33434 is the traditional traceroute port; nothing
listens there, so when our packet finally *does* reach the destination, the
target responds with ICMP "Port Unreachable" instead of "Time Exceeded," which
is how we know we've arrived.

**Lines 24-38**: We read from the raw ICMP socket. The reply is a raw IP packet;
the first 20 bytes are the IP header, and bytes 12-15 contain the source address
of whoever sent the ICMP reply (that's the router that dropped our packet). We
use `MaybeUninit` because Rust won't let us read uninitialized memory; the
`unsafe` block is safe here since `recv` tells us exactly how many bytes it
wrote.

**Lines 41-55**: The main loop. We increment TTL from 1 to 15, printing each
hop. When the responding IP matches our target, we've reached the destination and
break out.

This needs `sudo` to run because of the raw ICMP socket.

```text
$ sudo cargo run
 1  <tailscale-ip>
 2  <router-ip>
 3  *
 4  *
 5  *
 6  *
 7  <isp-hop-1-ip>
 8  *
 9  <isp-hop-3-ip>
10  51.10.23.171
11  51.10.36.17
12  104.44.28.110
13  104.44.11.190
14  104.44.28.233
15  *
```

It works! We can see our Tailscale gateway, home router, ISP, and Microsoft's
network. But there are two problems: it doesn't know when to stop (it runs all
the way to hop 15), and we only get one probe per TTL with no timing
information.
