---
date: 2020-07-28T18:00:00+05:30
draft: false
title: "TIL: Linux Productivity Tools and Rust Ownership Concepts"
description:
  "Today I learned about Linux productivity enhancements including volume
  control in xmonad, mouse gestures with Fusuma, and fundamental Rust ownership
  principles."
tags:
  - til
  - linux
  - xmonad
  - rust
  - productivity
  - fusuma
  - ownership
---

Today I explored various Linux productivity tools and deepened my understanding
of Rust's ownership model, discovering how these technologies can enhance both
system interaction and programming efficiency.

## Linux Desktop Productivity

### Volume Control in Xmonad

[Adding a Volume Control to xmonad](http://dmwit.com/volume/) demonstrates how
to integrate system volume controls into the xmonad tiling window manager:

```haskell
-- xmonad.hs configuration for volume control
import XMonad.Util.EZConfig
import XMonad.Actions.Volume

myKeys =
    [ ("M-<F1>", toggleMute >> return ())
    , ("M-<F2>", lowerVolume 4 >> return ())
    , ("M-<F3>", raiseVolume 4 >> return ())
    ]

main = xmonad $ defaultConfig
    `additionalKeysP` myKeys

-- Alternative using shell commands
volumeKeys =
    [ ("<XF86AudioMute>", spawn "amixer set Master toggle")
    , ("<XF86AudioLowerVolume>", spawn "amixer set Master 5%-")
    , ("<XF86AudioRaiseVolume>", spawn "amixer set Master 5%+")
    ]
```

{{< tip title="Xmonad Volume Control Options" >}} **Implementation Approaches:**

- **XMonad.Actions.Volume**: Pure Haskell solution using ALSA
- **Shell commands**: Call `amixer` or `pactl` directly
- **Media keys**: Bind to standard XF86Audio\* keys for laptop compatibility
- **Visual feedback**: Integrate with notification systems like `dunst`
  {{< /tip >}}

### AMD Laptop Performance Tuning

[Disabling Turbo Boost on AMD Laptops](https://www.kernel.org/doc/Documentation/cpu-freq/boost.txt)
explains thermal management techniques:

```bash
# Check current turbo boost status
cat /sys/devices/system/cpu/cpufreq/boost

# Disable turbo boost to reduce heat/improve battery
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost

# Re-enable turbo boost for performance
echo 1 | sudo tee /sys/devices/system/cpu/cpufreq/boost

# Check current CPU frequencies
cat /proc/cpuinfo | grep MHz

# Monitor CPU temperature
sensors
```

### Mouse Gestures with Fusuma

[Fusuma for Mouse Gestures in Linux](https://github.com/iberianpig/fusuma) and
[How to Use Fusuma](https://italolelis.com/posts/multitouch-gestures-ubuntu-fusuma/)
provide touchpad gesture support:

```yaml
# ~/.config/fusuma/config.yml
swipe:
  3:
    left:
      command: "xdotool key alt+Right" # Browser forward
    right:
      command: "xdotool key alt+Left" # Browser back
    up:
      command: "xdotool key super" # Show activities
    down:
      command: "xdotool key ctrl+alt+d" # Show desktop
  4:
    left:
      command: "xdotool key ctrl+alt+Right" # Switch workspace
    right:
      command: "xdotool key ctrl+alt+Left" # Switch workspace
    up:
      command: "xdotool key ctrl+alt+Up" # Show all workspaces
    down:
      command: "xdotool key ctrl+alt+Down" # Show current workspace

pinch:
  in:
    command: "xdotool key ctrl+minus" # Zoom out
  out:
    command: "xdotool key ctrl+plus" # Zoom in
```

```bash
# Install fusuma
sudo gem install fusuma

# Add user to input group
sudo gpasswd -a $USER input

# Start fusuma
fusuma

# Run as daemon
fusuma -d
```

{{< note title="Fusuma Requirements" >}} Fusuma requires:

- Ruby and gems
- User in `input` group
- Touchpad with multitouch support
- X11 (doesn't work with Wayland out of the box)
- `xdotool` for generating key events {{< /note >}}

## Rust Ownership and Borrowing

### Fundamental Ownership Concepts

[Gary Explains: Rust: What is Ownership and Borrowing?](https://www.youtube.com/watch?v=79phqVpE7cU&feature=youtu.be)
breaks down Rust's memory management system:

```rust
// Ownership Rules:
// 1. Each value in Rust has a single owner
// 2. When the owner goes out of scope, the value is dropped
// 3. There can only be one owner at a time

fn ownership_examples() {
    // Basic ownership
    let s1 = String::from("hello");
    let s2 = s1; // s1 is moved to s2, s1 is no longer valid
    // println!("{}", s1); // This would compile error!
    println!("{}", s2); // This works

    // Function ownership
    let s = String::from("world");
    takes_ownership(s); // s is moved into function
    // println!("{}", s); // This would compile error!

    let x = 5;
    makes_copy(x); // x is copied (integers implement Copy trait)
    println!("{}", x); // This still works
}

fn takes_ownership(some_string: String) {
    println!("{}", some_string);
} // some_string goes out of scope and is dropped

fn makes_copy(some_integer: i32) {
    println!("{}", some_integer);
} // some_integer goes out of scope, but nothing special happens
```

### Borrowing and References

```rust
// Borrowing allows using values without taking ownership
fn borrowing_examples() {
    let s1 = String::from("hello");

    // Immutable borrow
    let len = calculate_length(&s1);
    println!("The length of '{}' is {}.", s1, len); // s1 still valid

    // Mutable borrow
    let mut s2 = String::from("hello");
    change(&mut s2);
    println!("{}", s2);

    // Borrowing rules demonstration
    let mut s = String::from("hello");

    // Multiple immutable borrows are fine
    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);

    // But can't have mutable borrow while immutable borrows exist
    // let r3 = &mut s; // This would compile error!

    // After immutable borrows are done, mutable borrow is fine
    let r3 = &mut s;
    println!("{}", r3);
}

fn calculate_length(s: &String) -> usize { // s is a reference to a String
    s.len()
} // s goes out of scope, but because it doesn't have ownership, nothing is dropped

fn change(some_string: &mut String) {
    some_string.push_str(", world");
}
```

### Practical Ownership Patterns

```rust
// Common patterns for working with ownership

// 1. Returning ownership from functions
fn create_string() -> String {
    let s = String::from("hello");
    s // Return moves ownership to caller
}

// 2. Taking and returning ownership
fn process_string(s: String) -> String {
    // Process the string
    format!("{} processed", s)
}

// 3. Borrowing for read-only operations
fn read_string(s: &String) -> usize {
    s.len() // Just reading, no ownership needed
}

// 4. Mutable borrowing for modifications
fn modify_string(s: &mut String) {
    s.push_str(" modified");
}

// 5. Clone when you need independent copies
fn clone_example() {
    let s1 = String::from("hello");
    let s2 = s1.clone(); // Explicit clone

    println!("{} {}", s1, s2); // Both are valid
}

// 6. Using lifetimes with references
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() {
        x
    } else {
        y
    }
}

// 7. Struct with borrowed data
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 {
        3
    }

    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention please: {}", announcement);
        self.part
    }
}
```

{{< example title="Memory Safety Benefits" >}} **Rust's Ownership System
Prevents:**

- **Use after free**: References can't outlive their data
- **Double free**: Each value has exactly one owner
- **Memory leaks**: Values are automatically cleaned up
- **Data races**: Mutable references are exclusive
- **Iterator invalidation**: Borrowed data can't be modified {{< /example >}}

## System Notification Tools

### Ghosd for Transparent Notifications

[Ghosd - Transparent System Notifications](http://neugierig.org/software/ghosd/)
provides lightweight OSD notifications:

```bash
# Simple notification
echo "Volume: 50%" | ghosd

# With positioning
ghosd --position=top --timeout=2000 << EOF
System Update Available
Click to install
EOF

# Integration with volume control
amixer set Master 5%+ | grep -o '[0-9]*%' | ghosd --position=center
```

## Personal Development Insights

### The 4 Rules for Getting Better

[4 Rules to Getting Better](https://www.reddit.com/r/getdisciplined/comments/1q96b5/i_just_dont_care_about_myself/cdah4af/)
provides a framework for self-improvement:

{{< quote title="Rules for Personal Growth" footer="Reddit r/getdisciplined" >}}

1. **No more zero days** - Do something every day toward your goal, however
   small
2. **Be grateful to the 3 yous** - Past you (for setting you up), present you
   (for doing the work), future you (for the results)
3. **Forgive yourself** - Mistakes happen, learn and move forward
4. **Exercise and books** - Physical and mental health are foundational
   {{< /quote >}}

```python
# Implementation of "no zero days" tracking
from datetime import datetime, timedelta
import json

class ProgressTracker:
    def __init__(self, goal: str):
        self.goal = goal
        self.entries = []

    def log_progress(self, description: str, time_spent: int = 0):
        """Log daily progress, no matter how small"""
        entry = {
            'date': datetime.now().isoformat(),
            'description': description,
            'time_spent_minutes': time_spent
        }
        self.entries.append(entry)
        print(f"✓ Progress logged: {description}")

    def get_streak(self) -> int:
        """Calculate current streak of non-zero days"""
        if not self.entries:
            return 0

        today = datetime.now().date()
        streak = 0

        for i in range(len(self.entries) - 1, -1, -1):
            entry_date = datetime.fromisoformat(self.entries[i]['date']).date()
            expected_date = today - timedelta(days=streak)

            if entry_date == expected_date:
                streak += 1
            else:
                break

        return streak

    def summary(self):
        """Show progress summary"""
        total_time = sum(entry['time_spent_minutes'] for entry in self.entries)
        streak = self.get_streak()

        print(f"Goal: {self.goal}")
        print(f"Total entries: {len(self.entries)}")
        print(f"Total time: {total_time} minutes")
        print(f"Current streak: {streak} days")

# Usage example
tracker = ProgressTracker("Learn Rust")
tracker.log_progress("Read about ownership and borrowing", 30)
tracker.log_progress("Completed 3 exercises on ownership", 45)
tracker.summary()
```

## Key Takeaways

### Linux Productivity Integration

The tools explored today demonstrate how Linux environments can be customized
for enhanced productivity:

- **Window Manager Integration**: Custom key bindings for system controls
- **Hardware Optimization**: CPU tuning for performance vs battery life balance
- **Input Enhancement**: Gesture controls for natural interaction
- **Notification Systems**: Lightweight feedback mechanisms

### Rust's Safety Through Constraints

Rust's ownership system illustrates how programming language constraints can
enhance safety:

{{< note title="Ownership Design Philosophy" >}} **Rust's Approach:**

- Make memory safety issues **compile-time errors** rather than runtime bugs
- **Zero-cost abstractions** - safety without performance penalty
- **Explicit control** over memory layout and lifetime
- **Prevent entire classes** of common programming errors {{< /note >}}

### Personal Development Framework

The "4 Rules" approach provides a systematic method for consistent improvement:

- **Consistency over intensity** - Small daily actions compound
- **Self-compassion** - Guilt and shame are counterproductive
- **Holistic health** - Physical and mental wellness support each other
- **Gratitude practice** - Acknowledge progress and effort

This combination of system optimization, programming safety, and personal
development reflects the interconnected nature of technical and personal growth
in software development.

---

_Today's exploration reinforced that effective development environments, safe
programming languages, and sustainable personal practices all share common
principles: they provide structure that enables creativity while preventing
common pitfalls._
