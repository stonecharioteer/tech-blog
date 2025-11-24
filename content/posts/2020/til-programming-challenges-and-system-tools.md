---
date: 2020-07-27T18:00:00+05:30
draft: false
title: "TIL: Programming Challenges, System Tools, and Learning Resources"
description:
  "Today I learned about Advent of Code programming challenges, GPU hash tables,
  Python gotchas, Rust concurrent data structures, and various development tools
  and learning resources."
tags:
  - til
  - advent-of-code
  - rust
  - python
  - gpu-computing
  - haskell
  - programming-challenges
---

Today I discovered a wealth of programming challenges, advanced data structures,
and learning resources that span from competitive programming to systems
development and functional programming concepts.

## Programming Challenges and Competitions

### Advent of Code: Programming for Fun

[Advent of Code](https://adventofcode.com/) offers annual programming challenges
that are more engaging than typical competitive programming platforms:

```python
# Example Advent of Code 2020 Day 1: Two Sum Variant
# Find two numbers that sum to 2020 and multiply them

def solve_two_sum(numbers, target=2020):
    """Find two numbers that sum to target"""
    seen = set()

    for num in numbers:
        complement = target - num
        if complement in seen:
            return num * complement
        seen.add(num)

    return None

def solve_three_sum(numbers, target=2020):
    """Find three numbers that sum to target"""
    numbers.sort()

    for i in range(len(numbers) - 2):
        left, right = i + 1, len(numbers) - 1

        while left < right:
            current_sum = numbers[i] + numbers[left] + numbers[right]

            if current_sum == target:
                return numbers[i] * numbers[left] * numbers[right]
            elif current_sum < target:
                left += 1
            else:
                right -= 1

    return None

# Real-world application: expense tracking
def find_expense_combinations(expenses, budget):
    """Find combinations of expenses that fit within budget"""
    valid_combinations = []

    # Two expenses
    two_sum = solve_two_sum(expenses, budget)
    if two_sum:
        valid_combinations.append(("two_expenses", two_sum))

    # Three expenses
    three_sum = solve_three_sum(expenses, budget)
    if three_sum:
        valid_combinations.append(("three_expenses", three_sum))

    return valid_combinations

# Example usage
expenses = [1721, 979, 366, 299, 675, 1456]
combinations = find_expense_combinations(expenses, 2020)
print(f"Valid combinations: {combinations}")
```

{{< tip title="Advent of Code Benefits" >}} **Why Advent of Code is Superior to
LeetCode:**

- **Story-driven problems** - Each challenge has engaging narrative context
- **Progressive difficulty** - Problems get harder throughout December
- **Multiple approaches** - Usually several valid solution strategies
- **Community aspect** - Global leaderboards and solution sharing
- **Real-world applicable** - Problems often mirror actual programming scenarios
  {{< /tip >}}

### Rust Solutions and Learning

[BurntSushi's Rust Solutions to Advent of Code 2018](https://github.com/bcmyers/aoc2019)
and
[bcmyers's Rust Solutions to Advent of Code 2019](https://github.com/bcmyers/aoc2019)
provide excellent examples of idiomatic Rust:

```rust
// Example: Parsing and processing structured data (common AoC pattern)
use std::collections::HashMap;
use std::str::FromStr;

#[derive(Debug, Clone)]
struct Instruction {
    operation: String,
    argument: i32,
}

impl FromStr for Instruction {
    type Err = Box<dyn std::error::Error>;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split_whitespace().collect();
        if parts.len() != 2 {
            return Err("Invalid instruction format".into());
        }

        Ok(Instruction {
            operation: parts[0].to_string(),
            argument: parts[1].parse()?,
        })
    }
}

struct GameConsole {
    instructions: Vec<Instruction>,
    accumulator: i32,
    program_counter: usize,
    executed: HashMap<usize, bool>,
}

impl GameConsole {
    fn new(instructions: Vec<Instruction>) -> Self {
        Self {
            instructions,
            accumulator: 0,
            program_counter: 0,
            executed: HashMap::new(),
        }
    }

    fn run_until_loop(&mut self) -> Result<i32, &'static str> {
        loop {
            // Check if we've executed this instruction before (infinite loop detection)
            if self.executed.contains_key(&self.program_counter) {
                return Ok(self.accumulator);
            }

            // Check if program terminated normally
            if self.program_counter >= self.instructions.len() {
                return Ok(self.accumulator);
            }

            // Mark current instruction as executed
            self.executed.insert(self.program_counter, true);

            // Execute instruction
            let instruction = &self.instructions[self.program_counter];
            match instruction.operation.as_str() {
                "nop" => self.program_counter += 1,
                "acc" => {
                    self.accumulator += instruction.argument;
                    self.program_counter += 1;
                }
                "jmp" => {
                    self.program_counter = (self.program_counter as i32 + instruction.argument) as usize;
                }
                _ => return Err("Unknown instruction"),
            }
        }
    }
}

// Usage example
fn solve_handheld_halting(input: &str) -> Result<i32, Box<dyn std::error::Error>> {
    let instructions: Result<Vec<Instruction>, _> = input
        .lines()
        .map(|line| line.parse())
        .collect();

    let mut console = GameConsole::new(instructions?);
    Ok(console.run_until_loop()?)
}
```

## Advanced Data Structures

### GPU Hash Tables

[A GPU Hash Table](https://news.ycombinator.com/item?id=22541925) explores
parallel computing data structures:

```python
# Simulating GPU-style parallel hash table operations
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import hashlib

class ParallelHashTable:
    """Simulate GPU-style parallel hash table operations"""

    def __init__(self, size: int, num_threads: int = 4):
        self.size = size
        self.num_threads = num_threads
        self.buckets = [[] for _ in range(size)]
        self.locks = [threading.Lock() for _ in range(size)]

    def _hash(self, key: str) -> int:
        """Simple hash function"""
        return hash(key) % self.size

    def parallel_insert(self, key_value_pairs):
        """Insert multiple key-value pairs in parallel"""
        def insert_batch(batch):
            for key, value in batch:
                bucket_idx = self._hash(key)
                with self.locks[bucket_idx]:
                    # Check if key already exists
                    for i, (k, v) in enumerate(self.buckets[bucket_idx]):
                        if k == key:
                            self.buckets[bucket_idx][i] = (key, value)
                            break
                    else:
                        self.buckets[bucket_idx].append((key, value))

        # Split work among threads
        batch_size = len(key_value_pairs) // self.num_threads
        batches = [
            key_value_pairs[i:i + batch_size]
            for i in range(0, len(key_value_pairs), batch_size)
        ]

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            executor.map(insert_batch, batches)

    def parallel_lookup(self, keys):
        """Lookup multiple keys in parallel"""
        results = {}

        def lookup_batch(batch):
            batch_results = {}
            for key in batch:
                bucket_idx = self._hash(key)
                with self.locks[bucket_idx]:
                    for k, v in self.buckets[bucket_idx]:
                        if k == key:
                            batch_results[key] = v
                            break
                    else:
                        batch_results[key] = None
            return batch_results

        batch_size = len(keys) // self.num_threads
        batches = [
            keys[i:i + batch_size]
            for i in range(0, len(keys), batch_size)
        ]

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            batch_results = executor.map(lookup_batch, batches)

        for batch_result in batch_results:
            results.update(batch_result)

        return results

# GPU-style vectorized operations
def gpu_style_hash_operations():
    """Demonstrate vectorized hash operations"""
    # Generate test data
    keys = [f"key_{i}" for i in range(10000)]
    values = np.random.randint(0, 1000, 10000)

    # Vectorized hash computation
    hash_values = np.array([hash(key) % 1024 for key in keys])

    # Parallel conflict detection
    unique_hashes, inverse, counts = np.unique(hash_values, return_inverse=True, return_counts=True)
    conflicts = unique_hashes[counts > 1]

    print(f"Hash conflicts: {len(conflicts)} out of {len(unique_hashes)} buckets")

    # Simulate parallel insertion
    hash_table = ParallelHashTable(1024, num_threads=8)
    hash_table.parallel_insert(list(zip(keys, values)))

    # Parallel lookup test
    lookup_keys = keys[:1000]
    results = hash_table.parallel_lookup(lookup_keys)

    return hash_table, results

# Performance comparison
import time

def benchmark_hash_operations():
    """Compare sequential vs parallel hash operations"""
    data = [(f"key_{i}", i) for i in range(50000)]

    # Sequential
    start = time.time()
    sequential_table = {}
    for key, value in data:
        sequential_table[key] = value
    sequential_time = time.time() - start

    # Parallel
    start = time.time()
    parallel_table = ParallelHashTable(1024, num_threads=8)
    parallel_table.parallel_insert(data)
    parallel_time = time.time() - start

    print(f"Sequential: {sequential_time:.4f}s")
    print(f"Parallel: {parallel_time:.4f}s")
    print(f"Speedup: {sequential_time / parallel_time:.2f}x")
```

### Rust Concurrent Data Structures

[DashMap - Fast, Concurrent Hashmap in Rust](https://news.ycombinator.com/item?id=22699176)
introduces high-performance concurrent collections:

```rust
// Using DashMap for concurrent operations
use dashmap::DashMap;
use std::sync::Arc;
use std::thread;

fn concurrent_hashmap_example() {
    let map = Arc::new(DashMap::new());
    let mut handles = vec![];

    // Spawn multiple threads to insert data concurrently
    for i in 0..8 {
        let map_clone = Arc::clone(&map);
        let handle = thread::spawn(move || {
            for j in 0..1000 {
                let key = format!("thread_{}_key_{}", i, j);
                let value = i * 1000 + j;
                map_clone.insert(key, value);
            }
        });
        handles.push(handle);
    }

    // Wait for all threads to complete
    for handle in handles {
        handle.join().unwrap();
    }

    println!("Total entries: {}", map.len());

    // Concurrent iteration
    map.iter().for_each(|entry| {
        println!("{}: {}", entry.key(), entry.value());
    });
}

// Compare with standard HashMap + Mutex
use std::collections::HashMap;
use std::sync::Mutex;

fn mutex_hashmap_comparison() {
    let map = Arc::new(Mutex::new(HashMap::new()));
    let mut handles = vec![];

    for i in 0..8 {
        let map_clone = Arc::clone(&map);
        let handle = thread::spawn(move || {
            for j in 0..1000 {
                let key = format!("thread_{}_key_{}", i, j);
                let value = i * 1000 + j;

                // Must acquire lock for each operation
                let mut locked_map = map_clone.lock().unwrap();
                locked_map.insert(key, value);
                // Lock is released here
            }
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let final_map = map.lock().unwrap();
    println!("Mutex HashMap entries: {}", final_map.len());
}
```

## Python Advanced Concepts

### Python Gotchas and Best Practices

[Attack of Pythons: Gotchas](https://gist.githubusercontent.com/manojpandey/41b90cba1fd62095e247d1b2448ef85b/raw/0413c4805336b8030efc7de1e9fa0e229ca9903d/gotchas.md)
and
[Python Gotchas](https://docs.python-guide.org/writing/gotchas/#late-binding-closures)
highlight common Python pitfalls:

```python
# Late Binding Closures - A Classic Python Gotcha
def create_multipliers_wrong():
    """This doesn't work as expected!"""
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x: x * i)  # i is bound late!
    return multipliers

def create_multipliers_correct():
    """This works correctly"""
    multipliers = []
    for i in range(5):
        multipliers.append(lambda x, i=i: x * i)  # Capture i as default argument
    return multipliers

# Demonstrate the problem
wrong_multipliers = create_multipliers_wrong()
correct_multipliers = create_multipliers_correct()

print("Wrong approach:")
for i, multiply in enumerate(wrong_multipliers):
    print(f"Multiplier {i}: multiply(2) = {multiply(2)}")  # All print 8!

print("\nCorrect approach:")
for i, multiply in enumerate(correct_multipliers):
    print(f"Multiplier {i}: multiply(2) = {multiply(2)}")  # Prints 0, 2, 4, 6, 8

# Mutable Default Arguments - Another Classic Gotcha
def append_to_wrong(num, target=[]):
    """DON'T DO THIS!"""
    target.append(num)
    return target

def append_to_correct(num, target=None):
    """This is the right way"""
    if target is None:
        target = []
    target.append(num)
    return target

# Demonstrate mutable default argument problem
print("\nMutable defaults problem:")
print(append_to_wrong(1))  # [1]
print(append_to_wrong(2))  # [1, 2] - unexpected!
print(append_to_wrong(3))  # [1, 2, 3] - still growing!

print("\nCorrect approach:")
print(append_to_correct(1))  # [1]
print(append_to_correct(2))  # [2] - correct!
print(append_to_correct(3))  # [3] - correct!

# List comprehension variable leakage (Python 2 vs 3)
def comprehension_scoping():
    """Variable scoping in comprehensions"""
    # In Python 3, comprehension variables don't leak
    squares = [x**2 for x in range(5)]

    try:
        print(f"x after comprehension: {x}")  # This will fail in Python 3
    except NameError:
        print("x is not defined outside comprehension (Python 3 behavior)")

    # But regular loops do leak variables
    for y in range(5):
        pass
    print(f"y after loop: {y}")  # This works

# Class variable vs instance variable confusion
class Counter:
    count = 0  # Class variable - shared by all instances!

    def __init__(self):
        self.count += 1  # This creates an instance variable!

class CounterCorrect:
    def __init__(self):
        if not hasattr(CounterCorrect, 'count'):
            CounterCorrect.count = 0
        CounterCorrect.count += 1
        self.instance_id = CounterCorrect.count

# Demonstrate class variable confusion
c1 = Counter()
c2 = Counter()
print(f"c1.count: {c1.count}, c2.count: {c2.count}")  # Both are 1!
print(f"Counter.count: {Counter.count}")  # Still 0!

# Dictionary iteration order (Python < 3.7 vs 3.7+)
def dict_ordering():
    """Dictionary ordering behavior"""
    d = {'b': 2, 'a': 1, 'c': 3}

    # In Python 3.7+, insertion order is preserved
    print("Dictionary items:", list(d.items()))

    # For guaranteed ordering in older versions, use OrderedDict
    from collections import OrderedDict
    ordered_d = OrderedDict([('b', 2), ('a', 1), ('c', 3)])
    print("OrderedDict items:", list(ordered_d.items()))

# String interning surprises
def string_interning():
    """String interning can cause unexpected behavior"""
    a = "hello"
    b = "hello"
    print(f"a is b: {a is b}")  # Usually True (interned)

    a = "hello world"
    b = "hello world"
    print(f"a is b: {a is b}")  # May be False (not interned)

    # Always use == for string comparison, not is
    print(f"a == b: {a == b}")  # Always reliable

# Boolean arithmetic surprises
def boolean_arithmetic():
    """Booleans are subclass of int in Python"""
    print(f"True + True = {True + True}")  # 2
    print(f"False * 100 = {False * 100}")  # 0
    print(f"True / False will raise: ZeroDivisionError")

    # This can lead to unexpected behavior
    def count_trues(values):
        return sum(values)  # Works because True + True = 2

    result = count_trues([True, False, True, True])
    print(f"Sum of booleans: {result}")  # 3
```

{{< warning title="Python Gotcha Prevention" >}} **Best Practices to Avoid
Common Pitfalls:**

- Use `is` only for `None`, `True`, `False` comparisons
- Never use mutable objects as default arguments
- Be aware of late binding in closures - use default arguments to capture values
- Remember that `bool` is a subclass of `int` in Python
- Use `collections.OrderedDict` if you need guaranteed ordering in Python < 3.7
  {{< /warning >}}

## Learning Resources and Tools

### Functional Programming with Haskell

[Bartosz Milewski - School of Haskell](https://www.schoolofhaskell.com/user/bartosz/basics-of-haskell)
and
[Code and Exercises from Bartosz's School of Haskell](https://github.com/raviksharma/bartosz-basics-of-haskell)
provide excellent functional programming foundations:

```haskell
-- Basic Haskell concepts that influence other languages

-- Pure functions and immutability
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Pattern matching
describeList :: [a] -> String
describeList [] = "Empty list"
describeList [x] = "Singleton list"
describeList [x, y] = "Two-element list"
describeList _ = "Longer list"

-- Higher-order functions
applyTwice :: (a -> a) -> a -> a
applyTwice f x = f (f x)

-- Map, filter, fold - the foundation of functional programming
processNumbers :: [Int] -> Int
processNumbers nums = foldr (+) 0
                    $ filter (> 10)
                    $ map (* 2) nums

-- Currying and partial application
add :: Int -> Int -> Int
add x y = x + y

addFive :: Int -> Int
addFive = add 5  -- Partial application

-- Function composition
(.) :: (b -> c) -> (a -> b) -> a -> c
(f . g) x = f (g x)

-- Compose multiple operations
processData :: [Int] -> [Int]
processData = map (* 3) . filter even . map (+ 1)
```

### Programming Language Courses

[Coursera - Programming Languages [Course A]](https://www.coursera.org/learn/programming-languages)
and [Course B](https://www.coursera.org/learn/programming-languages-part-b)
provide deep language theory:

```sml
(* Standard ML examples from the course *)

(* Pattern matching and recursion *)
fun sum_list(xs) =
    case xs of
        [] => 0
      | x::xs' => x + sum_list(xs')

(* Higher-order functions *)
fun map(f, xs) =
    case xs of
        [] => []
      | x::xs' => f(x) :: map(f, xs')

fun filter(f, xs) =
    case xs of
        [] => []
      | x::xs' => if f(x) then x :: filter(f, xs') else filter(f, xs')

(* Closures and function composition *)
fun compose(f, g) = fn x => f(g(x))

fun curry(f) = fn x => fn y => f(x, y)
fun uncurry(f) = fn (x, y) => f x y
```

## Development Tools and Environment

### Git Visualization Tools

[A Viewer for Git and Diff Output](https://github.com/dandavison/delta) enhances
git diff readability:

```bash
# Install delta
cargo install git-delta

# Configure git to use delta
git config --global core.pager delta
git config --global interactive.diffFilter 'delta --color-only'
git config --global delta.navigate true
git config --global delta.light false
git config --global delta.line-numbers true

# Delta configuration options
git config --global delta.syntax-theme "Monokai Extended"
git config --global delta.features "line-numbers decorations"
git config --global delta.decorations.commit-decoration-style "bold yellow box ul"
git config --global delta.decorations.file-decoration-style "none"
```

### Feature Engineering Tools

[Featuretools: Python Framework for Automated Feature Engineering](https://www.featuretools.com/)
automates ML feature creation:

```python
# Automated feature engineering example
import featuretools as ft
import pandas as pd

# Create sample transaction data
customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'join_date': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01']),
    'age': [25, 35, 45]
})

transactions = pd.DataFrame({
    'transaction_id': range(1, 11),
    'customer_id': [1, 1, 2, 2, 2, 3, 3, 3, 3, 3],
    'amount': [10, 25, 15, 30, 20, 50, 35, 40, 25, 60],
    'timestamp': pd.date_range('2020-01-15', periods=10, freq='7D')
})

# Create entity set
es = ft.EntitySet(id='customer_data')

# Add entities
es = es.add_dataframe(
    dataframe_name='customers',
    dataframe=customers,
    index='customer_id',
    time_index='join_date'
)

es = es.add_dataframe(
    dataframe_name='transactions',
    dataframe=transactions,
    index='transaction_id',
    time_index='timestamp'
)

# Add relationship
relationship = ft.Relationship(
    parent_dataframe_name='customers',
    parent_column_name='customer_id',
    child_dataframe_name='transactions',
    child_column_name='customer_id'
)
es = es.add_relationship(relationship)

# Automatically generate features
feature_matrix, feature_defs = ft.dfs(
    entityset=es,
    target_dataframe_name='customers',
    max_depth=2
)

print("Generated features:")
for feature in feature_defs:
    print(f"- {feature}")

print("\nFeature matrix:")
print(feature_matrix)
```

{{< example title="Automated Feature Engineering Benefits" >}} **Featuretools
Capabilities:**

- **Aggregation features**: SUM, MEAN, COUNT, STD across time windows
- **Transformation features**: DAY, MONTH, WEEKDAY from timestamps
- **Deep feature synthesis**: Multi-level relationships and aggregations
- **Time-aware features**: Respect temporal relationships in data
- **Custom primitives**: Define domain-specific feature engineering operations
  {{< /example >}}

## Key Learning Insights

### Programming Challenge Benefits

Today's exploration of Advent of Code and competitive programming resources
highlights several advantages over traditional algorithm practice:

- **Narrative context** makes problems more engaging and memorable
- **Progressive difficulty** builds skills systematically
- **Multiple valid approaches** encourage creative problem-solving
- **Real-world applicability** bridges theoretical and practical programming

### Concurrent Programming Patterns

The GPU hash table and Rust concurrent data structures demonstrate modern
approaches to parallelism:

- **Lock-free data structures** enable better performance at scale
- **GPU-style vectorization** can be simulated for CPU-bound tasks
- **Rust's ownership model** provides memory safety in concurrent contexts
- **Trade-offs** between complexity and performance must be carefully considered

### Language Learning Strategy

The combination of theoretical courses and practical exercises provides a
comprehensive learning approach:

- **Theory** (Programming Languages courses) provides foundational understanding
- **Practice** (Advent of Code, project work) builds implementation skills
- **Community** (GitHub solutions, discussions) offers diverse perspectives
- **Progressive complexity** from simple concepts to advanced applications

---

_This exploration reinforced that effective learning combines theoretical
understanding with practical application, while modern development increasingly
requires awareness of concurrent and parallel programming patterns._
