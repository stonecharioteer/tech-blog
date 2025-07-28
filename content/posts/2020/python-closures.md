---
date: 2020-06-15T10:00:00+05:30
draft: false
title: "Python Closures: Understanding Scope and Variable Lifetime"
description: "An in-depth exploration of closures in Python, examining how variables persist across scopes through practical examples and bytecode analysis."
tags:
  - python
  - tutorial
  - closures
  - scope
  - intermediate
---

## Preamble 

About a year ago, a friend and I were discussing closures in programming languages, and how they were treated so specially in many technical circles. To us, the concept seemed weird. Python's closures were... *intuitive*, weren't they? Both of us were not exactly from a standard programming background, we'd both studied Mechanical Engineering, not Computer Science, but we were (and still are) super passionate about tech.

Which is why we were confused. Whatever it is that the world calls **closures** seems pretty obvious. At least to us they were.

And well, we weren't wrong. But we were mildly surprised at how Python deals with it.

## Intended Audience

This is an intermediate level article, and you might be confused reading it if you don't understand the following:

1. [Writing Python scripts.](https://docs.python.org/3/tutorial/index.html)
2. [Using the REPL Interpreter](https://docs.python.org/3/tutorial/interpreter.html)
3. [Writing functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
4. [Writing classes (knowledge of inheritance is not required)](https://docs.python.org/3/tutorial/classes.html)
5. Using the [`id`](https://docs.python.org/3/library/functions.html#id), [`help`](https://docs.python.org/3/library/functions.html#help) and [`dir`](https://docs.python.org/3/library/functions.html#dir) functions.
6. [Using the `dis` module to disassemble Python code.](https://docs.python.org/3/library/dis.html)

I have linked to the best articles (IMO) on these topics above, so if you like, you can go ahead and read those first.

Also, most articles deal with an article with respect to nested functions. While I *do* deal with nested functions, I do not start there. I start earlier, with a simple variable, and build up to nested... let's say objects.

## Introduction

Let's take a look.

```python
def some_func():
    something_to_return = 10
    print(f"id(something_to_return) = {id(something_to_return)}")
    return something_to_return
```

The `id` function in Python is a built-in that [returns the *identity*](https://docs.python.org/3/library/functions.html#id) of the object that represents the variable. I use this function to sniff around my code to see if I am passing around copies of a variable or if I am actually passing the variable (*sic* object) itself.

In this case, it is easy to test this theory.

```
>>> x = some_func()
id(something_to_return) = 10917664
>>> id(x)
10917664
```

This snippet prints out the `id` value of these variables, and while of course this number will vary, and it could be the same, but for objects with non-overlapping lifetime. In other words, during one specific *scope*, these numbers are guaranteed to be representative of a specific object.

## Scopes

The *scope* that I just brought up is, in very simple terms, like a space for your code to run in. In python, variables are shared from an outer scope to an inner scope.

```python
def test():
    x = 10

print(x) # This will result in a NameError exception since x was defined inside a function.

test()
print(x)
# no, calling the function doesn't add whatever is inside magically to
# the "higher" scope"
```

A higher scope is indicative of a scope that contains another scope. If that is too wordy for your taste:

```python
# this is scope 0
def func():
    # this is scope 1
    def func2():
        # this is scope 2
        pass
    pass 
```

In this example, scope 0 *contains* scope 1. Scope 1 *contains* scope 2. However, everything in scopes 0 and 1 are accessible in scope 2, and everything in scope 0 is accessible to scope 1.

Scope 0 is the outermost scope. Scope 1 is inside scope 0. Scope 1 is outside of scope 2. Scope 2 is inside scope 1.

This will become clearer in time.

## Sniffing around returned values

Now, let's look back at our closures. We saw that the `id` value of the integer that was returned is the same. which means, technically, that the same object was returned into the outer scope from the inner scope.

Let's expand this example.

```python
def func():
    x = 10
    print(id(10))
    return x

external_x = func()
print(id(external_x))

def func2(inp):
    print(id(inp))
    return inp

external_inp = func2(external_x)
print(id(external_inp))
assert external_x is external_inp, "The item is not the same. This assertion should not have been raised"
```

When I run the above snippet, here's what I get:

```
94093123237024
94093123237024
94093123237024
94093123237024
```

If you are following along, this means that the application passed around a variable `x`, created *inside* `func`, outside of its scope, and then *into* the scope of another function that returned it unmodified, and the `id` was never changed. This means that all through your process, you passed around a single object. You did not change it.

Now, you might wonder if this would work.

```python
def func():
    x = 10
    print(id(x))
    return x

ext_x = func()
print(id(ext_x))

def func2(inp):
    inp = inp**2
    return inp

ext_x2 = func2(ext_x)
print(id(ext_x2))
assert ext_x is ext_x2, "the objects are not the same"
```

When I run this, here's what I get:

```
94093123237024
94093123237024
94093123239904
---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-6-bb929bfaec24> in <module>
     13 ext_x2 = func2(ext_x)
     14 print(id(ext_x2))
---> 15 assert ext_x is ext_x2, "the objects are not the same"

AssertionError: the objects are not the same
```

This doesn't work. Why? Let's take it apart using another tool in the python standard library, the `dis` module.

## Disassembling our snippets

The `dis` module allows us to see the bytecode that Python generates from our source code. This can help us understand what's happening under the hood:

```python
import dis

def func2(inp):
    inp = inp**2
    return inp

dis.dis(func2)
```

When you examine the bytecode, you'll see that the assignment `inp = inp**2` creates a new object (the result of the power operation) and assigns it to the local variable `inp`. The original object is not modified - instead, a new integer object is created.

{{< note title="Integer Immutability" >}}
In Python, integers are immutable objects. When you perform operations like `inp**2`, Python creates a new integer object rather than modifying the existing one. This is why the `id` values are different.
{{< /note >}}

## Let's return a dictionary instead!

Let's see what happens with mutable objects:

```python
def create_dict():
    data = {'value': 10}
    print(f"Inside function: id(data) = {id(data)}")
    return data

my_dict = create_dict()
print(f"Outside function: id(my_dict) = {id(my_dict)}")

def modify_dict(d):
    d['value'] = 20
    print(f"Inside modify_dict: id(d) = {id(d)}")
    return d

modified_dict = modify_dict(my_dict)
print(f"After modification: id(modified_dict) = {id(modified_dict)}")
print(f"Original dict: {my_dict}")
print(f"Are they the same object? {my_dict is modified_dict}")
```

With mutable objects like dictionaries, the same object reference is passed around, and modifications affect the original object.

## Nested Functions - Finally

Now let's get to the heart of closures with nested functions:

```python
def outer_function(x):
    outer_variable = x
    
    def inner_function():
        # This inner function has access to outer_variable
        print(f"From inner function: outer_variable = {outer_variable}")
        return outer_variable * 2
    
    return inner_function

# Create a closure
multiplier = outer_function(10)
result = multiplier()
print(f"Result: {result}")
```

Here's where it gets interesting. Even after `outer_function` has finished executing, the `inner_function` still remembers the value of `outer_variable`. This is a closure - the inner function "closes over" the variables from its enclosing scope.

Let's examine what makes this possible:

```python
def create_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15

# Let's see what's in the closure
print(f"double.__closure__: {double.__closure__}")
print(f"Values in closure: {[cell.cell_contents for cell in double.__closure__]}")
```

## `__closure__` and what it means

The `__closure__` attribute reveals the secret behind closures. It contains a tuple of cell objects that hold the values from the enclosing scope:

```python
def outer(x, y):
    def inner():
        return x + y
    return inner

closure_func = outer(10, 20)
print(f"Closure cells: {closure_func.__closure__}")
print(f"Cell contents: {[cell.cell_contents for cell in closure_func.__closure__]}")

# Let's see the variable names
print(f"Code object variables: {closure_func.__code__.co_freevars}")
```

{{< info title="Free Variables" >}}
Variables that are referenced in a function but not defined locally are called "free variables." These are the variables that get captured in closures.
{{< /info >}}

## Practical Example: Building a Counter

Here's a practical example that demonstrates the power of closures:

```python
def create_counter(initial=0):
    count = initial
    
    def increment(step=1):
        nonlocal count
        count += step
        return count
    
    def decrement(step=1):
        nonlocal count
        count -= step
        return count
    
    def get_count():
        return count
    
    # Return a dictionary of functions
    return {
        'increment': increment,
        'decrement': decrement,
        'get_count': get_count
    }

counter = create_counter(5)
print(counter['get_count']())  # 5
print(counter['increment']())  # 6
print(counter['increment'](3))  # 9
print(counter['decrement'](2))  # 7
```

Each counter maintains its own state through closures, providing a clean way to create stateful functions without classes.

## Decorators and Closures

Decorators are perhaps the most common use of closures in Python:

```python
def timer_decorator(func):
    import time
    
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    
    return wrapper

@timer_decorator
def slow_function():
    import time
    time.sleep(1)
    return "Done!"

slow_function()
```

The decorator function returns a closure that wraps the original function, maintaining access to the original function reference.

## Common Pitfalls: Late Binding

Be careful with closures in loops:

```python
# This doesn't work as expected
functions = []
for i in range(3):
    functions.append(lambda: i)

# All functions return 2 (the final value of i)
for f in functions:
    print(f())  # 2, 2, 2

# Fix with default argument
functions = []
for i in range(3):
    functions.append(lambda x=i: x)

# Now each function captures its own value
for f in functions:
    print(f())  # 0, 1, 2
```

## A Personal Story

The conversation at the beginning of this article came about because I had just come out of an interview where the interviewer asked me to explain Python closures. I had faltered, not because I didn't know, but because, oddly enough, I thought there was nothing special about how you can essentially play ping pong with objects in Python. Most languages do this. Python does this only because C does it. You can return pointers, can't you?

All in all, a confusing interview led me to understand something in depth, and helped me learn.

## Conclusion

Closures in Python are indeed intuitive once you understand the underlying concepts of scope and variable lifetime. They provide a powerful mechanism for:

- Creating stateful functions without classes
- Implementing decorators
- Building factory functions
- Maintaining encapsulation

The key insight is that inner functions can capture and remember variables from their enclosing scope, even after the outer function has finished executing. This creates a "closed over" environment - hence the term "closure."

Understanding closures deeply will make you a better Python programmer and help you write more elegant, functional code.