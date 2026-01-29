---
date: 2020-09-16T10:00:00+05:30
draft: false
title:
  "TIL: Architecture of Open Source Applications, Compiler Development
  Resources, and Oil Shell"
description:
  "Today I learned about comprehensive open source architecture documentation,
  practical compiler development tutorials, the Cannoli Python compiler in Rust,
  and the Oil shell project."
tags:
  - "til"
  - "compiler"
  - "architecture"
  - "python"
  - "rust"
  - "shell"
  - "programming-languages"
---

Today's learning focused on understanding complex software architectures and
language implementation techniques.

## Architecture of Open Source Applications

[The Architecture of Open Source Applications](https://www.aosabook.org/en/index.html)
provides detailed architectural analysis of major open source projects:

### Volume Coverage:

#### **Infrastructure Projects:**

- **Apache web server**: Multi-process architecture and module system
- **PostgreSQL**: Query planning, storage engine, and ACID compliance
- **MySQL**: Storage engines, replication, and performance optimization
- **Redis**: In-memory data structures and persistence strategies

#### **Development Tools:**

- **Git**: Distributed version control architecture
- **Mercurial**: Alternative DVCS design decisions
- **Eclipse**: Plugin architecture and IDE extensibility
- **LLVM**: Compiler infrastructure and optimization passes

#### **Application Frameworks:**

- **Django**: Web framework architecture and ORM design
- **Rails**: Convention over configuration philosophy
- **jQuery**: JavaScript library design patterns
- **Node.js**: Event-driven architecture and non-blocking I/O

### Architectural Insights:

#### **Common Patterns:**

```
Plugin Architecture:
- Core system provides stable API
- Extensions add functionality without core changes
- Examples: Eclipse, Apache modules, browser extensions

Layered Architecture:
- Clear separation of concerns
- Each layer depends only on lower layers
- Examples: Network stacks, operating systems

Event-Driven Architecture:
- Components communicate via events
- Loose coupling and high scalability
- Examples: Node.js, GUI frameworks
```

#### **Performance Considerations:**

- **Caching strategies**: Redis, web servers, databases
- **Memory management**: Garbage collection vs manual allocation
- **Concurrency models**: Threading, async/await, actor systems
- **Data structure choices**: Hash tables, B-trees, bloom filters

## Compiler Development Resources

### Comprehensive Compiler Articles

[Phil Eaton's Compiler Articles](https://notes.eatonphil.com/tags/compiler.html)
provide practical, hands-on compiler development guidance:

#### **Language Implementation Steps:**

1. **Lexical Analysis**: Tokenizing source code
2. **Parsing**: Building abstract syntax trees
3. **Semantic Analysis**: Type checking and symbol resolution
4. **Code Generation**: Producing target code
5. **Optimization**: Improving performance and size

#### **Practical Implementation:**

```rust
// Simplified tokenizer example
#[derive(Debug, PartialEq)]
enum Token {
    Number(i64),
    Identifier(String),
    Plus,
    Minus,
    LeftParen,
    RightParen,
    EOF,
}

struct Lexer {
    input: Vec<char>,
    position: usize,
}

impl Lexer {
    fn next_token(&mut self) -> Token {
        self.skip_whitespace();

        match self.current_char() {
            Some('+') => { self.advance(); Token::Plus }
            Some('-') => { self.advance(); Token::Minus }
            Some('(') => { self.advance(); Token::LeftParen }
            Some(')') => { self.advance(); Token::RightParen }
            Some(c) if c.is_ascii_digit() => self.read_number(),
            Some(c) if c.is_ascii_alphabetic() => self.read_identifier(),
            None => Token::EOF,
            _ => panic!("Unexpected character: {:?}", self.current_char()),
        }
    }

    fn read_number(&mut self) -> Token {
        let mut number = String::new();
        while let Some(c) = self.current_char() {
            if c.is_ascii_digit() {
                number.push(c);
                self.advance();
            } else {
                break;
            }
        }
        Token::Number(number.parse().unwrap())
    }
}
```

### Cannoli - Python Compiler in Rust

[Cannoli](https://github.com/joncatanio/cannoli) demonstrates implementing a
Python subset compiler in Rust:

#### **Architecture Overview:**

```rust
// AST representation
#[derive(Debug, Clone)]
pub enum Expr {
    Number(i64),
    String(String),
    Identifier(String),
    BinaryOp {
        left: Box<Expr>,
        op: BinaryOperator,
        right: Box<Expr>,
    },
    Call {
        func: Box<Expr>,
        args: Vec<Expr>,
    },
}

#[derive(Debug, Clone)]
pub enum Stmt {
    Expression(Expr),
    Assignment {
        target: String,
        value: Expr,
    },
    If {
        condition: Expr,
        then_body: Vec<Stmt>,
        else_body: Option<Vec<Stmt>>,
    },
    While {
        condition: Expr,
        body: Vec<Stmt>,
    },
}
```

#### **Code Generation Strategy:**

- Target LLVM IR for optimization and portability
- Implement Python semantics (dynamic typing, reference counting)
- Handle Python-specific features (list comprehensions, generators)
- Provide runtime support for built-in functions

## Oil Shell - Unix Shell in Python Subset

[Oil Shell](https://www.oilshell.org/) represents a modern approach to Unix
shell design:

### Design Goals:

#### **Compatibility and Innovation:**

- **Bash compatibility**: Run existing shell scripts
- **Oil language**: New shell language with better syntax
- **Type safety**: Optional typing for shell variables
- **Error handling**: Better error reporting and debugging

#### **Architecture Improvements:**

```bash
# Traditional bash
if [ -f "$file" ]; then
    lines=$(wc -l < "$file")
    if [ "$lines" -gt 100 ]; then
        echo "Large file: $lines lines"
    fi
fi

# Oil shell equivalent
if test -f $file {
    var lines = $(wc -l < $file)
    if (lines > 100) {
        echo "Large file: $lines lines"
    }
}
```

### Implementation Strategy:

#### **Python-Based Implementation:**

- Written in OPy (Oil Python) - a subset of Python
- Transpiles to Python for execution
- Uses Python's parsing and AST capabilities
- Leverages Python's standard library

#### **Language Features:**

```oil
# Variables with types
var name: Str = "example"
var count: Int = 42
var files: List[Str] = glob("*.txt")

# Better string handling
var msg = "Hello $name, you have $count files"

# Structured data
var config = {
    host: "localhost",
    port: 8080,
    debug: true
}

# Error handling
try {
    var result = $(command_that_might_fail)
} catch {
    echo "Command failed"
    exit 1
}
```

## Supporting Resources

### LaTeX Learning

Understanding LaTeX syntax and best practices, particularly for technical
documentation and mathematical notation in compiler documentation.

### Educational Compiler Projects:

- **Small-C**: Historical compiler for C subset
- **LLVM tutorials**: Official documentation for compiler backend
- **"So You Want to Be a Compiler Wizard"**: Career guidance for compiler
  developers

### Advanced Topics:

- **JIT compilation**: Runtime code generation techniques
- **Functional programming**: Implementing languages with first-class functions
- **Python singledispatch**: Method overloading for interpreter implementation

These resources provide comprehensive coverage of both the theoretical
foundations and practical implementation techniques needed for understanding and
building complex software systems, from compilers to shells to large-scale
applications.
