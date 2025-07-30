---
date: 2021-03-22T10:00:00+05:30
draft: false
title: "TIL: Distributed Systems Education, Fallacies, and Self-Hosted Internet Archiving"
description: "Today I learned about CSE138 distributed systems lectures, the classic fallacies of distributed computing, and an interesting project for self-hosting internet archives."
tags:
  - distributed-systems
  - computer-science
  - education
  - networking
  - web-archiving
  - self-hosting
  - fallacies
---

## Distributed Systems Education

### CSE138 Distributed Systems Lectures
- [CSE138 (Distributed Systems) lectures, Spring 2020 - YouTube](https://youtube.com/playlist?list=PLNPUF5QyWU8O0Wd8QDh9KaM1ggsxspJ31)
- Comprehensive university-level course on distributed systems
- Covers fundamental concepts, algorithms, and practical considerations
- Free access to high-quality computer science education

### Course Topics
- **Consensus Algorithms**: Raft, Paxos, and other consensus mechanisms
- **Consistency Models**: CAP theorem, eventual consistency, strong consistency
- **Fault Tolerance**: Handling failures in distributed environments
- **Scalability**: Techniques for building systems that scale
- **Real-world Systems**: Case studies of production distributed systems

## Fundamental Concepts

### Fallacies of Distributed Computing
- [Fallacies of distributed computing - Wikipedia](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)
- Eight common false assumptions about distributed systems
- Originally identified by Peter Deutsch and James Gosling
- Essential knowledge for anyone building distributed systems

### The Eight Fallacies
1. **The network is reliable** - Networks fail, packets get lost
2. **Latency is zero** - Network calls have significant latency
3. **Bandwidth is infinite** - Network capacity is limited
4. **The network is secure** - Security cannot be assumed
5. **Topology doesn't change** - Network topology is dynamic
6. **There is one administrator** - Multiple parties manage different parts
7. **Transport cost is zero** - Network operations have costs
8. **The network is homogeneous** - Networks consist of diverse components

## Web Archiving and Self-Hosting

### 22120 - Self-Hosted Internet Archive
- [GitHub - i5ik/22120](https://github.com/i5ik/22120)
- NodeJS product for self-hosting internet archives offline
- Similar to ArchiveBox, SingleFile, and WebMemex but with unique features
- Allows creating personal, offline copies of web content

### Archive Features
- **Offline Browsing**: Access archived content without internet
- **Personal Control**: Own your data and browsing history
- **Full Pages**: Capture complete web pages including dynamic content
- **Search Capability**: Find content within your personal archive
- **Privacy**: Keep browsing and research private

## Key Takeaways

- **Education Access**: High-quality computer science education is increasingly available online
- **System Design**: Understanding distributed systems fallacies prevents common mistakes
- **Data Ownership**: Tools for personal data archiving become more important as web content changes
- **Learning Resources**: Combining theoretical knowledge with practical tools improves understanding

These resources span from fundamental computer science theory to practical tools for data preservation, showing the breadth of considerations in modern distributed systems and web technologies.