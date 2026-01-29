---
date: 2021-05-11T10:00:00+05:30
draft: false
title: "TIL: McFly - Smart Shell History Search"
description:
  "Today I learned about McFly, a shell history search tool that learns from
  your usage patterns and provides intelligent command suggestions with fuzzy
  searching."
tags:
  - "til"
  - "shell"
  - "cli"
  - "productivity"
  - "tools"
---

## McFly - Intelligent Shell History

[GitHub - cantino/mcfly](https://github.com/cantino/mcfly) - Fly through your
shell history. Great Scott!

McFly replaces your default shell history search (Ctrl+R) with a smarter
alternative:

### Key Features:

- **Learning Algorithm**: Prioritizes commands based on frequency, recency, and
  context
- **Fuzzy Search**: Find commands even with typos or partial matches
- **Visual Interface**: Shows command context and selection clearly
- **Cross-Shell Support**: Works with bash, zsh, and fish
- **Fast Performance**: Written in Rust for speed
- **Directory Context**: Considers which directory commands were run in

### Why It's Better:

- Learns your workflow patterns over time
- Reduces time spent searching through history
- More intuitive than standard Ctrl+R search
- Great for developers who run many similar commands

This is particularly useful for developers who frequently run complex commands
with multiple flags and need quick access to their command history.
