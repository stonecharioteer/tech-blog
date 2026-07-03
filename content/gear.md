---
date: "2025-04-13T10:54:37+05:30"
lastmod: "2026-07-03T00:00:00+05:30"
draft: false
title: "🖥️ My Gear"
aliases:
  - "/uses"
---

I get asked what devices I use (since I have a LOT of them). I wanted to
document these at one place so that I answer this question a little
deliberately.

## TLDR

### Devices

- Apple MacBook Pro (M5) laptop
- ASUS ROG Flow X13 (2022) laptop
- 2x Lenovo ThinkPad T14 Gen 2 Intel i5 laptops
- Beelink EQR5 Mini PC
- Beelink EQI12 Mini PC
- Apple iPad (A16) tablet
- White MoErgo Glove80 keyboard
- Logitech MX Ergo trackball

### Software

- macOS as my terminal and browser environment.
- [`pi.dev`](https://pi.dev/), tmux, and Neovim are the software I use the most.
- I practically live inside tmux; I can't leave it for anything.
- I still prefer Linux Mint for the desktop Linux experience, but lately I've
  given up on the desktop Linux dream.
- Headless Linux boxes that I SSH into for real work, including the ASUS ROG Flow
  X13 and ThinkPads.
- Proxmox on the Beelink EQI12, with OpenWrt as my router and dual WAN failover.
- Unbound for DNS and AdGuard Home for ad blocking.
- GitHub Actions runners for Merrilin.ai on the Beelink EQR5.
- Possibly Kubernetes on the ThinkPads for local services and Merrilin dev boxes.
- `.home.arpa` local DNS and a Tailscale exit node for remote access.

## Computers

### Laptop - Apple MacBook Pro (M5)

This is my primary device now, but mostly as a very nice terminal and browser.
For real development work, I predominantly SSH into either the ASUS ROG Flow X13
or the Beelink EQR5. Docker on macOS is a hack, and I cannot be convinced
otherwise.

### Mini PC - [Beelink EQR5](https://www.bee-link.com/products/beelink-eqr5)

This was my daily driver as of Sept. 2025, and it's still one of the machines I
SSH into for most of my work. It's headless now, like the rest of my Linux boxes.
I didn't think I'd enjoy using a Mini PC more than a laptop, but honestly, this
has been a great purchase. I got the AMD Ryzen 5 PRO 5650U model with 32GB RAM.

It also runs GitHub Actions runners for [Merrilin.ai](https://merrilin.ai/),
which makes it a nice local build and automation box without needing to keep
another machine awake.

### Mini PC - [Beelink EQI12](https://www.bee-link.com/products/beelink-eqi12-intel%C2%AE-core-1220p-12450h-12650h)

I've installed Proxmox on this, and run OpenWrt on it for my router. I've setup
dual WAN failover between ACT and Airtel, and I'm fairly happy with my setup.

The hardware here hasn't changed, but the network around it is a lot cleaner
now. I use Unbound for DNS, AdGuard Home for ad blocking, and `.home.arpa` domains
for home services. I also run a Tailscale exit node so I can route traffic back
through home when I need to. I may switch to Tailscale SSH eventually, but for
now the current setup works well enough.

I'm also self hosting other services on it, and I've documented those elsewhere.
My particular model has a 12th Gen Intel(R) Core(TM) i5-1235U CPU with 16GB DDR5
RAM. Most of these come with LPDDR5 RAM, but I wanted something I could upgrade
to 64 GB later.

### Laptops - 2x Lenovo ThinkPad T14 Gen 2 Intel i5

I also picked up two used Lenovo ThinkPad T14 Gen 2 Intel i5 models to use as headless
machines. I still need to set them up with Ubuntu 26.04 LTS, which is the latest
Ubuntu LTS as of this update. They're not daily-driver laptops for me; they're
part of the pool of Linux boxes I can SSH into when I need extra machines
around.

I'm thinking of putting Kubernetes on them so I can spin up services when I want
them. They might also become local Merrilin development boxes.

### Desktop - AMD Ryzen 9 7950X + AMD Radeon RX 7900 XTX (24GB)

This is mostly for the occassional gaming. I don't play many games these days,
and when I do, I usually rely on the Steam Deck. I run Windows 11 on it. I've
been able to run even Black Myth Wukong at full graphics, although I'll be the
first to admit that I'm not overly picky about monitor quality or framerates.

### Server - AMD Ryzen 7 5700X + AMD Radeon R9 270X

This is my storage server, with 6x8TB hard-drives, running Linux Mint and with
software-based RAID6. I used to self-host Jellyfin on it, but lately I just use
it as cold storage for some data. I keep it turned off most of the time, only
turning it on to archive something.

### Laptop - ASUS ROG Flow X13 (2022)

![ASUS ROG Flow X13](/images/laptop_x13_flow_product_image.png)

I got this just at the start of 2023, and it's a pretty sweet laptop. I wanted a
smaller form factor. ASUS cheaps out on the wifi card so I had to swap out the
Mediatek wifi card for an Intel one, which improved some of the wifi problems.
I've never been happy with bluetooth on Linux, so let's not get into that.

![ASUS ROG Flow X13](/images/laptop_x13_flow.jpg)

I used to predominantly use this on my desk, docked to my monitors, and carried
it with me whenever I was in the mood to work or study from a cafe. I also used
this as my work laptop at ChainSafe where we were asked to Bring Your Own Device
(BYOD). I don't use the stylus much, or the touch screen to be honest. But in
its tented mode, it's a sweet way to game.

These days, I've turned the ASUS ROG Flow X13 into a headless server. It took a bunch of
hacks to get it working properly, and that probably deserves its own blog post
one day. If you're interested in the RCA and the fixes, they're documented in
[this dotfiles PR](https://github.com/stonecharioteer/dotfiles-qtile/pull/37).

I'd earlier run Fedora and Linux Mint on this as a desktop, but it is headless now.

Here are the specs for this machine:
![ASUS ROG Flow X13 neofetch](/images/neofetch_x13_flow.png)

1. CPU: AMD Ryzen 9 6900HS with Radeon Graphics (16 core) @ 4.935 GHz
1. GPU: NVIDIA GeForce RTX 3050 Ti Mobile
1. RAM: 32 GiB
1. Storage: SSD - 1 TB SSD

I also run Windows 11 on this just to play games every now and then. The
Graphics Card on this is poorly cooled, so for any games, I need to ensure that
the temperatures are lower than 80 degrees Celsius.

## Gaming Machines

### Playstation 5

I don't like the PlayStation 5. I haven't used it beyond playing Spider-Man 2,
and I don't know if I'll use it for anything else.

### Nintendo Switch

The only reason I have a Switch is BOTW, and I've played more of that on my
Steam Deck than on the Switch. I also have a bunch of physical games that I hope
to play with friends or family, but so far I've barely used them. It's cool that
I have the Mario edition though.

### Steam Deck

I love my Steam Deck. It's great for on the go, and for gaming in between my
day. I don't play much lately, but I enjoy the occasional bullethell or
roguelike game. I wish I'd waited for the OLED model, but who knew that was
about to release. My next handheld is going to be something that has the Ryzen
AI chip, hopefully, but for now the Steam Deck runs everything I need. I barely
use my Nintendo Switch after gettingn it.

## Trackball - Logitech MX Ergo

![MX Ego](/images/trackball_logitech_mx_ergo.jpg)

I love my Logitech MX Ergo. I wish it had the same wheel as the MX Master series
but sadly it doesn't. I've used this trackball since 2021, and I think I cannot
use anything else. It's excellent. I keep coming back to it even though I also
have a Razer Bluetooth DeathAdder V2 X HyperSpeed.

I got the Razer because I wanted to have a regular mouse at the ready, and I gave
my MX Master 3 to my sister. Still, the MX Ergo remains the pointing device I
reach for most often.

I even use this to play games now (mostly RTS like Age of Mythology Retold).
I've tried other trackballs like the Kensington Expert Wireless, but I think I
prefer the form factor of a thumb trackball better.

## Keyboards

### White MoErgo Glove80 (Clicky Choc White keys)

The white Glove80 is my keyboard of choice lately. I use it wired with Linux.
You should look at the [review here.](https://danieldk.eu/MoErgo-Glove80-Review),
since it mirrors my experience exactly, except that I 100% recommend getting
white key switches. I love a loud click.

### Kinesis Advantage 2 (Kailh Box Jade Keys)

I used the Kinesis Advantage 2 for a couple of years, from 2021 to 2023. I wish
it weren't so bulky, but I've taped an Apple Magic Trackpad 2 to the blank space
between the two halves and I use that wired as well with Linux. Whenever I use a
Mac, this is my keyboard + touchpad of choice. I want to convert this keyboard
to a wireless setup someday, but I'm happy with it for now.

### CIDOO ABM066 - Alice

![AMB066 Keyboard](/images/keeb_abm066.jpg)

I bought this keyboard in 2022 and didn't use it much. I switched to it for a
while in 2025, but I don't use it much anymore. I like its form factor, and I've
customized only the placement of the number keys, since it was beyond
aggravating to me that the `6` key was on the left hand side of the board in the
default layout. I've used Gateron Green switches in this board, but I need to
swap them out since they're a little too smooth for my taste. It's got a
customizable LCD panel that displays the time, but you can only sync time to a
windows computer if the closed source software is installed.

## Phones & Tablets

### Phone - XTEink X4

I have an XTEink X4 that I've flashed the Crosspoint firmware on. I don't use it
much; I bought it mostly to research device support for Merrilin.

### Phone - Samsung Galaxy S23

I love this phone. It's a small phone that also supports Display Out. I connect
my XReal Air goggles to it to watch movies sometimes. That was the main reason I
bought this thing. Samsung doesn't make non-flagship Snapdragon devices any
longer. I will cherish this for as long as it lasts.

### Phone - BOOX Palma 1

Technically this isn't a phone, but an ereader. I use it every day, mostly for
reading fiction. I also read some blogs via FreshRSS using the FeedMe app. I use
Koreader to read books on this.

### Phone - OnePlus Open

This is my favourite phone. My heart broke when the screen decided to show the
infamous OnePlus green line of death. It cost way too much to repair, so I sold
my Samsung Galaxy S24 Ultra to get it fixed. I would have bought a OnePlus Open
2 someday, but sadly there doesn't seem to be one coming.

### Tablet - BOOX Tab Mini C

I have given up on Kindles since 2023, and this has been my ereader of choice
ever since I got it. The colors are decent, and it's great for EPUBs and
especially with Koreader. For PDFs I still default to ReadERA.

### Tablet - Apple iPad (A16)

I got an Apple iPad (A16) for testing Merrilin. I don't use it much, but I picked
up a third-party keyboard case for it and I do like using it to SSH into my ASUS
ROG Flow X13 when I want to do real work from a tablet. That said, I haven't been using
it that much lately. I'm happier on Android.

### Tablet - Samsung Galaxy Tab S9 Ultra

This is a massive tablet. I got this to replace my Samsung Galaxy Tab S7+. I use
it only at home, since it's too big to lug around. I use it to read technical
texts, PDFs mostly. I like watching some content on it too. I only wish Samsung
made a flagship 11 inch tablet, I'd have bought that instead. It is bonkers that
they only reserve their best display, processor and other specs for the 14 inch
model now.

### Tablet - Lenovo Tab

I got the Lenovo Tab because the Samsung Galaxy Tab S9 Ultra isn't something I
can take around with me wherever I go. I needed something relatively cheap so I won't feel the burn when
it breaks, and I'm happier on Android for this kind of device.
