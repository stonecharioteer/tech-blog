---
date: 2021-02-28T10:00:00+05:30
draft: false
title: "TIL: Cosmopolitan C Library, Distributed Systems Book, High Performance Browser Networking, and Rust Roguelike Tutorial"
description: "Today I learned about the Cosmopolitan C Library for portable executables, an accessible distributed systems book, high-performance browser networking principles, and building roguelike games in Rust."
tags:
  - TIL
  - C Programming
  - Distributed Systems
  - Networking
  - Browser Performance
  - Rust
  - Game Development
---

## Cosmopolitan C Library

[Cosmopolitan C Library](https://justine.lol/cosmopolitan/index.html)

Revolutionary C library that creates truly portable executables:

### What Makes It Special:
- **Actually Portable Executables**: Single binary runs on Windows, macOS, Linux, and BSD
- **No Runtime Dependencies**: Completely self-contained executables
- **Multi-Architecture**: Supports x86_64, ARM64, and other architectures
- **Zero Configuration**: Works out of the box without complex build systems

### How It Works:

#### **Polyglot Binary Format:**
- **Multiple Headers**: Contains DOS, PE, and ELF headers in one file
- **Fat Binary**: Includes code for different operating systems
- **Smart Loading**: OS picks appropriate code section automatically
- **Compression**: Efficient packing reduces file size

#### **System Abstraction:**
```c
#include "libc/stdio/stdio.h"
#include "libc/calls/calls.h"

int main() {
    printf("Hello from everywhere!\n");
    return 0;
}
```

### Key Features:
- **POSIX Compatibility**: Standard C library interface
- **Modern C**: Support for C11 and newer standards
- **Performance**: Optimized implementations for different platforms
- **Security**: Memory-safe alternatives and security features

### Use Cases:
- **Cross-Platform Tools**: Development utilities that work everywhere
- **Embedded Software**: Minimal runtime requirements
- **Game Development**: Portable game engines and tools
- **Scientific Computing**: Reproducible research across platforms

## Distributed Systems for Fun and Profit

[Distributed systems for fun and profit](http://book.mixu.net/distsys/)

Accessible introduction to distributed systems concepts:

### Learning Approach:
- **Practical Focus**: Real-world problems and solutions
- **Clear Explanations**: Complex concepts made understandable
- **Progressive Complexity**: Builds from basics to advanced topics
- **Implementation Examples**: Code samples and practical exercises

### Core Topics:

#### **Distributed System Basics:**
- **Scalability**: Handling increased load through distribution
- **Fault Tolerance**: Continuing operation despite failures
- **Consistency**: Maintaining data coherence across nodes
- **Performance**: Latency and throughput considerations

#### **System Models:**
- **Network Model**: How nodes communicate
- **Failure Model**: Types of failures and their handling
- **Timing Model**: Synchronous vs asynchronous systems
- **Consensus Model**: Agreement in distributed environments

### Key Insights:
- **Trade-offs**: Understanding CAP theorem implications
- **Complexity**: Distribution adds inherent complexity
- **Debugging**: Challenges in distributed system debugging
- **Testing**: Strategies for testing distributed systems

## High Performance Browser Networking

[High Performance Browser Networking (O'Reilly)](https://hpbn.co/)

Comprehensive guide to optimizing web application performance:

### Networking Fundamentals:

#### **Transport Protocols:**
- **TCP**: Connection-oriented, reliable transport
- **UDP**: Connectionless, fast but unreliable
- **HTTP/1.1**: Request-response over TCP
- **HTTP/2**: Multiplexing and server push
- **HTTP/3**: QUIC-based for improved performance

#### **Latency and Bandwidth:**
- **Speed of Light**: Physical limits of network communication
- **Last Mile**: Often the bottleneck in network performance
- **CDN Benefits**: Geographical distribution reduces latency
- **Connection Pooling**: Reusing connections for efficiency

### Browser Optimization:

#### **Resource Loading:**
- **Critical Rendering Path**: What blocks initial page render
- **Resource Prioritization**: Loading important resources first
- **Compression**: Gzip, Brotli for reducing transfer size
- **Caching**: Browser and HTTP caching strategies

#### **Modern Web APIs:**
- **Service Workers**: Offline capability and caching control
- **WebRTC**: Peer-to-peer communication
- **WebSockets**: Full-duplex communication
- **Server-Sent Events**: Real-time server-to-client updates

### Performance Techniques:
- **Minimize Round Trips**: Reduce network requests
- **Optimize Payloads**: Smaller, compressed resources
- **Leverage Caching**: Effective cache strategies
- **Use CDNs**: Geographic distribution of content

## Roguelike Tutorial in Rust

[Introduction - Roguelike Tutorial - In Rust](https://bfnightly.bracketproductions.com/rustbook/)

Complete guide to building roguelike games using Rust:

### What are Roguelikes:
- **Turn-Based**: Player and entities take turns
- **Procedural Generation**: Randomly generated levels
- **Permadeath**: Character death is permanent
- **ASCII Graphics**: Traditional text-based display

### Rust for Game Development:

#### **Performance Benefits:**
- **Zero-Cost Abstractions**: High-level code without runtime overhead
- **Memory Safety**: Prevents common game crashes
- **Concurrency**: Safe parallel processing
- **Predictable Performance**: No garbage collection pauses

#### **Game Architecture:**
```rust
// Entity Component System (ECS) pattern
struct Position { x: i32, y: i32 }
struct Renderable { glyph: char, color: Color }
struct Player;

// Systems process components
fn movement_system(positions: &mut Vec<Position>, input: Input) {
    // Update positions based on input
}
```

### Tutorial Progression:

#### **Basic Implementation:**
1. **Hello World**: Basic Rust setup and window creation
2. **Map Generation**: Creating dungeon layouts
3. **Entity System**: Players, monsters, and items
4. **Game Loop**: Turn-based mechanics

#### **Advanced Features:**
1. **Field of View**: Realistic vision systems
2. **Combat System**: Damage, health, and death
3. **Inventory**: Item management and usage
4. **AI Systems**: Monster behavior and pathfinding

### Technologies Used:
- **RLTK (Rust Libtcod Toolkit)**: Game development framework
- **Specs ECS**: Entity Component System
- **Serde**: Serialization for save games
- **Rand**: Random number generation

### Learning Outcomes:
- **Rust Proficiency**: Real-world Rust programming
- **Game Design**: Core roguelike mechanics
- **Algorithm Implementation**: Pathfinding, generation algorithms
- **Systems Programming**: Low-level game engine concepts

Each resource provides deep technical knowledge in its domain - from system-level programming to distributed architecture, web performance optimization, and game development with modern languages.