---
date: "2026-01-27T20:45:03+05:30"
title: "I use a Macbook now"
description:
  "After using Linux for nearly 20 years, I've gotten an M5 Macbook Pro as my
  daily driver."
tags:
  - "Macbook"
  - "OSX"
---

I got a Macbook. This feels like something you need to announce, especially when
you were planning on writing a post that you have been using Linux for 20 years.
I feel like I lost something by ordering one, but I have the following reasons.

- I'm preparing for interviews, and I want to focus on studying what I _need_ to
  study.
- I could have gotten a
  [Thinkpad P14s Gen 6, there's a model that has 96GB RAM,](https://www.lenovo.com/us/en/p/laptops/thinkpad/thinkpadp/thinkpad-p14s-gen-6-14-inch-amd-mobile-workstation/len101t0118)
  but I primarily wanted a machine for the go. That laptop has the Ryzen AI 350
  chip, but I assumed that the M5 would have better performance _vis-a-vis_
  local LLMs.
- I wanted a machine that lowers friction towards studying, this means I don't
  want to close my terminal sessions until I'm done, or until rebooting is
  inevitable.
- My previous laptop, the Asus X13 Flow is a lovely machine. I really like it,
  but its thermals suck on Linux, and the battery performance is abysmal. I
  tried to vibe-code
  [an app to monitor the power performance,](https://github.com/stonecharioteer/battery-cycles)
  but I realized that task is keeping me away from the actual task at hand:
  _studying for interviews_.
- I want to also record video, perhaps return to streaming.
- I want a lighter go-bag. With the Linux machine, I'd carry a charger, a
  powerbank and several accessories. I want to just carry a small GaN charger, a
  USB-C wire, my OnePlus Open, my Boox Palma and the laptop. I couldn't do that
  with the X13 Flow.

At the end of the day, my reasons are really irrelevant. I am just giving myself
reasons for this, but I did this because I need to focus. Any source of friction
is not good. I wanted to get the 13" Macbook Air, but they only sell the M4
version. I wish they'd released the M5 Macbook Air already. My friends also told
me that the memory bandwidth is lesser.

Oh, and I got the 15" M5 Macbook Pro with 32GB RAM and 512 GB Storage. I wish I
could afford the 2TB model, but I have to make do with this. I have enough
storage on my home servers, and I can also carry a portable SSD, I have a 2TB
one lying around.

I'm still _using_ Linux though. My desktop, MiniPc, storage server, steam deck
and the X13 Flow will continue to run Linux. I am going to write that post, but
for now, my priorities are [directed towards what I need to
study,]({{< ref "posts/2026/direction.md" >}}) especially given the job market.

## Also, What Gives, Apple?

The list of things I'm having to install to make this machine's GUI usable is
insane.

I've installed the following:

- [Aerospace Tiling Window Manager](https://github.com/nikitabobko/AeroSpace) -
  Apple is _pathetic_ at window management. How?!
- [BetterShot](https://www.bettershot.site/) - I like the fancy screenshots.
- [Linear Mouse](https://linearmouse.app/) - I need CTRL+scroll zoom on my
  trackball mouse.
- [Raycast](https://www.raycast.com/) - this has been a better launcher than
  Spotlight
- [Stats](https://github.com/exelban/stats) to show statistics in my menu bar,
  mainly RAM.
- [Vanilla](https://matthewpalmer.net/vanilla/) - I can't believe I cannot hide
  the menu bar items.

I thankfully had Claude update my
[Ansible playbooks](https://github.com/stonecharioteer/interview-prep) to
support OSX. I pushed some updates to it, and it's working like a charm. I need
to update it to install the above applications as well, I think.
