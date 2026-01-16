---
date: "2026-01-16T20:52:09+05:30"
title: "Using a local DNS namespace for local service discovery"
description:
  "I wanted to stop using IP addresses to access my homelab services, and I
  spent a Friday evening fixing that."
tags:
  - "homelab"
  - "dns"
  - "unbound"
  - "adguard-home"
---

I've been using several services on my homelab, but I hadn't sat down to
configure a DNS namespace for this network, so I was stuck trying to recall the
IPv4 address every single time. By the time I was done, I stopped accessing my
Jellyfin server with `http://192.168.1.20:8096` and started using
`http://media.home.arpa:8096`

To begin, let's list out my homelab infrastructure.

## Infrastructure

{{< info title="Note on IP Addresses" >}} The IP addresses shown throughout this
post are anonymized. I'm not naive enough to publish my actual internal network
addresses on the internet. {{< /info >}}

<table>
  <thead>
    <tr>
      <th>Server</th>
      <th>Type</th>
      <th>IP</th>
      <th>Services</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4"><strong>Beelink EQI12</strong><br/>(<a href="https://www.proxmox.com/en/proxmox-virtual-environment">Proxmox VE</a>)</td>
      <td>VM</td>
      <td>192.168.1.1</td>
      <td><a href="https://openwrt.org/">OpenWRT</a> - Router, MultiWAN Failover</td>
    </tr>
    <tr>
      <td>LXC Container</td>
      <td>192.168.1.2</td>
      <td><a href="https://adguard.com/en/adguard-home/overview.html">AdGuard Home</a> + <a href="https://nlnetlabs.nl/projects/unbound/about/">Unbound</a> - DNS, Ad-blocking</td>
    </tr>
    <tr>
      <td>LXC Container</td>
      <td>192.168.1.20</td>
      <td>Media Server - <a href="https://syncthing.net/">Syncthing</a>, <a href="https://jellyfin.org/">Jellyfin</a>, <a href="https://www.qbittorrent.org/">qBittorrent</a>, <a href="https://www.samba.org/">Samba</a></td>
    </tr>
    <tr>
      <td colspan="3"><em>Host IP: 192.168.1.10</em></td>
    </tr>
    <tr>
      <td><strong>Beelink EQR5</strong></td>
      <td>Linux Mint</td>
      <td>192.168.1.50</td>
      <td>Dev Environment</td>
    </tr>
  </tbody>
</table>

## DNS Resolution Flow

![DNS Resolution Flow](/images/posts/homelab/dns-flow.png)

## Setting up a local DNS namespace

I have had these services setup for a few months now, but I haven't setup a DNS
namespace. So I'm still accessing my services with the IP addresses instead of
easy-to-remember DNS names. Today, I wanted to fix that.

Unbound and Adguard are where my DNS lies, so I needed to figure out where to go
to add rules for this. I'm grateful for ChatGPT, because I used it to figure out
that I need to add a namespace file to `/etc/unbound/unbound.conf.d/home.conf`,
with rules for all these IPs. I first assumed that I'd be using `media.local`,
but I learnt that [RFC 6762](https://datatracker.ietf.org/doc/html/rfc6762)
reserves `.local` for mDNS, so that's a no-go. Instead,
[RFC 8375](https://datatracker.ietf.org/doc/html/rfc8375) designates
`.home.arpa` for home networks, which is exactly what I need. I like the sound
of that. I was today years old when I learnt that `.arpa` means "Address and
Routing Parameter Area".

Here's the Unbound configuration file I created at
`/etc/unbound/unbound.conf.d/home.conf`:

```yaml
server:
  local-zone: "home.arpa." static

  local-data: "dns.home.arpa.      IN A 192.168.1.2"
  local-data: "media.home.arpa.    IN A 192.168.1.20"
  local-data: "proxmox.home.arpa.  IN A 192.168.1.10"
  local-data: "router.home.arpa.   IN A 192.168.1.1"
  local-data: "x13flow.home.arpa.  IN A 192.168.1.100"
  local-data: "eqr5.home.arpa.     IN A 192.168.1.50"

  local-data-ptr: "192.168.1.1 router.home.arpa"
  local-data-ptr: "192.168.1.2 dns.home.arpa"
  local-data-ptr: "192.168.1.10 proxmox.home.arpa"
  local-data-ptr: "192.168.1.20 media.home.arpa"
  local-data-ptr: "192.168.1.50 eqr5.home.arpa"
  local-data-ptr: "192.168.1.100 x13flow.home.arpa"
```

After creating this file, restart Unbound to apply the changes:

```bash
sudo systemctl restart unbound
```

Now I can access my services using friendly names like `eqr5.home.arpa` or
`media.home.arpa` instead of remembering IP addresses.

## Adguard Home Configuration

After restarting Unbound, I needed to go to the DNS settings page in Adguard
Home and update the upstream DNS settings to explicitly use `127.0.0.1:5335`
(since unbound runs on the same host).

![Upstream DNS in Adguard Home](/images/posts/homelab/upstream-dns-adguard.png)

I also had to add this to the Private Reverse DNS providers section so that I
could investigate what an IP is, if it's registered and I've forgotten about it.

![Private Reverse DNS in Adguard Home](/images/posts/homelab/private-reverse-dns-adguard.png)

## macOS Gotcha: DNS Needs Explicit Domain Routing

On macOS, simply having the DNS server set is not enough for custom internal
domains like `home.arpa`.

macOS uses domain-scoped DNS resolvers, so queries for `home.arpa` were never
sent to my AdGuard/Unbound server by default.

To fix this, I had to explicitly tell macOS to route that domain to my local DNS
server by creating `/etc/resolver/home.arpa`:

```bash
sudo mkdir -p /etc/resolver
sudo tee /etc/resolver/home.arpa <<EOF
nameserver 192.168.1.2
EOF
```

Then flush the DNS cache:

```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

After this, `ping` and `curl` resolved `*.home.arpa` correctly.

## Verifying the Setup

A quick `dig` confirms the forward lookup is working:

```bash
$ dig media.home.arpa

; <<>> DiG 9.18.39 <<>> media.home.arpa
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 8001
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;media.home.arpa.		IN	A

;; ANSWER SECTION:
media.home.arpa.	2317	IN	A	192.168.1.20

;; Query time: 2 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; MSG SIZE  rcvd: 60
```

The `NOERROR` status and the `ANSWER SECTION` showing the correct IP confirms
that local DNS resolution is working.

Reverse lookup works well too.

```bash
$ dig -x 192.168.1.20

; <<>> DiG 9.18.39-0ubuntu0.24.04.2-Ubuntu <<>> -x 192.168.1.20
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 19623
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;20.1.168.192.in-addr.arpa.  IN      PTR

;; ANSWER SECTION:
20.1.168.192.in-addr.arpa. 3600 IN   PTR     media.home.arpa.

;; Query time: 3 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Fri Jan 16 23:26:26 IST 2026
;; MSG SIZE  rcvd: 82


```

## Next Steps

To sum up, whenever I add a new server, I need to assign a static IP in OpenWRT,
then add it to the Unbound `home.conf` file, and restart Unbound. It's a clunky
process, but I'm not adding devices every week, so it's good enough.

I'd also like this working over WireGuard so I can access my services remotely,
but for now, I've done what I set out to do: have friendly names for my services
instead of IPs.
