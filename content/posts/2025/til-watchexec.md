---
date: "2025-08-19T12:23:51+05:30"
title: "TIL: Watchexec - Modern File Watching for Development Workflows"
description:
  "Today I learned about watchexec, a cross-platform file watcher that replaced
  entr in my development workflow with better defaults and intuitive usage
  patterns for Hugo, Rust, and Go projects."
tags:
  - "til"
  - "tools"
  - "productivity"
  - "development-tools"
  - "file-watching"
  - "hugo"
  - "rust"
  - "go"
  - "cli"
---

Today I discovered `watchexec`, a modern cross-platform file watcher that has
completely replaced `entr` in my development workflow. It executes commands when
files change with much better defaults and a more intuitive interface than
traditional file watching tools.

{{< ai title="AI-Generated Content" >}} This post was written with assistance
from Claude (Anthropic's AI assistant) based on my experiences and requirements.
While the technical content and examples reflect real usage patterns, the
writing was collaboratively generated. The discovery of watchexec's advantages
over entr - particularly the reduction from verbose
`find . -name "*.go" | entr -r go test` to clean
`watchexec -e go 'go test ./...'` - represents genuine workflow improvements in
my development process. {{< /ai >}}

## The Core Discovery

Watchexec is a Rust-based tool that watches file system changes and triggers
commands. Unlike `entr`, which requires explicit file listing and complex `find`
commands, watchexec works intelligently out of the box.

## What is watchexec?

[Watchexec](https://github.com/watchexec/watchexec) is a simple, standalone tool
that watches a path and runs a command whenever files change. It's written in
Rust, cross-platform, and has sensible defaults that make it easier to use than
alternatives like `entr` or `inotifywait`.

Install it with:

```bash
# Cargo
cargo install watchexec-cli

# Homebrew (macOS/Linux)
brew install watchexec

# Arch Linux
pacman -S watchexec
```

## Hugo Development

For this blog, I use watchexec to auto-rebuild the site during development:

```bash
# Basic Hugo development server
watchexec -e md,yml,yaml,html,css,js 'hugo serve --buildDrafts'

# Only watch content and config changes
watchexec -w content -w hugo.yml -w layouts 'hugo'

# Build and serve on any change
watchexec -r 'hugo && hugo serve --port 1314'
```

The `-e` flag specifies file extensions to watch, and `-w` specifies
directories. The `-r` flag restarts the command (killing the previous process)
rather than running concurrent instances.

## Rust Development with Cargo

For Rust projects, watchexec shines with cargo commands:

```bash
# Auto-compile on save
watchexec -e rs 'cargo check'

# Run tests continuously
watchexec -e rs 'cargo test'

# Build and run
watchexec -e rs 'cargo run'

# Format and check
watchexec -e rs 'cargo fmt && cargo clippy'

# Watch specific files only
watchexec -w src -w Cargo.toml 'cargo build'
```

I particularly love using it during TDD workflows where I want tests to run
immediately after changing code.

## Go Development

Go development becomes much smoother with watchexec:

```bash
# Run tests on any Go file change
watchexec -e go 'go test ./...'

# Build and run
watchexec -e go 'go run main.go'

# Build with race detection
watchexec -e go 'go build -race .'

# Run specific test package
watchexec -w internal/auth 'go test ./internal/auth'

# Format and vet
watchexec -e go 'go fmt ./... && go vet ./...'
```

The ability to watch specific directories with `-w` is especially useful in
larger Go projects where you only want to run tests for the package you're
working on.

## Why I Switched from entr

I used `entr` for years, but watchexec has several advantages:

### Better Defaults

- **entr**: Requires explicit file listing via `find` or similar
- **watchexec**: Recursively watches current directory by default

```bash
# entr - verbose and error-prone
find . -name "*.go" | entr -r go test ./...

# watchexec - simple and intuitive
watchexec -e go 'go test ./...'
```

### Ignore Patterns

- **entr**: No built-in ignore patterns
- **watchexec**: Respects `.gitignore`, `.ignore`, and has smart defaults

Watchexec automatically ignores common build artifacts, `.git` directories, and
other noise. With entr, I had to carefully craft `find` commands to avoid
triggering on build outputs.

### Process Management

- **entr**: Basic process handling
- **watchexec**: Better process lifecycle management with `-r` flag

The `-r` flag in watchexec properly kills and restarts long-running processes,
which is perfect for development servers.

### Cross-Platform

- **entr**: Unix-only
- **watchexec**: Works on Windows, macOS, and Linux

## Caveats and Gotchas

While watchexec is excellent, there are some things to watch out for:

{{< warning title="Build Output Loops" >}} Be careful not to watch directories
that contain build outputs. If your command generates files in a watched
directory, you'll create an infinite loop.

```bash
# BAD - watching target/ where cargo outputs builds
watchexec -w . 'cargo build'

# GOOD - exclude target directory
watchexec -i target/ -e rs 'cargo build'
```

{{< /warning >}}

{{< note title="Performance with Large Projects" >}} In very large codebases,
watching too many files can impact performance. Use `-w` to watch specific
directories or `-i` to ignore large directories like `node_modules/` or
`target/`. {{< /note >}}

{{< tip title="Command Escaping" >}} Complex commands with pipes or redirections
need proper shell escaping:

```bash
# Use quotes for complex commands
watchexec 'cargo test 2>&1 | grep -E "(test|error)"'

# Or use shell flag
watchexec -s 'cargo test | tee test.log'
```

{{< /tip >}}

### Other Considerations

- **Debouncing**: Watchexec debounces file changes by default (50ms), which
  prevents multiple rapid triggers
- **Signal Handling**: Long-running processes are sent SIGTERM, then SIGKILL if
  they don't exit gracefully
- **Environment**: Commands run in the same directory where watchexec was
  started

## Cheatsheet

```bash
# Basic usage
watchexec <command>                    # Watch current dir, run command on any change
watchexec -e rs,toml 'cargo check'     # Watch only .rs and .toml files
watchexec -w src 'make test'           # Watch only src/ directory
watchexec -i target/ 'cargo build'     # Ignore target/ directory

# Process control
watchexec -r 'hugo serve'              # Restart command (kill previous)
watchexec -s 'make && ./app'           # Use shell for complex commands
watchexec --delay 1s 'slow-command'    # Add delay before running

# Filtering
watchexec -e go,mod 'go test'          # Extensions (comma-separated)
watchexec -w app -w lib 'make'         # Multiple watch dirs
watchexec -i '*.tmp' -i build/ 'make'  # Ignore patterns

# Development workflows
# Hugo development
watchexec -e md,yml,html 'hugo serve --buildDrafts'

# Rust development
watchexec -e rs 'cargo check'          # Fast syntax checking
watchexec -e rs 'cargo test'           # Run tests
watchexec -w src 'cargo run'           # Build and run

# Go development
watchexec -e go 'go test ./...'        # Run all tests
watchexec -e go 'go run main.go'       # Build and run
watchexec -w internal/api 'go test ./internal/api'  # Test specific package

# Multi-command workflows
watchexec -e rs 'cargo fmt && cargo clippy && cargo test'
watchexec -e go 'go fmt ./... && go vet ./... && go test ./...'

# Useful flags
-r, --restart           # Restart previous command
-s, --shell             # Use shell for command execution
-w, --watch <path>      # Watch specific path
-i, --ignore <pattern>  # Ignore pattern
-e, --exts <extensions> # File extensions to watch
--delay <duration>      # Delay before running command
-v, --verbose           # Verbose output
```

Watchexec has become an essential part of my development workflow. Its intuitive
interface and smart defaults make file watching trivial, letting me focus on
code instead of build tools. If you're still using `entr` or manually rerunning
commands, give watchexec a try.
