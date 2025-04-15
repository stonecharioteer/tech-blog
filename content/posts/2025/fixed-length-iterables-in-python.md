---
date: '2025-04-14T16:00:21+05:30'
draft: false
title: 'Fixed Length Iterables in Python'
tags:
  - "python"
---

If you want to create an iterable of fixed length in Python, use `collections.deque` with the `maxlen` parameter.

```python

import collections
fixed_list = collections.deque(5*[None], 10)

# this is now a fixed list of 10 items.
# by appending more items, you'd be 
# dropping items from the beginning

fixed_list.append(1)
print(fixed_list)
```

This is a short article, mostly to record something I see a lot of junior developers try to implement themselves.