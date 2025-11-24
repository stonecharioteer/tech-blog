---
date: 2021-01-06T10:00:00+05:30
draft: false
title:
  "TIL: Rust Design Patterns, Operating Systems Three Easy Pieces, and MIT
  Performance Engineering"
description:
  "Today I learned about the comprehensive Rust Design Patterns book, the
  excellent OSTEP operating systems textbook, MIT's performance engineering
  course, and other valuable computer science learning resources."
tags:
  - TIL
  - Rust
  - Design Patterns
  - Operating Systems
  - Performance Engineering
  - Computer Science
  - Education
---

## Rust Design Patterns

[Introduction - Rust Design Patterns](https://rust-unofficial.github.io/patterns/)

Comprehensive guide to idiomatic Rust programming patterns:

### Why Rust Design Patterns Matter:

- **Ownership-Aware Patterns**: Traditional patterns adapted for Rust's
  ownership system
- **Memory Safety**: Patterns that leverage Rust's guarantees
- **Performance**: Zero-cost abstractions and efficient implementations
- **Ergonomics**: Patterns that make Rust code more readable and maintainable

### Core Pattern Categories:

#### **Creational Patterns:**

**Builder Pattern in Rust:**

```rust
struct Config {
    debug: bool,
    log_level: String,
    max_connections: u32,
}

struct ConfigBuilder {
    debug: Option<bool>,
    log_level: Option<String>,
    max_connections: Option<u32>,
}

impl ConfigBuilder {
    fn new() -> Self {
        ConfigBuilder {
            debug: None,
            log_level: None,
            max_connections: None,
        }
    }

    fn debug(mut self, debug: bool) -> Self {
        self.debug = Some(debug);
        self
    }

    fn log_level(mut self, level: impl Into<String>) -> Self {
        self.log_level = Some(level.into());
        self
    }

    fn max_connections(mut self, max: u32) -> Self {
        self.max_connections = Some(max);
        self
    }

    fn build(self) -> Result<Config, &'static str> {
        Ok(Config {
            debug: self.debug.unwrap_or(false),
            log_level: self.log_level.unwrap_or_else(|| "info".to_string()),
            max_connections: self.max_connections.unwrap_or(100),
        })
    }
}

// Usage
let config = ConfigBuilder::new()
    .debug(true)
    .log_level("debug")
    .max_connections(1000)
    .build()?;
```

#### **Behavioral Patterns:**

**Strategy Pattern with Traits:**

```rust
trait CompressionStrategy {
    fn compress(&self, data: &[u8]) -> Vec<u8>;
    fn decompress(&self, data: &[u8]) -> Vec<u8>;
}

struct GzipCompression;
struct BrotliCompression;

impl CompressionStrategy for GzipCompression {
    fn compress(&self, data: &[u8]) -> Vec<u8> {
        // Gzip compression implementation
        todo!()
    }

    fn decompress(&self, data: &[u8]) -> Vec<u8> {
        // Gzip decompression implementation
        todo!()
    }
}

impl CompressionStrategy for BrotliCompression {
    fn compress(&self, data: &[u8]) -> Vec<u8> {
        // Brotli compression implementation
        todo!()
    }

    fn decompress(&self, data: &[u8]) -> Vec<u8> {
        // Brotli decompression implementation
        todo!()
    }
}

struct FileProcessor {
    compression: Box<dyn CompressionStrategy>,
}

impl FileProcessor {
    fn new(compression: Box<dyn CompressionStrategy>) -> Self {
        FileProcessor { compression }
    }

    fn process_file(&self, data: &[u8]) -> Vec<u8> {
        self.compression.compress(data)
    }
}
```

### Rust-Specific Patterns:

#### **RAII (Resource Acquisition Is Initialization):**

```rust
use std::fs::File;
use std::io::prelude::*;

struct FileHandler {
    file: File,
}

impl FileHandler {
    fn new(path: &str) -> std::io::Result<Self> {
        let file = File::create(path)?;
        Ok(FileHandler { file })
    }

    fn write_data(&mut self, data: &str) -> std::io::Result<()> {
        self.file.write_all(data.as_bytes())
    }
}

impl Drop for FileHandler {
    fn drop(&mut self) {
        // File automatically closed when FileHandler goes out of scope
        println!("File handler cleaned up");
    }
}

// Usage - automatic cleanup guaranteed
fn write_config() -> std::io::Result<()> {
    let mut handler = FileHandler::new("config.txt")?;
    handler.write_data("debug=true\n")?;
    // File automatically closed here
    Ok(())
}
```

#### **Newtype Pattern:**

```rust
struct UserId(u64);
struct PostId(u64);

impl UserId {
    fn new(id: u64) -> Self {
        UserId(id)
    }

    fn as_u64(&self) -> u64 {
        self.0
    }
}

// Type safety prevents mixing up IDs
fn get_user_posts(user_id: UserId, post_id: PostId) -> Vec<String> {
    // Can't accidentally pass PostId where UserId is expected
    todo!()
}
```

#### **Error Handling Patterns:**

```rust
use std::error::Error;
use std::fmt;

#[derive(Debug)]
enum DatabaseError {
    ConnectionFailed(String),
    QueryFailed(String),
    InvalidData(String),
}

impl fmt::Display for DatabaseError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            DatabaseError::ConnectionFailed(msg) => write!(f, "Connection failed: {}", msg),
            DatabaseError::QueryFailed(msg) => write!(f, "Query failed: {}", msg),
            DatabaseError::InvalidData(msg) => write!(f, "Invalid data: {}", msg),
        }
    }
}

impl Error for DatabaseError {}

type DatabaseResult<T> = Result<T, DatabaseError>;

fn fetch_user(id: u64) -> DatabaseResult<User> {
    // Implementation that can return specific error types
    todo!()
}
```

## Operating Systems: Three Easy Pieces (OSTEP)

[Operating Systems: Three Easy Pieces](http://pages.cs.wisc.edu/~remzi/OSTEP/)

Outstanding free textbook covering operating system fundamentals:

### The "Three Easy Pieces":

#### **1. Virtualization:**

- **CPU Virtualization**: How OS creates illusion of many CPUs
- **Memory Virtualization**: Virtual memory and address spaces
- **Process Management**: Process creation, scheduling, and switching

**Key Concepts:**

```c
// Process creation example
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        printf("Hello from child process\n");
        execvp("ls", (char *[]){"ls", "-l", NULL});
    } else if (pid > 0) {
        // Parent process
        printf("Hello from parent process\n");
        wait(NULL);  // Wait for child to complete
    } else {
        // Fork failed
        perror("fork failed");
    }

    return 0;
}
```

#### **2. Concurrency:**

- **Threads**: Lightweight processes sharing address space
- **Synchronization**: Locks, condition variables, semaphores
- **Common Problems**: Race conditions, deadlocks, starvation

**Thread Synchronization:**

```c
#include <pthread.h>
#include <stdio.h>

int counter = 0;
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *worker(void *arg) {
    for (int i = 0; i < 100000; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;

    pthread_create(&t1, NULL, worker, NULL);
    pthread_create(&t2, NULL, worker, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Final counter value: %d\n", counter);
    return 0;
}
```

#### **3. Persistence:**

- **File Systems**: Storage organization and management
- **I/O Devices**: Hard drives, SSDs, and device interfaces
- **Crash Consistency**: Ensuring data integrity across failures

### Learning Approach:

- **Practical Examples**: Real code demonstrations
- **Simulation**: Provided simulators for key concepts
- **Homework**: Hands-on programming assignments
- **Historical Context**: Evolution of OS concepts

## MIT Performance Engineering Course

[Performance Engineering of Software Systems | MIT OCW](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-172-performance-engineering-of-software-systems-fall-2018/)

Comprehensive course on making software fast:

### Course Philosophy:

- **Performance Matters**: Speed affects user experience and costs
- **Systematic Approach**: Methodical performance optimization
- **Measurement-Driven**: Profile before optimizing
- **Real-World Focus**: Practical techniques used in industry

### Key Topics Covered:

#### **Performance Analysis:**

```bash
# Profiling with perf
perf record ./my_program
perf report

# Memory profiling with valgrind
valgrind --tool=cachegrind ./my_program
valgrind --tool=massif ./my_program

# CPU profiling
perf stat -e cycles,instructions,cache-misses ./my_program
```

#### **Algorithmic Optimization:**

```c
// Cache-friendly matrix multiplication
void matrix_multiply_optimized(double **A, double **B, double **C, int n) {
    int i, j, k;
    for (i = 0; i < n; i++) {
        for (k = 0; k < n; k++) {  // Note: k and j loops swapped
            for (j = 0; j < n; j++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Loop tiling for better cache usage
void matrix_multiply_tiled(double **A, double **B, double **C, int n, int tile_size) {
    for (int ii = 0; ii < n; ii += tile_size) {
        for (int jj = 0; jj < n; jj += tile_size) {
            for (int kk = 0; kk < n; kk += tile_size) {
                for (int i = ii; i < min(ii + tile_size, n); i++) {
                    for (int j = jj; j < min(jj + tile_size, n); j++) {
                        for (int k = kk; k < min(kk + tile_size, n); k++) {
                            C[i][j] += A[i][k] * B[k][j];
                        }
                    }
                }
            }
        }
    }
}
```

#### **Memory Optimization:**

- **Cache Awareness**: Understanding cache hierarchies
- **Data Structure Layout**: Structure of arrays vs array of structures
- **Memory Alignment**: Avoiding false sharing
- **NUMA Awareness**: Non-uniform memory access considerations

#### **Parallel Programming:**

```c
#include <cilk/cilk.h>

// Parallel divide-and-conquer
int parallel_sum(int *arr, int n) {
    if (n <= 1000) {
        // Base case: sequential sum
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += arr[i];
        }
        return sum;
    }

    int mid = n / 2;
    int left_sum = cilk_spawn parallel_sum(arr, mid);
    int right_sum = parallel_sum(arr + mid, n - mid);
    cilk_sync;

    return left_sum + right_sum;
}
```

### Performance Engineering Principles:

#### **Measurement and Profiling:**

1. **Profile First**: Don't guess where bottlenecks are
2. **Microbenchmarks**: Isolate specific operations
3. **System-Level Metrics**: CPU, memory, I/O, network
4. **Statistical Significance**: Multiple runs, confidence intervals

#### **Optimization Strategies:**

1. **Algorithmic**: Better algorithms beat micro-optimizations
2. **Data Structure**: Choose appropriate data structures
3. **Compiler**: Help compiler optimize (const, restrict, inline)
4. **System**: Understand hardware and OS interactions

## Additional Learning Resources:

### Tech Interview Handbook

[Tech Interview Handbook](https://yangshun.github.io/tech-interview-handbook/)

- **Algorithm Practice**: Systematic approach to coding interviews
- **System Design**: Large-scale system architecture
- **Behavioral Questions**: Soft skills and cultural fit
- **Company-Specific**: Preparation for major tech companies

### Understanding Connections & Pools

[Understanding Connections & Pools](https://sudhir.io/understanding-connections-pools/)

- **Database Connections**: Connection lifecycle and management
- **Pool Sizing**: Optimal pool size calculation
- **Monitoring**: Connection pool health metrics
- **Best Practices**: Avoiding connection leaks and timeouts

These resources represent different aspects of becoming a proficient systems
programmer - from language-specific best practices to fundamental computer
science concepts and performance optimization techniques.
