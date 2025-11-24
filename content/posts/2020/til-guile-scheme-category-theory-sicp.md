---
date: 2020-08-11T10:00:00+05:30
draft: false
title:
  "TIL: Guile Scheme Compiler, Category Theory for Programmers, SICP, and Linux
  Process Tracking"
description:
  "Today I learned about the Guile Scheme baseline compiler, Bartosz Milewski's
  Category Theory for Programmers, the classic SICP book, and the challenges of
  tracking running processes on Linux systems."
tags:
  - til
  - scheme
  - lisp
  - category-theory
  - functional-programming
  - linux
  - system-programming
  - computer-science
---

Today's learning spanned from advanced programming language theory to practical
Linux system administration challenges.

## Guile Scheme Baseline Compiler

[A Baseline Compiler for Guile](https://wingolog.org/archives/2020/06/03/a-baseline-compiler-for-guile)
describes modern compiler development for the GNU Guile Scheme implementation:

### Compiler Architecture:

#### **Traditional Guile Compilation Pipeline:**

```scheme
;; Guile's traditional approach
Source Code → Tree-IL → CPS → Bytecode → VM

;; New baseline compiler approach
Source Code → Tree-IL → Direct Machine Code
```

#### **Baseline Compiler Benefits:**

```scheme
;; Traditional interpreted execution
(define (fibonacci n)
  (if (<= n 1)
      n
      (+ (fibonacci (- n 1))
         (fibonacci (- n 2)))))

;; With baseline compiler:
;; - Faster startup (no CPS conversion)
;; - Better debugging (clearer stack traces)
;; - Incremental optimization opportunity
;; - Reduced memory pressure
```

#### **Implementation Strategy:**

```scheme
;; Compiler generates direct assembly
(define-compiler-pass (compile-application app)
  (match app
    [($ <application> src proc args)
     (let* ([proc-code (compile-expr proc)]
            [args-code (map compile-expr args)]
            [argc (length args)])
       `(begin
          ,@proc-code
          ,@(append-map (lambda (arg) arg) args-code)
          (call-with-argc ,argc)))]))

;; Register allocation and stack management
(define (allocate-registers exprs)
  (fold (lambda (expr regs)
          (assign-registers expr regs))
        (make-register-set)
        exprs))
```

### Performance Implications:

#### **Startup Time Optimization:**

- **Reduced compilation phases**: Direct translation without intermediate
  representations
- **Lazy optimization**: Optimize hot paths after profiling
- **Incremental compilation**: Compile functions as needed
- **Better caching**: Store compiled code for reuse

#### **Runtime Characteristics:**

- **Predictable performance**: Consistent execution patterns
- **Debugging support**: Maintain source location information
- **Memory efficiency**: Reduced intermediate data structures
- **Interoperability**: Better C foreign function interface

## Category Theory for Programmers

[Bartosz Milewski's Category Theory for Programmers](https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/)
bridges mathematical concepts with practical programming:

### Core Category Theory Concepts:

#### **Categories and Morphisms:**

```haskell
-- Category consists of objects and morphisms (arrows)
-- In programming: types are objects, functions are morphisms

-- Identity morphism
id :: a -> a
id x = x

-- Composition of morphisms
compose :: (b -> c) -> (a -> b) -> (a -> c)
compose g f = \x -> g (f x)

-- Composition is associative
-- compose h (compose g f) = compose (compose h g) f
```

#### **Functors:**

```haskell
-- Functor maps between categories
class Functor f where
    fmap :: (a -> b) -> f a -> f b

-- Functor laws:
-- fmap id = id
-- fmap (g . f) = fmap g . fmap f

-- Examples of functors
instance Functor [] where
    fmap = map

instance Functor Maybe where
    fmap _ Nothing = Nothing
    fmap f (Just x) = Just (f x)

-- Using functors
numbers = [1, 2, 3, 4]
squared = fmap (^2) numbers  -- [1, 4, 9, 16]

maybeValue = Just 42
doubled = fmap (*2) maybeValue  -- Just 84
```

#### **Natural Transformations:**

```haskell
-- Natural transformation between functors
-- Safe head function using Maybe
safeHead :: [a] -> Maybe a
safeHead [] = Nothing
safeHead (x:_) = Just x

-- Length is a natural transformation from [] to Const Int
length :: [a] -> Int
-- Satisfies: length . fmap f = length (naturality condition)
```

#### **Monads:**

```haskell
-- Monad as a category theory concept
class Functor m => Monad m where
    return :: a -> m a     -- Unit natural transformation
    (>>=) :: m a -> (a -> m b) -> m b  -- Multiplication

-- Monad laws (category theory requirements):
-- Left identity: return a >>= f = f a
-- Right identity: m >>= return = m
-- Associativity: (m >>= f) >>= g = m >>= (\x -> f x >>= g)

-- IO Monad example
greetUser :: IO ()
greetUser = do
    putStrLn "What's your name?"
    name <- getLine
    putStrLn ("Hello, " ++ name)

-- Desugared version
greetUser' =
    putStrLn "What's your name?" >>= \_ ->
    getLine >>= \name ->
    putStrLn ("Hello, " ++ name)
```

#### **Kleisli Categories:**

```haskell
-- Kleisli category for a monad
-- Objects: same as base category
-- Morphisms: a -> m b (where m is a monad)

-- Kleisli composition
(>=>) :: Monad m => (a -> m b) -> (b -> m c) -> (a -> m c)
f >=> g = \x -> f x >>= g

-- Example: composing functions that might fail
safeDivide :: Double -> Double -> Maybe Double
safeDivide _ 0 = Nothing
safeDivide x y = Just (x / y)

safeSquareRoot :: Double -> Maybe Double
safeSquareRoot x
    | x < 0 = Nothing
    | otherwise = Just (sqrt x)

-- Kleisli composition
safeComputation :: Double -> Double -> Maybe Double
safeComputation x y = safeDivide x y >=> safeSquareRoot
```

## Structure and Interpretation of Computer Programs

[SICP](https://sarabander.github.io/sicp/html/index.xhtml) remains one of the
most influential computer science textbooks:

### Core SICP Principles:

#### **Abstraction and Modularity:**

```scheme
;; Building abstractions with procedures
(define (square x) (* x x))

(define (sum-of-squares x y)
  (+ (square x) (square y)))

;; Higher-order procedures
(define (sum term a next b)
  (if (> a b)
      0
      (+ (term a)
         (sum term (next a) next b))))

;; Using higher-order procedures
(define (sum-cubes a b)
  (sum (lambda (x) (* x x x))
       a
       (lambda (x) (+ x 1))
       b))

(define (pi-sum a b)
  (define (pi-term x)
    (/ 1.0 (* x (+ x 2))))
  (define (pi-next x)
    (+ x 4))
  (sum pi-term a pi-next b))
```

#### **Data Abstraction:**

```scheme
;; Abstract data types
(define (make-rat n d)
  (let ((g (gcd n d)))
    (cons (/ n g) (/ d g))))

(define (numer x) (car x))
(define (denom x) (cdr x))

(define (add-rat x y)
  (make-rat (+ (* (numer x) (denom y))
               (* (numer y) (denom x)))
            (* (denom x) (denom y))))

;; Using rational numbers
(define one-half (make-rat 1 2))
(define one-third (make-rat 1 3))
(define sum (add-rat one-half one-third))  ; 5/6
```

#### **Metalinguistic Abstraction:**

```scheme
;; Metacircular evaluator - Scheme interpreter in Scheme
(define (eval exp env)
  (cond ((self-evaluating? exp) exp)
        ((variable? exp) (lookup-variable-value exp env))
        ((quoted? exp) (text-of-quotation exp))
        ((assignment? exp) (eval-assignment exp env))
        ((definition? exp) (eval-definition exp env))
        ((if? exp) (eval-if exp env))
        ((lambda? exp) (make-procedure (lambda-parameters exp)
                                       (lambda-body exp)
                                       env))
        ((begin? exp) (eval-sequence (begin-actions exp) env))
        ((cond? exp) (eval (cond->if exp) env))
        ((application? exp)
         (apply (eval (operator exp) env)
                (list-of-values (operands exp) env)))))

(define (apply procedure arguments)
  (cond ((primitive-procedure? procedure)
         (apply-primitive-procedure procedure arguments))
        ((compound-procedure? procedure)
         (eval-sequence
           (procedure-body procedure)
           (extend-environment
             (procedure-parameters procedure)
             arguments
             (procedure-environment procedure))))))
```

## Linux Process Tracking Challenges

[The Difficulties of Tracking Running Processes on Linux](https://natanyellin.com/posts/tracking-running-processes-on-linux/)
explores the complexities of process monitoring:

### Process Tracking Methods:

#### **/proc Filesystem Monitoring:**

```bash
# Basic process information
cat /proc/PID/stat    # Process statistics
cat /proc/PID/status  # Human-readable status
cat /proc/PID/cmdline # Command line that started process
cat /proc/PID/environ # Environment variables

# Process tree relationships
cat /proc/PID/task/   # Thread information
ls /proc/PID/fd/      # Open file descriptors
```

#### **Race Conditions in Process Monitoring:**

```python
import os
import time
from pathlib import Path

def monitor_process_safely(pid):
    """Handle race conditions when monitoring processes"""
    try:
        # Check if process exists
        proc_path = Path(f"/proc/{pid}")
        if not proc_path.exists():
            return None

        # Read multiple files atomically (as much as possible)
        stat_path = proc_path / "stat"
        status_path = proc_path / "status"

        # Race condition: process might disappear between checks
        with stat_path.open() as f:
            stat_data = f.read().strip()

        # Process might have been replaced by another with same PID
        with status_path.open() as f:
            status_data = f.read()

        return {
            'stat': stat_data,
            'status': status_data,
            'timestamp': time.time()
        }

    except (FileNotFoundError, ProcessLookupError, PermissionError):
        # Process disappeared or access denied
        return None

# Handle PID reuse
def track_process_with_start_time(pid):
    """Use start time to identify unique process instances"""
    try:
        with open(f"/proc/{pid}/stat") as f:
            fields = f.read().split()
            start_time = int(fields[21])  # Process start time

        return {
            'pid': pid,
            'start_time': start_time,
            'unique_id': f"{pid}_{start_time}"
        }
    except (FileNotFoundError, IndexError):
        return None
```

#### **System-Level Process Monitoring:**

```bash
# Process accounting (if enabled)
sudo apt-get install acct
sudo accton /var/log/wtmp

# Monitor process creation/termination
lastcomm | head -10

# Real-time process monitoring
# Using bpftrace (eBPF)
sudo bpftrace -e '
tracepoint:syscalls:sys_enter_execve {
    printf("PID %d exec: %s\n", pid, str(args->filename));
}

tracepoint:syscalls:sys_enter_exit_group {
    printf("PID %d exit\n", pid);
}'

# Using perf events
sudo perf record -e sched:sched_process_exec,sched:sched_process_exit -a sleep 10
sudo perf script
```

#### **Advanced Monitoring Challenges:**

```python
# Container process monitoring
def monitor_container_processes(container_id):
    """Monitor processes inside containers"""
    try:
        # Find container's PID namespace
        with open(f"/sys/fs/cgroup/memory/docker/{container_id}/cgroup.procs") as f:
            container_pids = [int(line.strip()) for line in f if line.strip()]

        processes = []
        for pid in container_pids:
            try:
                with open(f"/proc/{pid}/stat") as f:
                    stat_data = f.read().split()
                    processes.append({
                        'pid': pid,
                        'name': stat_data[1].strip('()'),
                        'state': stat_data[2],
                        'ppid': int(stat_data[3])
                    })
            except FileNotFoundError:
                continue  # Process disappeared

        return processes
    except FileNotFoundError:
        return []  # Container not found
```

### Monitoring Tools Comparison:

#### **User-space vs Kernel-space Monitoring:**

- **ps/top**: Snapshots with race conditions
- **htop**: Better real-time display but still snapshots
- **eBPF/BPF**: Kernel-level monitoring with lower overhead
- **ftrace**: Kernel function tracing
- **perf**: Hardware and software event monitoring

These topics demonstrate the depth of computer science knowledge, from
theoretical foundations in category theory and language design to practical
challenges in system programming and process monitoring.
