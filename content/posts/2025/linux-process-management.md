---
date: "2025-07-25T15:57:25+05:30"
draft: true
title: "Linux Process Management"
description: "Understand how the linux process and memory management works with this deepdive."
tags:
  - "linux"
  - "internals"
  - "deep-dive"
url: "linux/memory"
---

Do you understand how processes and memory are managed within Linux? Neither do I, but I
want to learn.

I want to work through both of these in a way that explains it to me in first principles.
I don't like not understanding things, and I've used Linux long enough that I feel like I
should dig into these things. If this ends up being too broad a topic, I'll break this
down into multiple posts. For now, though, I want to use this as a way to practically
understand what's going on under the hood.

{{<info>}}
Some general housekeeping steps:

The code is accessible in github: [https://github.com/stonecharioteer/linux-process-management](https://github.com/stonecharioteer/linux-process-management)

If you'd like to follow along, you need the following:

1. Docker - to run some of the examples where I'll setup containers to have a limited space to work through things.
2. Python - for the examples you can run locally on your machine. Use `uv` and choose anything above python 3.12
3. _(Optional)_ Rust - for the examples to understand memory and process management deeply.
   {{</info>}}

## Process Management in Python - `psutil` Tutorial

For this section of this article, get a working python environment going. In 2025, I prefer using `uv`.

```python

```

{{< tip title="Recommended Resources" >}}
If you want to understand more about Linux Memory Management, here are a few resources:

- [The Linux Kernel Admin Guide: Memory Management](https://docs.kernel.org/admin-guide/mm/index.html)
- [The Linux Kernel: Memory Management](https://docs.kernel.org/mm/index.html)
- [Email Thread: Active Memory Mangement](https://docs.kernel.org/mm/active_mm.html#active-mm)
- [Lorenzo Stoakes - The Linux Memory Manager (No Starch Press; 2025; Early Access Only)](https://nostarch.com/linux-memory-manager)
  {{< /tip >}}
