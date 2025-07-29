---
date: 2020-07-26T18:00:00+05:30
draft: false
title: "TIL: Python Collections Optimization and Linux Display Management"
description: "Today I learned about Python collections.defaultdict performance benefits, the sorted function's reverse parameter, and using arandr as a frontend for xrandr in tiling window managers."
tags:
  - til
  - python
  - collections
  - linux
  - xrandr
  - arandr
  - tiling-window-managers
---

Today I discovered practical optimizations in Python's collections module and explored Linux display management tools that make working with multiple monitors much easier in tiling window managers.

## Python Collections Performance

### defaultdict vs dict.get() Performance

`collections.defaultdict` provides better performance than checking `{}.get()` for handling missing keys:

```python
import time
from collections import defaultdict, Counter
import random

# Performance comparison: defaultdict vs dict.get()
def benchmark_dict_patterns(n=100000):
    """Compare different patterns for handling missing dictionary keys"""
    data = [random.choice(['apple', 'banana', 'cherry', 'date']) for _ in range(n)]
    
    # Method 1: Using dict.get() with default
    start = time.time()
    counts1 = {}
    for item in data:
        counts1[item] = counts1.get(item, 0) + 1
    dict_get_time = time.time() - start
    
    # Method 2: Using defaultdict
    start = time.time()
    counts2 = defaultdict(int)
    for item in data:
        counts2[item] += 1
    defaultdict_time = time.time() - start
    
    # Method 3: Using dict with try/except
    start = time.time()
    counts3 = {}
    for item in data:
        try:
            counts3[item] += 1
        except KeyError:
            counts3[item] = 1
    try_except_time = time.time() - start
    
    # Method 4: Using dict with 'in' check
    start = time.time()
    counts4 = {}
    for item in data:
        if item in counts4:
            counts4[item] += 1
        else:
            counts4[item] = 1
    in_check_time = time.time() - start
    
    # Method 5: Using Counter (for comparison)
    start = time.time()
    counts5 = Counter(data)
    counter_time = time.time() - start
    
    print(f"Results for {n:,} operations:")
    print(f"dict.get():       {dict_get_time:.4f}s")
    print(f"defaultdict:      {defaultdict_time:.4f}s ({dict_get_time/defaultdict_time:.2f}x faster)")
    print(f"try/except:       {try_except_time:.4f}s")
    print(f"'in' check:       {in_check_time:.4f}s")
    print(f"Counter:          {counter_time:.4f}s")
    
    # Verify all methods produce same result
    assert dict(counts2) == counts1 == counts3 == counts4 == dict(counts5)
    
    return {
        'defaultdict': defaultdict_time,
        'dict_get': dict_get_time,
        'try_except': try_except_time,
        'in_check': in_check_time,
        'counter': counter_time
    }

# Run benchmark
results = benchmark_dict_patterns()
```

### Advanced defaultdict Usage Patterns

```python
from collections import defaultdict
import json

# Nested defaultdict for tree-like structures
def create_nested_defaultdict():
    """Create nested defaultdict for hierarchical data"""
    # Automatically creates nested structure
    tree = defaultdict(lambda: defaultdict(list))
    
    # Add data without checking if keys exist
    tree['animals']['mammals'].append('dog')
    tree['animals']['mammals'].append('cat')
    tree['animals']['birds'].append('eagle')
    tree['plants']['trees'].append('oak')
    tree['plants']['flowers'].append('rose')
    
    return tree

# Grouping data with defaultdict
def group_by_attribute(items, key_func):
    """Group items by a computed key function"""
    groups = defaultdict(list)
    for item in items:
        key = key_func(item)
        groups[key].append(item)
    return dict(groups)

# Example usage
people = [
    {'name': 'Alice', 'age': 25, 'city': 'New York'},
    {'name': 'Bob', 'age': 30, 'city': 'London'}, 
    {'name': 'Charlie', 'age': 25, 'city': 'New York'},
    {'name': 'Diana', 'age': 35, 'city': 'Paris'},
    {'name': 'Eve', 'age': 30, 'city': 'London'}
]

# Group by age
by_age = group_by_attribute(people, lambda p: p['age'])
print("Grouped by age:")
for age, group in by_age.items():
    print(f"  {age}: {[p['name'] for p in group]}")

# Group by city
by_city = group_by_attribute(people, lambda p: p['city'])
print("\nGrouped by city:")
for city, group in by_city.items():
    print(f"  {city}: {[p['name'] for p in group]}")

# Building indexes with defaultdict
def build_search_index(documents):
    """Build a search index from documents"""
    index = defaultdict(set)  # Use set to avoid duplicates
    
    for doc_id, content in enumerate(documents):
        words = content.lower().split()
        for word in words:
            # Clean word (remove punctuation)
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word:
                index[clean_word].add(doc_id)
    
    return index

# Example document search
documents = [
    "Python is a programming language",
    "JavaScript is also a programming language", 
    "Both Python and JavaScript are popular",
    "Learning programming languages takes time"
]

search_index = build_search_index(documents)

def search_documents(query, index, documents):
    """Search documents using the built index"""
    query_words = [word.lower() for word in query.split()]
    
    if not query_words:
        return []
    
    # Find documents containing first word
    result_docs = index[query_words[0]].copy()
    
    # Intersect with documents containing other words
    for word in query_words[1:]:
        result_docs &= index[word]
    
    return [(doc_id, documents[doc_id]) for doc_id in sorted(result_docs)]

# Test search
results = search_documents("Python programming", search_index, documents)
print(f"\nSearch results for 'Python programming': {len(results)} found")
for doc_id, content in results:
    print(f"  Doc {doc_id}: {content}")

# Counting with different data types
def advanced_counting_patterns():
    """Demonstrate various counting patterns with defaultdict"""
    
    # Count nested attributes
    transactions = [
        {'user': 'alice', 'category': 'food', 'amount': 25},
        {'user': 'bob', 'category': 'transport', 'amount': 15},
        {'user': 'alice', 'category': 'food', 'amount': 30},
        {'user': 'charlie', 'category': 'entertainment', 'amount': 50},
        {'user': 'bob', 'category': 'food', 'amount': 20},
    ]
    
    # Count by user and category
    user_category_counts = defaultdict(lambda: defaultdict(int))
    user_totals = defaultdict(int)
    category_totals = defaultdict(int)
    
    for transaction in transactions:
        user = transaction['user']
        category = transaction['category']
        amount = transaction['amount']
        
        user_category_counts[user][category] += amount
        user_totals[user] += amount
        category_totals[category] += amount
    
    print("\nTransaction analysis:")
    print("By user and category:")
    for user, categories in user_category_counts.items():
        print(f"  {user}: {dict(categories)}")
    
    print(f"\nUser totals: {dict(user_totals)}")
    print(f"Category totals: {dict(category_totals)}")

# Run examples
tree = create_nested_defaultdict()
print("Nested tree structure:")
print(json.dumps(tree, indent=2, default=list))

advanced_counting_patterns()
```

{{< tip title="defaultdict Performance Benefits" >}}
**Why defaultdict is faster than dict.get():**
- **Single hash lookup** - defaultdict only hashes the key once
- **No function call overhead** - dict.get() requires a method call
- **Optimized C implementation** - Less Python bytecode execution
- **No conditional logic** - Automatic default value creation
- **Memory efficiency** - Reduces object creation overhead
{{< /tip >}}

## Python's Sorted Function with Reverse

The `sorted` function has a convenient `reverse` flag for descending order:

```python
# Basic sorting with reverse parameter
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]

ascending = sorted(numbers)
descending = sorted(numbers, reverse=True)

print(f"Ascending:  {ascending}")   # [1, 1, 2, 3, 4, 5, 5, 6, 9]
print(f"Descending: {descending}")  # [9, 6, 5, 5, 4, 3, 2, 1, 1]

# Sorting complex objects
students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 19},
    {'name': 'Charlie', 'grade': 78, 'age': 21},
    {'name': 'Diana', 'grade': 96, 'age': 20}
]

# Sort by grade (highest first)
by_grade_desc = sorted(students, key=lambda s: s['grade'], reverse=True)
print("\nStudents by grade (highest first):")
for student in by_grade_desc:
    print(f"  {student['name']}: {student['grade']}")

# Multiple sort criteria with reverse
def multi_level_sort():
    """Demonstrate complex sorting with multiple criteria"""
    data = [
        ('Alice', 'Engineering', 85, 20),
        ('Bob', 'Arts', 92, 19),
        ('Charlie', 'Engineering', 78, 21),
        ('Diana', 'Arts', 96, 20),
        ('Eve', 'Engineering', 85, 19),
        ('Frank', 'Arts', 78, 22)
    ]
    
    # Sort by department (ascending), then grade (descending), then age (ascending)
    from operator import itemgetter
    
    # Method 1: Using multiple sorted() calls (applied in reverse order)
    result1 = sorted(data, key=itemgetter(3))       # Sort by age first
    result1 = sorted(result1, key=itemgetter(2), reverse=True)  # Then by grade (desc)
    result1 = sorted(result1, key=itemgetter(1))    # Finally by department
    
    # Method 2: Using tuple key with negation for reverse
    result2 = sorted(data, key=lambda x: (x[1], -x[2], x[3]))
    
    # Method 3: Custom comparison with multiple criteria
    def sort_key(item):
        name, dept, grade, age = item
        return (dept, -grade, age)  # Negative grade for descending
    
    result3 = sorted(data, key=sort_key)
    
    print("Multi-level sort results:")
    print("(Name, Department, Grade, Age)")
    for item in result3:
        print(f"  {item}")
    
    # Verify all methods produce same result
    assert result1 == result2 == result3

# Advanced sorting patterns
def advanced_sorting_patterns():
    """Show advanced use cases for sorted() with reverse"""
    
    # Sort dictionary by values (descending)
    word_counts = {'apple': 23, 'banana': 45, 'cherry': 12, 'date': 67}
    
    # Get items sorted by count (highest first)
    sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    print("\nWords by frequency:")
    for word, count in sorted_items:
        print(f"  {word}: {count}")
    
    # Sort by string length (longest first), then alphabetically
    words = ['cat', 'elephant', 'dog', 'hippopotamus', 'ant', 'zebra']
    
    sorted_words = sorted(words, key=lambda w: (-len(w), w))
    print(f"\nWords by length (desc), then alphabetically: {sorted_words}")
    
    # Custom reverse logic for complex objects
    class Task:
        def __init__(self, name, priority, due_date):
            self.name = name
            self.priority = priority  # 1 = high, 2 = medium, 3 = low
            self.due_date = due_date
        
        def __repr__(self):
            return f"Task({self.name}, P{self.priority}, {self.due_date})"
    
    from datetime import date
    tasks = [
        Task("Fix bug", 1, date(2020, 8, 1)),
        Task("Write docs", 2, date(2020, 7, 30)),
        Task("Code review", 1, date(2020, 7, 29)),
        Task("Meeting", 3, date(2020, 7, 31)),
    ]
    
    # Sort by priority (high first), then due date (earliest first)
    sorted_tasks = sorted(tasks, key=lambda t: (t.priority, t.due_date))
    print("\nTasks by priority and due date:")
    for task in sorted_tasks:
        print(f"  {task}")

# Run examples
multi_level_sort()
advanced_sorting_patterns()

# Performance comparison: sorted() vs list.sort()
def sorting_performance_comparison():
    """Compare sorted() vs list.sort() performance"""
    import random
    import time
    
    # Generate test data
    data = [random.randint(1, 1000) for _ in range(100000)]
    
    # Test sorted() - creates new list
    data_copy1 = data.copy()
    start = time.time()
    result = sorted(data_copy1, reverse=True)
    sorted_time = time.time() - start
    
    # Test list.sort() - modifies in place
    data_copy2 = data.copy()
    start = time.time()
    data_copy2.sort(reverse=True)
    sort_time = time.time() - start
    
    print(f"\nPerformance comparison (100K integers):")
    print(f"sorted():    {sorted_time:.4f}s")
    print(f"list.sort(): {sort_time:.4f}s")
    print(f"sort() is {sorted_time/sort_time:.2f}x faster (in-place)")
    
    # Verify results are identical
    assert result == data_copy2

sorting_performance_comparison()
```

{{< note title="Sorting Best Practices" >}}
**When to use sorted() vs list.sort():**
- **sorted()**: When you need to keep the original list unchanged
- **list.sort()**: When you want to modify the list in-place (more memory efficient)
- **reverse=True**: Always prefer this over manual reversal
- **Complex keys**: Use lambda functions or operator.itemgetter for clarity
- **Multiple criteria**: Consider using tuple keys with negation for mixed sort orders
{{< /note >}}

## Linux Display Management

### arandr: GUI Frontend for xrandr

`arandr` provides a visual interface for configuring multiple monitors in tiling window managers:

```bash
# Install arandr
sudo apt install arandr

# Launch arandr
arandr

# Save configuration script
# arandr can generate shell scripts for your monitor setup
```

### xrandr Command Line Usage

```bash
# Basic xrandr commands for monitor management

# List available displays and their capabilities
xrandr

# Extended output showing all modes
xrandr --verbose

# Basic dual monitor setup
xrandr --output HDMI1 --mode 1920x1080 --right-of eDP1

# Three monitor setup
xrandr --output eDP1 --mode 1920x1080 --pos 0x0 \
       --output HDMI1 --mode 1920x1080 --pos 1920x0 \
       --output DP1 --mode 1920x1080 --pos 3840x0

# Set primary display
xrandr --output eDP1 --primary

# Rotate display
xrandr --output HDMI1 --rotate left

# Disable a display
xrandr --output HDMI1 --off

# Enable a display
xrandr --output HDMI1 --auto

# Set custom resolution
xrandr --output HDMI1 --mode 1920x1080 --rate 60

# Mirror displays
xrandr --output HDMI1 --same-as eDP1

# Create custom mode (for displays not detected properly)
gtf 1920 1080 60  # Generate modeline
xrandr --newmode "1920x1080_60.00" 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync
xrandr --addmode HDMI1 1920x1080_60.00
xrandr --output HDMI1 --mode 1920x1080_60.00
```

### Integration with Tiling Window Managers

```bash
# i3wm configuration for monitor management
# ~/.config/i3/config

# Workspace assignments to specific monitors
workspace 1 output eDP1
workspace 2 output eDP1
workspace 3 output HDMI1
workspace 4 output HDMI1
workspace 5 output DP1

# Keybindings for monitor switching
bindsym $mod+Shift+m exec arandr

# Auto-detect and configure monitors on startup
exec --no-startup-id ~/.screenlayout/default.sh

# Monitor hotplug detection
exec --no-startup-id bash -c 'while true; do sleep 1; if xrandr | grep "HDMI1 connected"; then ~/.screenlayout/dual.sh; fi; done'
```

```bash
# Example monitor configuration scripts generated by arandr

# ~/.screenlayout/single.sh (laptop only)
#!/bin/sh
xrandr --output eDP1 --primary --mode 1920x1080 --pos 0x0 --rotate normal \
       --output HDMI1 --off \
       --output DP1 --off

# ~/.screenlayout/dual.sh (laptop + external)
#!/bin/sh
xrandr --output eDP1 --primary --mode 1920x1080 --pos 0x0 --rotate normal \
       --output HDMI1 --mode 1920x1080 --pos 1920x0 --rotate normal \
       --output DP1 --off

# ~/.screenlayout/triple.sh (all monitors)
#!/bin/sh
xrandr --output eDP1 --mode 1920x1080 --pos 1920x0 --rotate normal \
       --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal \
       --output DP1 --mode 1920x1080 --pos 3840x0 --rotate normal

# Make scripts executable
chmod +x ~/.screenlayout/*.sh
```

### Automated Monitor Detection

```python
# Python script for automatic monitor configuration
#!/usr/bin/env python3
import subprocess
import re
import os

class MonitorManager:
    def __init__(self):
        self.connected_outputs = self.get_connected_outputs()
        self.config_dir = os.path.expanduser("~/.screenlayout")
    
    def get_connected_outputs(self):
        """Get list of connected monitor outputs"""
        result = subprocess.run(['xrandr'], capture_output=True, text=True)
        
        connected = []
        for line in result.stdout.split('\n'):
            if ' connected' in line and ' disconnected' not in line:
                output = line.split()[0]
                connected.append(output)
        
        return connected
    
    def detect_configuration(self):
        """Detect appropriate configuration based on connected monitors"""
        num_monitors = len(self.connected_outputs)
        
        if num_monitors == 1:
            return "single"
        elif num_monitors == 2:
            return "dual"
        elif num_monitors >= 3:
            return "triple"
        else:
            return "single"
    
    def apply_configuration(self, config_name):
        """Apply a saved monitor configuration"""
        script_path = f"{self.config_dir}/{config_name}.sh"
        
        if os.path.exists(script_path):
            subprocess.run(['bash', script_path])
            print(f"Applied configuration: {config_name}")
            return True
        else:
            print(f"Configuration not found: {script_path}")
            return False
    
    def auto_configure(self):
        """Automatically configure monitors based on detection"""
        config = self.detect_configuration()
        return self.apply_configuration(config)
    
    def list_configurations(self):
        """List available configurations"""
        if not os.path.exists(self.config_dir):
            return []
        
        configs = []
        for file in os.listdir(self.config_dir):
            if file.endswith('.sh'):
                configs.append(file[:-3])  # Remove .sh extension
        
        return configs

# Usage example
if __name__ == "__main__":
    import sys
    
    manager = MonitorManager()
    
    if len(sys.argv) > 1:
        config = sys.argv[1]
        manager.apply_configuration(config)
    else:
        print(f"Connected monitors: {manager.connected_outputs}")
        print("Auto-configuring...")
        manager.auto_configure()
        
        print(f"Available configurations: {manager.list_configurations()}")

# Save as ~/.local/bin/monitor-config
# chmod +x ~/.local/bin/monitor-config
```

{{< example title="Monitor Management Workflow" >}}
**Typical Multi-Monitor Setup Process:**
1. **Connect monitors** and boot system
2. **Launch arandr** to visually arrange displays
3. **Save configuration** as shell script
4. **Integrate with window manager** for automatic application
5. **Create hotkeys** for switching between configurations
6. **Set up hotplug detection** for dynamic configuration
{{< /example >}}

### Advanced xrandr Techniques

```bash
# Advanced monitor configuration techniques

# Scale display for HiDPI
xrandr --output eDP1 --scale 1.5x1.5

# Fractional scaling
xrandr --output eDP1 --scale 1.25x1.25

# Set specific DPI
xrandr --output eDP1 --dpi 144

# Brightness control
xrandr --output eDP1 --brightness 0.8

# Color temperature adjustment (requires redshift)
redshift -O 3000  # Warm
redshift -O 6500  # Cool
redshift -x       # Reset

# Monitor positioning with offset
xrandr --output HDMI1 --pos 1920x-200  # Slight vertical offset

# Detailed monitor information
xrandr --query --verbose | grep -A 10 "eDP1"

# Test configuration before applying
xrandr --output HDMI1 --mode 1920x1080 --dry-run
```

## Key Insights

### Python Performance Optimization

Today's exploration of `collections.defaultdict` demonstrates how choosing the right data structure can provide measurable performance improvements:

- **Algorithmic efficiency** - Single hash lookup vs multiple operations
- **Implementation details** - C-level optimizations in standard library
- **Memory patterns** - Reduced object creation and method call overhead
- **Code clarity** - Simpler, more readable code often performs better

### Linux Desktop Productivity

The combination of `arandr` and `xrandr` showcases how GUI tools can complement command-line utilities:

- **Visual configuration** - arandr for initial setup and experimentation
- **Scriptable automation** - xrandr for reproducible configurations
- **Integration points** - Window manager hooks and hotplug detection
- **Workflow optimization** - Saved configurations for different scenarios

### Development Environment Considerations

Both topics relate to optimizing development environments:

- **Code performance** affects development feedback loops
- **Monitor configuration** impacts workspace efficiency and productivity
- **Automation** reduces manual configuration overhead
- **Tool integration** creates seamless workflows

---

*Today's learning reinforced that small optimizations in both code and environment setup can compound to create significant productivity improvements over time.*