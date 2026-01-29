---
date: 2022-01-24T10:00:00+05:30
draft: false
title: "TIL: Creating Fixed Length Iterables in Python"
description:
  TIL how to create fixed-length iterables in Python using collections.deque
  with maxlen parameter. Perfect for creating circular buffers and bounded
  collections.
tags:
  - "til"
  - "python"
  - "data-structures"
  - "collections"
---

If you want to create an iterable of a fixed length in python, use
`collections.deque` with the `maxlen` parameter.

```python
import collections

fixed_list = collections.deque(5*[None], 10)

# this is now a fixed list of items 10.
# by _appending_ more items, you'd be dropping items
# from the beginning.

fixed_list.append(1)
print(fixed_list)
```

Note that this merely calls `appendleft`.
