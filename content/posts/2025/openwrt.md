---
date: '2025-08-22T21:05:02+05:30'
title: 'Openwrt'
description: 'How I spent my week setting up multi-wan failover on OpenWRT on my Beelink EQI12'
tags:
  - "homelab"
  - "ai"
  - "openwrt"
  - "proxmox"
---

I got a [Beelink EQI12](https://www.bee-link.com/products/beelink-eqi12-intel%C2%AE-core-1220p-12450h-12650h) two weeks ago, thanks to a friend flying in from Dubai. This MiniPC has been my plan to replace the weak [Linkstar H68K](https://www.seeedstudio.com/LinkStar-H68K-1432-p-5501.html) [OpenWrt](https://openwrt.org/) router I had for about 2 years now. While the Linkstar has worked just fine, I wanted to upgrade to something more powerful so I could install other services on it as well. I didn't want to install PiHole on a Raspberry Pi anymore. I'm a little tired of Pis and their problems.

So I setup [Proxmox](https://www.proxmox.com/) on this server, and then installed [OpenWrt](https://openwrt.org/) on a VM on it. At first I assumed it would be easy. I was *very* wrong.

I used ChatGPT to constantly debug this. What made my life easier at first was:

1. Getting a USB HDMI Capture Card. I picked something cheap, and I used it with my laptop. I needed to be able to take screenshots to paste over to ChatGPT. When I tried using a phone to take photos of a monitor running this, that didn't end well. GPT5 hallucinated network cards, and didn't manage to differentiate between `0` and `8`. I couldn't `ssh` into the server to take photos from other computers because well, *the damned network was down, wasn't it?* Funnily enough, ChatGPT recommended getting a cheap capture card and that's what I did.
2. I tested out the network with a spare router I had lying around. I connected my existing network to the EQI12, and then connected the spare NIC to the router and things worked quite well that way. I didn't know that I was adding a layer of "easy mode" by doing that because I was letting the Linkstar do all the heavy lifting. But having that travel router was very helpful.
3. Having a second ISP, to debug the primary one. I've had 2 ISPs for 4 years now, and everyone should, if you're working remotely.

I'm enjoying having AI summarize what I did, just so that I can wave away the details, but here I'm asking it to give the details

{{<ai title="🔧 Debugging OpenWRT For Dual WAN Failover with ChatGPT">}}

I set up a **reliable failover system** using [OpenWrt](https://openwrt.org/) and [`mwan3`](https://openwrt.org/docs/guide-user/network/wan/multiwan/mwan3) on a mini PC router.

### ✅ Goals:

* Primary WAN: **PPPoE (wired)**
* Backup WAN: **WWAN (wireless client to mobile hotspot)**
* Automatically switch between them based on connectivity
* Use **real HTTP checks** (not just ping) for reliability

---

### ⚙️ Key Components:

* **[OpenWrt](https://openwrt.org/)** running in a [Proxmox](https://www.proxmox.com/) VM on an EQI12 mini PC
* **[mwan3](https://openwrt.org/docs/guide-user/network/wan/multiwan/mwan3)** for multi-WAN tracking and routing policies
* **[`httping`](https://openwrt.org/packages/pkgdata_owrt18_6/httping)** to test actual HTTP response from:

  * `https://github.com`
  * `https://amazon.com`
  * `https://google.com`

---

### 🧠 How it works:

* Both interfaces (`wan` and `wwan`) use `httping` for tracking
* Custom interface configs:

  ```sh
  option track_method 'httping'
  list track_ip 'https://github.com'
  list track_ip 'https://amazon.com'
  list track_ip 'https://google.com'
  ```
* Policy:

  ```
  config policy 'wan_first'
      list use_member 'wan_m1_w3'
      list use_member 'wwan_m2_w2'
  ```
* Rule:

  ```
  config rule 'default_rule'
      option dest_ip '0.0.0.0/0'
      option use_policy 'wan_first'
      option family 'ipv4'
  ```

---

### 🔄 Behavior:

* If **WAN is online**, all traffic uses `wan`
* If **WAN fails**, traffic **fails over to `wwan`**
* If **WAN recovers**, it **automatically switches back**

---

### 📊 Debugging & Monitoring:

* Run `mwan3 status` to view current WAN state and policy usage
* Use `logread -t mwan3` to see interface events and failover activity

{{</ai>}}

## Problems I Faced

* ChatGPT really likes to convince me that `mwan3` has a `script` feature. No. It does not. Thanks Claude.
* GPT5 SUCKS. It is so damned slow. I've gotten used to being productive with Claude. Using GPT5 and the Web App for ChatGPT is so damned horrible. I'm happier with Claude thank you very much.
* ACT is better with [PPPoE](https://openwrt.org/docs/guide-user/network/wan/wan_interface_protocols#protocol_pppoe_ppp_over_ethernet) connections, not DHCP. I am glad I have my account password saved for such an occasion. I wish people didn't pivot to the OTP login, that's such a travesty.
* Airtel is surprisingly easier, albeit because it comes with its own router. I'm not a big fan of that. I had to use Airtel over WiFi and ACT over Ethernet, since the EQI12 only has 2 NICs.
* The silliest error I faced was that I'd put in `1.1.1.1 8.8.8.8` as the entry in DNS config. These had to be *one per line*. This happened because ChatGPT kept telling me to add both nameservers in one command using `uci`.
* [`dnsmasq`](https://openwrt.org/docs/guide-user/base-system/dhcp_configuration) errors! So many `dnsmasq` errors. I wish I had the time to read the docs, but honestly I don't.

All in all, it works now, and that was 2 days of my life spent. I am not sure if I'd say it was "well-spent" though. If you're choosing to be your family's sysadmin, YMMV.


