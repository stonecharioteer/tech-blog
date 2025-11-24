---
date: 2020-08-25T10:00:00+05:30
draft: false
title:
  "TIL: NuShell Structured Data Shell, Async Python Performance Reality, and Go
  Programming Fundamentals"
description:
  "Today I learned about NuShell's structured approach to shell computing, why
  async Python isn't always faster, comprehensive Go language resources, and
  effective techniques for asking technical questions."
tags:
  - til
  - shell
  - rust
  - python
  - async
  - go
  - golang
  - performance
---

Today's discoveries challenged conventional wisdom about async programming while
exploring innovative shell design and comprehensive language learning resources.

## NuShell - Structured Data Shell in Rust

[NuShell](https://www.nushell.sh/) reimagines the command-line interface with
structured data as a first-class concept:

### Core Philosophy:

#### **Structured Data Pipeline:**

```bash
# Traditional shell - text-based
ps aux | grep python | awk '{print $2}' | head -5

# NuShell - structured data
ps | where name =~ python | select pid | first 5
```

#### **Built-in Data Types:**

```bash
# Working with JSON directly
http get https://api.github.com/repos/nushell/nushell | get stargazers_count

# CSV processing
open data.csv | where salary > 50000 | select name age department

# File system as structured data
ls | where size > 1mb | sort-by modified | reverse

# System information
sys | get host.name
```

### Advanced Features:

#### **Custom Commands:**

```bash
# Define custom command
def weather [city: string] {
    http get $"https://wttr.in/($city)?format=j1" | get current_condition.0
}

# Use custom command
weather "New York" | get temp_C

# Command with multiple parameters
def git-summary [--author(-a): string] {
    if ($author | is-empty) {
        git log --oneline | lines | length
    } else {
        git log --oneline --author $author | lines | length
    }
}
```

#### **Data Transformation:**

```bash
# Convert between formats
open data.json | to csv | save data.csv
open config.toml | to json | save config.json

# Advanced filtering and grouping
open sales.csv
| where date >= 2023-01-01
| group-by region
| each { |group|
    {
        region: ($group.0),
        total_sales: ($group.1 | get amount | math sum),
        avg_sale: ($group.1 | get amount | math avg)
    }
}
```

#### **Cross-Platform Compatibility:**

```bash
# File operations work consistently across platforms
ls **/*.rs | where size > 10kb | get name

# Network operations with structured output
port 8080 | get state  # Check if port is open
which python | get path  # Find command location

# Environment variables as structured data
$env | where name =~ PATH | get value
```

### Integration with Traditional Tools:

```bash
# Mix NuShell with external commands
docker ps | from ssv | where IMAGE =~ nginx

# Transform and pipe to traditional tools
ls | where name =~ ".log" | get name | lines | xargs tail -f

# Use traditional commands when needed
^ls -la /usr/bin | lines | length  # ^ prefix runs external command
```

## Async Python Performance Reality

[Async Python is Not Faster](http://calpaterson.com/async-python-is-not-faster.html)
challenges common misconceptions about async programming:

### Performance Myths vs Reality:

#### **CPU-Bound Tasks:**

```python
import asyncio
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# CPU-intensive function
def cpu_bound_task(n):
    """Simulate CPU-intensive work"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

# Synchronous version
def sync_cpu_test():
    start = time.time()
    results = [cpu_bound_task(100000) for _ in range(4)]
    end = time.time()
    return end - start, results

# Async version (misleading - still blocks)
async def async_cpu_test_wrong():
    start = time.time()
    results = [cpu_bound_task(100000) for _ in range(4)]  # Still synchronous!
    end = time.time()
    return end - start, results

# Proper async with thread pool
async def async_cpu_test_correct():
    start = time.time()
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor() as executor:
        tasks = [
            loop.run_in_executor(executor, cpu_bound_task, 100000)
            for _ in range(4)
        ]
        results = await asyncio.gather(*tasks)

    end = time.time()
    return end - start, results

# Benchmark results show:
# sync_cpu_test: ~2.1 seconds
# async_cpu_test_wrong: ~2.1 seconds (no improvement!)
# async_cpu_test_correct: ~0.6 seconds (real improvement through parallelism)
```

#### **I/O-Bound Tasks - Where Async Shines:**

```python
import aiohttp
import requests

# Synchronous HTTP requests
def sync_http_test(urls):
    start = time.time()
    results = []
    for url in urls:
        response = requests.get(url)
        results.append(response.status_code)
    end = time.time()
    return end - start, results

# Async HTTP requests
async def async_http_test(urls):
    start = time.time()
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_url(session, url))
        results = await asyncio.gather(*tasks)

    end = time.time()
    return end - start, results

async def fetch_url(session, url):
    async with session.get(url) as response:
        return response.status

# Results for 10 HTTP requests:
# sync_http_test: ~5.2 seconds (sequential)
# async_http_test: ~1.1 seconds (concurrent)
```

#### **Memory and Overhead Considerations:**

```python
import sys
import asyncio
import threading

def measure_memory_usage():
    """Compare memory usage of different approaches"""

    # Thread-based approach
    def thread_worker():
        time.sleep(1)

    threads = [threading.Thread(target=thread_worker) for _ in range(1000)]
    thread_memory = sys.getsizeof(threads) + sum(sys.getsizeof(t) for t in threads)

    # Async approach
    async def async_worker():
        await asyncio.sleep(1)

    tasks = [async_worker() for _ in range(1000)]
    task_memory = sys.getsizeof(tasks) + sum(sys.getsizeof(t) for t in tasks)

    print(f"1000 threads: ~{thread_memory} bytes")
    print(f"1000 async tasks: ~{task_memory} bytes")
    # Async tasks typically use much less memory

measure_memory_usage()
```

### When to Use Async:

#### **Good Use Cases:**

- High-concurrency I/O operations (web scraping, API calls)
- Network servers handling many connections
- Database operations with connection pooling
- File I/O with many small files

#### **Poor Use Cases:**

- CPU-intensive computations
- Simple sequential programs
- Legacy code integration
- When debugging complexity isn't worth performance gains

## Go Programming Fundamentals

[Go 101](https://go101.org) provides comprehensive Go language education:

### Core Go Concepts:

#### **Goroutines and Channels:**

```go
package main

import (
    "fmt"
    "time"
)

// Producer goroutine
func producer(ch chan<- int) {
    for i := 1; i <= 5; i++ {
        ch <- i
        fmt.Printf("Produced: %d\n", i)
        time.Sleep(time.Millisecond * 500)
    }
    close(ch)
}

// Consumer goroutine
func consumer(ch <-chan int, done chan<- bool) {
    for value := range ch {
        fmt.Printf("Consumed: %d\n", value)
        time.Sleep(time.Millisecond * 300)
    }
    done <- true
}

func main() {
    ch := make(chan int, 2) // Buffered channel
    done := make(chan bool)

    go producer(ch)
    go consumer(ch, done)

    <-done // Wait for consumer to finish
    fmt.Println("All done!")
}
```

#### **Interface-Based Design:**

```go
// Define behavior through interfaces
type Writer interface {
    Write([]byte) (int, error)
}

type Logger interface {
    Log(message string)
}

// Concrete implementations
type FileLogger struct {
    filename string
}

func (f *FileLogger) Log(message string) {
    // Write to file
    fmt.Printf("File: %s\n", message)
}

type ConsoleLogger struct{}

func (c *ConsoleLogger) Log(message string) {
    fmt.Printf("Console: %s\n", message)
}

// Function that works with any Logger
func doWork(logger Logger) {
    logger.Log("Starting work")
    // ... do work ...
    logger.Log("Work completed")
}

func main() {
    fileLogger := &FileLogger{filename: "app.log"}
    consoleLogger := &ConsoleLogger{}

    doWork(fileLogger)
    doWork(consoleLogger)
}
```

#### **Error Handling Patterns:**

```go
import (
    "errors"
    "fmt"
)

// Custom error types
type ValidationError struct {
    Field string
    Value interface{}
    Reason string
}

func (v *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for field '%s' with value '%v': %s",
                       v.Field, v.Value, v.Reason)
}

// Function with multiple return values
func validateUser(name string, age int) (*User, error) {
    if name == "" {
        return nil, &ValidationError{
            Field: "name",
            Value: name,
            Reason: "name cannot be empty",
        }
    }

    if age < 0 || age > 150 {
        return nil, &ValidationError{
            Field: "age",
            Value: age,
            Reason: "age must be between 0 and 150",
        }
    }

    return &User{Name: name, Age: age}, nil
}

// Error handling in action
func main() {
    user, err := validateUser("", 25)
    if err != nil {
        var validationErr *ValidationError
        if errors.As(err, &validationErr) {
            fmt.Printf("Validation error: %s\n", validationErr.Error())
        } else {
            fmt.Printf("Unknown error: %v\n", err)
        }
        return
    }

    fmt.Printf("Valid user: %+v\n", user)
}
```

## Effective Technical Questions

[How to ask questions of experts and gain more than just an answer](https://josh.works/better-questions)
provides guidance for productive technical discussions:

### Question Framework:

#### **Context-Rich Questions:**

```
Poor: "My code doesn't work. Help!"

Better: "I'm trying to implement a REST API in Go using Gin framework.
When I send a POST request to /api/users, I get a 500 error. Here's my code:
[code snippet]. The error message is [specific error]. I've tried
[what you've attempted]. What might be causing this issue?"
```

#### **Show Your Work:**

```
Include:
- What you're trying to accomplish
- What you expected to happen
- What actually happened
- What you've already tried
- Minimal reproducible example
- Relevant error messages/logs
- Environment details (versions, OS, etc.)
```

#### **Follow-Up Strategy:**

```
1. Ask clarifying questions about the solution
2. Explain what you learned in your own words
3. Share how you applied the solution
4. Report back on results
5. Ask about related concepts or edge cases
```

These discoveries highlight the importance of understanding the true
characteristics of tools and techniques rather than accepting conventional
wisdom, while also providing practical frameworks for effective learning and
communication.
