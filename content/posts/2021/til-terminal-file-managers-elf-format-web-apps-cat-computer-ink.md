---
date: 2021-02-18T10:00:00+05:30
draft: false
title:
  "TIL: Terminal File Managers, ELF Format, Responsible Web Apps, Cat Computer
  Debugging, and Ink Narrative Language"
description:
  "Today I learned about modern terminal file managers, ELF executable format
  internals, principles of responsible web applications, hilarious computer
  debugging involving cats, and Ink narrative scripting language for interactive
  storytelling."
tags:
  - "til"
  - "terminal"
  - "file-managers"
  - "elf"
  - "executables"
  - "web-development"
  - "debugging"
  - "storytelling"
  - "scripting-languages"
---

## Modern Terminal File Managers

### lf - Terminal File Manager

[GitHub - gokcehan/lf: Terminal file manager](https://github.com/gokcehan/lf)

Fast, minimalist terminal file manager inspired by ranger:

#### **Key Features:**

- **Vi-like Bindings**: Familiar navigation for vi/vim users
- **Configurable**: Extensive customization through config files
- **Cross-platform**: Works on Linux, macOS, Windows, BSD
- **Fast**: Written in Go for excellent performance
- **Extensible**: Custom commands and integrations

#### **Configuration Example:**

```bash
# ~/.config/lf/lfrc
set preview true
set hidden true
set ignorecase true

# Custom commands
cmd edit ${{
    $EDITOR "$f"
}}

cmd mkdir $mkdir -p "$(echo $* | tr ' ' '\ ')"

# Key bindings
map <enter> shell
map x $$f
map X !$f
map o &mimeopen $f
```

### nnn - The Unorthodox Terminal File Manager

[GitHub - jarun/nnn: n³ The unorthodox terminal file manager](https://github.com/jarun/nnn)

Feature-rich, lightning-fast terminal file manager:

#### **Unique Features:**

- **Disk Usage Analyzer**: Built-in du functionality
- **Plugin System**: Extensible with shell scripts
- **Contexts**: Multiple independent sessions
- **Bookmarks**: Quick navigation to frequent locations
- **Type-to-nav**: Instant search as you type

#### **Advanced Capabilities:**

```bash
# Selection and batch operations
nnn -P p    # Show preview pane
nnn -e      # Text in $EDITOR instead of $PAGER
nnn -r      # Use advcpmv patched cp, mv
nnn -x      # Copy path to clipboard on select

# Environment variables
export NNN_PLUG='f:finder;o:fzopen;p:preview-tui;d:diffs'
export NNN_CONTEXT_COLORS='1234'
export NNN_FIFO='/tmp/nnn.fifo'
```

#### **Plugin Examples:**

- **preview-tui**: Live file preview
- **finder**: fzf integration for fuzzy finding
- **diffs**: Compare files and directories
- **imgview**: Image viewing in terminal

## ELF Format Deep Dive

[In-depth: ELF - The Extensible & Linkable Format - YouTube](https://www.youtube.com/watch?v=nC1U1LJQL8o)

Comprehensive exploration of Linux executable format:

### ELF Structure:

#### **File Layout:**

```
ELF Header
Program Headers (optional)
Section 1
Section 2
...
Section Headers (optional)
```

#### **ELF Header Fields:**

```c
typedef struct {
    unsigned char e_ident[16];  // Magic number and info
    Elf64_Half    e_type;       // Object file type
    Elf64_Half    e_machine;    // Architecture
    Elf64_Word    e_version;    // Object file version
    Elf64_Addr    e_entry;      // Entry point address
    Elf64_Off     e_phoff;      // Program header offset
    Elf64_Off     e_shoff;      // Section header offset
    // ... more fields
} Elf64_Ehdr;
```

### Key Concepts:

#### **Sections vs Segments:**

- **Sections**: Linking view (source code perspective)
- **Segments**: Execution view (loader perspective)
- **Mapping**: Multiple sections can map to one segment

#### **Common Sections:**

- **.text**: Executable code
- **.data**: Initialized global variables
- **.bss**: Uninitialized global variables
- **.rodata**: Read-only data (string literals)
- **.symtab**: Symbol table
- **.strtab**: String table

### Analysis Tools:

```bash
# Basic information
file executable
readelf -h executable        # ELF header
readelf -S executable        # Section headers
readelf -l executable        # Program headers

# Disassembly
objdump -d executable        # Disassemble code
objdump -t executable        # Symbol table
objdump -R executable        # Relocations

# Debugging info
objdump -g executable        # Debug sections
nm executable                # List symbols
strings executable           # Extract strings
```

## Responsible Web Applications

[Responsible Web Applications](https://responsibleweb.app/)

Principles for building ethical, sustainable web applications:

### Core Principles:

#### **Performance Responsibility:**

- **Minimize Payload**: Only send necessary code and data
- **Optimize Loading**: Critical path optimization
- **Efficient Code**: Avoid unnecessary processing
- **Caching Strategies**: Reduce repeat requests

#### **Accessibility First:**

- **Semantic HTML**: Use proper HTML structures
- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Readers**: Compatible with assistive technologies
- **Color Contrast**: Sufficient contrast ratios

#### **Privacy Protection:**

- **Data Minimization**: Collect only necessary data
- **Consent Management**: Clear, informed consent
- **Local Processing**: Process data locally when possible
- **Transparent Policies**: Clear privacy policies

#### **Environmental Impact:**

- **Green Hosting**: Renewable energy providers
- **Efficient Algorithms**: Reduce computational load
- **Optimal Formats**: Use efficient image/video formats
- **Progressive Loading**: Load content as needed

### Implementation Guidelines:

#### **Performance Budget:**

```javascript
// Example performance budget
{
  "budget": [
    {
      "path": "/*",
      "timings": [
        {
          "metric": "first-contentful-paint",
          "budget": 2000
        },
        {
          "metric": "largest-contentful-paint",
          "budget": 2500
        }
      ],
      "resourceSizes": [
        {
          "resourceType": "total",
          "budget": 300
        }
      ]
    }
  ]
}
```

## Why Does My PC Crash Only When My Cat Is Nearby?

[Why does my PC crash only when my cat is nearby? - Super User](https://superuser.com/questions/1626284/why-does-my-pc-crash-only-when-my-cat-is-nearby)

Hilarious and educational debugging story about intermittent computer crashes:

### The Mystery:

- **Correlation**: Computer crashes only when cat is present
- **Timing**: Crashes occur during specific activities
- **Pattern**: Consistent enough to notice correlation

### The Investigation:

- **Environmental Factors**: Temperature, humidity, electromagnetic interference
- **Static Electricity**: Cat fur generating static discharge
- **Physical Interference**: Cat walking on keyboard, touching cables
- **Vibration**: Cat jumping causing mechanical issues

### The Solution:

**Static Electricity Culprit**: Cat's fur building up static charge, discharging
through computer components, causing voltage spikes that crash the system.

### Lessons Learned:

- **Correlation ≠ Causation**: But sometimes correlation leads to causation
- **Environmental Debugging**: Consider all environmental factors
- **Physical Issues**: Don't overlook mechanical/electrical causes
- **Grounding**: Proper grounding prevents static discharge issues

## Ink - Narrative Scripting Language

[ink - inkle's narrative scripting language](https://www.inklestudios.com/ink/)

Powerful scripting language for interactive fiction and narrative games:

### Core Features:

#### **Branching Narratives:**

```ink
You stand at a crossroads.

* [Go left]
  You head down the left path.
  ** [Continue walking]
     The path leads to a dark forest.
* [Go right]
  You take the right path.
  ** [Look around]
     You see a village in the distance.
* [Go back]
  You decide to return home.
  -> END
```

#### **Variables and Logic:**

```ink
VAR health = 100
VAR has_sword = false

{health > 50:
  You feel strong and ready for battle.
} {health <= 50:
  You're wounded and need to be careful.
}

{has_sword:
  * [Attack with sword]
    You swing your blade!
} {not has_sword:
  * [Punch]
    You throw a desperate punch.
}
```

### Advanced Features:

#### **Functions and Tunnels:**

```ink
=== fight_monster ===
You encounter a fearsome beast!
* [Fight] -> combat_sequence -> aftermath
* [Run] -> escape_sequence -> aftermath

= aftermath
The encounter is over.
-> END

=== combat_sequence ===
You engage in combat...
<- <- // Return to calling location

=== escape_sequence ===
You flee from danger...
<- <-
```

#### **Dynamic Text:**

```ink
VAR player_name = "Hero"
VAR times_visited = 0

~ times_visited++

{times_visited == 1: Hello, {player_name}! Welcome!}
{times_visited > 1: Welcome back, {player_name}.}
{times_visited > 5: You're becoming a regular here, {player_name}!}
```

### Integration:

#### **Game Engines:**

- **Unity**: Official Unity plugin
- **Unreal Engine**: Community plugins available
- **Web**: JavaScript runtime for web games
- **Mobile**: iOS and Android support

#### **Output Formats:**

- **JSON**: For custom integrations
- **C#**: Runtime compilation
- **JavaScript**: Web-based stories
- **Standalone**: Command-line player

### Use Cases:

- **Interactive Fiction**: Text-based adventure games
- **Dialogue Systems**: RPG conversation trees
- **Branching Stories**: Choose-your-own-adventure books
- **Educational Content**: Interactive learning materials

Each tool represents innovation in its domain - from efficient terminal
navigation to executable format understanding, ethical web development,
systematic debugging, and narrative design.
