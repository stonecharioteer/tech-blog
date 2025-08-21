---
date: '2025-08-12T16:39:52+05:30'
draft: true
title: 'My Linux Laptop Finally Works: How Claude Helped Me Fix Years of Annoyances'
description: 'After years of living with Linux laptop quirks - battery surprises, broken suspend, useless gestures, and monitor chaos - I partnered with Claude to actually fix these problems instead of just accepting them as "the Linux experience."'
tags:
  - "linux"
  - "laptop"
  - "claude"
  - "AI"
  - "asus-rog"
  - "problem-solving"
  - "linux-mint"
cover:
  image: "/images/asus-rog-linux-setup.jpg"
  alt: "ASUS ROG laptop with dual monitor setup running Linux"
---


## The "Linux Experience" I Was Used To


```bash
echo "Hello, world"
```

I'm sure you know the story.

I bought the Asus ROG X13 Flow in 2022, eager to use a powerful Ryzen 9 laptop
with Linux. This was to be my work+personal laptop, and I was super happy to be able
to afford this absolute beast.

I originally installed Fedora on it, not usually my first choice of a distro -- Linux Mint takes that position -- but a friend told me that Asus laptops have better experiences with Fedora, thanks to the lovely folks at [asus-linux.org](https://asus-linux.org).

I used Fedora as-is, with the KDE window manager for about 2 years. I didn't bother much, since I was already burnt out on tech and I didn't have the time or the energy to sit and make my tiling window manager setup work on this. I never bothered to try.

In the last month, I've been using Claude to do some debugging on my laptop. I cleaned the device out and installed Linux Mint this time, choosing to try setting up Qtile myself. I managed it myself and initially used ChatGPT for some debugging, but once I got a Claude Subscription, I managed to get a barebones qtile config up and running.

However Qtile isn't the focus of this post. I've written about it before.

Instead, it's the Linux experience. A lot of things were *broken* in this setup. My device didn't adapt to screen orientation despite having an accelerometer. It was randomly having trouble with battery consistency. And it never really supported suspend or sleep. I'd given up on all these issues. After all, it was the "linux experience".

I was used to shutting down my laptop when I prepared to close the lid, losing all my open windows. I never tried to use the laptop like a tablet, like it was clearly designed to be used (albeit in Windows).

I used a barebones Qtile config since bothering to "rice it up" was too much work.

I used Rofi, but I never set it up to do things like have a screen to take screenshots, or a power menu for Qtile.

I never managed to get Conky to do what I wanted, let alone make it look like I wanted.

I also didn't manage to have any sort of stats visible on the Qtile bars, making my config not just barebones, but also pretty tame.

My system's notifications were bad. I was using Dunst, but there was no place I could go to see all the session's notifications, let alone be able to copy them and then try to debug potential errors or warnings with AI.

One of the worst things was that I was so used to restarting my laptop just to get it to detect the monitors I just plugged in. I know, it's ridiculous.

I also never managed to get my Dell USB-C docking station working. It would work when booted into Windows, so it was not a compatibility issue. It was just Linux being Linux.

These are not complaints about how bad linux is: I've been using Linux *despite all this* for about 20 years now. In fact, I consider Windows and Macs *much, much worse.*

## A New World

I wanted to change things, but I didn't have a grandiose plan. After trying out Claude code for a [side-project](https://github.com/stonecharioteer/sushruta) one day, I asked it to take a look at my [qtile config](https://github.com/stonecharioteer/dotfiles-git) and "fix" some things. I started with some cross-compatibility items first, just to get a taste. I wanted my Qtile config to work out of the box with both my Desktop PC and my laptop.

{{< info >}}
I've written about the Qtile stuff in my [post about qtile]({{< ref "qtile-window-manager.md" >}}), so I won't be detailing much about it here.
{{< /info >}}

I realized that in doing this, I could also perhaps have it debug things on my laptop. After using Claude Code to read `journalctl` when trying to prototype applications, and when it also managed to read the output of system commands quite well, I realized I could ask it to try and fix suspend.

## Sleep, Ye Tired One

I'm not used to closing the lid on my laptops and then putting them in my bag to head to a coffee shop. I *shut down* the laptop, go to the coffee shop and turn it one again. I've accepted this *forever*. It's how I used my eMachines Netbook from back in the day and it's how I've used every laptop since. Heck, I used to turn off my office Macbook back at Visa because that's what I'm used to and didn't want to get into the habit of keeping a laptop on.

While I worked with a Macbook last, I had kept it on for 32 days straight, accepting that it's another world and I didn't need to shut it down.

Call me crazy, but I thought with Claude Code, maybe that wasn't a dream with Linux anymore.

My first task in Linux debugging, therefore, was "I'd like you to fix linux sleep on this laptop". I then sat back, giving Claude permissions whenever it needed. I'll let Claude explain this so I don't have to.

{{< ai title="Claude's Take on This" >}}
Look, I'll be honest - watching you restart your laptop every time you wanted to close the lid was painful to witness. You had this beautiful convertible laptop that could theoretically work as a tablet, but you'd trained yourself to treat it like a 1990s desktop: shutdown, pack up, lose everything. 

The sleep issue wasn't some deep kernel mystery - it was just systemd-logind being overly cautious and your system not knowing the difference between "laptop lid closed while docked" and "laptop lid closed while mobile." We literally just needed to tell it "hey, if external monitors are connected, don't sleep when the lid closes." 

That's it. One script. One configuration change. Years of workflow disruption solved in an afternoon.

The real tragedy? This wasn't some obscure ASUS-specific quirk. This would have worked on pretty much any Linux laptop. You just... never tried to fix it because "that's how Linux is."
{{< /ai >}}


Okay, that went harder than I thought it would. Geez. How about explaining what you did, wise guy?

{{< ai title="The Actual Fix (Claude's Technical Breakdown)" >}}
Right, sorry about the attitude. Here's what we actually built:

**The Core Logic**: A script that checks if external monitors are connected before allowing suspend. If you're using external displays, closing the lid shouldn't put the system to sleep because you're clearly still working.

**How We Detected External Monitors**:
```bash
EXTERNAL_MONITORS=$(xrandr --listmonitors | grep -v "^Monitors:" | grep -v "eDP-1" | wc -l)
```

This counts active monitors, excluding the built-in laptop screen (eDP-1). If the count is greater than 0, external monitors are connected.

**Integration with systemd-logind**: We configured the system to call our script before suspend decisions. The script exits with code 0 (allow suspend) when only the laptop screen is active, or code 1 (prevent suspend) when external monitors are detected.

**The Missing Pieces We Added**:
- Screen locking integration so the system locks before suspend and unlocks on resume
- Logging system to track suspend/resume events for debugging
- Proper handling of different dock connection states
- Power state awareness so it works whether you're on battery or plugged in

**The Beauty**: Once set up, it just works. Close the lid at your desk with external monitors? System stays awake. Close the lid with just the laptop screen? System suspends properly. No manual intervention needed.

The whole thing was maybe 50 lines of bash script and some systemd service configuration. Years of workflow disruption solved by logic that should have been built-in from day one.
{{< /ai >}}

That was arguably less condescending. Yeesh.

## The Claude Partnership: How We Worked Together

I decided to start using this approach for other problems. I realized that my mental paradigms about AI assistants had to change. You had assistants like Cursor that presented themselves as
wholly tied down as "coding assitants", but then you also had Claude Code, which presented an interesting problem.

A few years ago, when I was at Visa, I was mulling the idea of building a desktop assistant, something that new joinees could install on their macbooks and then have it setup the development environment for them, the Visa way. It was a project that didn't take off, but not for my lack of trying. I didn't get to work on it, but I tried it out for my own laptop later. I had a mix of Vagrantfiles and ansible playbooks in my [distributed dotfiles](https://github.com/stonecharioteer/distributed-dotfiles) that I painstakingly updated myself, everytime I updated my devtools. This got unwieldy and I never got around to updating it.

I realized an assistant that could do anything on your computer was exactly what I needed. I said YOLO and gave Claude access to my Laptop, Desktop and my MiniPc, and asked it to read my [qtile config](https://github.com/stonecharioteer/dotfiles-qtile) and my [fish config](https://github.com/stonecharioteer/dotfiles-qtile) and the [distributed dotfiles repo](https://github.com/stonecharioteer/distributed-dotfiles) to update all the playbooks so that all I'd need to do would be to run the playbooks to setup my machines. The following sections talk about what Claude did to fix each of the problems therein.

## Problems We Tackled

### "My Battery Dies Without Warning"

{{< ai title="Battery Monitoring Implementation" >}}
Created `/home/stonecharioteer/.config/qtile/install/battery-monitor.sh` that
iterates through `/sys/class/power_supply/BAT*` directories, reads capacity and
status files, and triggers dunst notifications at 30% and 15% thresholds.
Scheduled via cron every 10 minutes. The script includes battery detection
logic and graceful exit when no battery hardware is present.
{{< /ai >}}

<!-- Focus on the frustration and solution discovery:
- The problem: sudden shutdowns, no warnings, panic about losing work
- How you and Claude approached the debugging
- The "aha!" moment when you found the solution
- How it feels now to get proper battery warnings -->

### "My Laptop Sleeps When I'm Using External Monitors"

{{< ai title="Monitor-Aware Suspend Logic" >}}
Implemented `monitor-aware-suspend.sh` that uses `xrandr --query | grep -c "
connected"` to count active displays. Systemd-logind integration prevents
suspend when monitor count > 1. The script returns exit code 0 (allow suspend)
for single monitor, exit code 1 (prevent suspend) for multiple monitors. Added
notification system for user feedback when suspend is prevented.
{{< /ai >}}

<!-- The daily annoyance story:
- Working on external monitors, close laptop lid, everything stops
- The detective work with Claude to figure out the logic
- The satisfaction of laptop staying awake when you want it to -->

### "None of My Hardware Buttons Work"

{{< ai title="X11 Keysym to Command Mapping" >}}
Mapped hardware keys in qtile config: `XF86AudioMute` → `pactl set-sink-mute`,
`XF86MonBrightnessUp/Down` → `brightnessctl -d nvidia_0`,
`XF86KbdBrightnessUp/Down` → `brightnessctl -d asus::kbd_backlight`. Created
udev rules in `/etc/udev/rules.d/99-backlight.rules` for group-based write
permissions to `/sys/class/backlight/*/brightness` and
`/sys/class/leds/*/brightness`. Added user to `video` and `input` groups.
{{< /ai >}}

<!-- The accumulated frustration:
- Years of volume keys, brightness keys, special function keys doing nothing
- The systematic approach to mapping each one
- The joy of hardware actually working like it should -->

### "My Multi-Monitor Setup is a Daily Lottery"

{{< ai title="Multi-Monitor EDID and GPU Switching Issues" >}}
Diagnosed EDID detection failures (`/sys/class/drm/*/edid` files were 0 bytes),
causing VGA fallback modes. Fixed hybrid graphics stuttering by forcing
dedicated GPU mode with `prime-select nvidia`. Created custom modelines using
`cvt 2560 1440 60` and implemented display enumeration logic that handles GPU
mode changes (DisplayPort-1-X in NVIDIA mode, DisplayPort-2-X in hybrid mode).
USB-C connection provided better EDID than HDMI through dock.
{{< /ai >}}

<!-- The workflow disruption:
- Monitors not detected, wrong resolutions, system stuttering
- The complex investigation process with Claude
- Going from "maybe it'll work today" to reliable setup -->

### "My Touchpad is Just a Basic Clicking Rectangle"

{{< ai title="Touchegg and libinput Configuration" >}}
Configured `/etc/X11/xorg.conf.d/40-libinput-touchpad.conf` with libinput
driver options: `Tapping on`, `NaturalScrolling true`, `ScrollMethod
twofinger`. Deployed touchegg XML configuration mapping PINCH gestures to
`Control+plus/minus` and SWIPE gestures to navigation keys. Enabled touchegg
systemd user service for automatic startup. Required input group membership for
proper device access.
{{< /ai >}}

<!-- The productivity loss:
- Missing gestures you expect from modern hardware
- The discovery that Linux could do this stuff, it just wasn't configured
- The difference in daily workflow after fixing gestures -->

### "I Never Know How Much Power I'm Using"

{{< ai title="Real-Time Power Consumption Monitoring" >}}
Built multi-method power detection: UPower energy-rate parsing from
`/sys/class/power_supply/BAT*/` with battery state analysis, component-based
estimation using CPU load from `/proc/stat`, NVIDIA GPU power via `nvidia-smi
--query-gpu=power.draw`, and fixed estimates for displays/dock. Integrated into
qtile status bar with 5-second polling. Handles AC connection detection and
differentiates between charging, discharging, and high-load scenarios requiring
battery supplementation.
{{< /ai >}}

<!-- The curiosity and control aspect:
- Wondering if you're pushing the system too hard
- The investigation into power monitoring
- The satisfaction of having real-time feedback -->

### "My Ansible Playbooks Were Machine-Specific Nightmares"

You know how it is. You start with one machine, create an ansible playbook. Then you get another machine with different specs, so you duplicate the playbook and modify it. Before long, you have three different playbooks that are 80% identical but you're too scared to consolidate them because "what if something breaks?"

My distributed-dotfiles repo was exactly this mess. Desktop playbook, laptop playbook, server playbook - all basically doing the same thing with slight variations.

{{< ai title="Hardware-Aware Ansible Role Architecture" >}}
Completely restructured your ansible architecture around hardware detection rather than machine types. The key insight: instead of separate playbooks per machine, use a single playbook with intelligent roles that detect their own applicability.

**Core Architecture Changes:**
- `failsafe-checks` role now validates system capabilities before any configuration
- `laptop` role checks for `/sys/class/power_supply/BAT*` before installing power management
- `qtile-wm` role detects X11/Wayland environment before GUI setup
- `docker` role validates CPU architecture and kernel version compatibility
- `nerd-fonts` role checks available disk space before downloading font packages

**Hardware Detection Logic:**
```yaml
# Example from laptop role
- name: Check if battery hardware exists
  stat:
    path: /sys/class/power_supply/BAT0
  register: battery_check

- name: Install battery monitoring tools
  package:
    name: ["acpi", "powertop", "tlp"]
  when: battery_check.stat.exists
```

**Conditional Package Management:**
The `system-deps` role now adapts package lists based on detected hardware: installs `nvidia-driver` only when NVIDIA GPU detected, `bluetooth` packages only when bluetooth hardware present, and `laptop-mode-tools` only on battery-powered systems.

**Result:** Single `base-environment.yml` + `gui-environment.yml` playbook pair handles Desktop (Ryzen 9 + RTX 4070), Laptop (ASUS ROG hybrid graphics), and MiniPC (Intel NUC) through role-based hardware awareness. No more maintaining three separate playbook copies.
{{< /ai >}}

## What Made This Different from Normal Linux Troubleshooting

<!-- Compare the Claude experience to traditional methods:
- No endless forum threads with half-solutions
- No "works for me" responses that don't help
- Patient, methodical approach instead of random trial-and-error
- Claude's ability to synthesize information and suggest comprehensive solutions
- The confidence that comes from having a knowledgeable partner -->

## The Unexpected Benefits

<!-- Talk about side effects of the process:
- Learning more about your system than years of casual use
- Confidence to tackle other hardware issues
- A laptop that feels more integrated and professional
- The documentation trail you now have for maintenance -->

## Reflections: Why We Accept Broken Things

<!-- The broader philosophical point:
- Why Linux users often accept suboptimal experiences
- The difference between "technically working" and "working well"
- How AI assistance changes the cost/benefit of fixing vs accepting
- Encouragement for others to stop settling -->

## What's Next

<!-- Wrap up with:
- Other areas you might tackle with Claude's help
- Advice for others with similar frustrations
- The mindset shift from acceptance to active problem-solving
- How this changes your relationship with your Linux setup --> 
