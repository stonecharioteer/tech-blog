---
date: 2020-12-15T10:00:00+05:30
draft: false
title: "TIL: Display Switch KVM, USB Hub Control, Windows Service Wrapper, and Hiring Strategies"
description: "Today I learned about converting USB switches into KVM switches, controlling USB hub power, creating Windows services from executables, and smart hiring strategies."
tags:
  - til
  - hardware
  - usb
  - windows
  - hiring
  - system-administration
---

Today's learning focused on hardware control, system administration, and engineering management.

## USB Switch to KVM Conversion

[Display Switch](https://github.com/haimgel/display-switch) demonstrates how to turn a $30 USB switch into a full-featured multi-monitor KVM switch. This project uses DDC/CI (Display Data Channel Command Interface) to control monitor inputs programmatically, enabling seamless switching between multiple computers without expensive KVM hardware.

The solution works by:
- Detecting which computer is active based on USB device presence
- Automatically switching monitor inputs via DDC commands
- Supporting multiple monitors with independent control
- Providing hotkey support for manual switching

## USB Hub Per-Port Power Control

[uhubctl](https://github.com/mvp/uhubctl) provides per-port power control for USB hubs, allowing you to turn individual USB ports on and off programmatically. This is particularly useful for:
- Resetting problematic USB devices
- Power management in embedded systems
- Automated testing of USB devices
- Reducing power consumption

```bash
# List controllable USB hubs
uhubctl

# Turn off port 2 on hub 1-1
uhubctl -a off -p 2 -l 1-1

# Turn on all ports
uhubctl -a on
```

## Windows Service Wrapper

[WinSW (Windows Service Wrapper)](https://github.com/winsw/winsw) allows you to run any executable as a Windows service with a permissive license. This is invaluable for:
- Running non-service applications as services
- Managing application lifecycle automatically
- Ensuring applications start on boot
- Providing service-level logging and error handling

Configuration is done through XML files, making it easy to wrap existing applications without code changes.

## Smart Hiring Strategies

Erik Bernhardsson's article on [hiring smarter than the market](https://erikbern.com/2020/01/13/how-to-hire-smarter-than-the-market-a-toy-model.html) presents a mathematical model for competitive hiring. Key insights:
- Focus on qualities that correlate with performance but are undervalued by the market
- Develop interview processes that identify these hidden signals
- Consider non-traditional backgrounds and experiences
- Optimize for long-term value rather than short-term credentials

## Additional Discoveries

- **Linux 5.10 Features**: Major kernel update with improved hardware support and performance enhancements
- **USB Drive Phantom Load**: Investigation into USB drives that consume power even when inactive, important for battery-powered systems

These tools and concepts address practical system administration challenges while providing insights into building more efficient development and hardware environments.