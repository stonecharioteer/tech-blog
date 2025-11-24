---
date: 2020-08-31T10:00:00+05:30
draft: false
title:
  "TIL: Asciimatics Terminal Effects, Lock-Free Programming, EOPL, and Ranger
  File Manager"
description:
  "Today I learned about creating full-screen terminal animations with
  Asciimatics, wait-free and lock-free programming concepts, the Essentials of
  Programming Languages book, and the Vim-inspired Ranger file manager."
tags:
  - til
  - terminal
  - concurrency
  - programming-languages
  - file-management
  - python
  - vim
---

Today's discoveries ranged from terminal user interfaces to advanced concurrency
concepts and programming language theory.

## Asciimatics - Full-Screen Terminal Animations

[Asciimatics](https://github.com/peterbrittain/asciimatics) enables creating
sophisticated terminal-based animations and effects in Python:

### Core Features:

#### **Screen Management:**

```python
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.effects import Cycle, Stars
from asciimatics.particles import RingFirework, SerpentFirework, PalmFirework
from asciimatics.renderers import FigletText, Rainbow
import sys

def demo(screen):
    scenes = []
    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            screen.height // 2 - 3),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            screen.height // 2 + 3),
        Stars(screen, 200)
    ]
    scenes.append(Scene(effects, 500))

    # Fireworks effect
    fireworks = []
    for _ in range(20):
        fireworks.append(RingFirework(
            screen,
            screen.width // 2,
            screen.height // 2,
            screen.height,
            start_frame=randint(0, 250)))

    effects = fireworks + [Stars(screen, 200)]
    scenes.append(Scene(effects, 500))

    screen.play(scenes, stop_on_resize=True, start_scene=scenes[0])

Screen.wrapper(demo)
```

#### **Advanced Effects:**

```python
from asciimatics.effects import Print, Snow
from asciimatics.particles import Explosion
from asciimatics.paths import Path
from asciimatics.sprites import Sam

class CustomPath(Path):
    def process_colour_map(self, screen, colour_map):
        # Custom path animation logic
        return colour_map

    def is_finished(self, frame):
        return frame > self._max_frames

def complex_demo(screen):
    # Sprite animation
    path = Path()
    path.jump_to(-20, screen.height // 2)
    path.move_straight_to(screen.width + 20, screen.height // 2, screen.width // 4)

    effects = [
        Sam(screen, path),
        Snow(screen),
        Print(screen,
              Rainbow(screen, FigletText("Hello World!")),
              screen.height // 2 - 3,
              speed=1,
              transparent=False),
    ]

    scenes = [Scene(effects, -1)]
    screen.play(scenes)
```

#### **Interactive Applications:**

```python
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, Button
from asciimatics.widgets import TextBox, Widget

class DemoFrame(Frame):
    def __init__(self, screen):
        super(DemoFrame, self).__init__(screen,
                                      screen.height * 2 // 3,
                                      screen.width * 2 // 3,
                                      hover_focus=True,
                                      title="Contact Details",
                                      reduce_cpu=True)

        # Create layout
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        # Add widgets
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Email:", "email"))
        layout.add_widget(TextBox(3, "Address:", "address", as_string=True))
        layout.add_widget(Divider())

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)

        self.fix()

    def _ok(self):
        # Handle OK button
        self._scene.add_effect(PopUpDialog(self._screen, "Saved!", ["OK"]))

    def _cancel(self):
        raise StopApplication("User pressed quit")

def interactive_demo(screen):
    screen.play([Scene([DemoFrame(screen)], -1)], stop_on_resize=True)
```

### Use Cases:

- **System monitoring dashboards**: Real-time resource visualization
- **Game development**: Text-based games with visual effects
- **Data visualization**: Charts and graphs in terminal environments
- **Interactive tools**: Menu-driven applications and wizards

## Awesome Lock-Free Programming

[Awesome Lock-Free](https://github.com/rigtorp/awesome-lockfree) compiles
resources on wait-free and lock-free programming:

### Core Concepts:

#### **Lock-Free vs Wait-Free:**

```cpp
// Lock-based (traditional)
class Counter {
private:
    std::mutex mtx;
    int value = 0;
public:
    void increment() {
        std::lock_guard<std::mutex> lock(mtx);
        ++value;  // Thread blocks if lock is held
    }

    int get() {
        std::lock_guard<std::mutex> lock(mtx);
        return value;
    }
};

// Lock-free (using atomic operations)
class LockFreeCounter {
private:
    std::atomic<int> value{0};
public:
    void increment() {
        value.fetch_add(1);  // Never blocks, but may retry
    }

    int get() {
        return value.load();  // Always completes in finite steps
    }
};

// Wait-free (strongest guarantee)
class WaitFreeArray {
private:
    std::atomic<int> data[SIZE];
public:
    void set(int index, int val) {
        data[index].store(val);  // Always completes in bounded steps
    }

    int get(int index) {
        return data[index].load();  // No possibility of indefinite delay
    }
};
```

#### **Memory Ordering:**

```cpp
#include <atomic>

// Sequential consistency (strongest, slowest)
std::atomic<int> counter{0};
counter.store(42);  // Default: memory_order_seq_cst

// Relaxed ordering (weakest, fastest)
counter.store(42, std::memory_order_relaxed);

// Acquire-release semantics
std::atomic<bool> ready{false};
std::atomic<int> data{0};

// Producer thread
void producer() {
    data.store(42, std::memory_order_relaxed);
    ready.store(true, std::memory_order_release);  // Synchronizes with acquire
}

// Consumer thread
void consumer() {
    while (!ready.load(std::memory_order_acquire)) {
        // Wait for producer
    }
    int value = data.load(std::memory_order_relaxed);  // Guaranteed to see 42
}
```

#### **ABA Problem and Solutions:**

```cpp
// ABA Problem: Value changes from A to B to A, appearing unchanged
template<typename T>
class LockFreeStack {
private:
    struct Node {
        T data;
        Node* next;
    };

    std::atomic<Node*> head{nullptr};

public:
    void push(T data) {
        Node* new_node = new Node{data, nullptr};
        new_node->next = head.load();

        // Compare-and-swap loop
        while (!head.compare_exchange_weak(new_node->next, new_node)) {
            // Retry if another thread modified head
        }
    }

    bool pop(T& result) {
        Node* old_head = head.load();

        while (old_head &&
               !head.compare_exchange_weak(old_head, old_head->next)) {
            // Handle ABA: old_head updated by compare_exchange_weak
        }

        if (old_head) {
            result = old_head->data;
            delete old_head;  // Memory management challenge
            return true;
        }
        return false;
    }
};
```

### Advanced Techniques:

- **Hazard pointers**: Safe memory reclamation in lock-free structures
- **RCU (Read-Copy-Update)**: Optimized for read-heavy workloads
- **Compare-and-swap loops**: Building complex operations from atomic primitives
- **Memory fences**: Controlling instruction reordering

## Essentials of Programming Languages (EOPL)

[EOPL](http://eopl3.com/) provides comprehensive coverage of programming
language implementation:

### Core Topics:

#### **Interpreter Implementation:**

```scheme
; Simple expression language
(define-datatype expression expression?
  [const-exp (num integer?)]
  [var-exp (var symbol?)]
  [add-exp (exp1 expression?) (exp2 expression?)]
  [let-exp (var symbol?) (exp1 expression?) (body expression?)])

; Interpreter
(define eval-expression
  (lambda (exp env)
    (cases expression exp
      [const-exp (num) num]
      [var-exp (var) (apply-env env var)]
      [add-exp (exp1 exp2)
        (+ (eval-expression exp1 env)
           (eval-expression exp2 env))]
      [let-exp (var exp1 body)
        (let ([val (eval-expression exp1 env)])
          (eval-expression body (extend-env var val env)))])))
```

#### **Type Systems:**

```scheme
; Type checker for simple language
(define-datatype type type?
  [int-type]
  [bool-type]
  [proc-type (arg-type type?) (result-type type?)])

(define type-of
  (lambda (exp tenv)
    (cases expression exp
      [const-exp (num) (int-type)]
      [var-exp (var) (apply-tenv tenv var)]
      [add-exp (exp1 exp2)
        (let ([type1 (type-of exp1 tenv)]
              [type2 (type-of exp2 tenv)])
          (if (and (equal? type1 (int-type))
                   (equal? type2 (int-type)))
              (int-type)
              (error "Type error in addition")))])))
```

### Language Features Covered:

- **Lexical scoping**: Environment models and closure implementation
- **Control structures**: Continuations and exception handling
- **Object-oriented features**: Classes, inheritance, and method dispatch
- **Type inference**: Hindley-Milner algorithm and polymorphism

## Ranger - Vim-Inspired File Manager

[Ranger](https://github.com/ranger/ranger) provides a powerful, keyboard-driven
file management experience:

### Key Features:

#### **Installation and Basic Usage:**

```bash
# Install ranger
pip install ranger-fm

# Or via package manager
sudo apt install ranger  # Ubuntu/Debian
brew install ranger      # macOS

# Launch ranger
ranger

# Basic navigation
j/k     # Move down/up
h/l     # Move to parent/child directory
gg/G    # Go to top/bottom
/       # Search files
n/N     # Next/previous search result
```

#### **Advanced Navigation:**

```bash
# Bookmarks
m<key>  # Set bookmark
'<key>  # Go to bookmark
um<key> # Delete bookmark

# Tabs
gt/gT   # Next/previous tab
uq      # Close tab
gn      # New tab

# File operations
yy      # Copy file
dd      # Cut file
pp      # Paste file
dD      # Delete file
cw      # Rename file
:mkdir  # Create directory
```

#### **Configuration:**

```python
# ~/.config/ranger/rc.conf
set column_ratios 1,3,4
set hidden_filter ^\.|\.(?:pyc|pyo|bak|swp)$|^lost\+found$|^__(pycache|init)__$
set show_hidden false
set colorscheme default
set preview_files true
set preview_directories true
set collapse_preview true

# Custom key bindings
map <C-f> fzf_select
map <C-d> shell dragon-drag-and-drop -a -x %p
map bg shell setbg %f
map mkd console mkdir%space

# Custom commands
alias e    edit
alias q    quit
alias q!   quitall
alias qa   quitall
alias qall quitall
```

#### **Plugin Integration:**

```bash
# Image preview (requires w3m-img or similar)
set preview_images true
set preview_images_method w3m

# Video thumbnails (requires ffmpegthumbnailer)
set preview_videos true

# Archive contents (requires atool)
set preview_archives true

# PDF preview (requires pdftotext)
set preview_pdfs true
```

These tools demonstrate the diversity of terminal-based applications possible in
modern computing environments, from visual effects and concurrent programming to
language implementation and efficient file management.
