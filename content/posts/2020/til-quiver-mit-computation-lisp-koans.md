---
date: 2020-11-29T10:00:00+05:30
draft: false
title:
  "TIL: Quiver Diagram Editor, MIT Computation Structures, Lisp Koans, and
  Python System Services"
description:
  "Today I learned about Quiver's web-based commutative diagram editor, MIT's
  comprehensive computation structures course, Common Lisp learning through
  koans, and creating Python systemd services."
tags:
  - til
  - mathematics
  - diagrams
  - computer-science
  - lisp
  - python
  - systemd
  - file-management
---

Today's learning spanned mathematical visualization tools, foundational computer
science education, functional programming, and system administration with
Python.

## Quiver - Web-Based Commutative Diagram Editor

[Quiver](https://varkor.github.io/blog/2020/11/25/announcing-quiver.html) is an
innovative web-based tool for creating commutative diagrams, essential for
category theory, abstract algebra, and mathematical research.

### Key Features:

#### **Mathematical Precision:**

- **Category theory support**: Proper handling of objects, morphisms, and
  composition
- **Commutative diagram validation**: Automatic checking for diagram consistency
- **LaTeX integration**: Seamless export to academic papers and presentations
- **Professional rendering**: High-quality output suitable for publication

#### **User Experience:**

```
# Example usage workflow:
1. Create objects (categories, sets, groups)
2. Draw morphisms (functions, mappings, transformations)
3. Verify commutativity conditions
4. Export to TikZ, SVG, or direct LaTeX
```

#### **Collaborative Features:**

- **URL sharing**: Share diagrams via links for collaboration
- **Version control**: Track changes and iterations
- **Template library**: Common diagram patterns and structures
- **Cross-platform**: Works in any modern web browser

### Applications:

- **Research mathematics**: Category theory, algebraic topology, homological
  algebra
- **Computer science**: Type theory, programming language semantics
- **Education**: Teaching abstract mathematical concepts visually
- **Documentation**: Illustrating complex system architectures and relationships

## MIT Computation Structures Course

[MIT 6.004: Computation Structures](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-004-computation-structures-spring-2017/)
provides comprehensive coverage of digital systems from transistors to operating
systems.

### Curriculum Overview:

#### **Hardware Foundations:**

- **Digital abstraction**: Boolean logic, combinational and sequential circuits
- **Computer arithmetic**: Number representation, ALU design, floating-point
- **Processor design**: RISC architecture, pipelining, hazard handling
- **Memory hierarchy**: Caches, virtual memory, storage systems

#### **Software Systems:**

- **Assembly language**: Machine instruction sets and programming
- **Operating systems**: Processes, scheduling, memory management, I/O
- **Compilers**: Translation from high-level languages to machine code
- **System performance**: Analyzing and optimizing computer systems

#### **Design Methodology:**

- **Abstraction layers**: How complex systems are built from simple components
- **Trade-offs**: Performance vs. cost vs. power consumption
- **Testing and verification**: Ensuring correctness in digital systems
- **Engineering design process**: Requirements, implementation, validation

### Educational Value:

- **Fundamental understanding**: How computers work from first principles
- **Systems thinking**: Understanding interactions between hardware and software
- **Design skills**: Creating efficient and reliable digital systems
- **Practical experience**: Labs with real hardware and software tools

## Common Lisp Koans

[Google's Lisp Koans](https://github.com/google/lisp-koans) provide a structured
learning path for Common Lisp through progressive exercises, following the
proven koan methodology.

### Learning Approach:

#### **Progressive Skill Building:**

```lisp
;; Example koan progression:
;; Basic forms
(assert-equal 5 (+ 2 3))

;; List manipulation
(assert-equal '(1 2 3) (cons 1 '(2 3)))

;; Higher-order functions
(assert-equal '(2 4 6) (mapcar (lambda (x) (* x 2)) '(1 2 3)))

;; Macros and metaprogramming
(defmacro when-not (condition &body body)
  `(unless ,condition ,@body))
```

#### **Core Concepts Covered:**

- **S-expressions**: Uniform syntax for code and data
- **Functional programming**: Pure functions, recursion, higher-order functions
- **Macros**: Code generation and domain-specific languages
- **Object system (CLOS)**: Multiple inheritance, method dispatch, metaclasses

### Benefits of Koan-Style Learning:

- **Immediate feedback**: Broken tests guide learning progression
- **Hands-on practice**: Learning through doing rather than passive reading
- **Gradual complexity**: Each exercise builds on previous knowledge
- **Self-paced**: Work through concepts at your own speed

## Python systemd Services

[Python systemd tutorial](https://github.com/torfsen/python-systemd-tutorial)
demonstrates how to create robust system services using Python with proper
systemd integration.

### Service Implementation:

#### **Basic Service Structure:**

```python
#!/usr/bin/env python3
import systemd.daemon
import time
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Notify systemd that service is ready
    systemd.daemon.notify('READY=1')

    while True:
        # Service main loop
        logger.info("Service running...")
        time.sleep(10)

        # Periodic status updates
        systemd.daemon.notify('STATUS=Processing requests')

if __name__ == '__main__':
    main()
```

#### **Systemd Unit File:**

```ini
[Unit]
Description=My Python Service
After=network.target

[Service]
Type=notify
User=myservice
Group=myservice
WorkingDirectory=/opt/myservice
ExecStart=/opt/myservice/venv/bin/python /opt/myservice/service.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Best Practices:

- **Proper user isolation**: Run services with dedicated system users
- **Virtual environments**: Isolated Python dependencies
- **Logging integration**: Use systemd's journal for centralized logging
- **Graceful shutdown**: Handle SIGTERM for clean service termination
- **Health monitoring**: Implement status reporting and watchdog support

## Additional Resources

### Development Tools:

- **Digital File Management**: Systematic approaches to organizing digital
  assets
- **ripgrep-all (rga)**: Search across PDFs, documents, and archives
- **GitPython**: Programmatic Git repository manipulation

### Historical Computing:

- **Ken Thompson's 1976 Unix Shell Paper**: Foundational document transcribed
  and redistributed
- **urllib3**: Understanding HTTP client libraries and connection pooling

### System Administration:

- **Process tree visualization**: Using `pstree` for system debugging
- **Unix shell fundamentals**: Understanding command-line interfaces and
  scripting

These discoveries represent the intersection of theoretical computer science,
practical system administration, mathematical visualization, and programming
language design - essential knowledge areas for comprehensive technical
understanding.
