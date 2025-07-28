---
date: 2021-04-15T10:00:00+05:30
draft: false
title: "TIL: CORS Deep Dive, Piku Tiny PaaS, Rust Strings, and Deno Standard Library"
description: "Today I learned about CORS in depth, Piku for git-push deployments, why Rust strings seem challenging, and Deno's standard library for modern JavaScript runtime."
tags:
  - TIL
  - CORS
  - Deployment
  - Rust
  - Strings
  - Deno
  - JavaScript
---

## Deep Dive into CORS

[Deep dive in CORS: History, how it works, and best practices](https://ieftimov.com/post/deep-dive-cors-history-how-it-works-best-practices/)

Comprehensive exploration of Cross-Origin Resource Sharing:

### Historical Context:
- **Same-Origin Policy**: Browser security feature from the early web
- **AJAX Era**: XMLHttpRequest created need for cross-origin requests
- **CORS Solution**: W3C specification to safely allow cross-origin requests
- **Modern Challenges**: Single-page applications and microservices architecture

### How CORS Works:

#### **Simple Requests:**
- **Automatic Headers**: Browser adds Origin header automatically
- **Server Response**: Server includes Access-Control-Allow-Origin header
- **Browser Enforcement**: Browser blocks response if origins don't match

#### **Preflight Requests:**
- **OPTIONS Method**: Browser sends preflight request for complex requests
- **Permission Check**: Server responds with allowed methods, headers, origins
- **Actual Request**: Browser sends actual request only if preflight succeeds

### Best Practices:
- **Specific Origins**: Avoid wildcard (*) in production
- **Minimal Headers**: Only allow necessary headers
- **Credential Handling**: Careful with Access-Control-Allow-Credentials
- **Error Handling**: Proper CORS error responses

## Piku - Tiny PaaS

[GitHub - piku/piku](https://github.com/piku/piku) - The tiniest PaaS you've ever seen. Git push deployments to your own servers.

Lightweight Platform-as-a-Service for simple deployments:

### Key Features:
- **Git-Based Deployment**: Deploy with simple `git push`
- **Minimal Dependencies**: Single Python script with minimal requirements
- **Multi-Language Support**: Python, Node.js, Go, Ruby, and more
- **Process Management**: Automatic process supervision and restart
- **Environment Variables**: Configuration through environment files

### How It Works:
```bash
git remote add piku piku@server:app-name
git push piku main
```

### Perfect For:
- **Small Projects**: Personal projects and prototypes
- **Learning**: Understanding deployment concepts
- **Resource-Constrained**: Single server deployments
- **Simplicity**: When Kubernetes is overkill

## Why Rust Strings Seem Hard

[Why Rust strings seem hard](https://www.brandons.me/blog/why-rust-strings-seem-hard)

Excellent explanation of Rust's string complexity:

### The Challenge:
- **Multiple Types**: `String`, `&str`, `OsString`, `Path`, etc.
- **Memory Management**: Ownership and borrowing with strings
- **UTF-8 Enforcement**: Always valid Unicode, unlike C strings
- **Performance Considerations**: Zero-copy operations when possible

### Key Concepts:

#### **String Types:**
- **`String`**: Owned, mutable, heap-allocated
- **`&str`**: Borrowed, immutable, string slice
- **Relationship**: `String` can be borrowed as `&str`

#### **Common Patterns:**
```rust
let owned = String::from("hello");    // Owned string
let borrowed = &owned;                // Borrowed as &str
let slice = &owned[0..2];            // String slice
```

### Why It's Actually Logical:
- **Memory Safety**: Prevents buffer overflows and use-after-free
- **Performance**: Zero-cost abstractions where possible
- **Correctness**: UTF-8 validity guaranteed at compile time

## Deno Standard Library

[Deno Standard Library](https://deno.land/std@0.93.0)

Modern standard library for Deno JavaScript/TypeScript runtime:

### Philosophy:
- **Modern APIs**: Built for contemporary JavaScript features
- **TypeScript First**: Full TypeScript support out of the box
- **Web Standards**: Aligned with web platform APIs
- **Security**: Secure by default with explicit permissions

### Key Modules:
- **HTTP**: Web server and client functionality
- **File System**: File and directory operations
- **Testing**: Unit testing framework
- **Encoding**: Base64, hex, and other encoding utilities
- **Crypto**: Cryptographic functions
- **UUID**: UUID generation and validation

### Advantages Over Node.js:
- **No package.json**: Direct URL imports
- **Built-in TypeScript**: No compilation step needed
- **Web Standards**: Fetch, WebCrypto, etc.
- **Secure**: Permissions required for file, network access

Each tool represents a different approach to solving common development challenges with emphasis on simplicity, security, and modern standards.