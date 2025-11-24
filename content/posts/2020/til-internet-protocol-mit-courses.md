---
date: 2020-11-09T10:00:00+05:30
draft: false
title:
  "TIL: Internet Protocol RFC 760, MIT Algorithms Course, and Mathematics for
  Computer Science"
description:
  "Today I learned about the foundational Internet Protocol specification from
  1980, MIT's comprehensive algorithms course, and their mathematics for
  computer science curriculum."
tags:
  - til
  - networking
  - algorithms
  - mathematics
  - computer-science
  - mit
  - protocols
---

Today's learning focused on foundational computer science concepts, from
networking protocols to algorithmic thinking and mathematical foundations.

## DoD RFC 760 - Internet Protocol

[RFC 760](https://tools.ietf.org/html/rfc760) represents the original Internet
Protocol specification from January 1980, laying the groundwork for modern
internet communication.

### Historical Significance:

#### **Original Design Principles:**

- **Simplicity**: Minimal functionality for maximum reliability
- **Datagram service**: Connectionless, best-effort delivery
- **End-to-end principle**: Intelligence at endpoints, not in network
- **Scalability**: Design for networks of arbitrary size

#### **Core Protocol Features:**

```
Internet Header Format (RFC 760):
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version|  IHL  |Type of Service|          Total Length         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Identification        |Flags|      Fragment Offset    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Time to Live |    Protocol   |         Header Checksum       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                       Source Address                          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Destination Address                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Key Innovations:

#### **Addressing System:**

- **32-bit addresses**: Sufficient for early internet scale
- **Network/Host division**: Hierarchical addressing structure
- **Address classes**: Class A, B, C for different network sizes
- **Subnet concept**: Logical network subdivision

#### **Fragmentation and Reassembly:**

```python
# Conceptual fragmentation algorithm
def fragment_packet(packet, mtu):
    header_size = 20  # Basic IP header
    payload_size = mtu - header_size

    fragments = []
    offset = 0

    while offset < len(packet.data):
        fragment_data = packet.data[offset:offset + payload_size]

        fragment = IPPacket(
            identification=packet.identification,
            flags=0x2000 if offset + payload_size < len(packet.data) else 0,  # More fragments flag
            fragment_offset=offset // 8,  # 8-byte units
            data=fragment_data
        )

        fragments.append(fragment)
        offset += payload_size

    return fragments
```

### Evolution to Modern Internet:

The principles established in RFC 760 continue to influence modern networking,
despite the transition from IPv4 to IPv6 and the addition of numerous extensions
and optimizations.

## MIT 6.006 - Introduction to Algorithms

[MIT's Introduction to Algorithms](https://www.youtube.com/playlist?list=PLUl4u3cNGP61Oq3tWYp6V_F-5jb5L2iHb)
provides comprehensive coverage of algorithmic thinking and analysis techniques.

### Course Structure:

#### **Fundamental Concepts:**

- **Asymptotic analysis**: Big O, Omega, and Theta notation
- **Correctness proofs**: Loop invariants and induction
- **Problem-solving strategies**: Divide and conquer, dynamic programming,
  greedy algorithms

#### **Core Algorithms:**

##### **Sorting and Searching:**

```python
# Merge sort implementation with analysis
def merge_sort(arr):
    """
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    Recurrence: T(n) = 2T(n/2) + O(n)
    """
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
```

##### **Graph Algorithms:**

```python
# Breadth-first search for shortest paths
from collections import deque

def bfs_shortest_path(graph, start, end):
    """
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    if start == end:
        return [start]

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]

                if neighbor == end:
                    return new_path

                queue.append((neighbor, new_path))
                visited.add(neighbor)

    return None  # No path found
```

#### **Dynamic Programming:**

```python
# Classic dynamic programming example
def longest_common_subsequence(s1, s2):
    """
    Time Complexity: O(mn)
    Space Complexity: O(mn)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

## MIT 6.042J - Mathematics for Computer Science

[Mathematics for Computer Science](https://www.youtube.com/playlist?list=PLB7540DEDD482705B)
covers essential mathematical foundations for computer science.

### Core Mathematical Areas:

#### **Discrete Mathematics:**

- **Set theory**: Foundations of mathematical reasoning
- **Logic**: Propositional and predicate logic
- **Proof techniques**: Direct proof, contradiction, induction
- **Combinatorics**: Counting principles and probability

#### **Mathematical Proofs:**

```
Proof by Induction Template:

Base case: Prove P(1) is true
Inductive step: Assume P(k) is true for some k ≥ 1
               Prove P(k+1) is true
Conclusion: P(n) is true for all n ≥ 1

Example - Sum of first n natural numbers:
Claim: 1 + 2 + ... + n = n(n+1)/2

Base case: n = 1
Left side: 1
Right side: 1(1+1)/2 = 1 ✓

Inductive step: Assume true for k
1 + 2 + ... + k = k(k+1)/2

Prove for k+1:
1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1)
                        = (k+1)(k/2 + 1)
                        = (k+1)(k+2)/2 ✓
```

#### **Graph Theory:**

- **Graph properties**: Connectivity, cycles, trees
- **Graph algorithms**: Traversal, shortest paths, minimum spanning trees
- **Network analysis**: Flow networks, matching problems

#### **Probability and Statistics:**

```python
# Probability distributions in algorithm analysis
import random

def expected_comparison_quicksort(n):
    """
    Expected number of comparisons in quicksort
    E[X] = 2(n+1)H_n - 2n where H_n is nth harmonic number
    """
    harmonic_n = sum(1/i for i in range(1, n+1))
    return 2 * (n + 1) * harmonic_n - 2 * n

# Random algorithm example
def randomized_quickselect(arr, k):
    """
    Expected time: O(n)
    Worst case: O(n²)
    """
    if len(arr) == 1:
        return arr[0]

    pivot = random.choice(arr)
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]

    if k < len(less):
        return randomized_quickselect(less, k)
    elif k < len(less) + len(equal):
        return pivot
    else:
        return randomized_quickselect(greater, k - len(less) - len(equal))
```

These foundational resources provide the mathematical and algorithmic thinking
skills essential for advanced computer science work, from protocol design to
efficient algorithm implementation.
