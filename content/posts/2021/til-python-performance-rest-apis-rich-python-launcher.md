---
date: 2021-02-23T10:00:00+05:30
draft: false
title:
  "TIL: Python Performance, REST API Design, Rich Terminal Trees, and Python
  Launcher"
description:
  "Today I learned about achieving 12 requests per second in Python, designing
  beautiful REST APIs, rendering tree views with Rich, and a Rust-based Python
  launcher for version management."
tags:
  - TIL
  - Python
  - Performance
  - REST API
  - Terminal UI
  - Rust
  - Tools
---

## 12 Requests Per Second in Python

[12 requests per second in Python](https://suade.org/dev/12-requests-per-second-with-python/)

Detailed analysis of Python web application performance optimization:

### The Challenge:

- **Performance Bottlenecks**: Identifying what limits Python web app throughput
- **Realistic Benchmarking**: Testing with real-world scenarios, not just hello
  world
- **Optimization Strategies**: Practical techniques for improving performance
- **Infrastructure Considerations**: Hardware and deployment factors

### Performance Analysis:

#### **Baseline Measurements:**

- **Flask Application**: Basic REST API with database operations
- **Load Testing**: Using realistic request patterns and data
- **Bottleneck Identification**: CPU, I/O, memory, and network constraints
- **Profiling Tools**: cProfile, line_profiler, and memory profilers

#### **Optimization Techniques:**

**Database Optimization:**

```python
# Connection pooling
from sqlalchemy.pool import QueuePool
engine = create_engine(
    'postgresql://...',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30
)

# Query optimization
# Before: N+1 queries
users = User.query.all()
for user in users:
    print(user.profile.name)  # Additional query per user

# After: Eager loading
users = User.query.options(joinedload(User.profile)).all()
for user in users:
    print(user.profile.name)  # No additional queries
```

**Caching Strategies:**

```python
import redis
from functools import wraps

cache = redis.Redis()

def cached(expiration=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.setex(key, expiration, result)
            return result
        return wrapper
    return decorator
```

### Key Insights:

- **Database is Usually the Bottleneck**: Optimize queries first
- **Connection Pooling**: Essential for concurrent request handling
- **Caching**: Dramatic improvements for repeated operations
- **Async Processing**: Use Celery for heavy background tasks

## Designing Beautiful REST + JSON APIs

[Oktane17: Designing Beautiful REST + JSON APIs - YouTube](https://youtu.be/MiOSzpfP1Ww)

Comprehensive guide to REST API design principles:

### Core Design Principles:

#### **Resource-Oriented Design:**

```
GET    /users           # List users
POST   /users           # Create user
GET    /users/123       # Get specific user
PUT    /users/123       # Update user
DELETE /users/123       # Delete user
```

#### **Consistent Naming:**

- **Plural Nouns**: Use `/users` not `/user`
- **Hierarchical**: `/users/123/posts` for nested resources
- **Lowercase**: Consistent casing throughout API
- **Hyphen Separation**: Use `/user-profiles` not `/userProfiles`

### REST Must Be Hypertext-Driven

[REST APIs must be hypertext-driven » Untangled](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)

Roy Fielding's clarification on true REST principles:

#### **HATEOAS (Hypermedia as the Engine of Application State):**

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "_links": {
    "self": { "href": "/users/123" },
    "posts": { "href": "/users/123/posts" },
    "edit": { "href": "/users/123", "method": "PUT" },
    "delete": { "href": "/users/123", "method": "DELETE" }
  }
}
```

#### **API Evolution:**

- **Discoverability**: Clients discover available actions through links
- **Loose Coupling**: Clients don't hardcode URLs
- **Version Independence**: Links adapt to API changes
- **Self-Documenting**: API structure evident from responses

### HTTP Status Codes:

```
200 OK              # Successful GET, PUT
201 Created         # Successful POST
204 No Content      # Successful DELETE
400 Bad Request     # Client error
401 Unauthorized    # Authentication required
403 Forbidden       # Insufficient permissions
404 Not Found       # Resource doesn't exist
500 Internal Error  # Server error
```

## Rich Terminal Tree Views

[Rendering a tree view in the terminal with Python and Rich](https://www.willmcgugan.com/blog/tech/post/rich-tree/)

Creating beautiful terminal interfaces with the Rich library:

### Rich Library Features:

- **Styled Output**: Colors, bold, italic, underline in terminal
- **Complex Layouts**: Tables, panels, columns, and trees
- **Progress Bars**: Beautiful progress indicators
- **Syntax Highlighting**: Code syntax highlighting in terminal

### Tree Rendering:

#### **Basic Tree Structure:**

```python
from rich.console import Console
from rich.tree import Tree

console = Console()

# Create root node
tree = Tree("📁 Project Root")

# Add branches
src_branch = tree.add("📁 src")
src_branch.add("🐍 main.py")
src_branch.add("🐍 utils.py")

tests_branch = tree.add("📁 tests")
tests_branch.add("🧪 test_main.py")
tests_branch.add("🧪 test_utils.py")

tree.add("📄 README.md")
tree.add("📄 requirements.txt")

console.print(tree)
```

#### **File System Tree:**

```python
import os
from pathlib import Path

def create_file_tree(directory: Path) -> Tree:
    tree = Tree(f"📁 {directory.name}")

    for item in sorted(directory.iterdir()):
        if item.is_dir():
            # Recursively add subdirectories
            subtree = create_file_tree(item)
            tree.add(subtree)
        else:
            # Add files with appropriate icons
            icon = "🐍" if item.suffix == ".py" else "📄"
            tree.add(f"{icon} {item.name}")

    return tree
```

### Advanced Features:

- **Styling**: Custom colors and styles for different node types
- **Interactive**: Combine with click events for navigation
- **Live Updates**: Dynamic tree updates for monitoring
- **Large Datasets**: Efficient rendering of large hierarchies

## Python Launcher (Rust)

[python-launcher - crates.io](https://crates.io/crates/python-launcher)

Rust-based Python version launcher and manager:

### What It Does:

- **Version Detection**: Automatically detects appropriate Python version
- **PEP 514 Compliance**: Follows Python launcher specification
- **Fast Performance**: Rust implementation for speed
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Key Features:

#### **Automatic Version Selection:**

```bash
# Checks pyproject.toml, .python-version, or uses default
python3 script.py

# Explicit version specification
python3.9 script.py
python3.10 -m pip install package
```

#### **Configuration:**

```toml
# pyproject.toml
[tool.python-launcher]
default = "3.10"
prefer-active-venv = true
```

### Advantages:

- **Performance**: Faster startup than shell-based launchers
- **Reliability**: Robust version detection and selection
- **Standards Compliance**: Follows Python packaging standards
- **Modern Implementation**: Written in modern Rust with good error handling

Each resource demonstrates different aspects of Python ecosystem optimization -
from web application performance tuning to API design best practices, terminal
UI enhancement, and development tool innovation.
