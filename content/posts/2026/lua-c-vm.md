---
date: "2026-04-06T09:50:07+05:30"
draft: true
title: "Reading Lua, Part 3: Inside lvm.c, the Bytecode Interpreter Loop"
description:
  "The hot loop at the heart of Lua: instruction encoding, switch dispatch
  vs computed goto, and why LuaJIT throws all of this away in favor of traces."
tags:
  - "c"
  - "lua"
  - "performance"
  - "systems"
  - "interpreters"
series:
  - "Reading Lua"
---

<!--
PART 3 OUTLINE — lvm.c, the dispatch loop.
Source files: lvm.c, lopcodes.h, lopcodes.c
Hub: {{< ref "posts/2026/lua-c.md" >}}

This is the longest part. The dispatch loop is the heart of the interpreter
and the place where most performance lives.

## TLDR
- Lua's bytecode interpreter is a single function (`luaV_execute`) built
  around a giant switch on the opcode.
- Instructions are 32 bits, encoding an opcode and up to three register
  operands.
- The whole "computed goto vs switch" debate happens here, and you can
  toggle it with one `#define`.
- LuaJIT's win over stock Lua comes _almost entirely_ from replacing this
  loop with trace-compiled native code.

## Instruction Encoding
- 32-bit instructions, defined in `lopcodes.h`.
- Three formats: iABC (3 operands), iABx (1 operand + 1 long), iAsBx
  (signed long for jumps).
- Walk through how `GETARG_A`, `GETARG_B`, `GETARG_C` extract bitfields.
- Why fixed-width instructions: simple decode, predictable cache behavior.
- Compare to CPython's wordcode (16-bit) and JVM bytecode (variable).
- Performance experiment: count instructions with `luac -l` for a real program.

## The Opcode Set
- ~40 opcodes total. Walk through the categories:
  - Move/load: MOVE, LOADK, LOADBOOL, LOADNIL
  - Globals/upvalues: GETUPVAL, SETUPVAL, GETTABUP, SETTABUP
  - Tables: GETTABLE, SETTABLE, NEWTABLE, SETLIST
  - Arithmetic: ADD, SUB, MUL, DIV, MOD, POW, UNM
  - Comparison: EQ, LT, LE
  - Control flow: JMP, TEST, TESTSET, FORLOOP, FORPREP, TFORLOOP
  - Calls: CALL, TAILCALL, RETURN
  - Closures: CLOSURE, CLOSE
- Note how many ops are "fast paths" for common cases (e.g., FORLOOP
  is a fused increment + test + jump).

## The Dispatch Loop Structure
- `luaV_execute` is one big function. Why one function: register pinning.
  Read the register-allocation comment near the top.
- The hot pointer cache: `pc`, `base`, `k` — pinned to registers.
- After every operation, `pc++` and dispatch the next.
- The `Protect()` macro: things that might trigger GC must save `pc` first.

## Switch Dispatch vs Computed Goto
- Two `vmdispatch` macros, one for each strategy. Toggled by `LUA_USE_GOTO`
  on supported compilers.
- Switch dispatch:
  - One indirect branch at the bottom of the loop.
  - The CPU branch predictor sees it as one branch with 40+ targets — bad.
  - Result: ~10% predictor hit rate on real workloads.
- Computed goto (threaded code):
  - Each opcode handler ends with its _own_ dispatch.
  - The branch predictor now sees N branches, each with a much narrower
    distribution of next targets. ~90% predictor hit rate.
  - Typical speedup: 15-25% on interpreted Lua.
- Reference: "The Structure and Performance of Efficient Interpreters"
  (Ertl & Gregg, 2003).
- Performance experiment: build Lua twice (one with goto, one without),
  benchmark, profile.

## A Worked Example: ADD
- Show the C code for OP_ADD.
- The fast path: both operands are integers → integer add.
- The slower path: at least one is a float → float add.
- The slowest path: metamethods (`__add`).
- How the hierarchy is encoded with branch hints.
- Why this op got 3x more complex when Lua 5.3 split int/float.

## A Worked Example: GETTABLE
- Show the C code for OP_GETTABLE.
- The fast path: array part, integer key in range → direct index.
- The hash path: hash lookup with a chained probe.
- The metamethod path: `__index` chain walk.
- Why hash hits dominate string-keyed code.
- The "table inline cache" idea (LuaJIT does this; stock Lua doesn't).

## What LuaJIT Does Differently
- Trace compilation: record a hot loop as a linear trace, compile to
  native code, install side exits.
- Dynamic typing becomes static along the trace via type guards.
- Result: stock Lua runs ~10× slower than C; LuaJIT runs ~1-2× slower.
- The trace compiler eliminates the dispatch loop entirely on hot paths.
- Mike Pall's design notes are required reading. Link them.
- This is the natural sequel to reading lvm.c — and an obvious future post.

## Things That Confused Me
- Why `pc` is a `const Instruction *` and incremented before the operands
  are decoded. (Answer: it makes the operand offsets constant.)
- The `dojump` macro and how it interacts with TESTSET.
- Why some ops have explicit `vmbreak` and others fall through.

## Experiments to Run
- Build with `LUA_USE_GOTO` on and off. `hyperfine` a CPU-bound Lua script.
- `perf stat -e branch-misses` on both builds.
- Disassemble a Lua function and trace its execution by hand for one iteration.
- Compare against LuaJIT on the same workload.

## Up Next
- Part 4: the GC running underneath all of this.
  {{< ref "posts/2026/lua-c-gc.md" >}}
-->
