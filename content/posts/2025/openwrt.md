---
date: '2025-08-22T21:05:02+05:30'
draft: true
title: 'Openwrt'
description: 'How I spent my week setting up multi-wan failover on OpenWRT on my Beelink EQI12'
tags:
  - "homelab"
  - "chatGPT"
---

I got a Beelink EQI12 two weeks ago, thanks to a friend flying in from Dubai. This MiniPC has been my plan to replace the weak Linkstar H68K OpenWRT router I had for about 2 years now. While the Linkstar has worked just fine, I wanted to upgrade to something more powerful so I could install other services on it as well. I didn't want to install PiHole on a Raspberry Pi anymore. I'm a little tired of Pis and their problems.

So I setup Proxmox on this server, and then installed OpenWRT on a VM on it. At first I assumed it would be easy. I was *very* wrong.

I used ChatGPT to constantly debug this. What made my life easier at first was:

1. Getting a USB HDMI Capture Card. I picked something cheap, and I used it with my laptop. I needed to be able to take screenshots to paste over to ChatGPT. When I tried using a phone to take photos of a monitor running this, that didn't end well. GPT5 hallucinated network cards, and didn't manage to differentiate between `0` and `8`. I couldn't `ssh` into the server to take photos from other computers because well, *the damned network was down, wasn't it?* Funnily enough, ChatGPT recommended getting a cheap capture card and that's what I did.
2. I tested out the network with a spare router I had lying around. I connected my existing network to the EQI12, and then connected the spare NIC to the router and things worked quite well that way. I didn't know that I was adding a layer of "easy mode" by doing that because I was letting the Linkstar do all the heavy lifting. But having that travel router was very helpful.
3. Having a second ISP, to debug the primary one. I've had 2 ISPs for 4 years now, and everyone should, if you're working remotely.

I'm enjoying having AI summarize what I did, just so that I can wave away the details, but here I'm asking it to give the details

{{<ai title="🔧 Debugging OpenWRT For Dual WAN Failover with ChatGPT">}}

I set up a **reliable failover system** using OpenWRT and `mwan3` on a mini PC router.

### ✅ Goals:

* Primary WAN: **PPPoE (wired)**
* Backup WAN: **WWAN (wireless client to mobile hotspot)**
* Automatically switch between them based on connectivity
* Use **real HTTP checks** (not just ping) for reliability

---

### ⚙️ Key Components:

* **OpenWRT** running in a Proxmox VM on an EQI12 mini PC
* **mwan3** for multi-WAN tracking and routing policies
* **`httping`** to test actual HTTP response from:

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

All in all, it works now, and that was 2 days of my life spent. I am not sure if I'd say it was "well-spent" though. If you're choosing to be your family's sysadmin, YMMV.


