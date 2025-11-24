---
date: 2021-01-08T10:00:00+05:30
draft: false
title:
  "TIL: Visual NumPy Guide, Advent of Code Solutions, and Johnny Decimal
  Organization System"
description:
  "Today I learned about Jay Alammar's visual guide to NumPy, exploring Peter
  Norvig's Advent of Code solutions for learning algorithms, and the Johnny
  Decimal system for organizing digital information."
tags:
  - TIL
  - NumPy
  - Data Science
  - Python
  - Advent of Code
  - Algorithms
  - Organization
  - Productivity
---

## Visual NumPy and Data Representation

[A Visual Intro to NumPy and Data Representation – Jay Alammar](https://jalammar.github.io/visual-numpy/)

Brilliant visual guide to understanding NumPy through interactive diagrams:

### Why Visual Learning Works:

- **Complex Concepts**: NumPy operations involve multi-dimensional thinking
- **Abstract Operations**: Broadcasting and reshaping are hard to visualize
  mentally
- **Mathematical Foundation**: Linear algebra concepts become clearer with
  visuals
- **Debugging Aid**: Understanding data shapes prevents common errors

### Core NumPy Concepts Visualized:

#### **Array Creation and Structure:**

```python
import numpy as np

# 1D array visualization
arr_1d = np.array([1, 2, 3, 4])
# [1] [2] [3] [4]

# 2D array (matrix) visualization
arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6]])
# [[1] [2] [3]]
# [[4] [5] [6]]

# 3D array visualization
arr_3d = np.array([[[1, 2], [3, 4]],
                   [[5, 6], [7, 8]]])
# Layer 0: [[1] [2]]  Layer 1: [[5] [6]]
#          [[3] [4]]           [[7] [8]]
```

#### **Array Operations:**

```python
# Element-wise operations visualized
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Addition: [1] + [4] = [5]
#          [2] + [5] = [7]
#          [3] + [6] = [9]
result = a + b  # [5, 7, 9]

# Broadcasting visualization
scalar = 10
# [1] + 10 = [11]
# [2] + 10 = [12]
# [3] + 10 = [13]
result = a + scalar  # [11, 12, 13]
```

### Advanced Visualizations:

#### **Matrix Multiplication:**

```python
# Dot product visualization
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

# Visual representation of A @ B:
# Row 1 of A × Column 1 of B = (1×5 + 2×7) = 19
# Row 1 of A × Column 2 of B = (1×6 + 2×8) = 22
# Row 2 of A × Column 1 of B = (3×5 + 4×7) = 43
# Row 2 of A × Column 2 of B = (3×6 + 4×8) = 50
result = A @ B  # [[19, 22], [43, 50]]
```

#### **Reshaping and Indexing:**

```python
# Original shape: (6,)
arr = np.array([1, 2, 3, 4, 5, 6])

# Reshape to (2, 3):
# [[1] [2] [3]]
# [[4] [5] [6]]
reshaped = arr.reshape(2, 3)

# Reshape to (3, 2):
# [[1] [2]]
# [[3] [4]]
# [[5] [6]]
reshaped = arr.reshape(3, 2)
```

### Practical Applications:

#### **Data Science Workflows:**

```python
# Image processing example
image = np.random.rand(256, 256, 3)  # Height, Width, RGB channels

# Grayscale conversion (visual: RGB → single channel)
grayscale = np.mean(image, axis=2)   # Average across color channels

# Image resizing (visual: larger/smaller grid)
resized = image[::2, ::2, :]         # Every other pixel
```

#### **Machine Learning Data:**

```python
# Dataset visualization
X = np.random.rand(1000, 10)  # 1000 samples, 10 features
y = np.random.randint(0, 2, 1000)  # Binary labels

# Feature normalization (visual: data distribution shifting)
X_normalized = (X - X.mean(axis=0)) / X.std(axis=0)

# Train/test split (visual: data partitioning)
split_idx = int(0.8 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
```

### Learning Benefits:

- **Intuitive Understanding**: See what operations actually do to data
- **Debugging Skills**: Quickly spot shape mismatches and dimensionality issues
- **Performance Awareness**: Understand which operations are efficient
- **Mathematical Connection**: Bridge between code and underlying mathematics

## Advent of Code - Learning Through Problem Solving

[My solutions and walkthroughs for Advent of Code](https://github.com/mebeim/aoc)
[Peter Norvig's Advent of Code 2020 Solutions](https://github.com/norvig/pytudes/blob/master/ipynb/Advent-2020.ipynb)

Exploring algorithmic problem-solving through Advent of Code challenges:

### What is Advent of Code:

- **Daily Programming Puzzles**: 25 problems released from Dec 1-25
- **Increasing Difficulty**: Problems get progressively harder
- **Algorithmic Focus**: Emphasis on data structures and algorithms
- **Multiple Languages**: Solve in any programming language

### Learning from Peter Norvig's Solutions:

#### **Elegant Python Patterns:**

```python
# Pattern: Generator expressions for parsing
def parse_input(text):
    return [list(map(int, line.split())) for line in text.strip().split('\n')]

# Pattern: Using collections.Counter for frequency analysis
from collections import Counter
def find_mode(items):
    return Counter(items).most_common(1)[0]

# Pattern: Recursive solutions with memoization
from functools import lru_cache

@lru_cache(maxsize=None)
def count_arrangements(adapters, index=0):
    if index == len(adapters) - 1:
        return 1
    return sum(count_arrangements(adapters, i)
               for i in range(index + 1, len(adapters))
               if adapters[i] - adapters[index] <= 3)
```

#### **Data Structure Selection:**

```python
# Using sets for fast membership testing
visited = set()
if position not in visited:
    visited.add(position)

# Using deque for efficient queue operations
from collections import deque
queue = deque([start_position])
while queue:
    current = queue.popleft()

# Using complex numbers for 2D coordinates
position = 0 + 0j  # (0, 0)
directions = [1, -1, 1j, -1j]  # right, left, up, down
new_position = position + directions[0]  # Move right
```

### Algorithm Categories in AoC:

#### **Graph Algorithms:**

- **BFS/DFS**: Pathfinding and reachability
- **Dijkstra**: Shortest path with weights
- **Topological Sort**: Dependency resolution
- **Connected Components**: Network analysis

#### **Dynamic Programming:**

- **Memoization**: Avoid recomputing subproblems
- **Bottom-up**: Build solutions incrementally
- **State Space**: Define problem states clearly
- **Optimization**: Find optimal solutions

#### **Pattern Recognition:**

- **Cycle Detection**: Find repeating patterns
- **State Machines**: Model system behavior
- **Regular Expressions**: Text parsing and matching
- **Mathematical Sequences**: Number theory problems

### Best Practices from Expert Solutions:

#### **Code Organization:**

```python
def solve_part1(input_text):
    data = parse_input(input_text)
    return process_data_part1(data)

def solve_part2(input_text):
    data = parse_input(input_text)
    return process_data_part2(data)

def parse_input(text):
    # Centralized parsing logic
    pass

# Separate parsing from solving
# Reusable functions for both parts
```

#### **Testing and Validation:**

```python
def test_with_examples():
    example_input = """..."""
    assert solve_part1(example_input) == expected_result
    print("Part 1 example passed!")

# Always test with provided examples first
# Use assertions to catch regressions
```

## Johnny Decimal Organization System

[Home | Johnny•Decimal](https://johnnydecimal.com/)

Revolutionary system for organizing digital information and files:

### The Core Concept:

- **Hierarchical Structure**: 10 areas, 10 categories each, unlimited items
- **Numeric Identification**: Every item gets a unique number
- **Search Friendly**: Find anything by its number
- **Scalable**: Works for personal and business organization

### System Structure:

#### **Three Levels:**

```
Areas (10-19, 20-29, 30-39, etc.)
├── Categories (11, 12, 13, etc.)
    └── Items (11.01, 11.02, 11.03, etc.)
```

#### **Example Implementation:**

```
10-19 Personal Development
├── 11 Learning & Education
│   ├── 11.01 Online Courses
│   ├── 11.02 Books to Read
│   └── 11.03 Skill Practice
├── 12 Health & Fitness
│   ├── 12.01 Workout Plans
│   ├── 12.02 Meal Planning
│   └── 12.03 Medical Records
└── 13 Career Development
    ├── 13.01 Resume Versions
    ├── 13.02 Portfolio Projects
    └── 13.03 Interview Prep

20-29 Home & Life Management
├── 21 Financial Management
├── 22 Home Maintenance
└── 23 Travel & Vacation
```

### Digital Implementation:

#### **File System Organization:**

```
/Documents/
├── 11.01 Online Courses/
│   ├── python-course/
│   └── design-fundamentals/
├── 11.02 Books to Read/
│   ├── programming-books.md
│   └── business-books.md
├── 21.01 Budget & Expenses/
│   ├── 2021-budget.xlsx
│   └── monthly-tracking.xlsx
└── 21.02 Tax Documents/
    ├── 2020-tax-return.pdf
    └── receipts/
```

#### **Note-Taking Integration:**

```markdown
# 11.03 Daily Learning Notes

## 2021-01-08 - NumPy Visualization Study

- Reviewed Jay Alammar's visual NumPy guide
- Key insight: Broadcasting is like stretching arrays
- Next: Practice with real dataset

## Cross-references:

- See 13.02 for portfolio project using NumPy
- See 21.03 for data analysis of expenses
```

### Benefits of the System:

#### **Cognitive Load Reduction:**

- **No More "Where Did I Put That?"**: Everything has a number
- **Consistent Structure**: Same hierarchy everywhere
- **Muscle Memory**: Numbers become automatic
- **Reduced Decisions**: Clear place for everything

#### **Scalability:**

- **Personal Use**: Organize your entire digital life
- **Team Projects**: Shared understanding of structure
- **Business Applications**: Department and project organization
- **Long-term Maintenance**: Structure remains stable over time

### Implementation Tips:

#### **Getting Started:**

1. **Audit Current Organization**: What areas of life/work do you manage?
2. **Define Areas**: 10 broad categories (can use fewer initially)
3. **Break Down Categories**: What subcategories exist in each area?
4. **Assign Numbers**: Start with most important/frequent items
5. **Iterate**: Refine structure as you use it

#### **Digital Tools Integration:**

```python
# Python script to create Johnny Decimal folder structure
import os

areas = {
    10: "Personal Development",
    20: "Home & Life Management",
    30: "Work Projects"
}

categories = {
    11: "Learning & Education",
    12: "Health & Fitness",
    21: "Financial Management",
    22: "Home Maintenance"
}

def create_structure(base_path):
    for area_num, area_name in areas.items():
        area_path = f"{base_path}/{area_num}-{area_num+9} {area_name}"
        os.makedirs(area_path, exist_ok=True)

        for cat_num, cat_name in categories.items():
            if area_num <= cat_num < area_num + 10:
                cat_path = f"{area_path}/{cat_num} {cat_name}"
                os.makedirs(cat_path, exist_ok=True)
```

These three resources represent different approaches to managing complexity -
visual learning for technical concepts, structured problem-solving for algorithm
development, and systematic organization for information management.
