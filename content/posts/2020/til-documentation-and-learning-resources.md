---
date: 2020-07-17T19:00:00+05:30
draft: false
title: "TIL: Documentation Systems and Educational Resources"
description:
  "Today I learned about effective documentation systems, comprehensive learning
  resources for computer science, and modern educational platforms from my
  archive."
tags:
  - til
  - documentation
  - education
  - computer-science
  - learning-resources
  - sphinx
  - rust
  - cryptography
---

Today I explored my archive and discovered excellent resources on documentation
systems, educational content, and structured learning approaches that every
developer should know about.

## The Four-Part Documentation System

### Divio's Documentation Framework

[Divio's Documentation System](https://www.divio.com/blog/documentation/)
presents a revolutionary approach to organizing technical documentation into
four distinct types:

{{< note title="The Four Types of Documentation" >}}

1. **Tutorials** - Learning-oriented, hands-on lessons
2. **How-to Guides** - Problem-oriented, step-by-step solutions
3. **Reference** - Information-oriented, systematic descriptions
4. **Explanation** - Understanding-oriented, theoretical knowledge {{< /note >}}

This framework was beautifully explained in the video
**[What Nobody Tells You about Documentation](https://www.youtube.com/watch?v=t4vKPhjcMZg)** -
one of the greatest presentations on documentation structure I've encountered.

### Why This Framework Works

Each documentation type serves a different user need:

```
                Learning        Working
    Study   |  Tutorials   |  How-to Guides  |
            |              |                 |
    Work    | Explanation  |   Reference     |
```

**Tutorials** guide newcomers through their first successful experience with
your product. **How-to guides** solve specific real-world problems for
experienced users. **Reference** materials provide systematic, complete
information. **Explanations** clarify concepts and design decisions.

{{< example title="Documentation Type Examples" >}}

- **Tutorial**: "Build your first Django app"
- **How-to**: "How to deploy Django with Docker"
- **Reference**: "Django settings configuration"
- **Explanation**: "Why Django uses MVT architecture" {{< /example >}}

### Google Season of Docs

[Google Season of Docs](https://developers.google.com/season-of-docs) is a
program designed to improve open source documentation by connecting technical
writers with open source communities. It's similar to Google Summer of Code but
focuses specifically on documentation projects.

## Advanced Sphinx Documentation

### Sphinx Tabs Extension

[`sphinx-tabs`](https://github.com/djungelorm/sphinx-tabs) enables tabbed
content in Sphinx documentation:

```rst
.. tabs::

   .. tab:: Python

      .. code-block:: python

         def hello():
             print("Hello from Python!")

   .. tab:: JavaScript

      .. code-block:: javascript

         function hello() {
             console.log("Hello from JavaScript!");
         }
```

This creates clean, organized documentation where users can switch between
different implementations or languages.

### Modern Documentation Themes

[MkDocs Material](https://squidfunk.github.io/mkdocs-material/) provides a
beautiful Material Design theme for MkDocs documentation:

- **Responsive Design**: Works perfectly on mobile and desktop
- **Search Integration**: Fast client-side search
- **Dark Mode**: Automatic theme switching
- **Navigation**: Intuitive sidebar and navigation
- **Code Highlighting**: Beautiful syntax highlighting

## Computer Science Educational Resources

### Comprehensive CS Curriculum

[OSSU Computer Science Curriculum](https://github.com/ossu/computer-science)
provides a complete Computer Science education using free online courses:

{{< tip title="Self-Directed CS Education" >}} The OSSU curriculum is equivalent
to a complete CS degree, covering:

- Programming fundamentals
- Math for CS (calculus, statistics, discrete math)
- Systems programming
- Theory (algorithms, data structures)
- Applications (databases, graphics, AI)
- Unix, networking, and security {{< /tip >}}

### Specialized Learning Platforms

**[Missing Semester of Your CS Education](https://missing.csail.mit.edu/)** -
MIT course covering practical computing skills often overlooked in traditional
CS programs:

- Shell scripting and command-line tools
- Version control with Git
- Text editors (Vim)
- Data wrangling
- Virtual machines and containers
- Security and cryptography

**[CS 61B Data Structures, Spring 2019](https://sp19.datastructur.es/)** -
Berkeley's excellent data structures course with comprehensive materials and
assignments.

### Mathematics for Programming

[Foundations of Applied Mathematics](https://foundations-of-applied-mathematics.github.io/)
provides extensive Python and data science resources with mathematical
foundations:

- **Linear Algebra**: NumPy-based implementations
- **Optimization**: Scipy optimization algorithms
- **Data Science**: Statistics and machine learning
- **Numerical Methods**: Computational mathematics

## Programming Language Resources

### Rust Learning Materials

**[Jon Gjengset's YouTube Channel](https://www.youtube.com/channel/UC_iD0xppBwwsrM9DegC5cQQ)**
features intermediate Rust content:

- **[Crust of Rust](https://youtu.be/rAl-9HwD858)** series
- Live coding sessions
- Advanced Rust concepts explanation
- Real-world Rust applications

**[Jon Gjengset's Blog](https://thesquareplanet.com/)** includes excellent
articles on distributed systems, including MIT 6.824 and RAFT consensus
algorithm analysis.

**[Little Book of Rust Macros](https://danielkeep.github.io/tlborm/book/index.html)** -
Comprehensive guide to Rust's macro system:

```rust
// Declarative macros
macro_rules! say_hello {
    () => {
        println!("Hello!");
    };
}

// Procedural macros for more complex transformations
```

### Ruby Object-Oriented Design

**[Practical Object Oriented Design in Ruby - Sandi Metz](https://www.poodr.com/)**
is considered the definitive guide to OOP principles in Ruby. Metz explains
complex concepts like:

- Single Responsibility Principle
- Dependency injection
- Interface design
- Testing strategies

{{< quote title="POODR Philosophy" footer="Sandi Metz" >}} The purpose of design
is to allow you to design later, and its primary goal is to reduce the cost of
change. {{< /quote >}}

### Functional Programming

[Common Lisp: A Gentle Introduction by David S. Touretzky](https://www.cs.cmu.edu/~dst/LispBook/book.pdf)
provides an excellent introduction to functional programming concepts:

```lisp
;; Recursive function definition
(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))
```

## Cryptography and Security

### Learning Cryptography

**[Real World Cryptography](https://livebook.manning.com/book/real-world-cryptography/welcome/v-7/)** -
Modern approach to understanding cryptographic principles and implementations.

**[Understanding SHA Algorithms](https://www.maximintegrated.com/en/design/technical-documents/app-notes/7/7015.html)**
provides deep technical insight into SHA hash functions.

### Cryptographic Demonstrations

**[SHA256 Animation](https://github.com/in3rsha/sha256-animation)** - Visual
representation of how SHA-256 hashing works, step by step.

**[Malicious SHA1](https://malicioussha1.github.io/)** demonstrates practical
collision attacks against SHA-1, showing why it's no longer considered secure.

## Project-Based Learning

### Learning Through Building

[Project-Based Learning Repository](https://github.com/tuvtran/project-based-learning)
curates tutorials organized by programming language where you build real
applications:

{{< example title="Project Categories" >}}

- **Web Development**: Build a blog, e-commerce site, or social network
- **Game Development**: Create games in various languages
- **Mobile Apps**: iOS and Android development projects
- **Data Science**: Analysis projects with real datasets
- **DevOps**: Infrastructure and deployment projects {{< /example >}}

### Learn AI from Scratch

[Learn AI from Scratch](https://learnaifromscratch.github.io) takes a bottom-up
approach to understanding artificial intelligence:

1. Mathematical foundations
2. Linear algebra and calculus
3. Statistics and probability
4. Machine learning algorithms
5. Neural networks
6. Deep learning

## Specialized Technical Content

### Advanced Screencast Resources

**[Semicolon&Sons Intermediate Screencasts](https://www.semicolonandsons.com/)**
provides high-quality technical screencasts covering advanced programming
topics.

### Data Structures Research

**[Succinct/Compact Data Structures](https://github.com/miiohio/succinct)** for
Python - implementations of space-efficient data structures:

```python
# Succinct data structures use minimal space
# while maintaining fast query operations
from succinct import BitVector, RankSelect

# Compressed representation of binary data
bv = BitVector("1101001010")
rs = RankSelect(bv)
```

These structures are crucial for big data applications where memory efficiency
is paramount.

## Key Learning Insights

### Documentation Best Practices

1. **Structure Matters**: Use the four-type framework for comprehensive
   documentation
2. **User-Centric**: Different users need different types of information
3. **Visual Enhancement**: Tools like Sphinx tabs improve user experience
4. **Modern Themes**: Good visual design increases documentation adoption

### Educational Strategy

1. **Systematic Learning**: Follow structured curricula like OSSU
2. **Practical Application**: Project-based learning reinforces concepts
3. **Multiple Perspectives**: Learn from various sources and authors
4. **Depth and Breadth**: Balance specialized knowledge with general CS
   education

### Technical Growth

1. **Fundamentals First**: Strong mathematical and theoretical foundations
2. **Language Diversity**: Exposure to different programming paradigms
3. **Security Awareness**: Understanding cryptographic principles
4. **Modern Tools**: Stay current with documentation and development tools

{{< tip title="Continuous Learning Strategy" >}} The best technical education
combines structured learning (courses, books) with practical application
(projects) and community engagement (open source, discussions). These resources
provide multiple pathways to deep technical understanding. {{< /tip >}}

This exploration reinforces that great technical education requires both
systematic study and hands-on practice, supported by excellent documentation and
learning resources.

---

_These discoveries from my 2020 learning archive demonstrate the timeless value
of well-structured educational content and documentation systems that serve
learners at every level._
