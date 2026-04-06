---
date: "2026-04-06T09:50:05+05:30"
draft: true
title: "Reading Lua, Part 1: TValue, How Lua Represents Everything"
description:
  "Lua's universal value type, tagged unions in C, the cost of dynamic typing,
  and why LuaJIT throws all of this away in favor of NaN tagging."
tags:
  - "c"
  - "lua"
  - "performance"
  - "systems"
series:
  - "Reading Lua"
---

<!--
PART 1 OUTLINE — TValue, the universal value.
Source files: lobject.h, lobject.c, lstring.c, ltable.c
Hub: {{< ref "posts/2026/lua-c.md" >}}

## TLDR
- Every value in Lua — number, string, table, function, nil — is a TValue.
- TValue is a tagged union: a `Value` payload plus a type tag.
- Understanding TValue unlocks ~60% of the codebase. Read this file first.
- The performance story is _all about_ how dynamic typing punishes the cache.

## The Shape of a Value
- Walk through `lobject.h` line by line for the TValue definition.
- Show the `Value` union: lua_Integer, lua_Number, GCObject*, void*, etc.
- Show the type tag and the helper macros (`ttype`, `setnvalue`, etc.).
- Diagram: 16 bytes on 64-bit (8 payload + tag + padding).

## Tagged Unions in C
- Why C unions are the right tool here.
- The discipline of "always check the tag before reading the value."
- How Lua's macros enforce this at the source level.
- A side-by-side: how you'd write the same thing in Rust (enum) vs Go (interface).

## Lua 5.1 vs 5.3 vs 5.4
- 5.3 added an integer subtype — why, and what it changed in TValue.
- The arithmetic dispatch in `lvm.c` got a lot uglier as a result.
- 5.4 added `<close>` variables — another tag bit consumed.
- Lesson: tagged unions don't scale gracefully when types proliferate.

## Strings, Tables, Functions: GCObject
- TValue holds a `GCObject*` for collectable types.
- The `CommonHeader` macro at the top of every GC type — shared GC metadata.
- Walk through `TString`: the inline-data trick for short strings.
- String interning: `lstring.c` and the global string table.
- Why interning matters for table key lookup performance.

## Tables: The One Data Structure
- `Table` struct in `lobject.h` — array part + hash part.
- The hybrid layout and why it exists.
- How `ltable.c` decides whether to grow the array or the hash.
- Performance experiment: measure access cost for sequential vs sparse keys.

## The Cache-Line Story
- `sizeof(TValue)` on 64-bit Lua: 16 bytes. Four per cache line.
- Compare to a CPython PyObject (much heavier) and a JS SMI (much lighter).
- Why Lua's "everything is a TValue on the stack" beats CPython's
  "everything is a heap-allocated PyObject pointer" for raw throughput.
- Pointer-chasing overhead for strings, tables, closures.

## The Performance Counterpoint: NaN Tagging
- LuaJIT, JavaScriptCore, and Spidermonkey all use NaN tagging instead.
- The trick: IEEE 754 doubles have 2^51 unused NaN bit patterns.
- Stuff a 48-bit pointer + 3 type bits into a NaN payload.
- Result: every value is exactly 8 bytes. _Eight_ TValues per cache line.
- Why Lua proper doesn't do this: portability + readability.
- Link to Mike Pall's writeups on LuaJIT's value representation.

## Things That Confused Me
- The macro layering — `setobj`, `setobj2s`, `setobj2t`, `setobj2n`.
  They differ in barriers and write semantics, not in the actual store.
- Why some macros take an `L` parameter even when they don't appear to use it.
  (Spoiler: write barriers.)

## Experiments to Run
- Print `sizeof(TValue)`, `sizeof(Table)`, `sizeof(TString)` on your machine.
- Microbenchmark: integer-keyed table access vs string-keyed.
- Microbenchmark: stack-allocated locals vs upvalues vs globals.
- Disassemble a tiny Lua function with `luac -l` and map every operand back
  to a TValue slot.

## Up Next
- Part 2: where do these TValues actually live? `lua_State` and the stack.
  {{< ref "posts/2026/lua-c-state.md" >}}
-->
