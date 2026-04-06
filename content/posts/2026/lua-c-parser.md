---
date: "2026-04-06T09:50:09+05:30"
draft: true
title: "Reading Lua, Part 5: The Single-Pass Compiler"
description:
  "Lua compiles source straight to bytecode in one pass with no AST. How
  it's possible, why it's fast, and what it gives up in exchange."
tags:
  - "c"
  - "lua"
  - "performance"
  - "systems"
  - "compilers"
series:
  - "Reading Lua"
---

<!--
PART 5 OUTLINE — lparser.c + lcode.c, the single-pass compiler.
Source files: llex.c, lparser.c, lcode.c, lopcodes.h
Hub: {{< ref "posts/2026/lua-c.md" >}}

## TLDR
- Lua's compiler is a single pass: source code goes in, bytecode comes out,
  no AST in between.
- The parser (`lparser.c`) and the codegen (`lcode.c`) are tightly coupled —
  the parser calls codegen as it recognizes constructs.
- This is _fast_ to compile and easy to read, but it gives up most
  optimization opportunities.
- The trade-off is the deepest design tension in Lua, and the place where
  LuaJIT had to start over from scratch.

## TLDR for Compiler People
- Recursive-descent parser, operator-precedence climbing for expressions.
- On-the-fly codegen with a small peephole window in `lcode.c`.
- Register allocation is greedy and tied to expression evaluation.
- Jump patching uses linked lists of pending jumps (the "patch list" idiom).

## The Lexer
- `llex.c` — hand-written, ~600 LOC.
- One-character lookahead. Strings are interned at lex time.
- Why hand-written: error messages, performance, embedding control.
- Lessons in writing a fast lexer in C without flex.

## The Parser
- Recursive descent for statements: `block`, `statement`, `funcbody`, etc.
- Operator-precedence climbing for expressions (`subexpr` and the priority
  table).
- Why precedence climbing > shunting yard for hand-written parsers.
- The grammar is small enough to fit in `lparser.c`'s comments at the top.

## No AST: How Is That Possible?
- The parser doesn't build a tree. As it recognizes a construct, it
  immediately calls into `lcode.c` to emit bytecode.
- All "expression state" is captured in a tiny struct: `expdesc`.
- `expdesc` has a kind tag (literal, local, upvalue, indexed, ...) and
  enough data to either:
  - Defer codegen (e.g. for short-circuit operators), or
  - Emit immediately when forced into a register.
- This is the key insight: defer just enough that you can do peephole
  optimizations on the next operator.

## FuncState: Per-Function Compilation Context
- One `FuncState` per function being compiled, linked into a stack as
  nested functions are entered.
- Tracks: current pc, local variables, upvalues, constants, register
  watermark.
- Walk through the fields and how they're consumed by `lcode.c`.

## Register Allocation
- Greedy, stack-discipline. The "next free register" is just the high
  watermark.
- Locals are pinned (their register is their slot for the function's life).
- Temporaries are popped after each statement.
- Why this works: Lua's value model means every value is one slot;
  no need for graph coloring.
- The cost: no live-range splitting, no register coalescing. LuaJIT does
  both in its IR.

## Peephole Optimizations in lcode.c
- Constant folding for arithmetic on literals (`luaK_arith`).
- Combining LOADNIL runs into a single multi-slot LOADNIL.
- Replacing LOADBOOL+JMP with TESTSET when possible.
- Folding negative literals into the immediate field of operations.
- Each optimization is local — they look at the most recent emitted
  instruction and maybe rewrite it.
- Why "peephole only" is the right call here: the compiler has to be
  cheap _and_ correct in one pass.

## Jump Patching
- Forward jumps don't know their target yet.
- `lcode.c` keeps each unresolved jump as a linked list embedded in the
  bytecode itself (the jump's offset field points to the next pending jump).
- When the target is reached, the list is walked and all offsets are
  patched.
- The "true list" / "false list" trick for short-circuit operators —
  separate patch lists for each branch outcome.
- This is one of the most beautiful pieces of code in Lua. Worth a careful
  read.

## What This Design Gives Up
- No global optimizations: no inlining, no escape analysis, no SSA.
- No type information beyond what the literals tell you.
- Bytecode quality is decent but not great — there's slack to recover.
- LuaJIT's IR (SSA-based) and trace compilation exist precisely to recover
  this slack at runtime instead of at parse time.

## What It Gives You In Return
- _Compile speed_. Lua compiles faster than almost anything else, including
  most parsers that don't even codegen.
- _Memory_. No AST means no AST-sized allocations.
- _Simplicity_. The whole compiler is ~3000 LOC across two files.
- _Embeddability_. You can `loadstring` user code at runtime without fear.

## The Performance Story
- Compile time: dominated by lexing and parsing, not codegen.
- Compile-time allocation: bounded — no AST, no IR.
- Cold-start cost for embedded Lua is essentially zero.
- Compare to LuaJIT, which has a similar bytecode compiler _and_ a trace
  IR compiler that runs only on hot code.

## Things That Confused Me
- The patch list trick — I had to draw it on paper before it clicked.
- `expdesc` kinds like `VRELOCABLE` and `VNONRELOC` and the dance between
  them. They control whether codegen can still pick a destination register.
- How `discharge2reg` collapses a deferred expression into a real register.

## Experiments to Run
- Time `loadstring` on a large Lua source file. Compare to Python's `compile`.
- `luac -l -p` a hand-written program and verify the peephole opts fired.
- Force a constant fold by tweaking source — show before/after bytecode.

## Wrapping Up the Series
- Back to the hub: {{< ref "posts/2026/lua-c.md" >}}
- The bonus post: from reading Lua to building with LÖVE.
  {{< ref "posts/2026/love2d.md" >}}
-->
