---
date: 2020-10-09T10:00:00+05:30
draft: false
title:
  "TIL: Rust Terminal Libraries, Text Editor Development, Tau vs Pi, and TypeLit
  Typing Practice"
description:
  "Today I learned about Rust libraries for terminal applications, building text
  editors from scratch, the mathematical argument for Tau over Pi, and improving
  typing skills with classic literature."
tags:
  - til
  - rust
  - text-editors
  - mathematics
  - typing
  - terminal
  - programming
---

Today's discoveries spanned from practical Rust development to mathematical
philosophy and skill improvement techniques.

## Rust Terminal Application Libraries

Several powerful Rust crates enable sophisticated terminal user interfaces:

### Core Terminal Libraries:

#### **Crossterm - Cross-Platform Terminal Manipulation:**

```rust
// Cargo.toml
[dependencies]
crossterm = "0.27"

// Basic usage
use crossterm::{
    cursor, execute, style,
    terminal::{self, ClearType},
    Result
};
use std::io::stdout;

fn main() -> Result<()> {
    // Enter raw mode for character-by-character input
    terminal::enable_raw_mode()?;

    // Clear screen and move cursor
    execute!(
        stdout(),
        terminal::Clear(ClearType::All),
        cursor::MoveTo(0, 0),
        style::Print("Hello, Terminal!")
    )?;

    // Restore terminal
    terminal::disable_raw_mode()?;
    Ok(())
}
```

#### **TUI-rs - Rich Terminal User Interfaces:**

```rust
// Cargo.toml
[dependencies]
tui = "0.19"
crossterm = "0.27"

use tui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout},
    style::{Color, Modifier, Style},
    text::{Span, Spans},
    widgets::{Block, Borders, List, ListItem, Paragraph},
    Terminal,
};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize terminal
    let stdout = std::io::stdout();
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    terminal.draw(|f| {
        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .margin(1)
            .constraints([Constraint::Percentage(50), Constraint::Percentage(50)])
            .split(f.size());

        let paragraph = Paragraph::new("Hello, TUI!")
            .block(Block::default().title("Greeting").borders(Borders::ALL));
        f.render_widget(paragraph, chunks[0]);

        let items: Vec<ListItem> = vec![
            ListItem::new("Item 1"),
            ListItem::new("Item 2"),
            ListItem::new("Item 3"),
        ];
        let list = List::new(items)
            .block(Block::default().title("List").borders(Borders::ALL))
            .style(Style::default().fg(Color::White))
            .highlight_style(Style::default().add_modifier(Modifier::ITALIC))
            .highlight_symbol(">>");
        f.render_widget(list, chunks[1]);
    })?;

    Ok(())
}
```

#### **Termium - Lower-Level Terminal Control:**

```rust
// Cargo.toml
[dependencies]
termion = "1.5"

use termion::raw::IntoRawMode;
use termion::{clear, cursor, style};
use std::io::{stdout, Write};

fn main() {
    let _stdout = stdout().into_raw_mode().unwrap();

    print!("{}{}{}Bold and Red Text{}{}",
           clear::All,
           cursor::Goto(1, 1),
           style::Bold,
           style::Reset,
           cursor::Goto(1, 3));

    stdout().flush().unwrap();
}
```

## Text Editor Development Tutorials

### Hecto - Modern Text Editor in Rust:

[Hecto Tutorial](https://www.philippflenker.com/hecto/) demonstrates building a
complete text editor from scratch:

```rust
// Core editor structure
pub struct Editor {
    should_quit: bool,
    terminal: Terminal,
    cursor_position: Position,
    offset: Position,
    document: Document,
    status_message: StatusMessage,
}

impl Editor {
    pub fn run(&mut self) {
        loop {
            if let Err(error) = self.refresh_screen() {
                die(&error);
            }
            if self.should_quit {
                break;
            }
            if let Err(error) = self.process_keypress() {
                die(&error);
            }
        }
    }

    fn process_keypress(&mut self) -> Result<(), std::io::Error> {
        let pressed_key = Terminal::read_key()?;
        match pressed_key {
            Key::Ctrl('q') => self.should_quit = true,
            Key::Up | Key::Down | Key::Left | Key::Right
            | Key::PageUp | Key::PageDown | Key::End | Key::Home => {
                self.move_cursor(pressed_key);
            }
            Key::Char(c) => {
                self.document.insert(&self.cursor_position, c);
                self.move_cursor(Key::Right);
            }
            Key::Delete => self.document.delete(&self.cursor_position),
            Key::Backspace => {
                if self.cursor_position.x > 0 || self.cursor_position.y > 0 {
                    self.move_cursor(Key::Left);
                    self.document.delete(&self.cursor_position);
                }
            }
            _ => (),
        }
        Ok(())
    }
}
```

### Kilo-inspired C Tutorial:

[antirez/Kilo](https://viewsourcecode.org/snaptoken/kilo/index.html) provides
step-by-step text editor construction:

#### **Core Features Implementation:**

- Raw mode terminal control
- Keyboard input handling
- Screen drawing and cursor movement
- File I/O operations
- Search functionality
- Status bar and message display

### Wilo - Minimalist Rust Editor:

[Wilo](https://github.com/prabirshrestha/wilo) demonstrates a simple but
functional text editor architecture:

```rust
// Simplified editor loop
struct Editor {
    buffer: Vec<String>,
    cursor_x: usize,
    cursor_y: usize,
    screen_width: usize,
    screen_height: usize,
}

impl Editor {
    fn draw_screen(&self) {
        print!("{}{}", clear::All, cursor::Goto(1, 1));

        for (i, line) in self.buffer.iter().enumerate() {
            if i >= self.screen_height - 1 { break; }
            println!("{}\r", line);
        }

        print!("{}", cursor::Goto(
            (self.cursor_x + 1) as u16,
            (self.cursor_y + 1) as u16
        ));
    }
}
```

## The Tau Manifesto - Mathematical Philosophy

[The Tau Manifesto](https://tauday.com/tau-manifesto/) argues for using τ (tau)
= 2π instead of π as the fundamental circle constant:

### Core Arguments for Tau:

#### **Geometric Intuition:**

- **Full circle**: τ radians = 1 full rotation (360°)
- **Half circle**: τ/2 radians = half rotation (180°)
- **Quarter circle**: τ/4 radians = quarter rotation (90°)
- **Eighth circle**: τ/8 radians = eighth rotation (45°)

#### **Mathematical Simplification:**

```
Traditional with π:
- Circle area: A = πr²
- Circle circumference: C = 2πr
- Radians in full circle: 2π

With τ = 2π:
- Circle area: A = (τ/2)r²
- Circle circumference: C = τr
- Radians in full circle: τ
```

#### **Educational Benefits:**

- Students naturally think in terms of full rotations
- Trigonometric identities become more intuitive
- Unit circle relationships are clearer

#### **Examples of Tau Clarity:**

```python
import math

# Traditional approach
angle_degrees = 90
angle_radians = angle_degrees * math.pi / 180
# Result: π/2

# With tau
TAU = 2 * math.pi
angle_radians = angle_degrees * TAU / 360
# Result: τ/4 (more intuitive)

# Frequency to angular frequency
frequency = 60  # Hz
omega_traditional = 2 * math.pi * frequency
omega_tau = TAU * frequency  # Cleaner
```

### Practical Implications:

- Programming languages could adopt tau constants
- Engineering calculations become more intuitive
- Educational materials could be simplified
- Scientific notation could be cleaner

## TypeLit - Typing Practice with Literature

[TypeLit.io](https://typelit.io) provides typing practice using passages from
classic literature:

### Features:

- **Classic texts**: Practice with works from Dickens, Austen, Shakespeare
- **Proper punctuation**: Learn to type complex sentences with correct
  punctuation
- **Progress tracking**: Monitor words per minute and accuracy
- **Literature exposure**: Encounter great writing while improving typing skills

### Benefits for Programmers:

- **Symbol familiarity**: Practice with punctuation used in code
- **Accuracy improvement**: Develop muscle memory for precise character entry
- **Speed development**: Increase coding velocity through better typing
- **Cultural literacy**: Exposure to classical literature

### Implementation Concept:

```javascript
// Simplified typing practice implementation
class TypingPractice {
  constructor(text) {
    this.text = text;
    this.position = 0;
    this.errors = 0;
    this.startTime = null;
  }

  handleKeypress(key) {
    if (!this.startTime) this.startTime = Date.now();

    if (key === this.text[this.position]) {
      this.position++;
      return { correct: true, progress: this.position / this.text.length };
    } else {
      this.errors++;
      return { correct: false, expected: this.text[this.position] };
    }
  }

  getStats() {
    const timeMinutes = (Date.now() - this.startTime) / 60000;
    const wordsTyped = this.position / 5; // Standard: 5 characters = 1 word
    const wpm = wordsTyped / timeMinutes;
    const accuracy = ((this.position - this.errors) / this.position) * 100;

    return { wpm, accuracy, errors: this.errors };
  }
}
```

These discoveries highlight the intersection of practical programming skills,
mathematical thinking, and continuous learning - all essential elements for
effective software development.
