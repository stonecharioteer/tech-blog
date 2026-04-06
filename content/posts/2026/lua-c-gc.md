---
date: "2026-04-06T09:50:08+05:30"
draft: true
title: "Reading Lua, Part 4: Lua's Incremental Garbage Collector"
description:
  "Tri-color marking, write barriers, and the generational mode added in 5.4.
  How the GC interleaves with the interpreter and what it costs you."
tags:
  - "c"
  - "lua"
  - "performance"
  - "systems"
  - "garbage-collection"
series:
  - "Reading Lua"
---

<!--
PART 4 OUTLINE — lgc.c, the garbage collector.
Source files: lgc.h, lgc.c, plus barrier macros sprinkled through lvm.c, ltable.c
Hub: {{< ref "posts/2026/lua-c.md" >}}

## TLDR
- Lua uses an incremental, tri-color, mark-and-sweep collector.
- "Incremental" means GC work is sliced into small steps interleaved with
  allocation, so there's no long stop-the-world pause.
- Lua 5.4 added an optional generational mode on top.
- The cost shows up in two places: GC steps in the allocator, and write
  barriers in the dispatch loop.

## Why GC at All
- Lua values are dynamically typed and dynamically sized — manual memory
  management is impractical for the user.
- The C side gets `lua_Alloc`: a single function pointer for all allocation.
  This is the cleanest allocator hook in any language I've read.
- Embed contexts (game engines, databases) can route Lua allocations through
  their own arenas.

## Tri-Color Invariants
- The classic Dijkstra tri-color algorithm:
  - White: not yet visited (candidate for collection).
  - Gray: visited but children not yet scanned.
  - Black: visited and scanned.
- The invariant: no black object may point to a white object.
- Lua uses _two_ whites (current and other) to handle objects allocated
  during a GC cycle without re-marking.

## Write Barriers
- The barrier maintains the tri-color invariant when mutation happens
  mid-collection.
- Two flavors:
  - Forward barrier: when a black object gets a new white child, mark the
    child gray immediately.
  - Backward barrier: when a black object is mutated, demote it back to
    gray to be re-scanned later.
- Lua uses both — forward for most types, backward for tables (because
  tables mutate so often, demoting once is cheaper than barriering every
  field).
- Walk through `luaC_barrier` and `luaC_barrierback` in `lgc.c`.
- Show where they're invoked from `lvm.c` in OP_SETTABLE etc.

## The Incremental State Machine
- GC has a state field: `GCSpause`, `GCSpropagate`, `GCSatomic`,
  `GCSswpallgc`, `GCSswpfinobj`, `GCSswptobefnz`, `GCSswpend`, `GCScallfin`.
- Each GC step does a bounded amount of work and advances the state.
- The `atomic` phase is the only stop-the-world part — minimal but real.
- Diagram: state machine with transitions and what happens in each.

## Pacing: How Much GC Per Allocation?
- `gcstepmul` and `gcpause` knobs.
- The "debt" model: every allocation increments debt; GC steps work it down.
- Why this matters for latency-sensitive code (games, servers).
- How to tune it: bigger pause = more throughput, less latency smoothness.

## Generational Mode (Lua 5.4)
- Why generational: most objects die young.
- Lua's twist: generational mode is _optional_ and can switch back to
  incremental on the fly if survival rates are high.
- Walk through the minor vs major collection paths.
- Compare to OCaml's minor heap and Go's no-generations decision.

## The Performance Story
- Throughput cost: write barriers add a branch + maybe a function call to
  every store. Measurable but small.
- Latency story: incremental keeps pauses sub-millisecond on typical
  workloads. Generational keeps them even smaller.
- Allocation cost: `lua_Alloc` is one indirect call per allocation.
  Custom allocators can crush this.
- Compare to:
  - Go: concurrent GC, no generations, write barriers always on.
  - OCaml: generational, very fast minor GC, short majors.
  - JVM: a half-dozen GCs to choose from.
  - CPython: refcounting + cycle collector. Different model entirely.

## Finalizers
- `__gc` metamethod. How it's implemented.
- Why finalizers run in a separate phase (`GCScallfin`).
- The "resurrection" problem and Lua's solution.

## Things That Confused Me
- The two-white trick. It took me reading the code three times to see
  why it's correct.
- The `GCObject` linked-list weaving — every collectable object lives in a
  list, and there are several different lists for different stages.
- The `barrierback` returning to gray feels wrong until you realize it's
  a throughput optimization.

## Experiments to Run
- Time `collectgarbage("collect")` for a heap of N tables. Plot vs N.
- Measure pause distribution for a tight allocation loop.
- Implement a custom `lua_Alloc` that uses an arena. Measure the throughput
  difference.
- Toggle generational mode and rerun the same benchmarks.

## Up Next
- Part 5: where do the bytecode and the GC objects come from in the first
  place? The compiler.
  {{< ref "posts/2026/lua-c-parser.md" >}}
-->
