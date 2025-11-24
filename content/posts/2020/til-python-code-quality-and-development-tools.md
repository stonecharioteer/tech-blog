---
date: 2020-07-18T18:00:00+05:30
draft: false
title: "TIL: Python Code Quality and Development Tools Deep Dive"
description:
  "Today I learned about advanced Python code quality tools, CPython internals
  resources, and modern development practices from my archive of learning notes."
tags:
  - til
  - python
  - code-quality
  - cpython
  - development-tools
  - testing
  - profiling
---

Diving deep into my learning archive, I discovered a treasure trove of Python
development tools and resources that every serious Python developer should know
about. These discoveries span from code quality enforcement to CPython internals
understanding.

## Python Code Quality Authority (PyCQA)

The [Python Code Quality Authority](https://github.com/PyCQA) is an organization
that maintains several essential Python code quality tools:

{{< note title="PyCQA Tools Ecosystem" >}}

- **pylint** - Comprehensive static analysis
- **flake8** - Style guide enforcement
- **mccabe** - Cyclomatic complexity analysis
- **prospector** - Meta-tool combining multiple analyzers
- **bandit** - Security-focused static analysis {{< /note >}}

### McCabe Complexity Analysis

[Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity),
also known as McCabe Complexity, measures the number of linearly independent
paths through a program's source code. The
[`mccabe` module](https://github.com/pycqa/mccabe) helps identify overly complex
functions:

```python
# Example of measuring complexity
from mccabe import get_code_complexity

def complex_function(x):
    if x > 10:
        if x > 20:
            if x > 30:
                return "very high"
            return "high"
        return "medium"
    return "low"

# This function would have high cyclomatic complexity
```

{{< tip title="Complexity Guidelines" >}}

- **1-10**: Simple, low risk
- **11-20**: Moderate complexity
- **21-50**: High complexity, consider refactoring
- **>50**: Very high risk, definitely refactor {{< /tip >}}

### Advanced Code Quality with Prospector

[Prospector](http://prospector.landscape.io) is a meta-tool that runs multiple
Python code analysis tools and presents the results in a unified format:

```bash
# Install and run prospector
pip install prospector
prospector myproject/
```

It combines:

- **pylint** for comprehensive analysis
- **pep8/pycodestyle** for style checking
- **pep257/pydocstyle** for docstring conventions
- **pyflakes** for logical errors
- **mccabe** for complexity analysis

## CPython Internals Resources

Understanding Python's internals makes you a better Python developer. Here are
the essential resources I discovered:

### Core Learning Materials

1. **[CPython Internals Book by Anthony Shaw](https://realpython.com/products/cpython-internals-book/)** -
   Comprehensive guide to Python's implementation
2. **[CPython Source Code Guide](https://realpython.com/cpython-source-code-guide/)** -
   RealPython's detailed walkthrough
3. **[Advanced Internals of CPython by Prashanth Raghu](https://intopythoncom.files.wordpress.com/2017/04/merged.pdf)** -
   Deep technical PDF resource

### Video Resources

{{< example title="Must-Watch CPython Content" >}}

- **[CPython Internals: 10 Hour Codewalk](http://pgbovine.net/cpython-internals.htm)** -
  Philip Guo's comprehensive video series
- **[Soul of the Beast - Pablo Salgado (EuroPython 2019)](https://www.youtube.com/watch?v=1_23AVsiQEc)** -
  Excellent talk on CPython architecture
- **[BangPypers Meetup - Code Quality and Testing](http://www.youtube.com/watch?v=eVYdPdvS2nQ)** -
  Practical insights from the community {{< /example >}}

## Modern Python Development Practices

### Import Sorting with isort

[`isort`](https://pypi.org/project/isort/) automatically sorts Python imports
according to PEP 8 guidelines:

```python
# Before isort
import sys
from myproject import settings
import os
from django.conf import settings as django_settings

# After isort
import os
import sys

from django.conf import settings as django_settings

from myproject import settings
```

Configuration in `pyproject.toml`:

```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
```

### Profiling with Line Profiler

[`line_profiler`](https://github.com/pyutils/line_profiler) provides
line-by-line timing information:

```python
@profile
def slow_function():
    # Your code here
    time.sleep(0.1)
    result = sum(range(1000000))
    return result

# Run with: kernprof -l -v script.py
```

### Memory Profiling with Guppy/Heapy

[Guppy3/Heapy](https://github.com/zhuyifei1999/guppy3) helps identify memory
leaks and understand memory usage:

```python
from guppy import hpy
h = hpy()
print(h.heap())

# Shows detailed memory usage by object type
```

## File Watching and Automation

### The `entr` Command

[`entr`](https://github.com/clibs/entr) runs commands when files change -
perfect for development workflows:

```bash
# Run tests when Python files change
find . -name "*.py" | entr python -m pytest

# Restart server on code changes
find . -name "*.py" | entr -r python app.py

# Run linting on save
find . -name "*.py" | entr pylint
```

{{< tip title="Development Workflow" >}} `entr` is incredibly useful for
continuous testing, linting, or building during development. It's more reliable
than many IDE file watchers and works across all platforms. {{< /tip >}}

## Advanced Python Features and PEPs

### PEP 618: Optional Length-Checking to zip

[PEP 618](https://www.python.org/dev/peps/pep-0618/) introduced `strict`
parameter to `zip()`:

```python
# Before PEP 618 - silent truncation
list1 = [1, 2, 3]
list2 = [4, 5]
result = list(zip(list1, list2))  # [(1, 4), (2, 5)]

# After PEP 618 - explicit error
result = list(zip(list1, list2, strict=True))  # ValueError!
```

### PEP 622: Structural Pattern Matching

[PEP 622](https://www.python.org/dev/peps/pep-0622/) brought pattern matching to
Python 3.10+:

```python
def handle_data(data):
    match data:
        case {"type": "user", "name": str(name)}:
            return f"User: {name}"
        case {"type": "product", "id": int(product_id)}:
            return f"Product ID: {product_id}"
        case list() if len(data) > 10:
            return "Large list"
        case _:
            return "Unknown data"
```

Try it in the
[Pattern Matching Playground](https://mybinder.org/v2/gh/gvanrossum/patma/master?urlpath=lab/tree/playground-622.ipynb).

## Flask-Specific Quality Tools

### Flask Extensions for Code Quality

```bash
# Flask-specific linting
pip install pylint-flask pylint-flask-sqlalchemy
```

These plugins understand Flask patterns and reduce false positives:

```python
# Without pylint-flask: "Instance of 'Flask' has no 'route' member"
# With pylint-flask: Correctly understands Flask patterns
from flask import Flask
app = Flask(__name__)

@app.route('/')  # No longer flagged as error
def home():
    return "Hello World"
```

### Profiling Flask Applications

Use Werkzeug's profiler middleware for detailed performance analysis:

```python
from werkzeug.contrib.profiler import ProfilerMiddleware
from flask import Flask

app = Flask(__name__)
app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                                 restrictions=[30])  # Top 30 calls
```

## Python Packaging Evolution

### Modern Python Packaging

The landscape is evolving rapidly:

- **[Poetry](https://github.com/python-poetry/poetry)** - Modern dependency
  management
- **[Flit](https://flit.readthedocs.io/)** - Simple publishing workflow
- **[pyproject.toml](https://snarky.ca/what-the-heck-is-pyproject-toml/)** - New
  standard for project metadata

### PEP 508: Dependency Specification

[PEP 508](https://www.python.org/dev/peps/pep-0508/) defines the format for
dependency specifications:

```python
# Basic dependency
requests >= 2.25.0

# Environment markers
dataclasses; python_version < "3.7"
pywin32; sys_platform == "win32"

# Complex conditions
scipy >= 1.0.0; (python_version >= "3.7" and platform_machine != "aarch64")
```

## Development Environment Tools

### Quality of Life Improvements

{{< note title="Useful Development Tools" >}}

- **[commitizen](https://github.com/commitizen-tools/commitizen)** - Enforces
  conventional commit messages
- **[implements](https://pypi.org/project/implements/)** - Interface
  verification for Python
- **[Micro](https://github.com/zyedidia/micro)** - Modern terminal-based text
  editor
- **[Windows Terminal](https://github.com/microsoft/terminal)** - Modern
  terminal for Windows {{< /note >}}

## Key Takeaways

1. **Code Quality is Multi-Dimensional**: Use multiple tools (pylint, flake8,
   prospector) for comprehensive analysis
2. **Understanding Internals Matters**: CPython knowledge helps write better,
   more efficient code
3. **Automation is Essential**: Tools like `entr` and proper CI/CD make
   development smoother
4. **Modern Python is Evolving**: Stay updated with new PEPs and packaging
   standards
5. **Profiling Before Optimizing**: Use proper tools to identify actual
   bottlenecks

{{< quote title="Development Philosophy" footer="From the Archive" >}} The best
developers don't just write code that works - they write code that's
maintainable, efficient, and follows established patterns. These tools help
achieve that goal systematically. {{< /quote >}}

This exploration of Python development tools reinforces that professional Python
development requires a comprehensive toolkit beyond just knowing the language
syntax.

---

_These discoveries came from my learning archive spanning 2020, showing how
Python tooling and best practices continue to evolve while maintaining backward
compatibility and developer productivity._
