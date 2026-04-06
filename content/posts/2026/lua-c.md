---
date: "2026-04-06T09:50:04+05:30"
draft: true
title: "Learning C by Reading the Lua Source"
description:
  "Why the Lua interpreter is one of the best C codebases to learn from, and
  the start of a deep series on what reading it taught me about C, interpreters,
  and performance."
tags:
  - "c"
  - "lua"
  - "systems"
  - "performance"
  - "learning-in-public"
---

<!--
HUB POST OUTLINE — this is the landing page for the series.
Write it as a real essay, not a table of contents. The argument should stand
on its own even for a reader who never clicks through to a single part.

## TLDR
- Lua's reference interpreter is ~17K lines of clean ANSI C with no
  dependencies. It's the smallest "real" interpreter you can read end-to-end.
- I'm reading it as part of my push toward systems and performance work
  ({{< ref "posts/2026/direction.md" >}}).
- This is the hub post for a multi-part series. Each part takes one piece of
  the interpreter and goes deep, with a performance lens throughout.

## Why C, Why Now
- Tie back to direction.md — performance/systems trajectory.
- The "real project" problem with C tutorials: K&R is great but it doesn't
  give you a system to navigate.
- Reading > writing as a first step at this stage of my career.
- I wanted a codebase where idiomatic C is on display, not legacy C.

## Why Lua Specifically
- Size: ~17K LOC. Compare CPython (~600K), SQLite (~150K core), redis (~150K).
- Zero external dependencies — `make` and you're done.
- Authors are academics (Ierusalimschy et al.) who optimize for readability.
- It's the codebase Robert Nystrom recommends pairing with Crafting Interpreters.
- {{< note title="Caveat" >}}
  SQLite and redis are also famously readable. Lua wins on _size_ — small
  enough that you can hold the whole thing in your head, which matters when
  you're learning.
  {{< /note >}}

## The Performance Lens
- Every design choice in stock Lua has a "and LuaJIT did this instead"
  counterpoint. That contrast is where I learned the most.
- Throughout the series I'll measure things, not just describe them:
  - `sizeof` of core structs
  - cache line behavior
  - GC pause distribution
  - dispatch loop overhead with switch vs computed goto
- I'll also call out the exact source files and line ranges I'm referring to,
  so you can read along.

## Setting Up to Read
- Where to get the source (lua.org tarball — explain why over the git mirror).
- Building it: `make linux` / `make macosx`. That's the entire build system.
- Tooling I used:
  - `rg` for navigation, `ctags` for jumps
  - `cflow` / `cscope` for call graphs
  - `lldb` to step through `lua -e "print(1+2)"` and watch the VM dispatch live
  - `hyperfine` for microbenchmarks
- How I take notes — annotate in the margins, then write the post from the notes.

## A Reading Order That Worked
- Don't start at `lua.c` (the REPL) or `lapi.c` (the C API surface). Go:
  1. `lobject.h` — the value representation
  2. `lstate.h` / `lstate.c` — execution state
  3. `lvm.c` — the bytecode interpreter loop
  4. `lgc.c` — incremental GC
  5. `lparser.c` / `lcode.c` — single-pass compiler
- The principle: data → state → execution → memory → frontend.
- Each of these gets its own post in the series (links below).

## The Series
- Part 1: TValue — {{< ref "posts/2026/lua-c-tvalue.md" >}}
- Part 2: lua_State and the stack — {{< ref "posts/2026/lua-c-state.md" >}}
- Part 3: Inside lvm.c — {{< ref "posts/2026/lua-c-vm.md" >}}
- Part 4: Lua's incremental GC — {{< ref "posts/2026/lua-c-gc.md" >}}
- Part 5: The single-pass compiler — {{< ref "posts/2026/lua-c-parser.md" >}}
- Bonus: from reading Lua to building with LÖVE — {{< ref "posts/2026/love2d.md" >}}

## What I'd Do Differently
- Read the Lua reference manual _first_, then the source. I did it backwards.
- Skip `ldebug.c` on the first pass.
- Embed Lua in a tiny C program _before_ reading `lapi.c`.

## Resources
- Roberto Ierusalimschy, "The Implementation of Lua 5.0" (paper) — start here.
- Crafting Interpreters by Robert Nystrom — pair with Part 3.
- The Lua reference manual.
- Mike Pall's LuaJIT wiki — the performance counterpoint for the whole series.
-->
