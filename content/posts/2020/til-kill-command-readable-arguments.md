---
date: 2020-11-21T10:00:00+05:30
draft: false
title: "TIL: Kill Command with Readable Signal Arguments"
description:
  "Today I learned that the kill command accepts human-readable signal names
  instead of just numeric codes, making process management more intuitive and
  safer."
tags:
  - til
  - unix
  - process-management
  - signals
  - system-administration
---

Today I discovered a simple but important improvement to using the `kill`
command that makes process management safer and more readable.

## Using Readable Signal Names

Instead of memorizing and using numeric signal codes, the `kill` command accepts
human-readable signal names:

### Traditional Numeric Approach:

```bash
# Hard to remember and error-prone
kill -9 1234    # SIGKILL
kill -15 1234   # SIGTERM
kill -19 1234   # SIGSTOP
kill -18 1234   # SIGCONT
```

### Better Readable Approach:

```bash
# Clear, self-documenting commands
kill -KILL 1234   # Force terminate process
kill -TERM 1234   # Graceful termination request
kill -STOP 1234   # Pause process execution
kill -CONT 1234   # Resume paused process
```

## Common Signal Names

### Process Termination:

- **`-TERM` (15)**: Polite termination request - allows cleanup
- **`-KILL` (9)**: Immediate forceful termination - no cleanup possible
- **`-QUIT` (3)**: Quit with core dump for debugging

### Process Control:

- **`-STOP` (19)**: Pause process execution (cannot be caught or ignored)
- **`-TSTP` (20)**: Terminal stop signal (Ctrl+Z equivalent)
- **`-CONT` (18)**: Resume stopped process execution

### Application Signals:

- **`-HUP` (1)**: Hangup - often used to reload configuration
- **`-USR1` (10)**: User-defined signal 1 - application-specific behavior
- **`-USR2` (12)**: User-defined signal 2 - application-specific behavior

## Benefits of Readable Names

### Safety and Clarity:

```bash
# Immediately clear what this does
kill -TERM $(pgrep myapp)

# vs unclear numeric version
kill -15 $(pgrep myapp)
```

### Self-Documenting Scripts:

```bash
#!/bin/bash
# Graceful service restart script

PID=$(pgrep myservice)
if [ -n "$PID" ]; then
    echo "Requesting graceful shutdown..."
    kill -TERM $PID

    # Wait for graceful shutdown
    sleep 5

    # Force kill if still running
    if kill -0 $PID 2>/dev/null; then
        echo "Forcing termination..."
        kill -KILL $PID
    fi
fi
```

### Reduced Errors:

Using readable names eliminates the risk of accidentally using the wrong signal
number, which could have unintended consequences on system stability.

This simple practice makes process management commands more maintainable and
reduces the cognitive load of remembering numeric signal codes.
