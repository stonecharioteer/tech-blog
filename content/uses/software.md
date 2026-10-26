---
date: "2026-10-26T20:55:50+05:30"
draft: false
title: "Software I use"
description: "My Mac apps, terminal tools, and software I run at home."
weight: 20
---

I use macOS as my terminal and browser environment. Most of my development
work happens on Linux machines I SSH into. The
[hardware I use]({{< ref "/uses/hardware" >}}) has its own page.

## Terminal tools

- [pi](https://pi.dev/) is my preferred AI coding agent.
- [Herdr](https://herdr.dev/) keeps my terminal sessions running. I used tmux
  for years, but I use Herdr instead now.
- [Neovim](https://neovim.io/) is my editor.

## Mac apps

<!-- Keep this list sorted alphabetically by app name. -->

- [Aerospace Tiling Window Manager](https://github.com/nikitabobko/AeroSpace) -
  Apple is _pathetic_ at window management. How?!
- [Amphetamine](https://apps.apple.com/us/app/amphetamine/id937984704?mt=12)
  to keep my personal Mac awake. I started using it before I used Caffeine
  with my Stream Deck.
- [Barly](https://www.barly.app/en/) to hide menu bar icons I don't need to
  see all the time.
- [BetterShot](https://www.bettershot.site/) - I like the fancy screenshots.
- [Caffeine](https://www.caffeine-app.net/en/) with my Stream Deck on my
  work laptop. I'm fairly happy with it, so I might replace Amphetamine on my
  personal Mac with it soon.
- [Itsycal](https://www.mowglii.com/itsycal/) for a calendar in the menu bar.
  Install it with `brew install --cask itsycal`.
- [Linear Mouse](https://linearmouse.app/) - I need CTRL+scroll zoom on my
  trackball mouse.
- [Raycast](https://www.raycast.com/) - this has been a better launcher than
  Spotlight
- [Stats](https://github.com/exelban/stats) to show statistics in my menu bar,
  mainly RAM.

## Files

- [Syncthing](https://syncthing.net/) to sync files between my devices.
- [LocalSend](https://localsend.org/) to send files between devices on the
  same network.
- [KDE Connect](https://kdeconnect.kde.org/) to connect my Android, iPhone,
  and macOS devices. It's excellent for this.

## At home

- [Linux Mint](https://linuxmint.com/) is still my preferred desktop Linux
  distribution, though my Linux machines are mostly headless now.
- [Proxmox VE](https://www.proxmox.com/en/proxmox-virtual-environment/overview)
  runs on the Beelink EQI12. [OpenWrt](https://openwrt.org/) handles routing
  and dual WAN failover between ACT and Airtel.
- [Unbound](https://nlnetlabs.nl/projects/unbound/about/) handles DNS, with
  [AdGuard Home](https://adguard.com/en/adguard-home/overview.html) for ad
  blocking. I use `.home.arpa` names for local services.
- [Tailscale](https://tailscale.com/) gives me remote access. I also run an
  exit node for when I want to route traffic through home.
- [GitHub Actions runners](https://docs.github.com/en/actions/hosting-your-own-runners)
  run builds for [Merrilin](https://merrilin.ai/) on the Beelink EQR5.

I'm also considering Kubernetes on the ThinkPads for local services and
Merrilin development boxes.
