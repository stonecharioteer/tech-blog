---
date: 2021-01-17T12:10:57+05:30
draft: true
title: "A Half Hour To Learn Data Structures And Algorithms"
description: "A high-level overview of essential data structures and algorithms for self-taught developers preparing for technical interviews, with practical Python examples."
tags:
  - data-structures-and-algorithms
  - python
  - interview-prep
  - learning
  - programming-tutorials
---

As a self-taught developer, one of my weaknesses is interviewing. I suck at taking leetcode-style tests, and I am held back by my knowledge of algorithms and data structures. One of the things I hope to fix is the latter part, and I hope it will lead to the remediation of the former.

In this article, which will quite possibly delve not further than a high level into the topic, I will go through all the data structures and algorithms I've come across thus far in my interview process.

## Data Structures

In programming, a data structure is *something* that holds data and offers it to the user (*sic.* programmer) in an accessible way. Data Structures are different tools, to speak of it in a tooling paradigm, and they are often misused by a developer because they didn't take the time to learn how to use it, or that such tools are available.

In learning a language, and for this article, I will be using Python, you often learn the basic constructs that the language offers and don't realize that the built-in tools can often be used to construct more complex tools.

The reason why you don't want to use the *default* constructs as a solve-it-all macguffin is that it is not always optimal. Sometimes, the way that a particular data structure offers up its data is not *meant* to be used in the way that you are attempting to use it.

### Python List Operations Performance

Here's a breakdown of common Python list operations and their time complexities:

| Operation | Description | Time Complexity |
|-----------|-------------|-----------------|
| `list[i]` | Indexing a list | O(1) |
| `list[i] = x` | Indexed Assignment | O(1) |
| `list.append(item)` | Appending to a list | O(1) |
| `list.pop()` | Remove last item | O(1) |
| `list.pop(i)` | Remove item at index i | O(n) |
| `list.insert(i, item)` | Insert at index | O(n) |
| `del list` | Delete the list | O(n) |
| `for item in list` | Iterate through list | O(n) |
| `item in list` | Check if contains | O(n) |
| `list[i:j]` | Get slice | O(k) where k = j-i |
| `list.reverse()` | Reverse list | O(n) |
| `list1 + list2` | Concatenate lists | O(n) |
| `list.sort()` | Sort list | O(n log n) |

{{< note title="Performance Matters" >}}
Understanding these time complexities helps you choose the right data structure for your specific use case. A list might be perfect for some operations but terrible for others.
{{< /note >}}

### Linked Lists

Adding an item to a list at a non-final position takes O(n) time. So when you have a list that is *unordered*, and this order therein has some meaning to the list, you'd need a data structure that allows you to add an item *anywhere* in the list with O(1) time. It becomes especially necessary when you're adding an item *after* another item.

Think of a bookshelf, for example. You not only want to add a book at the very end of a shelf, but you might want to place it *next to* another in the shelf, perhaps a series. If you knew where the reference book was, it makes *no sense* to spend O(n) time looking for it. That would be like saying you want to *reindex* your entire bookshelf just to add a new book.

This is where you'd need a Linked List. A Linked List is a data structure wherein every item knows its predecessor and its successor. Each item is connected to its *immediate* neighbours.

```python
class Node:
    def __init__(self, data):
        self._data = data
        self._next = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

class LinkedList:
    """Linked List class definition"""
    def __init__(self):
        self._head = None

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, head):
        self._head = head

    def is_empty(self):
        return self._head is None

    def add(self, item):
        """Adds an item to the top of the list."""
        temp_node = Node(item)
        temp_node.next = self.head
        self.head = temp_node

    def __len__(self):
        current = self.head
        count = 0
        while current is not None:
            count += 1
            current = current.next
        return count

    def find(self, item):
        current = self.head
        while current is not None:
            if current.data == item:
                return current
            else:
                current = current.next
        return None

    def remove(self, item):
        current = self.head
        previous = None
        while current is not None:
            if current.data == item:
                if previous is None:  # Removing first item
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False
```

**Advantages of Linked Lists:**
- Dynamic size - grows and shrinks during runtime
- Efficient insertion/deletion at any position if you have a reference to the node
- Memory efficient - only allocates what's needed

**Disadvantages:**
- No random access - must traverse from head to reach an element
- Extra memory overhead for storing pointers
- Not cache-friendly due to non-contiguous memory layout

### Stacks

A stack is a Last In, First Out (LIFO) data structure. Think of it like a stack of plates - you can only add or remove plates from the top.

```python
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        """Add item to top of stack"""
        self.items.append(item)

    def pop(self):
        """Remove and return top item"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        """Return top item without removing it"""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def size(self):
        return len(self.items)
```

**Common uses for stacks:**
- Function call management (call stack)
- Undo operations in applications
- Expression evaluation and syntax parsing
- Backtracking algorithms

### Queues

A queue is a First In, First Out (FIFO) data structure. Think of it like a line at a store - first person in line is the first to be served.

```python
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        """Add item to rear of queue"""
        self.items.append(item)

    def dequeue(self):
        """Remove and return front item"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.popleft()

    def size(self):
        return len(self.items)
```

**Common uses for queues:**
- Process scheduling in operating systems
- Breadth-first search in graphs
- Handling requests in web servers
- Print job management

### Trees

Trees are hierarchical data structures with a root node and child nodes. Each node can have zero or more children.

```python
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + "|__" if self.parent else ""
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()
```

**Binary Search Tree (BST)**:
A special type of tree where each node has at most two children, and the left child is smaller than the parent, while the right child is larger.

```python
class BSTNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def insert(self, data):
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = BSTNode(data)
        elif data > self.data:
            if self.right:
                self.right.insert(data)
            else:
                self.right = BSTNode(data)

    def search(self, val):
        if val == self.data:
            return True
        if val < self.data:
            if self.left:
                return self.left.search(val)
            else:
                return False
        if val > self.data:
            if self.right:
                return self.right.search(val)
            else:
                return False
```

### Graphs

Graphs consist of vertices (nodes) connected by edges. They can represent networks, relationships, and many real-world problems.

```python
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)  # For undirected graph

    def print_graph(self):
        for vertex in self.graph:
            print(f"{vertex}: {self.graph[vertex]}")
```

## Algorithms

### Sorting Algorithms

#### Bubble Sort
The simplest but least efficient sorting algorithm. Repeatedly steps through the list, compares adjacent elements and swaps them if they're in the wrong order.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Time Complexity: O(n²)
# Space Complexity: O(1)
```

#### Quick Sort
A divide-and-conquer algorithm that picks a 'pivot' element and partitions the array around it.

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Time Complexity: O(n log n) average, O(n²) worst case
# Space Complexity: O(log n)
```

#### Merge Sort
Another divide-and-conquer algorithm that divides the array into halves, sorts them, then merges them back.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Time Complexity: O(n log n)
# Space Complexity: O(n)
```

### Searching Algorithms

#### Linear Search
Sequentially checks each element until the target is found.

```python
def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

# Time Complexity: O(n)
# Space Complexity: O(1)
```

#### Binary Search
Efficiently searches a sorted array by repeatedly dividing the search interval in half.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Time Complexity: O(log n)
# Space Complexity: O(1)
```

### Graph Algorithms

#### Breadth-First Search (BFS)
Explores all vertices at the current depth before moving to vertices at the next depth level.

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []
    
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return result
```

#### Depth-First Search (DFS)
Explores as far as possible along each branch before backtracking.

```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    
    return result
```

## Key Takeaways for Interviews

### When to Use What

- **Arrays/Lists**: When you need random access and the size is relatively stable
- **Linked Lists**: When you frequently insert/delete at arbitrary positions
- **Stacks**: For problems involving recursion, parsing, or "undo" functionality
- **Queues**: For problems involving processing in order or breadth-first operations
- **Trees**: For hierarchical data or when you need efficient searching/sorting
- **Graphs**: For network problems, pathfinding, or relationship modeling

### Common Interview Patterns

1. **Two Pointers**: Use for array problems involving pairs or subarrays
2. **Sliding Window**: For substring/subarray problems with constraints
3. **Divide and Conquer**: Break problems into smaller subproblems
4. **Dynamic Programming**: When problems have overlapping subproblems
5. **Backtracking**: For exploring all possible solutions

{{< tip title="Practice Strategy" >}}
Focus on understanding the **why** behind each data structure and algorithm rather than just memorizing implementations. Being able to explain trade-offs and use cases is more valuable than perfect syntax.
{{< /tip >}}

## Conclusion

Data structures and algorithms form the foundation of efficient programming. While this overview covers the basics, the key to mastering them is practice and understanding when to apply each tool.

For interview preparation, focus on:
1. Understanding time and space complexity
2. Being able to implement basic structures from scratch
3. Recognizing patterns in problems
4. Practicing on platforms like LeetCode, HackerRank, or CodeSignal

Remember, as a self-taught developer, your practical experience is valuable. These fundamentals will help you articulate your problem-solving approach and choose the right tools for the job.

The goal isn't to memorize every algorithm, but to understand the principles so you can reason about problems effectively and communicate your thought process clearly during interviews.