---
date: 2021-05-25T10:00:00+05:30
draft: false
title: "TIL: CRDTs, Extreme HTTP Performance, and BYTEPATH Game"
description:
  "Today I learned about CRDTs for distributed systems, extreme HTTP performance
  tuning achieving 1.2M API requests/second, and BYTEPATH - a replayable arcade
  shooter game."
tags:
  - TIL
  - Distributed Systems
  - Performance
  - HTTP
  - Game Development
  - CRDTs
---

## CRDTs: The Hard Parts

[CRDTs: The Hard Parts - YouTube](https://youtu.be/x7drE24geUw)

An excellent talk about Conflict-free Replicated Data Types (CRDTs) and the
challenging aspects of implementing them in distributed systems. CRDTs allow
multiple nodes to update shared data without coordination, automatically
resolving conflicts.

## Extreme HTTP Performance Tuning

[Extreme HTTP Performance Tuning: 1.2M API req/s on a 4 vCPU EC2 Instance](https://talawah.io/blog/extreme-http-performance-tuning-one-point-two-million/)

Fascinating deep dive into achieving 1.2 million API requests per second on a
single 4 vCPU EC2 instance. Covers:

- Network stack optimizations
- Application-level tuning
- System-level configuration
- Benchmarking methodologies
- Real-world performance considerations

## BYTEPATH - Arcade Shooter Game

[GitHub - a327ex/BYTEPATH](https://github.com/a327ex/BYTEPATH) - A replayable
arcade shooter with a focus on build theorycrafting.

An interesting game development project that combines:

- Arcade shooter mechanics
- Build theorycrafting (like RPG character builds)
- Replayability through different strategies
- Clean game architecture and code organization

Great resource for learning game development patterns and Lua programming.
