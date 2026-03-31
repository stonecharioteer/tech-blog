---
date: "2026-03-31T20:43:47+05:30"
title: "I Traced My Traffic Through a Home Tailscale Exit Node"
description:
  "A practical deep dive into Tailscale exit nodes: route changes, traceroute
  evidence, DERP fallback, trust boundaries, and why this model can be free."
tags:
  - "internet"
  - "vpn"
  - "tailscale"
  - "wireguard"
  - "homelab"
  - "proxmox"
  - "networking"
  - "self-hosted"
  - "privacy"
cover:
  image: "/images/posts/tailscale/exit-node-flow.png"
  alt: "Traffic flow comparison: with vs without a Tailscale exit node"
---

I set up Tailscale years ago but only used it for "reach my own devices" use
cases. This week I finally set up a proper home exit node: a tiny dedicated LXC
on my Proxmox box (1 vCPU, 512 MB RAM, basically just Tailscale).

To verify it worked, I pinged my home servers and they worked. But I wanted to
understand this deeper, so I turned to `traceroute`.

```text
traceroute github.com
traceroute to github.com (<destination-ip-redacted>), 64 hops max, 40 byte packets
 1  tailscale-gw (100.x.y.z)                     ~7 ms
 2  192.168.x.1                                  ~7 ms
 3  10.x.x.1                                     ~9-177 ms
 4  * * *
 5  * * *
 6  * * *
 7  home-isp-edge.example (<home-public-ip>)     ~11-14 ms
```

The 7th hop is where the cogs in my brain began turning. That's my home ISP. So
this is like a VPN, right? Or is it different?

## What is an exit node for?

Without an exit node, Tailscale sends traffic to my Tailscale _devices_, but
normal web traffic goes out through my local network or ISP ([exit nodes
docs][ts-exit]).

With an exit node enabled, my device changes its _default internet path_ to a
chosen device, which then sends traffic to the internet for me.

For internet traffic, an exit node behaves like a traditional VPN gateway, with
a caveat: Tailscale isn't always a VPN tunnel for all traffic, but the exit-node
mode is.

Without an exit node, we just have discoverability for services that we have
exposed on Tailscale. With an exit node, our device is effectively in a
full-tunnel VPN mode for internet traffic.

The traffic to the exit node is encrypted, and websites we access see the exit
node's public IP, not the IP of the ISP we are currently connected to on our
device.

![Traffic flow: with vs without exit node](/images/posts/tailscale/exit-node-flow.png)

{{< info title="Exit Node Is Not Anonymity" >}} An exit node moves where you
place trust, it doesn't remove trust entirely. The cafe WiFi can see that you're
sending encrypted traffic to Tailscale and how much traffic is flowing, but it
cannot read the contents. The exit node can still see where traffic is going
(metadata like destination IPs/domains), and websites see the exit node's public
IP. {{< /info >}}

## Under the hood

Before getting into routing, I want to cover how Tailscale connects devices in
the first place. I've been comparing it to a VPN, but Tailscale is really a mesh
network with a control plane on top of [WireGuard][wg].

{{< info title="Control Plane vs Data Plane" >}} ELI5: control plane is the map
and traffic cop; data plane is the road. Control plane decides who can talk to
whom and how to reach them. Data plane carries the encrypted packets
([control/data plane docs][ts-control-data]). {{< /info >}}

WireGuard by itself is mostly the _data plane_. Tailscale adds the _control
plane_ on top: identity/SSO, peer discovery, [NAT traversal][ts-nat]
coordination, ACL distribution, route distribution (including exit node default
routes), [MagicDNS][ts-magicdns], and fast device revocation. We _can_ run our
own WireGuard tunnels, but then we'd have to build and operate most of that
control-plane machinery ourselves.

When two devices connect, the flow looks like this:

1. Both devices (client + exit node) authenticate to Tailscale's control plane.
2. Control plane shares each peer's reachable endpoints (public/DERP candidates)
   and keys.
3. Both peers send UDP packets to each other to do [NAT hole-punching][ts-nat].
4. If punch-through succeeds, they establish a direct WireGuard-encrypted path.
5. If direct fails, they fall back to DERP relay (still end-to-end encrypted).

![Tailscale mesh connection: control plane, hole-punching, and DERP fallback](/images/posts/tailscale/mesh-connection.png)

Imagine your phone in a cafe and your home server are both behind routers. NAT
is like a front desk that tracks who went out, but does not let random outsiders
walk in directly. Hole-punching tries to make both sides "step out" at the same
time so their routers allow a path back in. If that timing or mapping fails,
DERP acts as a neutral meeting point; it forwards ciphertext between peers but
cannot decrypt it.

So the exit node connects by becoming a discovered peer and completing WireGuard
handshakes, not by me exposing a normal inbound VPN port. For exit nodes
specifically, the node advertises `0.0.0.0/0` and `::/0` to the control plane,
the control plane tells eligible clients, and the client chooses it. After that,
all internet traffic flows through the encrypted peer tunnel.

### How routing changes on your device

At a route level, enabling an exit node usually does the following:

- Tailscale accepts the exit node's advertised default routes (`0.0.0.0/0` and
  `::/0`).
- It installs policy routes so internet-bound traffic goes to the Tailscale
  tunnel interface (`tailscale0` on Linux, `utun` on macOS, `Wintun` on Windows;
  different labels, same role).
- It adds an "escape hatch" route for the exit node's own public IP via your
  normal gateway, so the tunnel transport itself doesn't loop.
- It either keeps or suppresses local LAN routes depending on
  `allow LAN access`.

A route is just a rule that says "for destination X, send packets to next-hop
Y." The default route is the catch-all rule for normal internet traffic. The
"escape hatch" route keeps traffic to the exit node's real public endpoint on
your normal network path so the tunnel does not try to tunnel itself.

The OS-specific plumbing differs, but the user outcome is the same:

- **Linux**: Tailscale uses kernel [policy routing][linux-pr] (`ip rule` + a
  separate route table) to steer default traffic to `tailscale0`, while
  exempting tunnel transport to avoid loops.
- **macOS / Windows**: Tailscale uses the OS VPN framework (Network Extension on
  macOS, virtual adapter + route priorities on Windows). More of the steering is
  hidden behind the framework, but the result is the same: a VPN adapter with a
  default route that captures internet traffic.

### How this compares to OpenVPN

Both Tailscale exit-node mode and OpenVPN achieve full-tunnel to one gateway,
but the internal mechanics differ. On Linux, the difference is clearest:

- **OpenVPN** rewrites the main routing table so "almost all destinations" go to
  `tun0` (commonly using `0.0.0.0/1` + `128.0.0.0/1`), plus one escape route for
  the VPN server.
- **Tailscale** uses `ip rule` + a separate routing table, selecting traffic by
  policy and marking tunnel transport packets to exempt them from the loop.

On macOS, both create a `utun` interface, send default traffic into it, and keep
an exception path for the tunnel endpoint. The differences are in the system
around the routing: WireGuard vs OpenVPN protocol, mesh topology vs
client-to-server, Tailscale device identity vs OpenVPN certs, and Tailscale's
NAT traversal with DERP fallback.

## Why Your Traffic Doesn't Hit Tailscale (And Why This Can Be Free)

Here's what surprised me at first: Tailscale's coordination service is primarily
control plane, not packet-hauling data plane ([how Tailscale works][ts-how],
[DERP][ts-derp]). It helps devices find each other, exchange identity and
policy, and set up encrypted peer paths. Your actual traffic then goes directly
peer-to-peer whenever possible.

For exit nodes, the normal path is:

`client -> exit node -> internet`

If direct connectivity is blocked, DERP relay is the fallback:

`client -> DERP relay -> exit node -> internet`

Either way, internet egress still happens at the exit node. DERP forwards
encrypted packets; it's a transport fallback, not a place where your browsing
gets terminated. The fallback mostly kicks in on locked-down networks: corporate
or guest WiFi that blocks UDP/peer paths, stricter carrier-grade NAT, or
environments with tightly controlled outbound traffic. On a typical home setup
(like my Proxmox node on home broadband), direct peer connectivity usually
works, so DERP may barely show up.

This is why Tailscale can offer a free tier while traditional VPN providers
charge for bandwidth. A traditional VPN provider pays for all the bandwidth you
use because your traffic routes through their servers. In Tailscale's model, my
home ISP and exit-node machine carry the egress traffic, not Tailscale's
infrastructure.

Napkin math for 100,000 users:

1. Assume 100 GB per user per month.
2. Total user traffic = `100,000 * 100 GB = 10,000,000 GB/month` (10 PB/month).
3. If a provider relayed all of that at `$0.02-$0.05/GB`, bandwidth alone is
   roughly `$200,000-$500,000/month`.
4. If fallback relay is 5%, relay volume is `500,000 GB/month` -> about
   `$10,000-$25,000/month`.
5. If fallback relay is 1%, relay volume is `100,000 GB/month` -> about
   `$2,000-$5,000/month`.

This is illustrative math with rough assumptions, not a claim about Tailscale's
internal traffic mix or exact costs.

### What about self-hosted OpenVPN or a commercial VPN?

It depends on what you're comparing against.

**vs. Nord/Mullvad/commercial VPNs**: You're paying for someone else to carry
your bandwidth. Typical pricing is $3-$12/month per user. For that you get
global exit locations and zero setup, but you're trusting their infrastructure
with your traffic metadata. With a Tailscale exit node at home, the bandwidth
cost is zero beyond what you already pay your ISP. The tradeoff is that you only
exit from one location (your home IP).

**vs. self-hosted OpenVPN**: This is where the comparison gets more interesting,
because the goal is the same: run your own gateway. But to make OpenVPN
reachable from the internet, you need to solve several problems that Tailscale
handles for you:

- **A stable address**: Most home ISPs assign dynamic IPs, so you'd need a
  dynamic DNS service (DuckDNS or similar, usually free) or a purchased domain
  with a DDNS updater. You don't strictly need to buy a domain, but you need a
  hostname that follows your IP around.
- **Port forwarding**: You'd open a port (typically UDP 1194) on your home
  router, directly exposing a service to the internet. Tailscale's NAT
  hole-punching and DERP fallback mean nothing needs to be exposed.
- **Certificate management**: OpenVPN requires a PKI, so you'd set up EasyRSA or
  similar, generate certs for each client, and handle revocation yourself.
  Tailscale uses [device identity tied to your SSO/IdP][ts-auth], with key
  rotation handled automatically.
- **Double NAT / carrier-grade NAT**: If either side is behind strict NAT (phone
  on a carrier network, home behind CGNAT), OpenVPN simply won't connect without
  the port forward working end-to-end. [Tailscale's hole-punching][ts-nat]
  handles most of these cases, and DERP covers the rest.

So: commercial VPNs trade money for convenience and exit diversity. Self-hosted
OpenVPN trades operational overhead for control. Tailscale exit nodes sit in
between; you get the control of self-hosting without the port forwarding, DDNS,
PKI, and NAT traversal headaches.

## Packet Walk: One Request End to End

When I type `curl example.com`, the command looks the same either way, but the
network path behind it is different. The table below compares those two paths
step-by-step.

Let's use `curl example.com` and compare the flow side-by-side.

<table>
  <thead>
    <tr>
      <th>Step</th>
      <th>Without Exit Node</th>
      <th>With Tailscale + Exit Node</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1. Route decision on client</td>
      <td>Default route points to local router / ISP gateway.</td>
      <td>Default route is steered to Tailscale, targeting the selected exit node.</td>
    </tr>
    <tr>
      <td>2. First network hop</td>
      <td>Packet leaves directly via local network interface to ISP path.</td>
      <td>Packet is encrypted in the tunnel and sent toward the exit node peer.</td>
    </tr>
    <tr>
      <td>3. Transport path</td>
      <td>Normal internet path from your current network.</td>
      <td>Direct peer-to-peer if possible; DERP relay if direct path fails.</td>
    </tr>
    <tr>
      <td>4. Internet egress point</td>
      <td>Your current network's public IP egresses the request.</td>
      <td>Exit node decrypts, NATs, and egresses via its public IP.</td>
    </tr>
    <tr>
      <td>5. Response return path</td>
      <td>Response returns directly to your current network public IP.</td>
      <td>Response returns to exit node, then back through encrypted tunnel to client.</td>
    </tr>
    <tr>
      <td>6. What the website sees</td>
      <td>IP/address context of the network you're currently on.</td>
      <td>IP/address context of the exit node network.</td>
    </tr>
  </tbody>
</table>

Let's look at that traceroute output again. The one from the intro showed hop 1
as my Tailscale exit gateway, reaching my home ISP edge by hop 7. Compare that
to the same MacBook _without exit node_:

```text
traceroute github.com
traceroute to github.com (<destination-ip-redacted>), 64 hops max, 40 byte packets
 1  192.168.x.1                                   ~4-5 ms
 2  * * *
 3  * * *
 4  * * *
 5  * * *
 6  * * *
 7  cafe-or-local-isp-edge.example (<local-public-ip>) ~11-16 ms
 8  isp-backbone.example                          ~11 ms
 9  * * *
10  upstream-cloud-edge.example                   ~31-36 ms
11  upstream-core.example                         ~32-71 ms
12  destination-network-edge.example              ~31-40 ms
```

Without exit node, hop 1 is just the local router, then the local ISP path and
upstream internet hops. The egress location shift is the key signal.

That lines up with what I wanted: traffic exits through home, not the network my
MacBook is currently on.

What changes here is mostly _where_ traffic exits and _who_ gets to observe
metadata on the local network. What doesn't change is that HTTPS is still your
main protection for content.

## How I Verified It on My Setup

I use a small checklist when I flip exit node on/off:

```bash
# 1) Egress identity check
curl ifconfig.me

# 2) Path shape check
traceroute github.com

# 3) Exit node health/path check
tailscale status
tailscale ping <exit-node-name>

# 4) DNS behavior check
dig <my-internal-domain>
dig github.com
```

Expected signals:

1. `curl ifconfig.me` should switch to your home/exit-node public IP.
2. `traceroute` should show hop 1 as the exit-node path when enabled.
3. `tailscale ping` should show direct path when possible, DERP when needed.
4. Internal domains should still resolve from the resolver path you expect.

## Exit Node Internals: Forwarding, NAT, and Return Path

This is the part that made the whole model click for me: an exit node is doing
real router work, not just "being online" in Tailscale.

{{< warning title="Exit Node Responsibilities" >}} The exit node is doing router
work, so it must have IP forwarding enabled and NAT/masquerade configured. In
plain terms: it accepts packets from Tailscale, sends them to the internet, then
maps replies back to the right client. If forwarding or NAT is missing, clients
look connected but internet traffic breaks. This is also the point where trust
shifts from "random cafe network" to "my own exit node machine."
{{< /warning >}}

{{< tip title="Proxmox LXC Gotcha" >}} If you're running Tailscale inside a
Proxmox LXC container (like I am), it won't work out of the box. LXC containers
don't have access to `/dev/net/tun` by default, and Tailscale needs it. On the
Proxmox **host**, you need to add this to your container config
(`/etc/pve/lxc/<CTID>.conf`):

```
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
```

Restart the container after adding this. On newer Proxmox versions (7+), you can
also enable the TUN feature through the web UI under the container's Options >
Features. I don't know what's worse, the Proxmox UI or their convoluted multiple
CLIs. {{< /tip >}}

On my LXC exit node, the setup boils down to two things:

1. **[IP forwarding][ts-forwarding]**: the kernel must be willing to route
   packets between interfaces:

   ```bash
   # /etc/sysctl.d/99-tailscale.conf
   net.ipv4.ip_forward = 1
   net.ipv6.conf.all.forwarding = 1
   ```

2. **NAT/masquerade**: outbound packets need to be rewritten with the exit
   node's public IP so replies come back to the right place. Tailscale handles
   this automatically on most Linux setups via `iptables` masquerade rules, but
   if you're debugging, check with:

   ```bash
   iptables -t nat -L POSTROUTING -v
   ```

Then on the exit node itself, you advertise the role:

```bash
tailscale up --advertise-exit-node
```

And on the client, you select it:

```bash
tailscale up --exit-node=<exit-node-name>
```

This is also why a broken exit-node setup can feel confusing: `tailscale status`
shows peers as "connected", but internet access still fails because forwarding
or NAT is misconfigured on the exit node side.

## Trust Boundaries

![Trust boundaries: untrusted cafe network, encrypted tunnel, trusted home network](/images/posts/tailscale/trust-boundaries.png)

The security story is really about trust placement. Without an exit node, you're
closer to trusting the network you're currently on. With an exit node, you're
closer to trusting the machine you picked as your gateway.

In my case, that trust call is easy to justify: this exit node is an LXC on my
own Proxmox server at home, and I keep it minimal on purpose (1 vCPU, 512 MB
RAM, basically just Tailscale).

{{< note title="Who Sees What" >}}

<table>
  <thead>
    <tr>
      <th>Party</th>
      <th>Can usually see</th>
      <th>Cannot usually see</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cafe WiFi / local ISP</td>
      <td>That you are connected to Tailscale, plus traffic volume/timing</td>
      <td>Contents of your tunneled traffic</td>
    </tr>
    <tr>
      <td>Exit node operator</td>
      <td>Destination metadata (IP/domain patterns), volume/timing, and any plain HTTP</td>
      <td>End-to-end HTTPS page contents</td>
    </tr>
    <tr>
      <td>Website you visit</td>
      <td>Your requests and the exit node public IP</td>
      <td>Your cafe network public IP</td>
    </tr>
  </tbody>
</table>

<p>Now let's zoom in specifically on the cafe router view.</p>

<table>
  <thead>
    <tr>
      <th>Scenario</th>
      <th>What the cafe router usually sees</th>
      <th>What it usually cannot see</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Without exit node</td>
      <td>Normal internet flows from your device to many destination IPs, plus traffic timing and volume.</td>
      <td>HTTPS page contents, passwords, and message bodies.</td>
    </tr>
    <tr>
      <td>With Tailscale + exit node</td>
      <td>Mostly one encrypted tunnel flow to Tailscale peers/relays, plus timing and volume metadata.</td>
      <td>The final websites/services you're reaching through the tunnel, and tunneled request contents.</td>
    </tr>
  </tbody>
</table>

<p>Small caveat: DNS handling can vary by OS and settings, so treat "usually"
as intentional wording here.</p>
{{< /note >}}

For me, this is the practical rule: if I wouldn't trust that machine with
outbound metadata, I should not use it as an exit node. That's exactly why I run
it in a tiny dedicated container with almost nothing else on it. Especially one
where npm packages can't bring my network down.

## Side Effect I Actually Like: AdGuard Visibility

One thing I realized after routing through my home exit node: my DNS telemetry
in AdGuard gets a lot more predictable for remote sessions.

When my MacBook is out on another network but using the exit node, queries that
reach my home DNS stack appear as coming through that home path. In practice,
that gives me a nice "this came from VPN-routed devices" bucket in one place.

The tradeoff is that per-device attribution can get blurrier depending on your
DNS and NAT setup. But for my use case, the aggregate visibility is actually a
win.

## DNS Behavior with Exit Nodes

DNS and routing are related, but they are not the same knob. Exit-node mode
changes where internet traffic egresses from. DNS settings decide which resolver
answers name lookups in the first place.

{{< info title="DNS Story" >}} Exit nodes change where your internet traffic
egresses, but DNS behavior still depends on your resolver setup. MagicDNS and
split DNS keep sending matching domains to the DNS servers Tailscale configured.
Public lookups may still follow your system resolver path, which can vary by OS
and settings. Practical rule: test both DNS and egress (`dig`/`nslookup` for
names, and `curl ifconfig.me` for public IP). {{< /info >}}

When debugging, I check this in order:

1. `curl ifconfig.me` matches the exit node public IP.
2. Internal names (like my homelab domains) resolve from the resolver I expect.
3. Public DNS lookups and web requests still work normally.

### Split DNS: Routing `.home.arpa` Through AdGuard

I set up [split DNS][ts-splitdns] in Tailscale so that anything under
`.home.arpa` (my chosen local domain) is resolved by the AdGuard DNS server
running on my home network. Public domains still go through the normal resolver
path, but any query for `*.home.arpa` gets routed to AdGuard at home.

So even when my MacBook is on a cafe network with the exit node enabled, I can
reach internal services by name (`nas.home.arpa`, `proxmox.home.arpa`) without
exposing those names to the public DNS chain. The split DNS config lives in the
Tailscale admin console under DNS settings; you add a nameserver for the domain
suffix and point it at the AdGuard instance's Tailscale IP.

The nice side effect: since these queries go through AdGuard, they also get
ad-blocking and tracking protection applied, and they show up in my AdGuard
query log alongside everything else. One place for all DNS visibility.

## Exit Node vs Subnet Route

I use these for different outcomes. If I want to "be on my home internet" from
anywhere, I use an exit node. If I only want access to private LAN services
while keeping normal browsing local, I use a [subnet router][ts-subnet].

{{< tip title="One-Sentence Difference" >}} Exit node means "send all internet
traffic through me" (`0.0.0.0/0`, `::/0`), while subnet router means "send only
these private networks through me" (for example `192.168.1.0/24`). {{< /tip >}}

One machine can do both roles, but I still choose per device whether I want full
internet egress control or just private-network reachability.

## Conclusion

After setting this up and tracing the path, my mental model is now simple: an
exit node makes Tailscale act like a full-tunnel VPN for internet traffic, with
my chosen machine acting as the gateway.

The trust tradeoff is just as simple: I stop trusting the network I'm currently
on, and start trusting the exit node I control. In my case, that's a tiny
dedicated home LXC, so that trade is worth it.

My sanity check is now three commands: `curl ifconfig.me`, `traceroute`, and a
DNS lookup. If those line up, I know traffic is leaving through home and the
setup is doing what I intended.

---

## References

- [Tailscale Exit Nodes](https://tailscale.com/kb/1103/exit-nodes) - official
  feature documentation
- [How Tailscale Works](https://tailscale.com/blog/how-tailscale-works) -
  control plane and encrypted peer networking
- [Tailscale Connection Types](https://tailscale.com/docs/reference/connection-types) -
  direct, DERP, and relay behavior
- [Tailscale Glossary](https://tailscale.com/docs/reference/glossary) -
  coordination server and control-plane terminology
- [NAT Traversal Improvements (Part 1)](https://tailscale.com/blog/nat-traversal-improvements-pt-1) -
  practical NAT traversal background
- [WireGuard Protocol](https://www.wireguard.com/) - the underlying encrypted
  tunnel protocol
- [Tailscale Subnet Routers](https://tailscale.com/kb/1019/subnets) - private
  network access without full tunnel
- [Tailscale Split DNS](https://tailscale.com/kb/1054/dns#using-dns-settings-in-the-admin-console) -
  per-domain resolver configuration
- [Tailscale MagicDNS](https://tailscale.com/kb/1081/magicdns) - automatic DNS
  for tailnet devices
- [Tailscale Authentication](https://tailscale.com/kb/1013/sso-providers) -
  SSO/IdP integration for device identity
- [Tailscale IP Forwarding](https://tailscale.com/kb/1104/enable-ip-forwarding) -
  sysctl and forwarding setup for exit nodes and subnet routers
- [Linux Policy Routing](https://man7.org/linux/man-pages/man8/ip-rule.8.html) -
  `ip rule` man page for policy-based routing
- [AWS Data Transfer Pricing](https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer) -
  example outbound bandwidth pricing reference
- [Google Cloud Network Pricing](https://cloud.google.com/vpc/network-pricing) -
  example outbound bandwidth pricing reference
- [Azure Bandwidth Pricing](https://azure.microsoft.com/pricing/details/bandwidth/) -
  example outbound bandwidth pricing reference

---

[ts-exit]: https://tailscale.com/kb/1103/exit-nodes
[ts-control-data]:
  https://tailscale.com/docs/reference/glossary#coordination-server
[ts-how]: https://tailscale.com/blog/how-tailscale-works
[ts-derp]: https://tailscale.com/docs/reference/connection-types
[ts-nat]: https://tailscale.com/blog/nat-traversal-improvements-pt-1
[ts-subnet]: https://tailscale.com/kb/1019/subnets
[ts-splitdns]:
  https://tailscale.com/kb/1054/dns#using-dns-settings-in-the-admin-console
[ts-magicdns]: https://tailscale.com/kb/1081/magicdns
[ts-auth]: https://tailscale.com/kb/1013/sso-providers
[ts-forwarding]: https://tailscale.com/kb/1104/enable-ip-forwarding
[wg]: https://www.wireguard.com/
[linux-pr]: https://man7.org/linux/man-pages/man8/ip-rule.8.html
