---
date: 2021-03-14T10:00:00+05:30
draft: false
title: "TIL: Python eval(), exec(), and compile() Functions"
description:
  "Today I learned about the differences between Python's eval(), exec(), and
  compile() functions and their appropriate use cases for dynamic code
  execution."
tags:
  - "til"
  - "python"
  - "dynamic-execution"
  - "built-ins"
---

## Python Dynamic Code Execution Functions

[What's the difference between eval, exec, and compile? - Stack Overflow](https://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile/29456463?stw=2#29456463)

Understanding the three core functions for dynamic code execution in Python:

### eval() - Expression Evaluation

**Purpose**: Evaluates a single Python expression and returns the result

```python
result = eval("2 + 3 * 4")  # Returns 14
x = 5
result = eval("x * 2")      # Returns 10
```

**Characteristics:**

- **Single Expression**: Only works with expressions, not statements
- **Return Value**: Always returns a value
- **Use Cases**: Mathematical calculations, simple expressions
- **Limitations**: Cannot handle statements like assignments or loops

### exec() - Statement Execution

**Purpose**: Executes Python statements (does not return a value)

```python
exec("x = 10; y = 20; print(x + y)")  # Prints: 30
exec("""
for i in range(3):
    print(f"Hello {i}")
""")
```

**Characteristics:**

- **Multiple Statements**: Can execute complex code blocks
- **No Return Value**: Returns None
- **Use Cases**: Dynamic code execution, configuration scripts
- **Flexibility**: Can handle any valid Python code

### compile() - Code Object Creation

**Purpose**: Compiles source code into code objects for repeated execution

```python
# Compile once, execute multiple times
code = compile("x * 2", "<string>", "eval")
x = 5
result1 = eval(code)  # Returns 10
x = 10
result2 = eval(code)  # Returns 20
```

**Modes:**

- **'eval'**: For expressions (use with eval())
- **'exec'**: For statements (use with exec())
- **'single'**: For single interactive statements

### Performance Considerations

**Compilation Overhead:**

- `eval()` and `exec()` compile code every time
- `compile()` allows pre-compilation for repeated use
- Significant performance improvement for repeated execution

**Example - Repeated Execution:**

```python
import timeit

# Without compile() - slower
def slow_version():
    for i in range(1000):
        eval("2 + 3 * 4")

# With compile() - faster
code = compile("2 + 3 * 4", "<string>", "eval")
def fast_version():
    for i in range(1000):
        eval(code)
```

### Security Considerations

**Major Risks:**

- **Code Injection**: User input can execute arbitrary code
- **System Access**: Malicious code can access file system, network
- **Data Exposure**: Can access and modify global variables

**Safer Alternatives:**

```python
# Restricted globals and locals
safe_globals = {"__builtins__": {}}
safe_locals = {"x": 10, "y": 20}
result = eval("x + y", safe_globals, safe_locals)

# Use ast.literal_eval for safe data parsing
import ast
data = ast.literal_eval("{'key': 'value'}")  # Only literals
```

### Best Practices

1. **Avoid When Possible**: Use alternative approaches first
2. **Sanitize Input**: Never execute untrusted user input
3. **Restrict Scope**: Use limited globals and locals dictionaries
4. **Use ast.literal_eval**: For parsing data structures safely
5. **Pre-compile**: Use compile() for repeated execution

These functions provide powerful dynamic execution capabilities but require
careful consideration of security and performance implications.
