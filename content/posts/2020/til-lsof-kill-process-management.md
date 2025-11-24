---
date: 2020-11-03T10:00:00+05:30
draft: false
title: "TIL: lsof for Process Scanning and Advanced kill Command Usage"
description:
  "Today I learned how to use lsof to scan processes running in specific paths
  and discovered that the kill command accepts verbose, readable signal names
  for safer process management."
tags:
  - til
  - unix
  - process-management
  - system-administration
  - debugging
  - lsof
---

Today I discovered powerful Unix tools for process investigation and management
that make system debugging much more efficient and safer.

## Using lsof to Scan Processes by Path

The `lsof` (list open files) command can identify processes that are using files
in a specific directory path, which is invaluable for debugging and system
maintenance.

### Basic lsof Path Scanning:

#### **Find Processes Using a Directory:**

```bash
# See all processes accessing files in /var/log
lsof +D /var/log

# More efficient for large directories (doesn't recurse)
lsof +d /var/log

# Find processes with files open in current directory
lsof +d .

# Find processes using any files under /home/user
lsof +D /home/user
```

#### **Practical Use Cases:**

```bash
# Before unmounting a filesystem
lsof +D /mnt/external-drive

# Debug why a directory can't be deleted
lsof +D /tmp/app-cache

# Find processes preventing package updates
lsof +D /usr/lib/myapp

# Identify processes holding log files open
lsof +D /var/log/myapp
```

### Advanced lsof Usage:

#### **Combine with Other Filters:**

```bash
# Processes in path owned by specific user
lsof +D /home/user -u user

# Network connections from processes in specific path
lsof +D /opt/myapp -i

# Find processes with deleted files still open
lsof +D /var/lib/myapp | grep '(deleted)'

# Monitor real-time file access
lsof +D /var/log -r 2  # refresh every 2 seconds
```

#### **Output Interpretation:**

```bash
# lsof output columns explained
$ lsof +d /tmp
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
chrome   1234 user   15u   REG    8,1    12345  67890 /tmp/temp_file
```

- **COMMAND**: Process name
- **PID**: Process ID
- **USER**: Process owner
- **FD**: File descriptor (15u = file descriptor 15, read/write)
- **TYPE**: File type (REG = regular file, DIR = directory)
- **DEVICE**: Device identifier
- **SIZE/OFF**: File size or offset
- **NODE**: Inode number
- **NAME**: Full path to file

### Troubleshooting Scenarios:

#### **"Device or resource busy" Errors:**

```bash
# Can't unmount filesystem
umount: /mnt/data: device is busy.

# Find the culprit
lsof +D /mnt/data
# Shows processes still accessing files on the mounted filesystem

# Alternative approach
fuser -v /mnt/data  # Shows processes using the mount point
```

#### **Disk Space Issues:**

```bash
# Find processes with large deleted files still open
lsof +D /var/log | grep deleted | sort -k7 -nr

# Find processes writing to a specific directory
lsof +D /var/log -a -w  # -a = AND, -w = write access only
```

## Advanced kill Command with Verbose Signals

The `kill` command accepts human-readable signal names, making process
management safer and more self-documenting.

### Verbose Signal Usage:

#### **Common Readable Signals:**

```bash
# Graceful termination (allows cleanup)
kill -TERM 1234
kill -SIGTERM 1234

# Force termination (immediate, no cleanup)
kill -KILL 1234
kill -SIGKILL 1234

# Stop/pause process (can be resumed)
kill -STOP 1234
kill -TSTP 1234   # Terminal stop (Ctrl+Z equivalent)

# Resume stopped process
kill -CONT 1234
kill -SIGCONT 1234

# Reload configuration (common in daemons)
kill -HUP 1234
kill -SIGHUP 1234
```

#### **Advanced Signal Management:**

```bash
# Check if process is running (signal 0 doesn't affect process)
if kill -0 1234 2>/dev/null; then
    echo "Process 1234 is running"
else
    echo "Process 1234 is not running"
fi

# Graceful restart script
graceful_restart() {
    local pid=$1

    echo "Sending TERM signal to process $pid"
    kill -TERM $pid

    # Wait up to 10 seconds for graceful shutdown
    for i in {1..10}; do
        if ! kill -0 $pid 2>/dev/null; then
            echo "Process terminated gracefully"
            return 0
        fi
        sleep 1
    done

    echo "Process didn't terminate gracefully, forcing..."
    kill -KILL $pid
}
```

### Combining lsof and kill:

#### **Advanced Process Management:**

```bash
# Kill all processes using files in a directory
lsof +D /path/to/app | awk 'NR>1 {print $2}' | sort -u | xargs kill -TERM

# More precise version with error handling
kill_processes_in_path() {
    local path=$1
    local signal=${2:-TERM}

    echo "Finding processes using files in $path"
    local pids=$(lsof +D "$path" 2>/dev/null | awk 'NR>1 {print $2}' | sort -u)

    if [ -z "$pids" ]; then
        echo "No processes found using files in $path"
        return 0
    fi

    echo "Found processes: $pids"
    echo "Sending $signal signal..."

    for pid in $pids; do
        if kill -0 "$pid" 2>/dev/null; then
            echo "Killing process $pid"
            kill -"$signal" "$pid"
        fi
    done
}

# Usage
kill_processes_in_path /opt/myapp TERM
```

#### **Service Management Patterns:**

```bash
# Safe service restart
restart_service() {
    local service_path=$1

    # Find main process
    local main_pid=$(pgrep -f "$service_path/bin/main")

    if [ -n "$main_pid" ]; then
        echo "Stopping service (PID: $main_pid)"
        kill -TERM "$main_pid"

        # Wait and verify
        sleep 5
        if kill -0 "$main_pid" 2>/dev/null; then
            echo "Service didn't stop gracefully, forcing..."
            kill -KILL "$main_pid"
        fi
    fi

    # Clean up any remaining processes
    lsof +D "$service_path" | awk 'NR>1 {print $2}' | sort -u | while read pid; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "Cleaning up remaining process: $pid"
            kill -TERM "$pid"
        fi
    done
}
```

These tools provide powerful capabilities for system administration, debugging,
and process management, making it easier to understand what processes are doing
and manage them safely.
