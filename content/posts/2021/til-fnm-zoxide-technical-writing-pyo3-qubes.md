---
date: 2021-04-18T10:00:00+05:30
draft: false
title: "TIL: Fast Node Manager, Zoxide Smart CD, Technical Writing, PyO3, and Qubes OS"
description: "Today I learned about fnm for fast Node.js version management, zoxide as a smarter cd command, technical writing resources, PyO3 for Python-Rust integration, and Qubes OS security architecture."
tags:
  - TIL
  - Node.js
  - Shell
  - Writing
  - Python
  - Rust
  - Security
---

## fnm - Fast Node Manager

[GitHub - Schniz/fnm](https://github.com/Schniz/fnm) - 🚀 Fast and simple Node.js version manager, built in Rust.

Lightning-fast alternative to nvm for managing Node.js versions:

### Key Advantages:
- **Rust Performance**: Significantly faster than shell-based alternatives
- **Cross-Platform**: Works on Windows, macOS, Linux
- **Simple API**: Intuitive commands for version switching
- **Shell Integration**: Automatic version switching based on `.nvmrc`
- **Minimal Dependencies**: Single binary installation

### Common Commands:
```bash
fnm install 16        # Install Node 16
fnm use 16           # Switch to Node 16
fnm default 16       # Set Node 16 as default
fnm list             # List installed versions
```

Perfect for developers who frequently switch between Node.js versions.

## Zoxide - Smarter CD Command

[GitHub - ajeetdsouza/zoxide](https://github.com/ajeetdsouza/zoxide) - A smarter cd command.

Intelligent directory navigation that learns from your usage patterns:

### How It Works:
- **Frequency Tracking**: Remembers directories you visit often
- **Fuzzy Matching**: Jump to directories with partial names
- **Recency Weighting**: Prioritizes recently visited directories
- **Smart Ranking**: Combines frequency and recency for optimal results

### Usage Examples:
```bash
z foo            # Jump to most frecent directory matching "foo"
z foo bar        # Jump to directory matching both "foo" and "bar"
zi foo           # Interactive selection when multiple matches
```

### Benefits:
- Reduces typing for common navigation
- Works across all your shell sessions
- Integrates with existing shell workflows
- Available for bash, zsh, fish, and PowerShell

## Technical Writing Guide

[How to Write a Technical Book — SerHack Blog](https://serhack.me/articles/how-to-write-technical-book/)

Comprehensive guide to writing technical books and documentation:

### Key Topics:
- **Planning**: Structuring content and defining audience
- **Writing Process**: Maintaining consistency and flow
- **Technical Accuracy**: Ensuring code examples work
- **Publishing**: Traditional vs self-publishing considerations
- **Marketing**: Building audience and promoting content

### Valuable Insights:
- Start with detailed outline
- Write code first, explanations second
- Get early feedback from target audience
- Focus on reader's learning journey
- Balance depth with accessibility

## PyO3 - Python-Rust Integration

[Introduction - PyO3 user guide](https://pyo3.rs/v0.13.2/)

Library for creating Python extensions in Rust:

### Capabilities:
- **Python Extensions**: Write fast Python modules in Rust
- **Python Bindings**: Call Rust code from Python
- **Native Types**: Seamless conversion between Python and Rust types
- **Error Handling**: Proper exception handling across language boundaries
- **Memory Safety**: Rust's safety guarantees in Python extensions

### Use Cases:
- Performance-critical Python code
- Existing Rust libraries exposed to Python
- CPU-intensive computations
- System-level programming accessible from Python

## Qubes OS - Security Through Isolation

[Introduction | Qubes OS](https://www.qubes-os.org/intro/)

Security-focused operating system using virtualization for isolation:

### Security Model:
- **Compartmentalization**: Different activities in separate VMs
- **Minimal Trust**: Assume components will be compromised
- **Isolation**: Prevent malware from spreading between domains
- **Controlled Communication**: Secure inter-domain communication

### Architecture:
- **Dom0**: Privileged management domain
- **AppVMs**: Isolated application virtual machines  
- **Templates**: Base images for creating VMs
- **Networking**: Separate VMs for network functions

### Use Cases:
- High-security environments
- Researchers handling malware
- Journalists protecting sources
- Anyone requiring strong compartmentalization

Each tool represents best-in-class solutions for their respective domains, emphasizing performance, security, and developer productivity.