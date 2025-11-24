---
date: 2020-12-06T10:00:00+05:30
draft: false
title: "TIL: Fantasy Map Generation and Disabling Laptop Internal Keyboards"
description:
  "Today I learned about algorithmic fantasy map generation for games and
  stories, and discovered methods for disabling laptop internal keyboards on
  Ubuntu."
tags:
  - til
  - maps
  - procedural-generation
  - ubuntu
  - hardware
  - system-administration
---

Today's learning covered creative computational techniques and practical system
administration solutions.

## Algorithmic Fantasy Map Generation

[Generating fantasy maps](http://mewo2.com/notes/terrain/?utm_source=mybridge&utm_medium=email&utm_campaign=read_more)
explores sophisticated algorithms for creating realistic fantasy world maps
programmatically.

### Core Techniques:

#### **Terrain Generation:**

- **Heightmap generation**: Using noise functions (Perlin, simplex) to create
  realistic elevation
- **Erosion simulation**: Hydraulic and thermal erosion for natural-looking
  landscapes
- **Climate modeling**: Temperature and precipitation based on latitude,
  elevation, and proximity to water
- **Biome placement**: Logical distribution of forests, deserts, grasslands
  based on climate

#### **Procedural Details:**

- **River networks**: Flow accumulation algorithms to create realistic river
  systems
- **Coastline generation**: Fractal techniques for natural-looking shorelines
- **Mountain ranges**: Plate tectonics simulation for believable geological
  features
- **Vegetation patterns**: Ecological modeling for forest distribution

### Applications:

- **Game development**: Procedurally generated worlds for RPGs and strategy
  games
- **Worldbuilding**: Tools for authors and tabletop RPG creators
- **Educational tools**: Understanding geography and climate systems
- **Artistic projects**: Generating maps for fictional stories and campaigns

### Technical Implementation:

The algorithms combine mathematical models with artistic principles to create
maps that feel both realistic and fantastical, suitable for fictional worlds
while maintaining geographical plausibility.

## Disabling Laptop Internal Keyboard

[Ubuntu solution for disabling laptop's internal keyboard](https://askubuntu.com/questions/160945/is-there-a-way-to-disable-a-laptops-internal-keyboard#178741)
provides multiple approaches for temporarily or permanently disabling the
built-in keyboard.

### Method 1: xinput (Temporary)

```bash
# List input devices to find keyboard ID
xinput list

# Disable the internal keyboard (replace XX with actual ID)
xinput float XX

# Re-enable when needed
xinput reattach XX 3
```

### Method 2: Blacklisting Kernel Module (Permanent)

```bash
# Find the keyboard module
lsmod | grep keyboard

# Create blacklist file
sudo echo "blacklist atkbd" >> /etc/modprobe.d/blacklist-keyboard.conf

# Update initramfs and reboot
sudo update-initramfs -u
```

### Method 3: udev Rules (Selective)

```bash
# Create udev rule to ignore specific keyboard
sudo nano /etc/udev/rules.d/99-disable-internal-keyboard.rules

# Add rule content:
# SUBSYSTEM=="input", ATTRS{name}=="AT Translated Set 2 keyboard", ENV{DEVNAME}=="*event*", RUN+="/bin/sh -c 'echo remove > %S%p/uevent'"
```

### Use Cases:

- **External keyboard preference**: Using mechanical or ergonomic keyboards
  exclusively
- **Cleaning and maintenance**: Preventing accidental input during laptop
  cleaning
- **Damaged keyboards**: Temporary solution while awaiting repair
- **Kiosk deployments**: Preventing unauthorized input in public terminals

These methods provide flexibility for different scenarios, from temporary
disabling for maintenance to permanent solutions for dedicated workstation
setups.
