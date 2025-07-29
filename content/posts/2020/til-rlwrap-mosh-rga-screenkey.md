---
date: 2020-12-03T10:00:00+05:30
draft: false
title: "TIL: rlwrap for Readline, Mosh Mobile Shell, rga Document Search, and DMOTE Keyboard"
description: "Today I learned about rlwrap for adding readline support to any command, Mosh for reliable remote connections, rga for searching inside documents, and the innovative DMOTE ergonomic keyboard design."
tags:
  - til
  - terminal
  - ssh
  - search-tools
  - keyboards
  - ergonomics
  - productivity
---

Today's discoveries focused on terminal productivity tools, remote connection solutions, and innovative hardware design.

## rlwrap - Universal Readline Support

[rlwrap](https://github.com/hanslub42/rlwrap) is a readline wrapper that adds command history, editing capabilities, and tab completion to any interactive command-line program.

### Key Features:
- **Command history**: Navigate through previous commands with arrow keys
- **Line editing**: Full Emacs or vi-style editing capabilities
- **Tab completion**: Customizable completion for arguments and options
- **History persistence**: Commands saved across sessions

### Usage Examples:
```bash
# Add readline support to any REPL
rlwrap python3
rlwrap node
rlwrap sqlite3 database.db

# Custom completion files
rlwrap -f ~/.rlwrap/completions/myprogram myprogram

# Persistent history per program
rlwrap -H ~/.history/python_history python3
```

### Benefits:
- **Improved REPL experience**: Essential for languages without built-in readline
- **Consistent interface**: Same editing commands across different tools
- **Productivity boost**: Faster command entry and repetition
- **Zero configuration**: Works immediately with any interactive program

## Mosh - Mobile Shell

[Mosh (Mobile Shell)](https://mosh.org/) provides a superior alternative to SSH for unreliable network connections, particularly useful for mobile and intermittent connectivity scenarios.

### Advantages Over SSH:

#### **Network Resilience:**
- **Connection roaming**: Maintains session when switching networks
- **Intermittent connectivity**: Handles temporary disconnections gracefully
- **Poor network performance**: Responsive even with high latency or packet loss
- **Mobile-friendly**: Designed for laptops closing/opening, Wi-Fi switching

#### **Technical Features:**
- **UDP-based protocol**: More efficient than TCP for interactive sessions
- **Client-side echo**: Immediate response to typing, corrected when server responds
- **Intelligent scrollback**: Only transmits screen differences
- **Strong crypto**: AES-128-OCB authenticated encryption

### Use Cases:
- **Mobile development**: Coding on trains, planes, coffee shops
- **Remote work**: Maintaining connections during network instability
- **International connections**: Better performance over long distances
- **Intermittent networks**: Development in areas with unreliable connectivity

## rga - Ripgrep for All Document Types

[rga (ripgrep-all)](https://phiresky.github.io/blog/2019/rga--ripgrep-for-zip-targz-docx-odt-epub-jpg/) extends ripgrep's lightning-fast search to work with PDFs, Office documents, ebooks, archives, and even images with OCR.

### Supported Formats:
```bash
# Archive formats
rga "search term" *.zip *.tar.gz *.7z

# Office documents
rga "quarterly report" *.docx *.xlsx *.pptx

# PDFs and ebooks
rga "chapter summary" *.pdf *.epub *.mobi

# With OCR for images
rga --rga-adapters=tesseract "text in image" *.png *.jpg
```

### Advanced Features:
- **Preprocessing adapters**: Automatically detects and converts file types
- **Parallel processing**: Multi-threaded search across large document collections
- **Caching**: Preprocessed content cached for faster subsequent searches
- **Configurable**: Choose which adapters to use for different scenarios

### Performance Benefits:
- **Native speed**: Built on ripgrep's optimized search engine
- **Smart filtering**: Only processes files likely to contain matches
- **Memory efficient**: Streams large documents without loading entirely
- **Index-free**: No need to build search indexes, works immediately

## DMOTE Ergonomic Keyboard

[The DMOTE](https://viktor.eikman.se/article/the-dmote/) represents advanced ergonomic keyboard design, addressing common issues with traditional and even split keyboards.

### Design Principles:

#### **Ergonomic Innovations:**
- **3D printed case**: Custom-fit design for individual hand geometry
- **Concave key wells**: Keys positioned for natural finger movement
- **Adjustable thumb clusters**: Optimized thumb key placement
- **Tenting and tilting**: Customizable wrist angles

#### **Technical Features:**
- **Hot-swappable switches**: Easy key switch replacement without soldering
- **Modular design**: Components can be adjusted or replaced
- **Open source**: Full build documentation and 3D models available
- **QMK firmware**: Fully programmable layout and macros

### Benefits for Developers:
- **Reduced strain**: Better wrist positioning reduces RSI risk
- **Customization**: Layout optimized for programming symbols and shortcuts
- **Comfort**: Long coding sessions with less fatigue
- **Adaptability**: Can be modified as needs change

### Additional Tools:

- **Screenkey**: Display pressed keys on screen for presentations and tutorials
- **Unclutter**: Automatically hide cursor when idle to reduce visual distraction
- **User Research Guide**: Framework for understanding user needs and behaviors

These tools collectively address common pain points in development workflows: improving terminal interactions, maintaining reliable remote connections, searching across diverse document types, and creating more comfortable physical interfaces for extended computer use.