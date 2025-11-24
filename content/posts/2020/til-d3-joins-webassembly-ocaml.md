---
date: 2020-08-27T10:00:00+05:30
draft: false
title:
  "TIL: D3.js Data Joins, WebAssembly Basics, OCaml Scientific Computing, and
  Vim-like System Layers"
description:
  "Today I learned about D3.js data join patterns for dynamic visualizations,
  hands-on WebAssembly development, OCaml for scientific computing, and creating
  Vim-like interaction layers for desktop environments."
tags:
  - til
  - d3js
  - data-visualization
  - webassembly
  - ocaml
  - scientific-computing
  - vim
  - desktop-environments
---

Today's discoveries spanned from web visualization techniques to low-level
programming and system customization.

## D3.js Data Joins - The Core Pattern

[D3 Selection Join](https://observablehq.com/@d3/selection-join) and
[Thinking With Joins](https://bost.ocks.org/mike/join/) explain D3's fundamental
approach to data-driven document manipulation:

### Understanding the Join Pattern:

#### **Traditional DOM Manipulation:**

```javascript
// Imperative approach - manually managing elements
function updateChart(data) {
  const container = d3.select("#chart");
  container.selectAll("div").remove(); // Remove all existing

  data.forEach((d) => {
    container
      .append("div")
      .style("width", d * 10 + "px")
      .style("height", "20px")
      .style("background", "steelblue")
      .text(d);
  });
}
```

#### **D3 Data Join Pattern:**

```javascript
// Declarative approach - describe the relationship between data and elements
function updateChart(data) {
  const bars = d3.select("#chart").selectAll("div").data(data);

  // Enter: Create new elements for new data
  bars
    .enter()
    .append("div")
    .style("height", "20px")
    .style("background", "steelblue")
    .merge(bars) // Merge with existing elements
    .style("width", (d) => d * 10 + "px")
    .text((d) => d);

  // Exit: Remove elements with no corresponding data
  bars.exit().remove();
}
```

#### **Modern Join API (D3 v5+):**

```javascript
function updateChart(data) {
  d3.select("#chart")
    .selectAll("div")
    .data(data)
    .join("div") // Handles enter, update, exit automatically
    .style("width", (d) => d * 10 + "px")
    .style("height", "20px")
    .style("background", "steelblue")
    .text((d) => d);
}

// With custom enter/update/exit handling
function advancedChart(data) {
  d3.select("#chart")
    .selectAll("div")
    .data(data)
    .join(
      (enter) =>
        enter
          .append("div")
          .style("opacity", 0)
          .call((enter) =>
            enter.transition().duration(500).style("opacity", 1),
          ),
      (update) => update.style("background", "orange"),
      (exit) => exit.transition().duration(500).style("opacity", 0).remove(),
    )
    .style("width", (d) => d * 10 + "px")
    .style("height", "20px")
    .text((d) => d);
}
```

### Complex Data Binding:

#### **Nested Selections:**

```javascript
// Binding hierarchical data
const matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9],
];

const table = d3.select("#table");

const rows = table.selectAll("tr").data(matrix).join("tr");

const cells = rows
  .selectAll("td")
  .data((d) => d) // Each row's data becomes the data for its cells
  .join("td")
  .text((d) => d);
```

#### **Object Constancy with Key Functions:**

```javascript
// Maintain element identity across updates
const data = [
  { id: "a", value: 10 },
  { id: "b", value: 20 },
  { id: "c", value: 30 },
];

function updateWithKeys(data) {
  d3.select("#chart")
    .selectAll("div")
    .data(data, (d) => d.id) // Key function ensures object constancy
    .join("div")
    .style("width", (d) => d.value * 10 + "px")
    .text((d) => `${d.id}: ${d.value}`);
}

// When data changes, elements smoothly transition rather than recreating
const newData = [
  { id: "b", value: 25 }, // Updated
  { id: "c", value: 30 }, // Unchanged
  { id: "d", value: 15 }, // New
  // 'a' removed
];
```

## WebAssembly Hands-On Development

[Hands-on WebAssembly: Try the Basics](https://evilmartians.com/chronicles/hands-on-webassembly-try-the-basics)
provides practical WebAssembly development experience:

### Core WebAssembly Concepts:

#### **Basic C to WASM Compilation:**

```c
// math.c - Simple C functions for WebAssembly
#include <emscripten.h>

EMSCRIPTEN_KEEPALIVE
int add(int a, int b) {
    return a + b;
}

EMSCRIPTEN_KEEPALIVE
double fibonacci(int n) {
    if (n <= 1) return n;
    double a = 0, b = 1, c;
    for (int i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

EMSCRIPTEN_KEEPALIVE
void sort_array(int* arr, int length) {
    // Simple bubble sort
    for (int i = 0; i < length - 1; i++) {
        for (int j = 0; j < length - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
```

#### **Compilation and JavaScript Integration:**

```bash
# Compile C to WebAssembly
emcc math.c -o math.js -s EXPORTED_FUNCTIONS="['_add', '_fibonacci', '_sort_array']" -s MODULARIZE=1 -s EXPORT_NAME="MathModule"
```

```javascript
// Using compiled WebAssembly module
async function loadWasm() {
  const Module = await MathModule();

  // Call simple functions
  console.log("Add:", Module._add(5, 3)); // 8
  console.log("Fibonacci:", Module._fibonacci(10)); // 55

  // Work with memory for arrays
  const arraySize = 5;
  const arrayPtr = Module._malloc(arraySize * 4); // 4 bytes per int
  const array = new Int32Array(Module.HEAP32.buffer, arrayPtr, arraySize);

  // Fill array with data
  array.set([64, 34, 25, 12, 22]);

  // Sort using WASM function
  Module._sort_array(arrayPtr, arraySize);

  // Read sorted result
  console.log("Sorted:", Array.from(array)); // [12, 22, 25, 34, 64]

  // Clean up memory
  Module._free(arrayPtr);
}

loadWasm();
```

#### **Performance Comparison:**

```javascript
// JavaScript vs WebAssembly performance
function jsFibonacci(n) {
  if (n <= 1) return n;
  let a = 0,
    b = 1,
    c;
  for (let i = 2; i <= n; i++) {
    c = a + b;
    a = b;
    b = c;
  }
  return b;
}

async function benchmarkFibonacci() {
  const Module = await MathModule();
  const n = 40;

  // JavaScript benchmark
  console.time("JS Fibonacci");
  const jsResult = jsFibonacci(n);
  console.timeEnd("JS Fibonacci");

  // WebAssembly benchmark
  console.time("WASM Fibonacci");
  const wasmResult = Module._fibonacci(n);
  console.timeEnd("WASM Fibonacci");

  console.log("Results match:", jsResult === wasmResult);
}
```

## OCaml Scientific Computing

[OCaml Scientific Computing](https://ocaml.xyz/book/) demonstrates OCaml's
capabilities for numerical and scientific applications:

### OCaml for Numerical Computing:

#### **Matrix Operations:**

```ocaml
(* Using Owl library for scientific computing *)
#require "owl";;
open Owl;;

(* Create matrices *)
let a = Mat.uniform 3 3;;  (* 3x3 random matrix *)
let b = Mat.eye 3;;        (* 3x3 identity matrix *)

(* Matrix operations *)
let c = Mat.(a + b);;      (* Addition *)
let d = Mat.(a *@ b);;     (* Matrix multiplication *)
let e = Mat.transpose a;;  (* Transpose *)

(* Linear algebra *)
let eigenvals = Linalg.D.eigvals a;;
let det = Linalg.D.det a;;
let inv = Linalg.D.inv a;;

(* Statistical operations *)
let mean = Mat.mean a;;
let std = Mat.std a;;
let sum = Mat.sum a;;
```

#### **Plotting and Visualization:**

```ocaml
(* Data visualization with Plot module *)
let x = Mat.linspace 0. (2. *. Owl_const.pi) 100;;
let y = Mat.sin x;;

(* Create plot *)
let h = Plot.create "sine_wave.png";;
Plot.plot ~h x y;;
Plot.xlabel h "x";;
Plot.ylabel h "sin(x)";;
Plot.title h "Sine Wave";;
Plot.output h;;

(* Histogram *)
let data = Mat.gaussian 1000 1;;  (* 1000 random numbers *)
let h2 = Plot.create "histogram.png";;
Plot.histogram ~h:h2 ~bin:30 data;;
Plot.output h2;;
```

#### **Optimization and Root Finding:**

```ocaml
(* Numerical optimization *)
let f x = (x -. 2.) ** 2. +. (x -. 1.) ** 4.;;  (* Function to minimize *)
let df x = 2. *. (x -. 2.) +. 4. *. (x -. 1.) ** 3.;;  (* Derivative *)

(* Find minimum using gradient descent *)
let minimize_result = Optimise.D.minimise f df 0.;;

(* Root finding *)
let g x = x ** 3. -. 2. *. x -. 5.;;  (* Find roots of this function *)
let root = Root1d.D.brent g 1. 3.;;  (* Find root between 1 and 3 *)
```

## Vim-like Layer for Desktop Environments

[Vim-like Layer for Xorg and Wayland](https://cedaei.com/posts/vim-like-layer-for-xorg-wayland/)
describes creating system-wide Vim-style key bindings:

### Implementation Approaches:

#### **Using xcape and xmodmap (X11):**

```bash
# Map Caps Lock to Escape when pressed alone, Ctrl when held
setxkbmap -option caps:ctrl_modifier
xcape -e 'Caps_Lock=Escape'

# Create system-wide Vim-like bindings
xmodmap -e "keycode 43 = h H Left Left"      # h -> Left
xmodmap -e "keycode 44 = j J Down Down"      # j -> Down
xmodmap -e "keycode 45 = k K Up Up"          # k -> Up
xmodmap -e "keycode 46 = l L Right Right"    # l -> Right
```

#### **Custom Key Daemon:**

```python
#!/usr/bin/env python3
# vim_layer.py - System-wide Vim bindings

import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess
import threading

class VimLayer:
    def __init__(self):
        self.insert_mode = True
        self.devices = self.find_keyboards()

    def find_keyboards(self):
        devices = []
        for path in evdev.list_devices():
            device = InputDevice(path)
            if ecodes.EV_KEY in device.capabilities():
                devices.append(device)
        return devices

    def toggle_mode(self):
        self.insert_mode = not self.insert_mode
        print(f"Mode: {'INSERT' if self.insert_mode else 'NORMAL'}")

    def handle_normal_mode(self, key):
        """Handle Vim-like commands in normal mode"""
        key_mappings = {
            'h': 'xdotool key Left',
            'j': 'xdotool key Down',
            'k': 'xdotool key Up',
            'l': 'xdotool key Right',
            'w': 'xdotool key ctrl+Right',
            'b': 'xdotool key ctrl+Left',
            '0': 'xdotool key Home',
            '$': 'xdotool key End',
            'gg': 'xdotool key ctrl+Home',
            'G': 'xdotool key ctrl+End',
            'dd': 'xdotool key Home shift+End Delete',
            'yy': 'xdotool key Home shift+End ctrl+c',
            'p': 'xdotool key ctrl+v',
            'i': lambda: self.toggle_mode(),
            'a': lambda: [subprocess.run(['xdotool', 'key', 'Right']), self.toggle_mode()],
        }

        if key in key_mappings:
            action = key_mappings[key]
            if callable(action):
                action()
            else:
                subprocess.run(action.split())

    def listen(self):
        for device in self.devices:
            threading.Thread(target=self.process_device, args=(device,)).start()

    def process_device(self, device):
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY and event.value == 1:  # Key press
                key = ecodes.KEY[event.code]

                if key == 'KEY_ESC':
                    self.insert_mode = False
                elif not self.insert_mode:
                    self.handle_normal_mode(key.replace('KEY_', '').lower())

if __name__ == '__main__':
    vim_layer = VimLayer()
    vim_layer.listen()
```

These discoveries showcase the breadth of modern computing - from elegant data
visualization patterns to low-level performance optimization, scientific
computing capabilities, and system customization techniques that enhance
productivity across different domains.
