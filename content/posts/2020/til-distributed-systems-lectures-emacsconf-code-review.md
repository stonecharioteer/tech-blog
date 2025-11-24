---
date: 2020-12-08T10:00:00+05:30
draft: false
title:
  "TIL: Distributed Systems Lectures, EmacsConf 2020, Code Review Excellence,
  and Accessibility Guidelines"
description:
  "Today I learned about comprehensive distributed systems education, EmacsConf
  2020 presentations, strategies for making code reviewers love your work, and
  modern web accessibility practices."
tags:
  - til
  - distributed-systems
  - emacs
  - code-review
  - accessibility
  - javascript
  - python
---

Today's learning spanned distributed systems theory, editor conferences, code
review best practices, and web accessibility standards.

## Distributed Systems Lecture Series

[Distributed Systems lecture series](https://youtube.com/playlist?list=PLeKd45zvjcDFUEv_ohr_HdUFe97RItdiB)
provides comprehensive coverage of distributed computing concepts through
academic-quality presentations.

### Core Topics Covered:

- **Consensus algorithms**: Raft, PBFT, and Byzantine fault tolerance
- **Consistency models**: Strong consistency, eventual consistency, and CAP
  theorem implications
- **Distributed storage**: Replication strategies, sharding, and data
  consistency
- **System design patterns**: Leader election, distributed locking, and
  coordination primitives

### Educational Value:

- **Theoretical foundations**: Mathematical proofs and formal verification
- **Practical applications**: Real-world system examples and case studies
- **Implementation guidance**: How theory translates to production systems
- **Research insights**: Latest developments in distributed computing research

## EmacsConf 2020

[EmacsConf 2020](https://emacsconf.org/2020/) showcased the vibrant Emacs
community with presentations on advanced editing techniques, package
development, and innovative Emacs applications.

### Notable Presentations:

- **Org-mode innovations**: Advanced task management and publishing workflows
- **Package development**: Creating and maintaining Emacs extensions
- **Integration techniques**: Connecting Emacs with external tools and services
- **Performance optimization**: Making Emacs faster and more responsive

The conference demonstrated Emacs' continued evolution and the creativity of its
user community in extending the editor's capabilities.

## Gerald Jay Sussman on Flexible Systems

[Gerald Jay Sussman's talk on Flexible Systems](https://youtu.be/cblhgNUoX9M)
explores the power of generic operations in building adaptable software systems.

### Key Concepts:

- **Generic procedures**: Operations that work across multiple data types
- **Dispatch mechanisms**: How systems choose appropriate implementations
- **Extensibility patterns**: Adding new types without modifying existing code
- **Composability**: Building complex systems from simple, interchangeable parts

Sussman's insights apply to modern software architecture, showing how functional
programming principles create more maintainable and extensible systems.

## Code Review Excellence

[How to Make Your Code Reviewer Fall in Love with You](https://mtlynch.io/code-review-love/)
provides practical strategies for creating pull requests that reviewers
appreciate.

### Pre-Review Preparation:

- **Self-review first**: Find and fix obvious issues before submitting
- **Clear descriptions**: Explain the problem, solution, and design decisions
- **Appropriate scope**: Keep changes focused and reasonably sized
- **Test coverage**: Include tests that demonstrate correctness

### Communication Strategies:

- **Proactive explanations**: Address potential questions in comments
- **Constructive responses**: Handle feedback professionally and thoroughly
- **Quick turnarounds**: Respond to reviews promptly to maintain momentum
- **Learning mindset**: Treat reviews as learning opportunities

## Python Learning Resources

[Intermediate Python](https://book.pythontips.com/en/latest/) covers advanced
Python concepts beyond basic syntax:

### Advanced Topics:

- **Decorators and context managers**: Meta-programming techniques
- **Generators and iterators**: Memory-efficient data processing
- **Threading and multiprocessing**: Concurrent programming patterns
- **Performance optimization**: Profiling and optimization strategies

## Modern JavaScript Education

[The Modern JavaScript Tutorial](https://javascript.info/) provides
comprehensive coverage of contemporary JavaScript development:

### Coverage Areas:

- **Language fundamentals**: ES6+ features and modern syntax
- **Browser APIs**: DOM manipulation, events, and web platform features
- **Asynchronous programming**: Promises, async/await, and error handling
- **Advanced patterns**: Modules, classes, and functional programming concepts

## Web Accessibility Standards

[ARIA Labels and Descriptions](https://benmyers.dev/blog/aria-labels-and-descriptions/)
explains the differences between `aria-label`, `aria-labelledby`, and
`aria-describedby` attributes:

### Key Distinctions:

- **`aria-label`**: Provides accessible names when visible text is insufficient
- **`aria-labelledby`**: References other elements that label the current
  element
- **`aria-describedby`**: Points to elements that provide additional description

### Implementation Guidelines:

- **Screen reader compatibility**: How different attributes are announced
- **Context appropriateness**: When to use each approach
- **Testing strategies**: Validating accessibility implementations

These resources collectively provide deep technical knowledge across distributed
systems, development tools, code quality practices, and inclusive web
development.
