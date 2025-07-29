---
date: 2020-08-05T10:00:00+05:30
draft: false
title: "TIL: Python's raise from Statement, Grub Customization, Liquorix Kernel, and Hardware Benchmarking"
description: "Today I learned about Python's raise from clause for exception chaining, customizing the Grub bootloader, the Liquorix kernel for desktop performance, and comprehensive hardware benchmarking with Phoronix Test Suite."
tags:
  - til
  - python
  - exceptions
  - linux
  - grub
  - kernel
  - benchmarking
  - system-administration
---

Today's discoveries spanned from Python exception handling best practices to Linux system customization and performance optimization.

## Python's raise from Statement

[Python's raise statement with from clause](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement) enables proper exception chaining to preserve full tracebacks:

### Exception Chaining Fundamentals:

#### **Basic raise from Usage:**
```python
def process_file(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data['required_field']
    except FileNotFoundError as e:
        raise ValueError(f"Configuration file {filename} not found") from e
    except KeyError as e:
        raise ValueError(f"Missing required field in {filename}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filename}") from e

# Usage example
try:
    config = process_file('config.json')
except ValueError as e:
    print(f"Error: {e}")
    print(f"Original cause: {e.__cause__}")
    print(f"Full traceback includes both exceptions")
```

#### **Suppressing Exception Context:**
```python
def clean_error_without_context():
    try:
        risky_operation()
    except InternalError:
        # Suppress the original exception from traceback
        raise UserFriendlyError("Operation failed") from None

def clean_error_with_context():
    try:
        risky_operation()
    except InternalError as e:
        # Preserve original exception for debugging
        raise UserFriendlyError("Operation failed") from e
```

#### **Advanced Exception Chaining Patterns:**
```python
import logging
from contextlib import contextmanager

class DatabaseError(Exception):
    """Custom exception with enhanced context"""
    def __init__(self, message, query=None, params=None):
        super().__init__(message)
        self.query = query
        self.params = params

@contextmanager
def database_transaction():
    """Context manager with proper exception handling"""
    connection = None
    try:
        connection = get_database_connection()
        connection.begin()
        yield connection
        connection.commit()
    except DatabaseConnectionError as e:
        if connection:
            connection.rollback()
        raise DatabaseError("Transaction failed - connection issue") from e
    except DatabaseQueryError as e:
        if connection:
            connection.rollback()
        raise DatabaseError(
            "Transaction failed - query error",
            query=e.query,
            params=e.params
        ) from e
    finally:
        if connection:
            connection.close()

# Usage with comprehensive error handling
def update_user_profile(user_id, profile_data):
    try:
        with database_transaction() as db:
            # Multiple operations that might fail
            user = db.get_user(user_id)
            if not user:
                raise UserNotFoundError(f"User {user_id} not found")
            
            validate_profile_data(profile_data)
            db.update_user_profile(user_id, profile_data)
            db.log_user_activity(user_id, "profile_updated")
            
    except UserNotFoundError:
        # Re-raise without chaining - this is the root cause
        raise
    except ValidationError as e:
        raise ProfileUpdateError("Invalid profile data") from e
    except DatabaseError as e:
        logging.error(f"Database error updating user {user_id}: {e.__cause__}")
        raise ProfileUpdateError("Failed to update profile") from e
```

#### **Exception Chaining Best Practices:**
```python
def api_request_with_retries(url, max_retries=3):
    """Example showing when to chain vs when not to chain"""
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.ConnectionError as e:
            last_exception = e
            if attempt == max_retries - 1:
                # Chain the last connection error
                raise APIConnectionError(
                    f"Failed to connect to {url} after {max_retries} attempts"
                ) from e
            time.sleep(2 ** attempt)  # Exponential backoff
            
        except requests.HTTPError as e:
            # Don't retry on HTTP errors - raise immediately with context
            raise APIHttpError(
                f"HTTP {e.response.status_code}: {e.response.reason}"
            ) from e
            
        except requests.Timeout as e:
            last_exception = e
            if attempt == max_retries - 1:
                raise APITimeoutError(
                    f"Request to {url} timed out after {max_retries} attempts"
                ) from e
            time.sleep(1)
```

## Grub Bootloader Customization

[Grub Customizer](https://itsfoss.com/grub-customizer-ubuntu/) provides a GUI tool for customizing the GRUB bootloader:

### Grub Configuration Methods:

#### **Manual Configuration:**
```bash
# Edit GRUB configuration
sudo nano /etc/default/grub

# Common customizations
GRUB_DEFAULT=0                    # Default menu entry
GRUB_TIMEOUT=10                   # Menu timeout in seconds
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"  # Kernel parameters
GRUB_CMDLINE_LINUX=""
GRUB_GFXMODE=1920x1080           # Screen resolution
GRUB_BACKGROUND="/path/to/image.jpg"  # Custom background

# Apply changes
sudo update-grub
```

#### **Advanced Grub Customization:**
```bash
# Custom menu entries
sudo nano /etc/grub.d/40_custom

# Add custom entry
menuentry "Ubuntu Safe Mode" {
    set root='hd0,gpt2'
    linux /vmlinuz root=/dev/sda2 ro recovery nomodeset
    initrd /initrd.img
}

menuentry "Memory Test" {
    set root='hd0,gpt1'
    linux16 /memtest86+.bin
}

# Custom theme installation
sudo mkdir -p /boot/grub/themes/mytheme
sudo cp -r mytheme/* /boot/grub/themes/mytheme/

# Enable theme in /etc/default/grub
GRUB_THEME="/boot/grub/themes/mytheme/theme.txt"
```

#### **Grub Rescue Operations:**
```bash
# Boot repair from live USB
sudo add-apt-repository ppa:yannubuntu/boot-repair
sudo apt update
sudo apt install boot-repair
sudo boot-repair

# Manual GRUB reinstallation
sudo mount /dev/sda2 /mnt  # Root partition
sudo mount /dev/sda1 /mnt/boot/efi  # EFI partition
sudo grub-install --target=x86_64-efi --efi-directory=/mnt/boot/efi --bootloader-id=ubuntu /dev/sda
sudo update-grub
```

## Liquorix Kernel for Desktop Performance

[Liquorix Kernel](https://liquorix.net/) provides optimized kernel builds for desktop and multimedia workloads:

### Liquorix Features:

#### **Performance Optimizations:**
- **MuQSS Scheduler**: Better interactive performance than CFS
- **Low latency**: Optimized for real-time audio/video work
- **Desktop responsiveness**: Reduced input lag and smoother UI
- **Gaming optimizations**: Better frame time consistency

#### **Installation:**
```bash
# Add Liquorix repository
curl -s 'https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x9ae4078033f8024d' | sudo apt-key add -
echo "deb http://liquorix.net/debian sid main" | sudo tee /etc/apt/sources.list.d/liquorix.list

# Install Liquorix kernel
sudo apt update
sudo apt install linux-image-liquorix-amd64 linux-headers-liquorix-amd64

# Reboot and select Liquorix kernel from GRUB menu
```

#### **Kernel Comparison:**
```bash
# Check current kernel
uname -r

# Compare different kernels
# Standard Ubuntu kernel: 5.4.0-generic
# Liquorix kernel: 5.4-liquorix-amd64
# XanMod kernel: 5.4.0-xanmod1

# Performance testing
# Audio latency test
sudo apt install rt-tests
cyclictest -t1 -p 80 -n -i 500 -l 100000

# System responsiveness
time (dd if=/dev/zero of=/tmp/test bs=1M count=1000; sync)
```

## Phoronix Test Suite - Hardware Benchmarking

[Phoronix Test Suite](https://www.phoronix-test-suite.com/) provides comprehensive open-source benchmarking tools:

### Benchmarking Capabilities:

#### **Installation and Basic Usage:**
```bash
# Install Phoronix Test Suite
sudo apt install phoronix-test-suite

# List available tests
phoronix-test-suite list-available-tests

# System information
phoronix-test-suite system-info

# Hardware detection
phoronix-test-suite detailed-system-info
```

#### **CPU Benchmarking:**
```bash
# CPU-intensive benchmarks
phoronix-test-suite install pts/compress-7zip
phoronix-test-suite run pts/compress-7zip

# Multi-threaded compilation test
phoronix-test-suite install pts/build-linux-kernel
phoronix-test-suite run pts/build-linux-kernel

# Encryption performance
phoronix-test-suite install pts/openssl
phoronix-test-suite run pts/openssl
```

#### **GPU and Graphics Benchmarking:**
```bash
# OpenGL performance
phoronix-test-suite install pts/unigine-valley
phoronix-test-suite run pts/unigine-valley

# Vulkan benchmarks
phoronix-test-suite install pts/vkmark
phoronix-test-suite run pts/vkmark

# GPU compute
phoronix-test-suite install pts/luxcorerender
phoronix-test-suite run pts/luxcorerender
```

#### **Automated Test Suites:**
```bash
# Comprehensive system test
phoronix-test-suite install pts/desktop
phoronix-test-suite run pts/desktop

# Server benchmarks
phoronix-test-suite install pts/server
phoronix-test-suite run pts/server

# Custom test suite
phoronix-test-suite build-suite

# Batch testing with results upload
phoronix-test-suite batch-setup
phoronix-test-suite batch-run pts/desktop
phoronix-test-suite upload-result
```

#### **Results Analysis:**
```bash
# View test results
phoronix-test-suite list-saved-results
phoronix-test-suite show-result [result-name]

# Compare results
phoronix-test-suite merge-results result1 result2
phoronix-test-suite compare-results-to-baseline result1 baseline

# Generate reports
phoronix-test-suite result-file-to-pdf result1
phoronix-test-suite result-file-to-csv result1
```

### Multiple Kernel Testing:

```bash
# Automated kernel comparison script
#!/bin/bash
KERNELS=("5.4.0-generic" "5.4-liquorix" "5.4.0-xanmod1")
TESTS=("pts/compress-7zip" "pts/openssl" "pts/build-linux-kernel")

for kernel in "${KERNELS[@]}"; do
    echo "Testing kernel: $kernel"
    # Boot into specific kernel (manual step)
    # Then run benchmarks
    for test in "${TESTS[@]}"; do
        phoronix-test-suite run $test
        mv ~/.phoronix-test-suite/test-results/* "./results-$kernel-$(basename $test)/"
    done
done

# Generate comparison report
phoronix-test-suite merge-results results-*
```

These tools and techniques provide comprehensive approaches to Python error handling, Linux system customization, and performance analysis - essential skills for effective software development and system administration.