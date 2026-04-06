---
date: "2026-04-06T09:50:06+05:30"
draft: true
title: "Reading Lua, Part 2: lua_State and the Stack Discipline"
description:
  "What a Lua coroutine actually is, why Lua's stack is just an array of
  TValues, and how a register-based VM lays out call frames."
tags:
  - "c"
  - "lua"
  - "performance"
  - "systems"
series:
  - "Reading Lua"
---

<!--
PART 2 OUTLINE — lua_State, stack, call frames.
Source files: lstate.h, lstate.c, ldo.c, lapi.c
Hub: {{< ref "posts/2026/lua-c.md" >}}

## TLDR
- A `lua_State` is everything Lua needs to execute: stack, call info, hooks,
  GC roots. A coroutine is _literally_ a separate `lua_State`.
- The stack is one flat array of TValues. Call frames are described by a
  parallel `CallInfo` linked list.
- Lua is a _register-based_ VM, but the registers are slots in this stack.
- The performance story: fewer dispatches per operation than a stack VM,
  at the cost of bigger bytecode.

## What lua_State Holds
- Walk through `lstate.h` field by field.
- The two stacks: `stack` (TValue[]) and `ci` (CallInfo linked list).
- `top`, `base`, `stack_last` — the invariants between them.
- GC roots: openupval list, the global table, the registry.
- The error handler chain (longjmp targets).

## global_State vs lua_State
- One global_State per Lua _universe_, shared by all coroutines.
- Holds the GC, the string table, the metatable cache.
- Coroutines share the global_State but have independent stacks. This is why
  coroutines are cheap: ~few KB each, not a full OS stack.

## The Stack Is an Array
- One `TValue *stack` allocated up front.
- Grows by realloc when it overflows. _All TValue pointers in the VM must
  be relocated_ — that's why Lua uses indices internally, not raw pointers.
- The "stack overflow" check in the dispatch loop.
- Diagram: stack with multiple call frames, top, and base markers.

## Call Frames: CallInfo
- `CallInfo` struct: `func`, `top`, `previous`, `next`, status flags.
- Forms a doubly-linked list, _not_ stored on the value stack.
- Why split: the value stack must be relocatable; call frames have stable
  identity (they hold raw `TValue *` cursors).
- How `ldo.c` builds and tears down a CallInfo on every Lua call.

## Register-Based vs Stack-Based VMs
- Stack VM (CPython, JVM): operands are pushed/popped. Many small ops.
- Register VM (Lua, Dalvik): operands are stack slots addressed by index.
- Lua's "registers" are just `base[i]` for some i.
- Why register-based wins on _instruction count_: an `ADD` is one op,
  not three (`LOAD`, `LOAD`, `ADD`).
- Why it loses on _instruction size_: each opcode encodes 3 register
  indices, so it's 32 bits instead of 8.
- Reference: Ierusalimschy's Lua 5.0 paper has the original benchmarks
  showing the win.

## Tail Calls in O(1) Stack
- Lua guarantees tail calls don't grow the stack. The reference manual says
  so, and `ldo.c` enforces it.
- How `OP_TAILCALL` works: reuse the current CallInfo instead of pushing a
  new one. Walk through the implementation.
- Why this matters for functional-style Lua and for Scheme-like patterns.

## Coroutines as Stacks
- `lua_newthread` creates a new `lua_State` sharing the same `global_State`.
- `coroutine.resume` is implemented via `lua_resume`, which uses `setjmp`/
  `longjmp` to context-switch between stacks.
- This is _not_ a kernel thread, _not_ an OS context switch — it's a
  longjmp + a state pointer swap. Microseconds, not milliseconds.
- Performance experiment: time `coroutine.resume` against a function call.

## setjmp/longjmp as Exceptions
- C has no exceptions, so Lua uses `setjmp`/`longjmp` for error propagation.
- `lua_pcall` sets a jump buffer; `luaL_error` jumps to it.
- This is the cleanest use of `setjmp`/`longjmp` I've ever read.
- Caveat: destructors don't run, so Lua has no RAII. Resources must be
  GC-managed instead.

## The Performance Story
- Coroutine creation cost: a few KB of allocation, no syscalls.
- Compare to OS threads (~MB) and Go goroutines (~few KB but with a runtime).
- Lua coroutines are arguably the cheapest concurrency primitive in any
  mainstream language.
- Counterpoint: they're cooperative, single-threaded. No parallelism.

## Things That Confused Me
- `L->base` vs `ci->func+1` — they're the same thing, but the redundancy
  threw me. It's a cache for the hot path.
- Why `top` is updated so aggressively in the VM loop. (Answer: GC needs to
  know which slots are live.)

## Experiments to Run
- `print(collectgarbage("count"))` before and after creating 10k coroutines.
- Time deep recursion with and without tail calls.
- Disassemble a function that uses upvalues and trace where they live.

## Up Next
- Part 3: now that we know where values live, how does the VM execute them?
  {{< ref "posts/2026/lua-c-vm.md" >}}
-->
