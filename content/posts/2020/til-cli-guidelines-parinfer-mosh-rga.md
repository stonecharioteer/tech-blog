---
date: 2020-12-04T10:00:00+05:30
draft: false
title:
  "TIL: CLI Design Guidelines, Parinfer for Lisp Editing, Mosh Mobile Shell, and
  ripgrep-all for Document Search"
description:
  "Today I learned about comprehensive CLI design guidelines, Parinfer's
  revolutionary approach to Lisp code editing, Mosh as a robust replacement for
  SSH, and ripgrep-all for searching inside various document formats."
tags:
  - "til"
  - "cli"
  - "user-experience"
  - "lisp"
  - "code-editing"
  - "ssh"
  - "networking"
  - "file-search"
  - "document-processing"
---

## CLI Guidelines - Designing Great Command-Line Interfaces

[CLI Guidelines](https://clig.dev/)

Comprehensive guide for creating user-friendly command-line tools:

### Core Design Principles:

#### **Human-First Design:**

- **Helpful by Default**: Show useful information without being asked
- **Fail Gracefully**: Clear error messages with actionable suggestions
- **Consistent Behavior**: Follow established conventions
- **Progressive Disclosure**: Start simple, allow complexity when needed

#### **Error Handling Best Practices:**

```bash
# Bad error message
error: invalid input

# Good error message
error: expected a number, got "hello"
Try: mycommand --count 5

# Even better with suggestions
error: unknown flag '--hep'
Did you mean '--help'?

# Excellent with context
error: cannot connect to database
  database: postgresql://localhost:5432/myapp
  reason: connection refused
  help: is PostgreSQL running? try 'brew services start postgresql'
```

### Guidelines by Category:

#### **Arguments and Flags:**

```bash
# Prefer flags over positional arguments for clarity
# Good
deploy --environment staging --version 1.2.3

# Less clear
deploy staging 1.2.3

# Support both short and long forms
grep -r --recursive      # Both work
grep -R --recursive      # Consistent

# Use consistent flag naming
--verbose / -v           # Standard conventions
--quiet / -q
--help / -h
--version / -V (capital for version)
```

#### **Output and Feedback:**

```bash
# Show progress for long operations
Downloading... [████████████████████████████] 100% (15.2 MB/s)

# Provide machine-readable output options
mycommand --format json
mycommand --format csv
mycommand --format table  # Human-readable default

# Color coding (but respect NO_COLOR)
✓ Success: Database backup completed
⚠ Warning: Low disk space
✗ Error: Connection failed

# Quiet modes for scripts
mycommand --quiet         # No output on success
mycommand --silent        # Minimal output
```

#### **Configuration and Environment:**

```bash
# Configuration hierarchy (most to least specific)
1. Command-line flags
2. Environment variables
3. Configuration files
4. Defaults

# Environment variable naming
MYAPP_DATABASE_URL
MYAPP_LOG_LEVEL
MYAPP_CONFIG_PATH

# Config file locations (XDG spec)
~/.config/myapp/config.yaml    # Primary
~/.myapp.yaml                  # Fallback
/etc/myapp/config.yaml         # System-wide
```

### Advanced Features:

#### **Interactive Elements:**

```python
# Example: Interactive confirmation
import click

@click.command()
@click.option('--force', is_flag=True, help='Skip confirmation')
def delete_database(force):
    if not force:
        click.confirm('This will delete all data. Continue?', abort=True)

    with click.progressbar(tables, label='Dropping tables') as bar:
        for table in bar:
            drop_table(table)

    click.secho('✓ Database deleted', fg='green')

# Tab completion support
@click.command()
@click.argument('environment', type=click.Choice(['dev', 'staging', 'prod']))
def deploy(environment):
    """Deploy to specified environment."""
    pass
```

#### **Documentation Integration:**

```bash
# Multi-level help
mycommand --help              # Overview
mycommand deploy --help       # Subcommand help
mycommand --help-advanced     # Advanced options

# Examples in help text
Usage: git-deploy [OPTIONS] ENVIRONMENT

  Deploy application to specified environment.

  Examples:
    git-deploy staging
    git-deploy prod --version 1.2.3
    git-deploy dev --force --no-backup

Options:
  --version TEXT    Specific version to deploy
  --force          Skip safety checks
  --no-backup      Skip database backup
  --help           Show this message and exit.
```

## Parinfer - Revolutionary Lisp Editing

[Parinfer - simpler Lisp editing](https://shaunlebron.github.io/parinfer/)

Innovative approach to editing Lisp code that infers parentheses from
indentation:

### The Parentheses Problem:

#### **Traditional Lisp Editing Challenges:**

```lisp
;; Traditional Lisp - parentheses can be overwhelming
(defn factorial [n]
  (if (<= n 1)
    1
    (* n (factorial (- n 1)))))

;; Easy to have mismatched parens
(defn broken [x]
  (if (> x 0)
    (inc x)
    (dec x))  ; Missing closing paren somewhere?
```

### Parinfer Modes:

#### **Indent Mode:**

- **Indentation drives structure**: Parentheses inferred from indentation
- **Writing-focused**: Natural for entering new code
- **Familiar**: Works like Python or other indentation-based languages

```lisp
;; Type this (without worrying about parens):
defn factorial [n]
  if (<= n 1)
    1
    * n (factorial (- n 1))

;; Parinfer automatically adds parens:
(defn factorial [n]
  (if (<= n 1)
    1
    (* n (factorial (- n 1)))))
```

#### **Paren Mode:**

- **Parentheses drive structure**: Indentation adjusted to match parens
- **Editing-focused**: Good for modifying existing code
- **Traditional**: Familiar to experienced Lisp programmers

```lisp
;; Move a closing paren:
(defn example [x]
  (if (> x 0)
    (inc x))
    (dec x))

;; Parinfer adjusts indentation:
(defn example [x]
  (if (> x 0)
    (inc x)
    (dec x)))
```

### Smart Features:

#### **Cursor-Based Inference:**

```lisp
;; Cursor position affects paren inference
;; Cursor at end of line:
(map inc [1 2 3|])
;; Result: (map inc [1 2 3])

;; Cursor in middle:
(map inc [1 2| 3])
;; Different grouping possible based on context
```

#### **Tab Stops:**

```lisp
;; Smart tab stops for alignment
(let [x    1
      y    2    ; Aligned automatically
      long 3])

;; Function arguments align naturally
(function arg1
          arg2     ; Aligned with first arg
          arg3)
```

### Editor Integration:

#### **Available Implementations:**

- **Atom**: Lisp editing with Parinfer integration
- **VS Code**: Parinfer extension for modern editor
- **Vim/Neovim**: Multiple Parinfer plugins available
- **Emacs**: Parinfer packages for the classic Lisp editor
- **Sublime Text**: Community-maintained Parinfer support

#### **Configuration Example (VS Code):**

```json
{
  "parinfer.defaultMode": "indent",
  "parinfer.forceBalance": true,
  "parinfer.previewCursorScope": true,
  "parinfer.dimParens": true
}
```

### Benefits for Lisp Learning:

#### **Reduced Cognitive Load:**

- **Focus on Logic**: Less mental energy spent on parentheses
- **Visual Structure**: Indentation makes nesting obvious
- **Error Prevention**: Automatic balancing prevents common mistakes
- **Gentle Learning Curve**: Familiar indentation-based editing

#### **Before/After Comparison:**

```lisp
;; Without Parinfer - manual paren management
(defn process-items [items]
  (map (fn [item]
         (if (valid? item)
           (transform item)
           (default-value))) items))

;; With Parinfer - focus on structure
defn process-items [items]
  map (fn [item]
        if (valid? item)
          transform item
          default-value) items
```

## Mosh - Mobile Shell

[Mosh: the mobile shell](https://mosh.org/)

Robust, responsive terminal application that handles intermittent connectivity:

### Problems with Traditional SSH:

#### **Common SSH Issues:**

- **Connection Drops**: WiFi disconnections kill sessions
- **Lag**: Every keystroke waits for round-trip
- **IP Changes**: Moving between networks breaks connections
- **Firewall Issues**: NAT and firewall complications

### Mosh Solutions:

#### **Key Technologies:**

```
State Synchronization Protocol (SSP):
- Client and server maintain synchronized terminal state
- Only sends differences, not full screen updates
- Works over UDP for better handling of packet loss

Predictive Echo:
- Shows typed characters immediately
- Underlines predictions until confirmed by server
- Reduces perceived latency dramatically
```

#### **Roaming Support:**

```bash
# Traditional SSH breaks when IP changes
ssh user@server
# WiFi → 4G transition = broken connection

# Mosh maintains connection across IP changes
mosh user@server
# WiFi → 4G → different WiFi = seamless transition
```

### Technical Architecture:

#### **Connection Process:**

```bash
# 1. Mosh client connects via SSH
mosh user@server

# 2. SSH launches mosh-server on remote host
# 3. mosh-server chooses UDP port and prints connection info
# 4. SSH connection terminates
# 5. Client connects directly via UDP
# 6. State synchronization begins
```

#### **State Synchronization:**

```
Client State:  "hello world"
Server State:  "hello world"

User types:    "hello world!"
Client State:  "hello world!" (immediately shown)
Server State:  "hello world"  (until network packet arrives)

Network packet arrives:
Server State:  "hello world!" (synchronized)
```

### Advanced Features:

#### **Predictive Text Display:**

```
# User types quickly:
$ git commit -m "fix bug"
  ^^^^^^^^^^^^^^^^^^  (underlined = predicted)

# Once server confirms:
$ git commit -m "fix bug"
  ^^^^^^^^^^^^^^^^^^  (normal display = confirmed)

# If server differs:
$ git commit -m "fix bug"
                    ^^^  (server had different response)
```

#### **Firewall and NAT Traversal:**

```bash
# Mosh uses UDP port range (default 60000-61000)
# Configure firewall to allow:
iptables -A INPUT -p udp --dport 60000:61000 -j ACCEPT

# Or specify port range:
mosh --server="mosh-server new -p 2222" user@server

# Works through NAT (unlike SSH X11 forwarding)
```

### Installation and Usage:

#### **Installation:**

```bash
# Ubuntu/Debian (both client and server needed)
sudo apt install mosh

# macOS
brew install mosh

# CentOS/RHEL
sudo yum install mosh

# Client connects to server (server auto-installed via SSH)
mosh user@hostname
```

#### **Advanced Options:**

```bash
# Specify SSH port
mosh --ssh="ssh -p 2222" user@server

# Set prediction mode
mosh --predict=always user@server    # Always predict
mosh --predict=never user@server     # Never predict
mosh --predict=adaptive user@server  # Default

# Specify colors (for 256-color support)
mosh --colors=256 user@server
```

## ripgrep-all (rga) - Search Inside Documents

[rga: ripgrep, but also search in PDFs, E-Books, Office documents, zip, tar.gz, etc.](https://phiresky.github.io/blog/2019/rga--ripgrep-for-zip-targz-docx-odt-epub-jpg/)

Extended version of ripgrep that searches inside various file formats:

### Supported File Types:

#### **Archive Formats:**

```bash
# Search inside compressed archives
rga "search term" archive.zip
rga "function name" backup.tar.gz
rga "config setting" bundle.tar.xz

# Nested archives supported
rga "password" archive.zip/nested.tar.gz/document.pdf
```

#### **Document Formats:**

```bash
# Office documents
rga "quarterly report" presentation.pptx
rga "budget analysis" spreadsheet.xlsx
rga "project timeline" document.docx

# PDF documents
rga "machine learning" research_paper.pdf
rga "installation guide" manual.pdf

# E-books
rga "character development" novel.epub
rga "design patterns" programming_book.mobi
```

#### **Media and Other Formats:**

```bash
# Image text extraction (OCR)
rga "street sign" photo.jpg
rga "license plate" security_footage.png

# Subtitle files
rga "dramatic scene" movie.mkv  # Searches embedded subtitles
rga "dialogue" subtitles.srt

# Database files
rga "user_table" database.sqlite
```

### Advanced Usage:

#### **Adapter Configuration:**

```bash
# List available adapters
rga --rga-list-adapters

# Use specific adapter
rga --rga-adapters=zip,tar "search term"

# Disable slow adapters (like OCR)
rga --rga-adapters=-tesseract "search term"

# Cache results for faster repeated searches
rga --rga-cache-max-blob-len=10M "search term"
```

#### **Integration with ripgrep Options:**

```bash
# Case-insensitive search
rga -i "Search Term" documents/

# Show context lines
rga -C 3 "important phrase" reports/

# Search specific file types only
rga -t pdf "research data" papers/

# JSON output for processing
rga --json "api_key" config_files/

# Parallel processing
rga -j 8 "performance" large_archive.zip
```

### Performance Considerations:

#### **Caching Strategy:**

```bash
# Enable caching for large files
export RGA_CACHE_DIR=~/.cache/rga
rga --rga-cache-max-blob-len=100M "search term"

# Preprocess large archives
rga --rga-cache-compression-level=1 "index term" huge_backup.tar.gz
```

#### **Resource Management:**

```bash
# Limit memory usage for OCR
rga --rga-adapters=-tesseract "text" images/

# Parallel processing limits
rga -j 4 "search term" documents/  # Use 4 threads max

# Skip large files
rga --max-filesize=50M "config" archive.zip
```

### Practical Applications:

#### **Log Analysis:**

```bash
# Search compressed log archives
rga "ERROR" logs.tar.gz
rga -A 5 -B 5 "database timeout" application_logs.zip

# Find configuration in backups
rga "database.*password" system_backup.tar.gz
```

#### **Research and Documentation:**

```bash
# Academic research
rga -i "neural network" papers/*.pdf
rga "methodology" thesis_sources.zip

# Code archaeology
rga "deprecated function" legacy_code.tar.gz
rga "TODO.*security" project_archive.zip

# Compliance and auditing
rga "personal.*data" document_archive.tar.gz
rga "license.*agreement" contracts.zip
```

#### **Troubleshooting Script:**

```bash
#!/bin/bash
# search-everywhere.sh - comprehensive search tool

search_term="$1"
directory="${2:-.}"

echo "Searching for '$search_term' in $directory"
echo "======================================="

echo "Regular files:"
rg "$search_term" "$directory"

echo -e "\nDocuments and archives:"
rga "$search_term" "$directory"

echo -e "\nCase-insensitive search:"
rga -i "$search_term" "$directory"

echo -e "\nWith context:"
rga -C 2 "$search_term" "$directory"
```

These tools represent modern approaches to common development and system
administration tasks - creating user-friendly CLIs, making complex code editing
more accessible, handling unreliable network connections, and searching through
diverse file formats efficiently.
