---
date: 2021-03-25T10:00:00+05:30
draft: false
title: "TIL: Modern Rust CLI Tools - System Monitoring, HTTP Requests, and DNS"
description: "Today I discovered five excellent Rust-based CLI tools: bottom, dust, procs for system monitoring, xh for HTTP requests, and nip.io for wildcard DNS resolution."
tags:
  - rust
  - system-monitoring
  - cli-tools
  - performance
  - unix-utilities
  - system-administration
  - http-client
  - dns
  - development-tools
---

## Modern System Monitoring Tools

### bottom - Cross-Platform System Monitor
- [GitHub - ClementTsang/bottom](https://github.com/ClementTsang/bottom)
- Modern alternative to `top` and `htop` written in Rust
- Cross-platform system and process monitor with rich visualizations
- Customizable interface with graphs, tables, and real-time updates

### dust - Intuitive Disk Usage Tool
- [GitHub - bootandy/dust](https://github.com/bootandy/dust)
- More intuitive version of `du` command written in Rust
- Visual representation of disk usage with colored output
- Fast scanning and clear hierarchy display

### procs - Modern Process Viewer
- [GitHub - dalance/procs](https://github.com/dalance/procs)
- Modern replacement for `ps` command written in Rust
- Enhanced output formatting with colors and additional information
- Better defaults and more user-friendly interface

### xh - Friendly HTTP Request Tool
- [GitHub - ducaale/xh](https://github.com/ducaale/xh)
- Fast and friendly tool for sending HTTP requests
- Rust-based alternative to curl and HTTPie
- Intuitive syntax with JSON support and colorized output

## Development and Testing Tools

### nip.io - Wildcard DNS Service
- [nip.io - wildcard DNS for any IP Address](https://nip.io/)
- Wildcard DNS service that maps any IP address to a hostname
- Useful for local development and testing without DNS configuration
- Format: `anything.192.168.1.1.nip.io` resolves to `192.168.1.1`

## Tool Comparisons

### bottom vs top/htop
- **Visualization**: Rich graphs for CPU, memory, network, and disk usage
- **Customization**: Configurable layouts and display options
- **Cross-platform**: Consistent behavior across different operating systems
- **Performance**: Efficient resource usage despite rich interface

### dust vs du
- **Visual Output**: Tree structure with color-coded size indicators
- **Speed**: Fast directory traversal and analysis
- **Clarity**: Immediately see which directories consume most space
- **User Experience**: More intuitive than traditional `du` output

### procs vs ps
- **Readable Output**: Better column formatting and color coding
- **Additional Info**: More process information displayed by default
- **Modern Interface**: Improved user experience with sensible defaults
- **Filtering**: Better process filtering and search capabilities

## Key Takeaways

- **Rust Ecosystem**: Growing ecosystem of system tools written in Rust
- **User Experience**: Modern tools prioritize usability without sacrificing functionality
- **Performance**: Rust enables fast, efficient system utilities
- **Cross-platform**: Consistent behavior across different operating systems
- **Tool Evolution**: Traditional Unix tools can be significantly improved with modern approaches

These tools demonstrate how modern programming languages and UX principles can enhance traditional system administration utilities, making them more accessible and powerful for daily use.