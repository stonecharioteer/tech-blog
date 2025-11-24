---
date: "2025-04-13T10:54:37+05:30"
draft: false
title: "Python Reverse a List"
description:
  "Comparing three methods to reverse lists in Python: slice notation,
  reversed(), and .reverse(). Includes performance benchmarks and readability
  considerations."
tags:
  - "python"
  - "data-structures-and-algorithms"
---

There are a couple of ways to reverse a list in python:

```python
my_list = [1,2,3,"apples","banana","fish","chicken"]
reverse_list_one = my_list[::-1]
reverse_list_one = reversed(my_list)
reverse_list_zero = my_list
reverse_list_zero.reverse()
```

Of these three ways, I prefer using `reversed` because it is readable and
there's no ambiguity about whether it does it in place or not. It should be
obvious to most people that `.reverse()` reverses a list in place, but I prefer
the verbosity of the method that returns a reversed list. It's a stylistic
choice.

The `[::-1]` syntax though is unreadable unless you know where it comes from.
The syntax is `List[start:stop_at:step_count]`. This can be used to collect
items of a list in a specific way. You could use it to collect all the alternate
items in a list through `my_list[::2]`, or every third item from the first to
the seventh index, through `my_list[0:7:2]` (If you don't want to include the
last item, remember that python's list intervals are half-open).

So `[::-1]` means collect all the items in this array but move through it -1
items at a time, meaning, start with the last item first and move backwards.

But which one of these is faster? We can use the timeit module to test this out.

```python
import timeit
import random

my_list = [random.randrange(10**6) for _ in range(10**3)]

trial_1 = timeit.timeit("reversed(my_list)", number=10**4, globals=dict(my_list=my_list))
print(trial_1)
my_list_1 = my_list
trial_2 = timeit.timeit("my_list_1.reverse()", number=10**4, globals=dict(my_list_1=my_list_1))
print(trial_2)
trial_3 = timeit.timeit("my_list[::-1]", number=10**4, globals=dict(my_list=my_list))
print(trial_3)
```

This attempts to reverse a list of a thousand numbers ranging from 0 to a
million ten thousand times. On my
[X13 Flow laptop](/gear/#laptop---asus-x13-flow-2022) and with python 3.12.3
this gets me the following output:

```
0.0005502169997271267
0.0013474229999701492
0.012336962999597745
```

I'm fairly surprised myself that `reversed` is the fastest way to reverse a list
in Python. I half expected to tell you that it'd be the list notation syntax.
And it's faster than the in-place method, which isn't surprising since it's not
trying to move things around to save memory.
[This StackOverflow answer](https://stackoverflow.com/questions/65540349/time-complexity-of-reversed-in-python-3)
shows that it's creating an iterator and not returning a list like the list
notation syntax would, so using `list(reversed(my_list))` would be a fairer
comparison.

```python
import timeit
import random

my_list = [random.randrange(10**6) for _ in range(10**3)]

trial_1 = timeit.timeit("reversed(my_list)", number=10**4, globals=dict(my_list=my_list))
my_list_1 = my_list
trial_2 = timeit.timeit("my_list_1.reverse()", number=10**4, globals=dict(my_list_1=my_list_1))
trial_3 = timeit.timeit("my_list[::-1]", number=10**4, globals=dict(my_list=my_list))
trial_4 = timeit.timeit("list(reversed(my_list))", number=10**4, globals=dict(my_list=my_list))
print(f"""
{ trial_1= }
{ trial_2= }
{ trial_3= }
{ trial_4= }
""")
```

Now we get a more realistic solution.

```
 trial_1= 0.0005320420000316517
 trial_2= 0.0013524949999919045
 trial_3= 0.011964209999860032
 trial_4= 0.032413619000180915
```

Honestly though, this doesn't prove anything. If I needed a reversed list to
_iterate_ over, the iterator approach with `reversed` is the best way to do it.
If I need an in-memory version of it, the list notation syntax is clean.
In-place reversal is useful only if I'm completely sure I would like to reverse
the list in place. This is useful when the list is perhaps an attribute of a
class, for example.
