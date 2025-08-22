---
date: '2025-08-21T00:00:00+05:30'
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
  image: "/images/posts/linux-and-claude.png"
  alt: "Linux and Claude collaboration for system debugging and optimization"
---


## The "Linux Experience" I Was Used To


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

## A Desktop AI Assistant

I decided to start using this approach for other problems. I realized that my mental paradigms about AI assistants had to change. You had assistants like Cursor that presented themselves as
wholly tied down as "coding assitants", but then you also had Claude Code, which presented an interesting problem.

A few years ago, when I was at Visa, I was mulling the idea of building a desktop assistant, something that new joinees could install on their macbooks and then have it setup the development environment for them, the Visa way. It was a project that didn't take off, but not for my lack of trying. I didn't get to work on it, but I tried it out for my own laptop later. I had a mix of Vagrantfiles and ansible playbooks in my [distributed dotfiles](https://github.com/stonecharioteer/distributed-dotfiles) that I painstakingly updated myself, everytime I updated my devtools. This got unwieldy and I never got around to updating it.

I realized an assistant that could do anything on your computer was exactly what I needed. I said YOLO and gave Claude access to my Laptop, Desktop and my MiniPc, and asked it to read my [qtile config](https://github.com/stonecharioteer/dotfiles-qtile) and my [fish config](https://github.com/stonecharioteer/dotfiles-qtile) and the [distributed dotfiles repo](https://github.com/stonecharioteer/distributed-dotfiles) to update all the playbooks so that all I'd need to do would be to run the playbooks to setup my machines. 

## Problems We Tackled
The following sections talk about what Claude did to fix each of the problems therein.

### "My Battery Dies Without Warning"

The problem was embarrassingly simple: my laptop would just die. Mid-sentence while coding, mid-call during meetings. No warning, no "hey maybe plug this thing in" - just black screen and panic about lost work.

I'd accepted this as normal Linux behavior. Surely the system knew about battery levels, right? But there were no notifications anywhere.

{{< ai title="The Diagnostic Process" >}}
First, we confirmed the system could actually read battery information:
```bash
ls /sys/class/power_supply/
cat /sys/class/power_supply/BAT0/capacity
cat /sys/class/power_supply/BAT0/status
```

The files were there, readable, updating in real-time. So why no notifications? Turns out nothing was actually *checking* these files and acting on them.

We built a simple monitoring script that:
1. Iterates through any `/sys/class/power_supply/BAT*` directories (handles multiple batteries)
2. Reads the capacity and charging status
3. Sends dunst notifications at 30% (warning) and 15% (critical)  
4. Only triggers when not charging (no spam when plugged in)
5. Gracefully exits on desktop machines with no battery

Scheduled it via cron every 10 minutes. Finally, civilized battery warnings.
{{< /ai >}}

<!-- Focus on the frustration and solution discovery:
- The problem: sudden shutdowns, no warnings, panic about losing work
- How you and Claude approached the debugging
- The "aha!" moment when you found the solution
- How it feels now to get proper battery warnings -->

### "My Laptop Sleeps When I'm Using External Monitors"

You know that workflow where you're at your desk, using external monitors, concentrating on work, then you close the laptop lid to get it out of the way? Yeah, your whole session dies. Everything stops, SSH connections drop, work vanishes.

I trained myself to never close the lid. Ever. Even when the laptop was clearly in the way and I had two perfectly good external monitors right there.

{{< ai title="Understanding the Problem" >}}
The issue was conceptual: systemd-logind treated "lid closed" as "user wants to suspend" with no context awareness. It didn't care that I had external monitors connected and was clearly still working.

We needed to teach the system about different contexts:
- Lid closed with only laptop screen = suspend (traveling)  
- Lid closed with external monitors = stay awake (docked)

The solution involved:
1. Creating a script that counts connected monitors with `xrandr --query | grep -c " connected"`
2. Integrating with systemd-logind through suspend inhibit mechanisms
3. Using exit codes: 0 = allow suspend, 1 = prevent suspend
4. Adding user notifications when suspend gets prevented

Now the laptop behaves intelligently. Close the lid at your desk? System stays awake. Close it on the go? Sleeps properly. Context-aware power management, finally.
{{< /ai >}}

<!-- The daily annoyance story:
- Working on external monitors, close laptop lid, everything stops
- The detective work with Claude to figure out the logic
- The satisfaction of laptop staying awake when you want it to -->

### "None of My Hardware Buttons Work"

This ASUS ROG laptop had beautiful multimedia keys. Volume up, volume down, brightness controls, keyboard backlight adjustment - all useless. Press them, nothing happens. They were basically expensive decorations.

I figured this was just "the Linux experience" and used software volume controls like some kind of caveman. Who needs hardware integration anyway?

{{< ai title="Mapping Hardware to Reality" >}}
The debugging process revealed that X11 was actually detecting the key presses, but nothing was bound to handle them.

We used `xev` to identify what keysyms the hardware was generating:
- Volume keys → `XF86AudioMute`, `XF86AudioLowerVolume`, `XF86AudioRaiseVolume`
- Screen brightness → `XF86MonBrightnessDown`, `XF86MonBrightnessUp`  
- Keyboard backlight → `XF86KbdBrightnessDown`, `XF86KbdBrightnessUp`

Then mapped each to actual commands in the qtile config:
- Audio controls → `pactl` commands for PulseAudio
- Screen brightness → `brightnessctl -d nvidia_0` (NVIDIA-specific path)
- Keyboard backlight → `brightnessctl -d asus::kbd_backlight` (ASUS-specific device)

The tricky part was permissions. Brightness controls need write access to `/sys/class/backlight/*/brightness` files, which are root-only by default. We created udev rules to make them group-writable and added the user to the appropriate groups.

But here's the interesting part: we also discovered that dunst notifications have different "roles" that affect how the system handles them. For volume notifications, we used the "volume" role, which automatically prevents the progress bar from going above 100%. Before this fix, you could spam the volume up key and the notification would show 150%, 200% - even though the actual audio was capped at 100%. The volume role teaches dunst about audio semantics, keeping the visual feedback accurate.

Result: every button actually does what its symbol suggests, with proper visual feedback that respects system limits. Revolutionary concept.
{{< /ai >}}

<!-- The accumulated frustration:
- Years of volume keys, brightness keys, special function keys doing nothing
- The systematic approach to mapping each one
- The joy of hardware actually working like it should -->

### "My Multi-Monitor Setup is a Daily Lottery"

Two beautiful 1440p monitors. A USB-C dock that cost more than my first laptop. The promise of a clean, professional setup. The reality? Maybe it works today, maybe it doesn't.

Sometimes both monitors would show up at 640x480. Sometimes only one would be detected. When they did work at proper resolution, the whole system would stutter like it was running on a Pentium II.

I learned to restart my laptop just to get monitors working. Every. Single. Day.

{{< ai title="Deep-Diving the Display Disaster" >}}
This turned into a proper investigation with multiple phases:

**Phase 1: EDID Detective Work**
We checked `/sys/class/drm/*/edid` files - all 0 bytes. The monitors weren't properly identifying themselves to the system, so Linux fell back to ancient VGA modes. That explained the 640x480 nonsense.

**Phase 2: Connection Analysis**  
Tested different cables and connection types:
- Direct DisplayPort → Full EDID, proper resolutions
- HDMI through dock → Partial EDID, bandwidth limitations  
- USB-C through dock → Full EDID, higher bandwidth

The dock's HDMI was the weak link, but USB-C provided proper monitor identification.

**Phase 3: The Stuttering Mystery**
Even with proper resolutions, everything felt laggy. Frame drops, input delays, general choppiness. The culprit? Hybrid graphics switching.

`prime-select query` showed "on-demand" mode, meaning the system was constantly switching between AMD integrated and NVIDIA discrete graphics. This caused frame timing chaos.

**The Fix:**
1. Forced dedicated GPU with `prime-select nvidia`
2. Created custom modelines with `cvt 2560 1440 60` for precise timing
3. Built auto-detection scripts that handle display name changes (GPU mode affects enumeration)
4. Switched problematic monitor from HDMI to USB-C

From daily lottery to rock-solid dual 1440p@60Hz. Finally.
{{< /ai >}}

<!-- The workflow disruption:
- Monitors not detected, wrong resolutions, system stuttering
- The complex investigation process with Claude
- Going from "maybe it'll work today" to reliable setup -->

### "My Touchpad is Just a Basic Clicking Rectangle"

Coming from years of Mac trackpads that do everything, this ASUS touchpad felt broken. No pinch-to-zoom, no swipe navigation, no gestures whatsoever. Just basic pointing and clicking like it's 2005.

I thought this was just Linux being Linux. Gesture support was probably some proprietary Mac thing that would never work properly elsewhere.

{{< ai title="Discovering Linux Can Actually Do Gestures" >}}
Turns out I was completely wrong. Linux has excellent gesture support through touchegg and libinput - it's just not configured out of the box.

The investigation revealed a two-layer problem:
1. **Basic touchpad behavior** was handled by libinput but needed proper configuration
2. **Advanced gestures** required touchegg daemon for X11 gesture recognition

**Layer 1: libinput Foundation**  
We configured `/etc/X11/xorg.conf.d/40-libinput-touchpad.conf` with proper options:
- `Tapping on` for tap-to-click
- `NaturalScrolling true` for Mac-like scroll direction  
- `ScrollMethod twofinger` for proper two-finger scrolling
- Palm rejection and sensitivity tuning

**Layer 2: Touchegg Gestures**
Created XML configuration mapping complex gestures:
- Two-finger pinch in/out → `Control+minus`/`Control+plus` (universal zoom)
- Two-finger swipe left/right → `Alt+Right`/`Alt+Left` (browser navigation)
- Three-finger swipe up → Application overview
- Four-finger swipe for workspace switching

Set up touchegg as a systemd user service for automatic startup. Added user to input group for proper device permissions.

But there was another bizarre issue: the touchscreen. When external monitors were connected, touching the laptop screen would register clicks on the wrong displays. Touch the top-left of the laptop screen, cursor appears on the external monitor. The touchscreen input was being mapped across the entire desktop instead of just the laptop screen.

**Touchscreen Coordinate Mapping Crisis**
This required mathematical precision. We needed to:
1. **Lock touchscreen to laptop display only** using coordinate transformation matrices
2. **Calculate proper scaling** between touchscreen coordinates and laptop screen dimensions  
3. **Handle rotation scenarios** when the laptop was used in tablet mode
4. **Maintain mapping during monitor changes** when external displays connect/disconnect

The solution involved `xinput` coordinate transformation matrices:
```bash
# Map touchscreen to laptop screen only
xinput set-prop "ELAN9008:00 04F3:2B63" "Coordinate Transformation Matrix" \
    $scale_x 0 0 0 $scale_y 0 0 0 1
```

Where `scale_x` and `scale_y` were calculated as ratios of laptop screen dimensions to total desktop dimensions, ensuring touch input stayed within the laptop screen boundaries regardless of external monitor configuration.

Result: Mac-quality gesture support on the touchpad AND proper touchscreen behavior that doesn't go haywire with external monitors. The touchscreen finally acts like it belongs to the laptop screen, not the entire desktop.
{{< /ai >}}

<!-- The productivity loss:
- Missing gestures you expect from modern hardware
- The discovery that Linux could do this stuff, it just wasn't configured
- The difference in daily workflow after fixing gestures -->

### "I Never Know How Much Power I'm Using"

Working on this hybrid graphics laptop with dual 1440p monitors, I had no idea if I was pushing the system too hard. Was the 100W charger sufficient? When did I need the 180W dock power? Was that compilation job going to drain the battery even while plugged in?

The system provided no feedback. I was flying blind on power consumption.

{{< ai title="Building Multi-Method Power Detection" >}}
This became surprisingly complex because different systems provide power information in different ways, and accuracy varies wildly.

**Method 1: UPower Battery Analysis**
The most accurate readings came from parsing `upower -i` output, specifically the `energy-rate` field. But this required understanding battery states:
- Charging: Total power = system consumption + charging rate
- Discharging while plugged in: AC maxed out, battery supplementing
- Discharging on battery: Direct system consumption reading

**Method 2: Component-Based Estimation**  
For validation and fallback, we built estimates from components:
- Base system (motherboard, RAM, storage): ~20W
- CPU power calculated from `/proc/stat` load data: 15W idle to 45W+ under load
- GPU power from `nvidia-smi --query-gpu=power.draw` 
- Dual 1440p monitors: ~30W
- USB-C dock: ~8W

**Integration Challenges:**
The tricky part was correlation. During high CPU workloads, we'd see 70-110W total consumption. Gaming or ML work pushed it to 80-130W. Peak multitasking could hit 150W+, triggering battery supplementation even with the dock's 180W capacity.

**The Result:**
Real-time power consumption in the qtile status bar, updating every 5 seconds. Icons indicate power source (🔋 on battery, ⚡ on AC). Now I can see immediately when a workload pushes beyond AC capacity, validate that the high-performance GPU mode is actually consuming more power, and make informed decisions about charger selection.

Finally, power consumption feedback that matches actual system behavior.
{{< /ai >}}

<!-- The curiosity and control aspect:
- Wondering if you're pushing the system too hard
- The investigation into power monitoring
- The satisfaction of having real-time feedback -->

### "Rofi Became My Universal Interface"

I'd been using rofi as a basic application launcher for years. Type a program name, hit enter, done. But working with Claude made me realize rofi could be so much more than that.

Why have separate UIs for different system functions when you could make rofi handle everything through a consistent, keyboard-driven interface?

{{< ai title="Building a Rofi-Powered Control Center" >}}
We transformed rofi from a simple app launcher into a comprehensive system interface with three major additions:

**1. Intelligent Screenshot Management**  
The screenshot script builds a dynamic menu based on your actual monitor configuration:
- Parses `xrandr --listmonitors` to detect connected displays
- Creates per-monitor options with real geometry info (e.g., "🖥️ LG 27GP850 (2560x1440 at 1920,0)")
- Handles full screen, active window, region selection, and per-monitor capture
- Automatically copies file paths to clipboard and sends notifications
- Uses scrot with proper monitor mapping for multi-display setups

**2. Power Menu with System Integration**  
Instead of hunting through desktop menus or memorizing systemctl commands:
- Clean interface with emoji icons: ⏻ Shutdown, ⟲ Reboot, ⇠ Logout, 🔒 Lock, ⏸ Suspend
- Integrates with qtile for proper logout, cinnamon-screensaver for locking
- Handles system power management through systemctl
- Consistent keyboard-driven workflow for all power operations

**3. Notification History Archaeology**  
This was the most complex: turning dunst's JSON notification history into a searchable, interactive interface:
- Parses complex JSON from `dunstctl history` with proper timestamp conversion
- Displays truncated summaries for browsing, full content on selection
- Automatic clipboard integration for easy sharing/debugging
- Multi-stage navigation: browse list → view details → return to list
- Handles missing data gracefully with formatted tables

**The Philosophy:**
Instead of remembering different UIs, shortcuts, and interfaces for different functions, everything becomes `Super+r` (rofi) + a few keystrokes. Screenshot? `Super+r screenshot`. Power menu? `Super+r power`. Notification history? `Super+r notif`.

Rofi becomes the universal interface layer over your entire system.
{{< /ai >}}

### Bringing them all together with Ansible

My distributed dotfiles repo used ansible, but I hadn't updated them in years.
They were machine-specific, and had tools I've since replaced with other tools.
I wanted to update them, so thought I'd task Claude with doing exactly that.


{{< ai title="Hardware-Aware Ansible Role Architecture" >}}
Completely restructured your ansible architecture around hardware detection
rather than machine types. The key insight: instead of separate playbooks per
machine, use a single playbook with intelligent roles that detect their own
applicability.

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
The `system-deps` role now adapts package lists based on detected hardware:
installs `nvidia-driver` only when NVIDIA GPU detected, `bluetooth` packages
only when bluetooth hardware present, and `laptop-mode-tools` only on
battery-powered systems.

**Result:** Single `base-environment.yml` + `gui-environment.yml` playbook pair
handles Desktop (Ryzen 9 + RTX 4070), Laptop (ASUS ROG hybrid graphics), and
MiniPC (Intel NUC) through role-based hardware awareness. No more maintaining
three separate playbook copies. {{< /ai >}}

## What Made This Different from Normal Linux Troubleshooting

I've to admit that I've never walked away from a Linux debugging session with
as big a smile on my face or as exciting a story to tell as this one. I've
spend years on Linux, accepting it as something that's always good but not
great. When I asked Claude to outline this post, it added in sections about
getting used to broken things. I'm not fully sure that's the case, but it
certainly feels that way.

Watching techtubers talk about Linux and using Arch linux or Hyperland as if
that's something novel is kind of weird to me. I've been on Linux for 20 years
now, and it has never really let me down. But at least this time, I've learnt
to not accept when something is seemingly not working as it should be.

Some tricks I discovered worked are as follows:

1. When debugging anything UI related, I ensured I took screenshots and told Claude that I kept screenshots in `~/Pictures/screenshots/`. It is so easy to tell it to "Look at the latest screenshot, that fix didn't work", and it was *excellent* at that.
2. `2>&1 | xclip -selection clipboard` is the best thing ever. I ensured Claude got the logs all the time. It was sometimes not good at picking up just the right lines in the logs, but that was easily remedied by giving it exactly the lines to look at, or the line numbers when using a physical log
3. Sometimes Claude isn't great at launching background services, doing that myself and then telling Claude to read the logs was better than expecting it to do everything itself.
4. Giving it access to multiple repositories through relative paths was easier than telling it to get them from github. I could launch multiple agents too, but that quickly got out of hands.
5. The YOLO mode is fun, for short bursts when I'm about to sleep. That way it does whatever it thinks it needs to, and then I could figure out what happened in the morning. But ensuring I have protected the main branch in my repos is necessary to prevent anxiety.

I found that this experience has only bolstered my belief that when it comes to
a computer, you can really do just about anything. That's why spending hours on
my Pentium 4 Computer was so much fun. It felt like I was constantly making
things possible. Nowadays I'm doing the same thing with Mini PCs.

Debugging Linux with Claude gives me the mental bandwidth to do other things,
like focussing on making software that people love. Users deserve empathy, and
that's something I have believed since the earliest days of my career.

It's time my own computers deserve my empathy, and the mental bandwidth to fix
things.

Eventually, I'd like to convert these distributed dotfiles and the debugging
system into a desktop tool perhaps. I'd want it to run with generic AI though,
not just Claude. I want users to be able to fix things on their Linux machines
with ease, using a conversational UI that also adapts to their needs.
