---
date: 2021-01-14T10:00:00+05:30
draft: false
title:
  "TIL: UNIX Programming Course, Finding Duplicate Files, and Livestreaming Tips"
description:
  "Today I discovered a comprehensive UNIX programming course, learned
  techniques for finding duplicate files on Linux, and found practical tips for
  technical livestreaming."
tags:
  - "unix"
  - "system-administration"
  - "duplicate-files"
  - "livestreaming"
  - "education"
  - "linux"
  - "content-creation"
---

## UNIX Systems Programming Education

### CS631 Advanced Programming in the UNIX Environment

- [CS631 Advanced Programming in the UNIX Environment - YouTube](https://youtube.com/playlist?list=PL0qfF8MrJ-jxMfirAdxDs9zIiBg2Wug0z)
- Complete university-level course on UNIX systems programming
- Covers advanced topics in UNIX/Linux system calls and programming
- Free access to high-quality computer science education

### Course Content Areas

- **System Calls**: Low-level interaction with the operating system
- **Process Management**: Creating, managing, and communicating between
  processes
- **File Systems**: Understanding UNIX file system internals
- **Network Programming**: Socket programming and network communications
- **Inter-Process Communication**: Pipes, signals, shared memory, and message
  queues
- **Security**: UNIX security model and secure programming practices

### Learning Benefits

- **Systems Understanding**: Deep knowledge of how UNIX systems work internally
- **Professional Skills**: Essential knowledge for systems programming roles
- **C Programming**: Advanced C programming in systems context
- **Performance**: Understanding performance implications of system calls
- **Debugging**: Techniques for debugging systems-level programs

## System Administration Tools

### Finding Duplicate Files on Linux

- [How to Find Duplicate Files on Linux - buildVirtual](https://buildvirtual.net/how-to-find-duplicate-files-on-linux/)
- Practical guide to identifying and managing duplicate files
- Multiple approaches using different tools and techniques
- Important for storage management and system cleanup

### Duplicate File Detection Methods

- **fdupes**: Dedicated tool for finding duplicate files
- **rdfind**: Another specialized duplicate finder
- **find + md5sum**: Manual approach using standard tools
- **dupe-guru**: GUI application for duplicate management
- **jdupes**: Improved version of fdupes with better performance

### Use Cases and Benefits

- **Storage Optimization**: Reclaim disk space by removing duplicates
- **Backup Cleanup**: Remove redundant files from backup sets
- **Media Management**: Organize photo and music collections
- **System Maintenance**: Regular cleanup as part of system maintenance
- **Data Deduplication**: Reduce storage requirements for large datasets

### Command Examples

```bash
# Using fdupes to find duplicates
fdupes -r /path/to/directory

# Using find and md5sum
find /path -type f -exec md5sum {} \; | sort | uniq -d -w32

# Using rdfind
rdfind -makehardlinks true /path/to/directory
```

## Content Creation and Education

### Livestreaming Tips for Technical Content

- [Livestream tips :: Jon Gjengset](https://thesquareplanet.com/blog/livestream-tips/)
- Practical advice for technical livestreaming
- Written by Jon Gjengset, known for Rust programming streams
- Covers technical, equipment, and presentation aspects

### Technical Livestreaming Considerations

- **Audio Quality**: Most important aspect of stream quality
- **Screen Setup**: Optimal resolution and font sizes for viewers
- **Content Planning**: Balancing preparation with spontaneity
- **Interaction**: Engaging with chat while maintaining focus
- **Technical Setup**: OBS configuration, scene management, hotkeys

### Educational Streaming Benefits

- **Learning in Public**: Teaching while learning new concepts
- **Community Building**: Creating educational communities around topics
- **Accessibility**: Making learning resources freely available
- **Real-time Feedback**: Immediate questions and discussions
- **Documentation**: Recorded streams serve as educational content

### Stream Content Ideas

- **Code Reviews**: Reviewing and discussing code quality
- **Tutorial Series**: Step-by-step learning content
- **Problem Solving**: Working through algorithms or system design
- **Tool Exploration**: Discovering and learning new tools
- **Project Development**: Building projects from start to finish

## Key Takeaways

- **Educational Resources**: High-quality computer science education
  increasingly available online
- **Systems Knowledge**: Understanding UNIX internals crucial for systems
  programming
- **Maintenance Skills**: Regular system maintenance requires knowledge of
  cleanup tools
- **Content Creation**: Technical livestreaming can be valuable for both
  creators and viewers
- **Community Learning**: Shared learning experiences benefit everyone involved
- **Practical Skills**: Combining theoretical knowledge with practical tools and
  techniques

These resources span from foundational computer science education to practical
system administration and modern content creation, showing how technical
knowledge can be both acquired and shared in various formats.
