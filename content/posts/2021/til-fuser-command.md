---
date: 2021-03-12T10:00:00+05:30
draft: false
title: "TIL: fuser Command for Process and File Investigation"
description:
  "Today I learned about the fuser command, a powerful Linux utility for
  identifying which processes are using specific files, directories, or network
  ports."
tags:
  - TIL
  - Linux
  - System Administration
  - Process Management
  - Debugging
---

## fuser - Identify Process Using Files/Ports

[fuser(1) - Linux man page](https://linux.die.net/man/1/fuser)

Essential Linux command for troubleshooting file access and network connections:

### What fuser Does:

- **File Usage**: Shows which processes are accessing specific files
- **Directory Monitoring**: Identifies processes with open files in directories
- **Network Analysis**: Finds processes using specific network ports
- **Mount Point Investigation**: Discovers what's preventing unmounting

### Basic Syntax:

```bash
fuser [options] file|directory|port
```

### Common Use Cases:

#### **File Access Investigation:**

```bash
# Show processes using a file
fuser /var/log/syslog

# Show detailed process information
fuser -v /etc/passwd

# Show processes using files in directory
fuser /home/user/
```

#### **Network Port Analysis:**

```bash
# Find process using TCP port 80
fuser 80/tcp

# Find process using UDP port 53
fuser 53/udp

# Multiple ports at once
fuser 80/tcp 443/tcp
```

#### **Mount Point Troubleshooting:**

```bash
# Why can't I unmount this drive?
fuser -m /mnt/external

# Show all processes with files open on filesystem
fuser -vm /mnt/external
```

### Output Interpretation:

#### **Access Type Indicators:**

- **c**: Current directory
- **e**: Executable being run
- **f**: Open file
- **F**: Open file for writing
- **r**: Root directory
- **m**: Memory-mapped file

#### **Example Output:**

```bash
$ fuser -v /var/log/messages
                     USER        PID ACCESS COMMAND
/var/log/messages:   root       1234 f     rsyslogd
                     root       5678 F     logrotate
```

### Powerful Options:

#### **Verbose Mode:**

```bash
# Show detailed information
fuser -v filename

# Include user names and process details
fuser -uv filename
```

#### **Kill Processes:**

```bash
# Kill all processes using file (dangerous!)
fuser -k filename

# Interactive kill with confirmation
fuser -ki filename

# Send specific signal
fuser -k -TERM filename
```

#### **Network Mode:**

```bash
# Show all network connections
fuser -n tcp port_number

# UDP connections
fuser -n udp port_number
```

### Practical Scenarios:

#### **"Device is busy" Error:**

```bash
# Can't unmount USB drive
umount /mnt/usb
# umount: /mnt/usb: device is busy

# Find the culprit
fuser -vm /mnt/usb
# Shows: bash (PID 1234) has current directory there

# Fix: change directory and unmount
cd ~
umount /mnt/usb
```

#### **Port Already in Use:**

```bash
# Development server won't start
# Error: Port 8000 already in use

# Find what's using the port
fuser 8000/tcp
# Output: 8000/tcp: 5432

# Get process details
ps aux | grep 5432
# Kill if necessary
kill 5432
```

#### **Log File Locked:**

```bash
# Can't edit log file
# Find processes with file open
fuser -v /var/log/application.log

# Safely stop services before editing
systemctl stop application
vi /var/log/application.log
```

### Security and Safety:

#### **Permission Requirements:**

- **Root Access**: Often needed for system files and other users' processes
- **Network Ports**: Some operations require elevated privileges
- **Process Inspection**: Limited to processes you own unless root

#### **Safety Considerations:**

- **Kill Command**: Use `-k` option very carefully
- **System Processes**: Don't kill critical system processes
- **Confirmation**: Use `-i` for interactive confirmation when killing

### Alternative Commands:

- **lsof**: More comprehensive file and process investigation
- **netstat**: Network connection analysis
- **ss**: Modern replacement for netstat
- **pgrep/pkill**: Process finding and killing by name

fuser is invaluable for system administration, debugging file access issues, and
understanding what processes are doing on your system.
