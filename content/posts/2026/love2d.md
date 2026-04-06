---
date: "2026-04-06T09:50:10+05:30"
draft: true
title: "From Reading Lua to Building With LÖVE"
description:
  "After reading the reference Lua interpreter, I picked up LÖVE to actually
  use the language. Here's the bridge — what changes when you switch from
  stock Lua to LuaJIT, and why a game framework is the right first project."
tags:
  - "lua"
  - "love2d"
  - "luajit"
  - "games"
  - "performance"
---

<!--
BONUS POST OUTLINE — bridges the lua-c series into a LÖVE project.
This is _not_ part of the Reading Lua series proper. It's a sequel.
Hub: {{< ref "posts/2026/lua-c.md" >}}

## TLDR
- After reading the Lua source ({{< ref "posts/2026/lua-c.md" >}}) I wanted
  to actually _write_ Lua, not just understand it.
- LÖVE is the most fun way to learn Lua: a 2D game framework with a tiny API
  and instant feedback.
- The twist: LÖVE ships with LuaJIT, not stock Lua. So everything I learned
  about the dispatch loop and the GC has a "but actually..." footnote.
- This post is the bridge.

## Why a Game Framework
- Games give you a tight feedback loop: you change a number, you see it.
- Performance matters in games — frame budget is 16.6ms — so the
  performance lens from the series stays relevant.
- The LÖVE API is small enough to learn in an afternoon.
- It's _fun_, which is the best learning multiplier I know.

## What LÖVE Is
- A 2D game framework: SDL2 + OpenGL + LuaJIT under the hood.
- You write `main.lua` with three callbacks: `love.load`, `love.update`,
  `love.draw`. That's the entire core API.
- Distribution is easy: a `.love` file is just a zip.
- Cross-platform: the same `.love` runs on Linux, macOS, Windows, Android.

## The LuaJIT Footnote
- LÖVE uses LuaJIT, _not_ the reference Lua I read for the series.
- What this changes:
  - Bytecode is different (LuaJIT has its own, denser instruction set).
  - The dispatch loop is replaced by trace compilation on hot paths.
  - Values use NaN tagging — 8 bytes each instead of 16.
  - You get the FFI: `ffi.cdef` to call C directly without bindings.
  - You get explicit JIT control: `jit.off()`, `jit.flush()`.
- A whole future post could be _just_ "what LuaJIT changes." Worth flagging.
- The mental model from reading stock Lua transfers, but the constants are
  different.

## The Game Loop
- Walk through `love.run` — it's just a Lua function, you can override it.
- The default loop: handle events → update → draw → wait.
- Where the frame budget goes.
- Why fixed timestep matters for physics.

## A Tiny First Project
- Pick something small: pong, asteroids, a falling-sand toy.
- Show `main.lua` end to end.
- Where to put assets, how `love.graphics` works.
- The minimum viable game in ~50 lines.

## Performance in LÖVE
- Frame budget: 16.6ms at 60fps, 8.3ms at 120fps.
- The big costs in a typical LÖVE game:
  - Draw call count (batch with SpriteBatch).
  - GC pauses (use `collectgarbage("step")` per frame, or pre-allocate).
  - Table allocations in hot loops.
- LuaJIT-specific tips:
  - Avoid the things on the [NYI list](https://wiki.luajit.org/NYI).
  - Use FFI structs for hot data.
  - Profile with `jit.p`.
- These tips only make sense if you understand _why_, which is what the
  Reading Lua series gives you.

## Things I Want to Try
- A small physics demo using LÖVE's box2d binding.
- An FFI-heavy demo: hand-rolled particle system in C structs.
- A "performance budget" experiment: how much can you do per frame?

## Where This Goes Next
- A standalone LuaJIT post: NaN tagging, traces, the IR, side exits.
- A "shipping a LÖVE game" post if I actually finish anything.
- Possibly: embedding LÖVE-style scripting in a Rust project for the
  performance/systems angle.

## Resources
- love2d.org wiki — the docs.
- Mike Pall's LuaJIT writeups.
- Sheepolution's "How to LÖVE" tutorial.
- The LÖVE Discord for help.
-->
