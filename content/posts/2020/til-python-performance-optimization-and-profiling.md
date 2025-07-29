---
date: 2020-09-09T19:00:00+05:30
draft: false
title: "TIL: Python Performance Optimization and Advanced Profiling"
description: "Today I learned about advanced Python performance optimization techniques, modern profiling tools, and practical strategies for identifying and eliminating performance bottlenecks."
tags:
  - til
  - python
  - performance
  - profiling
  - optimization
  - scalene
  - pandas
  - data-science
---

Today I explored comprehensive Python performance optimization techniques and discovered advanced profiling tools that provide deep insights into CPU usage, memory allocation, and execution bottlenecks.

## Advanced Python Profiling with Scalene

### Modern CPU and Memory Profiling

[Scalene](https://github.com/emeryberger/scalene) represents a new generation of Python profilers that provides detailed CPU and memory analysis:

```bash
# Install Scalene
pip install scalene

# Basic profiling
scalene your_script.py

# Profile with specific options
scalene --cpu-only your_script.py
scalene --memory-only your_script.py
scalene --profile-interval 0.01 your_script.py

# Web-based output
scalene --web your_script.py

# Profile specific functions
scalene --profile-only "function_name" your_script.py
```

{{< note title="Scalene Advantages" >}}
**Over Standard Profilers:**
- **Line-by-line profiling** - Shows exact bottleneck locations
- **Memory tracking** - Identifies memory allocations and leaks
- **GPU profiling** - CUDA memory and computation analysis
- **Low overhead** - Minimal impact on program execution
- **Copy detection** - Identifies unnecessary data copying
- **Web interface** - Interactive results exploration

**Technical Innovation:**
- **Statistical sampling** - Reduces profiling overhead
- **Native code support** - Profiles C extensions and libraries
- **Memory attribution** - Links allocations to specific lines
- **Growth tracking** - Shows memory usage over time
{{< /note >}}

### Comprehensive Performance Analysis

```python
# Example script for profiling with Scalene
import numpy as np
import pandas as pd
import time
from typing import List, Dict

@profile  # Scalene decorator for focused profiling
def inefficient_data_processing():
    """Intentionally inefficient data processing for profiling"""
    
    # Memory-intensive operations
    large_list = []
    for i in range(100000):
        large_list.append(i ** 2)  # Inefficient: list growth
    
    # Convert to numpy (better approach)
    data = np.array(large_list)
    
    # Inefficient pandas operations
    df = pd.DataFrame({'values': data})
    result = df['values'].apply(lambda x: x * 2)  # Slow: apply with lambda
    
    # Memory copying
    copied_data = data.copy()  # Unnecessary copy
    another_copy = copied_data.copy()  # Another unnecessary copy
    
    # CPU-intensive computation
    processed = []
    for value in result:
        processed.append(compute_expensive(value))
    
    return processed

def compute_expensive(x: float) -> float:
    """Simulate expensive computation"""
    total = 0
    for i in range(1000):
        total += x * (i ** 0.5)
    return total

def optimized_data_processing():
    """Optimized version of the same operations"""
    
    # Pre-allocate numpy array
    data = np.arange(100000) ** 2
    
    # Vectorized pandas operations
    df = pd.DataFrame({'values': data})
    result = df['values'] * 2  # Vectorized multiplication
    
    # Avoid unnecessary copying
    # Use views or in-place operations where possible
    
    # Vectorized computation where possible
    processed = np.array([compute_expensive(x) for x in result])
    
    return processed

# Performance comparison framework
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile function execution with cProfile"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = func(*args, **kwargs)
    
    profiler.disable()
    
    # Capture profiling output
    string_buffer = StringIO()
    stats = pstats.Stats(profiler, stream=string_buffer)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions
    
    return result, string_buffer.getvalue()

# Memory profiling with memory_profiler
try:
    from memory_profiler import profile as memory_profile
    
    @memory_profile
    def memory_intensive_function():
        """Function to analyze memory usage"""
        # Large list creation
        big_list = [i for i in range(1000000)]
        
        # Convert to numpy
        np_array = np.array(big_list)
        
        # Create pandas DataFrame
        df = pd.DataFrame({'data': np_array})
        
        # Memory-intensive operations
        df['squared'] = df['data'] ** 2
        df['cubed'] = df['data'] ** 3
        
        return df
        
except ImportError:
    print("memory_profiler not installed. Run: pip install memory-profiler")
```

## Fast Python Programming Techniques

### James Powell's Performance Insights

[Fast and Furious Python 7: Writing Fast Python Code](https://www.youtube.com/watch?v=Ix04KpZiUA8&t=1580s) reveals advanced optimization strategies:

```python
# High-performance Python patterns
import numpy as np
import numba
from collections import deque, defaultdict
import itertools
from functools import lru_cache, reduce
import operator

# 1. Vectorization with NumPy
def slow_element_wise_operation(data: List[float]) -> List[float]:
    """Slow: Python loop"""
    return [x ** 2 + 2 * x + 1 for x in data]

def fast_vectorized_operation(data: np.ndarray) -> np.ndarray:
    """Fast: NumPy vectorization"""
    return data ** 2 + 2 * data + 1

# 2. JIT compilation with Numba
@numba.jit(nopython=True)
def fast_numerical_computation(data: np.ndarray) -> float:
    """JIT-compiled function for numerical work"""
    total = 0.0
    for i in range(len(data)):
        total += data[i] ** 2
    return total / len(data)

# 3. Efficient data structures
def inefficient_frequent_lookups():
    """Slow: list lookups"""
    data = list(range(10000))
    lookups = [5000 in data for _ in range(1000)]  # O(n) each time
    return lookups

def efficient_frequent_lookups():
    """Fast: set lookups"""
    data = set(range(10000))
    lookups = [5000 in data for _ in range(1000)]  # O(1) each time
    return lookups

# 4. Memory-efficient iteration
def memory_inefficient_processing(filename: str):
    """Loads entire file into memory"""
    with open(filename) as f:
        lines = f.readlines()  # Loads everything
    
    return [line.upper() for line in lines]

def memory_efficient_processing(filename: str):
    """Generator-based processing"""
    with open(filename) as f:
        for line in f:  # Lazy iteration
            yield line.upper()

# 5. Caching expensive computations
@lru_cache(maxsize=1000)
def expensive_fibonacci(n: int) -> int:
    """Cached recursive computation"""
    if n < 2:
        return n
    return expensive_fibonacci(n - 1) + expensive_fibonacci(n - 2)

# 6. Bulk operations with operator module
def slow_reduction(numbers: List[int]) -> int:
    """Slow: manual reduction"""
    result = 1
    for num in numbers:
        result *= num
    return result

def fast_reduction(numbers: List[int]) -> int:
    """Fast: using reduce with operator"""
    return reduce(operator.mul, numbers, 1)

# 7. Efficient string operations
def slow_string_building(words: List[str]) -> str:
    """Slow: string concatenation"""
    result = ""
    for word in words:
        result += word + " "
    return result.strip()

def fast_string_building(words: List[str]) -> str:
    """Fast: join operation"""
    return " ".join(words)

# 8. Optimized container operations
def inefficient_data_grouping(items: List[tuple]) -> Dict:
    """Slow: manual grouping"""
    groups = {}
    for key, value in items:
        if key not in groups:
            groups[key] = []
        groups[key].append(value)
    return groups

def efficient_data_grouping(items: List[tuple]) -> Dict:
    """Fast: defaultdict"""
    groups = defaultdict(list)
    for key, value in items:
        groups[key].append(value)
    return dict(groups)

# Performance testing framework
import timeit
from typing import Callable, Any

def benchmark_function(func: Callable, *args, number: int = 1000, **kwargs) -> dict:
    """Benchmark function performance"""
    
    # Time execution
    execution_time = timeit.timeit(
        lambda: func(*args, **kwargs), 
        number=number
    )
    
    # Memory usage (simplified)
    import tracemalloc
    tracemalloc.start()
    
    result = func(*args, **kwargs)
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return {
        'execution_time': execution_time / number,
        'memory_current': current,
        'memory_peak': peak,
        'result_size': len(result) if hasattr(result, '__len__') else 1
    }

# Example benchmarking
if __name__ == "__main__":
    # Create test data
    test_data = list(range(10000))
    np_test_data = np.array(test_data, dtype=float)
    
    # Benchmark different approaches
    benchmarks = {
        'List comprehension': lambda: slow_element_wise_operation(test_data),
        'NumPy vectorized': lambda: fast_vectorized_operation(np_test_data),
        'Numba JIT': lambda: fast_numerical_computation(np_test_data),
    }
    
    print("Performance Comparison:")
    print("-" * 50)
    
    for name, func in benchmarks.items():
        stats = benchmark_function(func, number=100)
        print(f"{name:20} {stats['execution_time']*1000:8.2f}ms "
              f"{stats['memory_peak']/1024:8.1f}KB")
```

## Pandas Performance Optimization

### Efficient DataFrame Operations

Critical pandas performance insights from the archive:

```python
import pandas as pd
import numpy as np
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Critical pandas performance tip from archive:
# Using & and | operators is MUCH faster than zip() with any() or all()

def slow_pandas_filtering(df: pd.DataFrame) -> pd.DataFrame:
    """Inefficient: using zip with multiple conditions"""
    condition1 = df['column1'] > 100  
    condition2 = df['column2'] < 50
    condition3 = df['column3'] == 'target'
    
    # SLOW: Don't do this!
    combined_condition = [
        any([c1, c2, c3]) 
        for c1, c2, c3 in zip(condition1, condition2, condition3)
    ]
    
    return df[combined_condition]

def fast_pandas_filtering(df: pd.DataFrame) -> pd.DataFrame:
    """Efficient: using pandas boolean operators"""
    # FAST: Use & and | operators directly
    condition = (
        (df['column1'] > 100) | 
        (df['column2'] < 50) | 
        (df['column3'] == 'target')
    )
    
    return df[condition]

def even_faster_pandas_filtering(df: pd.DataFrame) -> pd.DataFrame:
    """Even faster: use .loc with intermediate DataFrames if needed"""
    # For complex filtering, sometimes multiple .loc calls are faster
    filtered = df.loc[df['column1'] > 100]  # First filter
    filtered = filtered.loc[filtered['column2'] < 50]  # Second filter
    filtered = filtered.loc[filtered['column3'] == 'target']  # Third filter
    
    return filtered

# Advanced pandas optimization techniques
class PandasOptimizer:
    """Collection of pandas optimization techniques"""
    
    @staticmethod
    def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame memory usage by choosing appropriate dtypes"""
        optimized_df = df.copy()
        
        for column in df.columns:
            col_type = df[column].dtype
            
            if col_type != 'object':
                # Optimize numeric columns
                col_min = df[column].min()
                col_max = df[column].max()
                
                if col_type == 'int64':
                    if col_min > np.iinfo(np.int8).min and col_max < np.iinfo(np.int8).max:
                        optimized_df[column] = df[column].astype(np.int8)
                    elif col_min > np.iinfo(np.int16).min and col_max < np.iinfo(np.int16).max:
                        optimized_df[column] = df[column].astype(np.int16)
                    elif col_min > np.iinfo(np.int32).min and col_max < np.iinfo(np.int32).max:
                        optimized_df[column] = df[column].astype(np.int32)
                
                elif col_type == 'float64':
                    if col_min > np.finfo(np.float32).min and col_max < np.finfo(np.float32).max:
                        optimized_df[column] = df[column].astype(np.float32)
            
            else:
                # Optimize object columns (strings)
                num_unique_values = len(df[column].unique())
                num_total_values = len(df[column])
                
                if num_unique_values / num_total_values < 0.5:
                    optimized_df[column] = df[column].astype('category')
        
        return optimized_df
    
    @staticmethod
    def efficient_groupby_operations(df: pd.DataFrame) -> pd.DataFrame:
        """Demonstrate efficient groupby patterns"""
        
        # Slow: Multiple separate groupby operations
        # result1 = df.groupby('category')['value'].mean()
        # result2 = df.groupby('category')['value'].sum()
        # result3 = df.groupby('category')['value'].count()
        
        # Fast: Single groupby with agg
        result = df.groupby('category')['value'].agg(['mean', 'sum', 'count'])
        
        # Even faster for multiple columns
        multi_result = df.groupby('category').agg({
            'value1': ['mean', 'sum'],
            'value2': ['max', 'min'],
            'value3': 'count'
        })
        
        return result, multi_result
    
    @staticmethod
    def vectorized_string_operations(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Use vectorized string operations instead of apply"""
        
        # Slow: apply with lambda
        # df['processed'] = df[column].apply(lambda x: x.upper().replace(' ', '_'))
        
        # Fast: vectorized string operations
        df['processed'] = df[column].str.upper().str.replace(' ', '_', regex=False)
        
        # Complex string processing
        df['cleaned'] = (df[column]
                        .str.strip()
                        .str.lower()
                        .str.replace(r'[^\w\s]', '', regex=True)
                        .str.replace(r'\s+', ' ', regex=True))
        
        return df
    
    @staticmethod
    def efficient_merge_operations(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame merge operations"""
        
        # Set index for faster merges if doing multiple merges on same keys
        df1_indexed = df1.set_index('key_column')
        df2_indexed = df2.set_index('key_column')
        
        # Fast merge using indices
        result = df1_indexed.join(df2_indexed, how='inner')
        
        # For large datasets, consider using merge with sorted data
        df1_sorted = df1.sort_values('key_column')
        df2_sorted = df2.sort_values('key_column')
        
        result_sorted = pd.merge(df1_sorted, df2_sorted, on='key_column', how='inner')
        
        return result

# Performance testing for pandas operations
def pandas_performance_comparison():
    """Compare different pandas operation approaches"""
    
    # Create test data
    np.random.seed(42)
    n_rows = 100000
    
    df = pd.DataFrame({
        'column1': np.random.randint(0, 200, n_rows),
        'column2': np.random.randint(0, 100, n_rows), 
        'column3': np.random.choice(['target', 'other1', 'other2'], n_rows),
        'value': np.random.randn(n_rows)
    })
    
    # Test filtering performance
    import time
    
    print("Pandas Performance Comparison:")
    print("-" * 40)
    
    # Test slow method
    start_time = time.perf_counter()
    slow_result = slow_pandas_filtering(df)
    slow_time = time.perf_counter() - start_time
    
    # Test fast method
    start_time = time.perf_counter()
    fast_result = fast_pandas_filtering(df)
    fast_time = time.perf_counter() - start_time
    
    # Test fastest method
    start_time = time.perf_counter()
    fastest_result = even_faster_pandas_filtering(df)
    fastest_time = time.perf_counter() - start_time
    
    print(f"Slow method (zip):     {slow_time:.4f}s")
    print(f"Fast method (&, |):    {fast_time:.4f}s ({slow_time/fast_time:.1f}x faster)")
    print(f"Fastest method (.loc): {fastest_time:.4f}s ({slow_time/fastest_time:.1f}x faster)")
    
    # Memory optimization test
    original_memory = df.memory_usage(deep=True).sum()
    optimized_df = PandasOptimizer.optimize_dtypes(df)
    optimized_memory = optimized_df.memory_usage(deep=True).sum()
    
    print(f"\nMemory optimization:")
    print(f"Original:  {original_memory / 1024 / 1024:.2f} MB")
    print(f"Optimized: {optimized_memory / 1024 / 1024:.2f} MB")
    print(f"Reduction: {(1 - optimized_memory/original_memory)*100:.1f}%")
```

## Concurrency and Parallelization

### Python Queue Performance Issues

[The Tragic Tale of the Deadlocking Python Queue](https://codewithoutrules.com/2017/08/16/concurrency-python/) highlights critical concurrency pitfalls:

```python
import queue
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

# Problematic queue usage that can deadlock
def problematic_queue_usage():
    """Demonstrates potential deadlock with Python queues"""
    
    def producer(q, items):
        for item in items:
            print(f"Producing {item}")
            q.put(item)
            time.sleep(0.1)  # Simulate work
        q.put(None)  # Sentinel value
    
    def consumer(q):
        results = []
        while True:
            item = q.get()
            if item is None:
                q.task_done()
                break
            
            print(f"Consuming {item}")
            results.append(item * 2)
            time.sleep(0.2)  # Simulate work
            q.task_done()
        
        return results
    
    # Problematic: Small queue size with blocking operations
    work_queue = queue.Queue(maxsize=2)  # Small buffer
    
    # This can deadlock if producer fills queue while consumer is slow
    producer_thread = threading.Thread(target=producer, args=(work_queue, range(10)))
    consumer_thread = threading.Thread(target=consumer, args=(work_queue,))
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()

# Better queue usage patterns
def safe_queue_usage():
    """Demonstrates safe queue usage patterns"""
    
    def producer(q, items):
        for item in items:
            q.put(item)
        q.put(None)  # Sentinel
    
    def consumer(q, results_list):
        while True:
            try:
                item = q.get(timeout=1.0)  # Use timeout
                if item is None:
                    break
                results_list.append(item * 2)
                q.task_done()
            except queue.Empty:
                continue
    
    # Safe: Unlimited queue size or proper synchronization
    work_queue = queue.Queue()  # Unlimited size
    results = []
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        producer_future = executor.submit(producer, work_queue, range(10))
        consumer_future = executor.submit(consumer, work_queue, results)
        
        producer_future.result()
        consumer_future.result()
    
    return results

# High-performance parallel processing
def parallel_processing_patterns():
    """Demonstrate different parallelization approaches"""
    
    def cpu_intensive_task(n):
        """Simulate CPU-intensive work"""
        total = 0
        for i in range(n * 10000):
            total += i ** 0.5
        return total
    
    def io_intensive_task(delay):
        """Simulate I/O-intensive work"""
        time.sleep(delay)
        return f"Task completed after {delay}s"
    
    # Test data
    cpu_tasks = [1000, 2000, 3000, 4000, 5000]
    io_tasks = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    # CPU-bound: Use ProcessPoolExecutor
    print("CPU-intensive tasks (ProcessPoolExecutor):")
    start_time = time.perf_counter()
    
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        cpu_results = list(executor.map(cpu_intensive_task, cpu_tasks))
    
    cpu_time = time.perf_counter() - start_time
    print(f"Completed in {cpu_time:.2f}s")
    
    # I/O-bound: Use ThreadPoolExecutor
    print("\nI/O-intensive tasks (ThreadPoolExecutor):")
    start_time = time.perf_counter()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        io_results = list(executor.map(io_intensive_task, io_tasks))
    
    io_time = time.perf_counter() - start_time
    print(f"Completed in {io_time:.2f}s")
    
    return cpu_results, io_results
```

## Memory Management and Optimization

### Memory Profiling Techniques

```python
import sys
import gc
from typing import Any, Dict
import tracemalloc

class MemoryProfiler:
    """Advanced memory profiling and analysis"""
    
    def __init__(self):
        self.snapshots = []
        
    def start_tracing(self):
        """Start memory tracing"""
        tracemalloc.start()
    
    def take_snapshot(self, label: str = None):
        """Take memory snapshot"""
        snapshot = tracemalloc.take_snapshot()
        self.snapshots.append((label or f"snapshot_{len(self.snapshots)}", snapshot))
        return snapshot
    
    def compare_snapshots(self, label1: str, label2: str, top_n: int = 10):
        """Compare two memory snapshots"""
        snap1 = next((s for l, s in self.snapshots if l == label1), None)
        snap2 = next((s for l, s in self.snapshots if l == label2), None)
        
        if not snap1 or not snap2:
            print("Snapshots not found")
            return
        
        diff = snap2.compare_to(snap1, 'lineno')
        
        print(f"Top {top_n} memory differences ({label2} vs {label1}):")
        for stat in diff[:top_n]:
            print(f"{stat.traceback.format()[-1].strip()}")
            print(f"  Size diff: {stat.size_diff:+,d} bytes")
            print(f"  Count diff: {stat.count_diff:+,d} blocks")
            print()
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage statistics"""
        current, peak = tracemalloc.get_traced_memory()
        
        # Force garbage collection for accurate measurement
        gc.collect()
        
        return {
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024,
            'objects_count': len(gc.get_objects()),
            'gc_stats': gc.get_stats()
        }

# Memory optimization techniques
def memory_efficient_data_processing():
    """Demonstrate memory-efficient patterns"""
    
    # Generator-based processing (memory efficient)
    def process_large_dataset_efficiently(filename: str):
        """Process large files without loading everything into memory"""
        def line_processor():
            with open(filename, 'r') as f:
                for line in f:
                    # Process line and yield result
                    yield line.strip().upper()
        
        return line_processor()
    
    # Memory-efficient aggregation
    def memory_efficient_aggregation(data_generator):
        """Aggregate data without storing intermediate results"""
        total = 0
        count = 0
        min_val = float('inf')
        max_val = float('-inf')
        
        for value in data_generator:
            total += value
            count += 1
            min_val = min(min_val, value)
            max_val = max(max_val, value)
        
        return {
            'mean': total / count if count > 0 else 0,
            'min': min_val if count > 0 else None,
            'max': max_val if count > 0 else None,
            'count': count
        }
    
    # Demonstrate usage
    profiler = MemoryProfiler()
    profiler.start_tracing()
    
    # Take initial snapshot
    profiler.take_snapshot("start")
    
    # Simulate memory-intensive operations
    large_list = [i for i in range(100000)]
    
    profiler.take_snapshot("after_list_creation")
    
    # Convert to generator (more memory efficient)
    data_gen = (i for i in range(100000))
    result = memory_efficient_aggregation(data_gen)
    
    profiler.take_snapshot("after_processing")
    
    # Compare memory usage
    profiler.compare_snapshots("start", "after_list_creation")
    
    return result

# Example performance test
if __name__ == "__main__":
    # Run pandas performance comparison
    pandas_performance_comparison()
    
    # Run memory profiling example
    memory_result = memory_efficient_data_processing()
    print(f"Aggregation result: {memory_result}")
```

## Key Performance Insights

### Critical Optimization Principles

{{< tip title="Python Performance Best Practices" >}}
1. **Profile First**: Always measure before optimizing
2. **Vectorize Operations**: Use NumPy/Pandas vectorized operations
3. **Choose Right Data Structures**: dict/set for lookups, deque for queues
4. **Minimize Python Loops**: Use built-in functions and comprehensions
5. **Cache Expensive Operations**: functools.lru_cache for repeated computations
6. **Memory Awareness**: Use generators for large datasets
7. **Pandas Operators**: Use & and | instead of apply() with complex logic
8. **JIT Compilation**: Consider Numba for numerical computations
{{< /tip >}}

### Performance Anti-Patterns to Avoid

{{< warning title="Common Performance Mistakes" >}}
- **Repeated DataFrame filtering** with apply() and lambda functions
- **String concatenation** in loops instead of join()
- **List lookups** instead of set/dict lookups for membership testing
- **Unnecessary data copying** in pandas operations
- **Small queue sizes** in threaded applications causing deadlocks
- **Global Interpreter Lock (GIL)** ignorance in threading decisions
- **Memory leaks** from circular references and unclosed resources
{{< /warning >}}

This comprehensive exploration of Python performance optimization demonstrates that writing fast Python code requires understanding both language internals and appropriate tool selection for different types of computational tasks.

---

*These performance optimization insights from my archive showcase the evolution from basic Python usage to advanced performance engineering, emphasizing the importance of profiling, measurement, and systematic optimization approaches.*