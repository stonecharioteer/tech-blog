---
date: 2020-12-12T10:00:00+05:30
draft: false
title:
  "TIL: Python Behind the Scenes - CPython VM, Compiler, and Object System Deep
  Dive"
description:
  "Today I learned about the comprehensive 'Python Behind the Scenes' series
  covering CPython's virtual machine, compiler architecture, bytecode execution,
  variable implementation, and object system internals."
tags:
  - "til"
  - "python"
  - "cpython"
  - "virtual-machine"
  - "compiler"
  - "bytecode"
  - "object-system"
  - "language-internals"
---

## Python Behind the Scenes Series

Comprehensive deep dive into CPython internals across multiple articles:

- [How the CPython VM works](https://tenthousandmeters.com/blog/python-behind-the-scenes-1-how-the-cpython-vm-works/)
- [How the CPython compiler works](https://tenthousandmeters.com/blog/python-behind-the-scenes-2-how-the-cpython-compiler-works/)
- [Stepping through the CPython source code](https://tenthousandmeters.com/blog/python-behind-the-scenes-3-stepping-through-the-cpython-source-code/)
- [How Python bytecode is executed](https://tenthousandmeters.com/blog/python-behind-the-scenes-4-how-python-bytecode-is-executed/)
- [How variables are implemented in CPython](https://tenthousandmeters.com/blog/python-behind-the-scenes-5-how-variables-are-implemented-in-cpython/)
- [How Python object system works](https://tenthousandmeters.com/blog/python-behind-the-scenes-6-how-python-object-system-works/)

### Part 1: CPython Virtual Machine Architecture

#### **High-Level Overview:**

```
Python Source Code (.py)
       ↓
   Parser (AST generation)
       ↓
   Compiler (Bytecode generation)
       ↓
   Virtual Machine (Bytecode execution)
       ↓
   Output/Effects
```

#### **Core Components:**

```c
// Simplified CPython VM structure
typedef struct {
    PyObject *f_code;        // Code object containing bytecode
    PyObject *f_globals;     // Global namespace dict
    PyObject *f_locals;      // Local namespace dict
    PyObject **f_valuestack; // Value stack for operations
    PyObject *f_trace;       // Trace function for debugging
    int f_stacksize;         // Current stack size
} PyFrameObject;

// Main evaluation loop
PyObject *
PyEval_EvalFrameEx(PyFrameObject *f, int throwflag) {
    // The heart of Python execution
    // Interprets bytecode instructions one by one
    for (;;) {
        opcode = NEXTOP();
        switch (opcode) {
            case LOAD_FAST:
                // Load local variable onto stack
                break;
            case BINARY_ADD:
                // Pop two values, add them, push result
                break;
            // ... hundreds of other opcodes
        }
    }
}
```

### Part 2: CPython Compiler Pipeline

#### **Compilation Phases:**

1. **Lexical Analysis**: Source code → tokens
2. **Parsing**: Tokens → Abstract Syntax Tree (AST)
3. **AST Optimization**: Tree transformations
4. **Code Generation**: AST → bytecode

#### **AST Structure Example:**

```python
# Python code
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Corresponding AST (simplified)
FunctionDef(
    name='factorial',
    args=arguments(args=[arg('n')]),
    body=[
        If(
            test=Compare(
                left=Name('n'),
                ops=[LtE()],
                comparators=[Num(1)]
            ),
            body=[Return(Num(1))],
            orelse=[
                Return(
                    BinOp(
                        left=Name('n'),
                        op=Mult(),
                        right=Call(
                            func=Name('factorial'),
                            args=[BinOp(Name('n'), Sub(), Num(1))]
                        )
                    )
                )
            ]
        )
    ]
)
```

#### **Bytecode Generation:**

```python
import dis

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

dis.dis(factorial)
```

Output:

```
  2           0 LOAD_FAST                0 (n)
              2 LOAD_CONST               1 (1)
              4 COMPARE_OP               1 (<=)
              6 POP_JUMP_IF_FALSE       12

  3           8 LOAD_CONST               1 (1)
             10 RETURN_VALUE

  4     >>   12 LOAD_FAST                0 (n)
             14 LOAD_GLOBAL              0 (factorial)
             16 LOAD_FAST                0 (n)
             18 LOAD_CONST               1 (1)
             20 BINARY_SUBTRACT
             22 CALL_FUNCTION            1
             24 BINARY_MULTIPLY
             26 RETURN_VALUE
```

### Part 3: Bytecode Execution Engine

#### **Stack-Based Virtual Machine:**

```c
// Bytecode execution example: BINARY_ADD
case BINARY_ADD: {
    PyObject *right = POP();   // Pop right operand
    PyObject *left = TOP();    // Get left operand (don't pop yet)
    PyObject *sum;

    // Try fast path for integers
    if (PyLong_CheckExact(left) && PyLong_CheckExact(right)) {
        sum = long_add(left, right);
    } else {
        // General case: call __add__ method
        sum = PyNumber_Add(left, right);
    }

    SET_TOP(sum);              // Replace left operand with result
    Py_DECREF(right);          // Clean up
    if (sum == NULL) goto error;
    DISPATCH();                // Continue to next instruction
}
```

#### **Execution Stack Management:**

```python
# Python code demonstrating stack operations
x = 10
y = 20
result = x + y * 2

# Corresponding stack operations:
# LOAD_CONST 10        -> Stack: [10]
# STORE_FAST x         -> Stack: [], x = 10
# LOAD_CONST 20        -> Stack: [20]
# STORE_FAST y         -> Stack: [], y = 20
# LOAD_FAST x          -> Stack: [10]
# LOAD_FAST y          -> Stack: [10, 20]
# LOAD_CONST 2         -> Stack: [10, 20, 2]
# BINARY_MULTIPLY      -> Stack: [10, 40]
# BINARY_ADD           -> Stack: [50]
# STORE_FAST result    -> Stack: [], result = 50
```

### Part 4: Variable Implementation

#### **Local Variables (LEGB Rule):**

```c
// Local variable access in CPython
typedef struct {
    PyObject **localsplus;     // Array of local variables
    int nlocals;               // Number of local variables
    int nfree;                 // Number of free variables (closures)
    // ... other fields
} PyCodeObject;

// Fast local variable access
#define GETLOCAL(i)     (fastlocals[i])
#define SETLOCAL(i, v)  (fastlocals[i] = v)

// LOAD_FAST implementation
case LOAD_FAST: {
    PyObject *value = GETLOCAL(oparg);
    if (value == NULL) {
        // UnboundLocalError
        goto error;
    }
    Py_INCREF(value);
    PUSH(value);
    DISPATCH();
}
```

#### **Global and Built-in Lookup:**

```c
// Global variable lookup (LOAD_GLOBAL)
case LOAD_GLOBAL: {
    PyObject *name = GETITEM(names, oparg);
    PyObject *v;

    // Try global namespace first
    v = PyDict_GetItem(f->f_globals, name);
    if (v == NULL) {
        // Try built-ins namespace
        v = PyDict_GetItem(f->f_builtins, name);
        if (v == NULL) {
            // NameError
            goto error;
        }
    }

    Py_INCREF(v);
    PUSH(v);
    DISPATCH();
}
```

#### **Closure and Cell Variables:**

```python
def outer(x):
    def inner():
        return x  # 'x' is a free variable in inner()
    return inner

# CPython creates a 'cell' object to store 'x'
# Both outer and inner reference the same cell
```

### Part 5: Python Object System

#### **PyObject Structure:**

```c
// Base object structure
typedef struct _object {
    Py_ssize_t ob_refcnt;    // Reference count
    struct _typeobject *ob_type;  // Type information
} PyObject;

// Variable-size objects
typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size;      // Number of items
} PyVarObject;

// Example: Integer object
typedef struct {
    PyObject_HEAD
    digit ob_digit[1];       // Actual integer data
} PyLongObject;
```

#### **Type System:**

```c
// Type object structure (simplified)
typedef struct _typeobject {
    PyVarObject_HEAD
    const char *tp_name;          // Type name
    Py_ssize_t tp_basicsize;      // Size of instances

    // Method slots
    destructor tp_dealloc;        // Destructor
    printfunc tp_print;           // Print function
    getattrfunc tp_getattr;       // Attribute access
    setattrfunc tp_setattr;       // Attribute setting

    // Number methods
    PyNumberMethods *tp_as_number;

    // Sequence methods
    PySequenceMethods *tp_as_sequence;

    // Mapping methods
    PyMappingMethods *tp_as_mapping;

    // ... many more slots
} PyTypeObject;
```

#### **Method Resolution and Dispatch:**

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):  # Multiple inheritance
    pass

# Method Resolution Order (MRO): D -> B -> C -> A -> object
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

# CPython uses C3 linearization algorithm for MRO
```

### Performance Implications:

#### **Optimization Strategies:**

```python
# Understanding performance through internals

# 1. Local variable access is fastest (LOAD_FAST)
def fast_locals():
    x = 10
    for i in range(1000000):
        y = x + i  # x is local, very fast

# 2. Global lookups are slower (LOAD_GLOBAL)
global_var = 10
def slower_globals():
    for i in range(1000000):
        y = global_var + i  # global_var requires dict lookup

# 3. Attribute access triggers method calls
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def attribute_access():
    p = Point(1, 2)
    for i in range(1000000):
        # Each p.x triggers __getattribute__ or __getattr__
        y = p.x + i

# 4. Built-in functions are optimized
def builtin_vs_custom():
    # Fast: built-in sum() is implemented in C
    result1 = sum(range(1000000))

    # Slower: Python loop with bytecode overhead
    result2 = 0
    for i in range(1000000):
        result2 += i
```

#### **Memory Management Insights:**

```python
import sys

# Understanding reference counting
x = [1, 2, 3]
print(sys.getrefcount(x))  # Should be 2 (x + getrefcount parameter)

y = x  # Increment reference count
print(sys.getrefcount(x))  # Should be 3

del y  # Decrement reference count
print(sys.getrefcount(x))  # Back to 2

# Circular references require garbage collector
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []

# Create circular reference
parent = Node("parent")
child = Node("child")
parent.children.append(child)
child.parent = parent  # Circular reference

# Without GC, this would be a memory leak
# CPython's cycle detector will find and clean this up
```

### Debugging and Introspection:

#### **Useful Tools:**

```python
import dis
import ast
import inspect

# Disassemble bytecode
def debug_bytecode():
    def sample(x, y):
        return x + y * 2

    print("Bytecode:")
    dis.dis(sample)

    print("\nCode object attributes:")
    code = sample.__code__
    print(f"co_names: {code.co_names}")        # Global names
    print(f"co_varnames: {code.co_varnames}")  # Local names
    print(f"co_consts: {code.co_consts}")      # Constants
    print(f"co_code: {code.co_code}")          # Raw bytecode

# Examine AST
def debug_ast():
    source = "x = 1 + 2 * 3"
    tree = ast.parse(source)
    print(ast.dump(tree, indent=2))

# Frame introspection
def debug_frames():
    frame = inspect.currentframe()
    print(f"Function: {frame.f_code.co_name}")
    print(f"Locals: {frame.f_locals}")
    print(f"Globals count: {len(frame.f_globals)}")

debug_bytecode()
debug_ast()
debug_frames()
```

Understanding CPython internals provides valuable insights for:

- **Performance optimization**: Knowing what operations are expensive
- **Memory management**: Understanding reference counting and GC
- **Debugging**: Better tools for investigating issues
- **Language design**: Appreciating the complexity of dynamic languages
- **Extension development**: Writing efficient C extensions

This knowledge bridges the gap between high-level Python programming and
low-level system understanding, making you a more effective Python developer.
