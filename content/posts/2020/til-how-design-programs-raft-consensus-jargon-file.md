---
date: 2020-12-05T10:00:00+05:30
draft: false
title:
  "TIL: How to Design Programs, Raft Consensus Algorithm, DWIM Philosophy, and
  The Jargon File"
description:
  "Today I learned about the systematic program design methodology from HtDP,
  the elegant Raft consensus algorithm visualization, the DWIM (Do What I Mean)
  principle in computing, and the legendary Jargon File documenting hacker
  culture."
tags:
  - "til"
  - "program-design"
  - "distributed-systems"
  - "consensus-algorithms"
  - "computer-culture"
  - "hacker-culture"
  - "software-philosophy"
---

## How to Design Programs (HtDP)

[How to Design Programs: An Introduction to Computing and Programming](http://htdp.org/2003-09-26/Book/curriculum.html)

Systematic methodology for program design that emphasizes thinking before
coding:

### Core Design Philosophy:

#### **The Design Recipe:**

1. **Data Analysis**: Understand the data your program processes
2. **Contract**: Specify input/output types and purpose
3. **Examples**: Create concrete examples of function behavior
4. **Template**: Write function skeleton based on data structure
5. **Body**: Fill in the function body
6. **Testing**: Verify function works with examples

#### **Example: Processing Lists**

```scheme
;; Data Definition
;; A List-of-Numbers is one of:
;; - empty
;; - (cons Number List-of-Numbers)

;; Contract and Purpose
;; sum : List-of-Numbers -> Number
;; Computes the sum of all numbers in the list

;; Examples
;; (sum empty) should produce 0
;; (sum (cons 3 (cons 7 empty))) should produce 10

;; Template (follows the data structure)
(define (sum lon)
  (cond
    [(empty? lon) ...]
    [(cons? lon) (... (first lon) ... (sum (rest lon)) ...)]))

;; Body (fill in the template)
(define (sum lon)
  (cond
    [(empty? lon) 0]
    [(cons? lon) (+ (first lon) (sum (rest lon)))]))

;; Testing
(check-expect (sum empty) 0)
(check-expect (sum (cons 3 (cons 7 empty))) 10)
```

### Key Principles:

#### **Structure Follows Data:**

```scheme
;; Binary Tree data definition
;; A BT is one of:
;; - 'leaf
;; - (make-node Number BT BT)

(define-struct node (value left right))

;; Template automatically follows data structure
(define (bt-template bt)
  (cond
    [(symbol? bt) ...]                          ; leaf case
    [(node? bt) (... (node-value bt)           ; node case
                     (bt-template (node-left bt))
                     (bt-template (node-right bt)))]))

;; Count nodes in binary tree
(define (count-nodes bt)
  (cond
    [(symbol? bt) 0]
    [(node? bt) (+ 1
                   (count-nodes (node-left bt))
                   (count-nodes (node-right bt)))]))
```

#### **Generative Recursion:**

```scheme
;; When structure doesn't follow data: generative recursion
;; Example: Collatz conjecture

;; collatz : Number -> Number
;; Counts steps to reach 1 in Collatz sequence
(define (collatz n)
  (cond
    [(= n 1) 0]
    [(even? n) (+ 1 (collatz (/ n 2)))]
    [else (+ 1 (collatz (+ (* 3 n) 1)))]))

;; Need termination argument since structure doesn't follow input
```

### Educational Benefits:

#### **Systematic Thinking:**

- **Problem Decomposition**: Break complex problems into manageable pieces
- **Type-Driven Development**: Let data definitions guide program structure
- **Test-First Mentality**: Examples before implementation
- **Refinement Process**: Iterative improvement through design recipe

#### **Transferable Skills:**

```python
# HtDP principles in Python

from typing import List, Union
from dataclasses import dataclass

# Data Definition
@dataclass
class Empty:
    pass

@dataclass
class Node:
    value: int
    rest: Union['Node', Empty]

ListOfInts = Union[Node, Empty]

# Contract and Purpose
def sum_list(lst: ListOfInts) -> int:
    """Computes the sum of all integers in the list."""

    # Examples (as doctests)
    """
    >>> sum_list(Empty())
    0
    >>> sum_list(Node(3, Node(7, Empty())))
    10
    """

    # Template follows data structure
    if isinstance(lst, Empty):
        return 0
    elif isinstance(lst, Node):
        return lst.value + sum_list(lst.rest)
```

## Raft Consensus Algorithm

[Raft Consensus Algorithm - Interactive Visualization](http://thesecretlivesofdata.com/raft/)

Elegant distributed consensus algorithm designed for understandability:

### Core Concepts:

#### **Server States:**

- **Follower**: Passive servers that respond to leaders and candidates
- **Candidate**: Server trying to become leader during election
- **Leader**: Handles all client requests and log replication

#### **Key Components:**

```
Term: Logical clock that increases monotonically
Log: Sequence of committed entries
Heartbeat: Leader sends to maintain authority
Election Timeout: Follower becomes candidate if no heartbeat
```

### Leader Election Process:

#### **Election Flow:**

```
1. Follower timeout → Become Candidate
2. Increment term, vote for self
3. Send RequestVote RPCs to all servers
4. If majority votes received → Become Leader
5. If another leader discovered → Become Follower
6. If election timeout → Start new election
```

#### **Election Safety Properties:**

```python
# Pseudo-code for election logic
class RaftServer:
    def __init__(self):
        self.state = "follower"
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.election_timeout = random_timeout()

    def start_election(self):
        self.state = "candidate"
        self.current_term += 1
        self.voted_for = self.server_id
        votes_received = 1  # Vote for self

        for server in other_servers:
            vote_granted = server.request_vote(
                term=self.current_term,
                candidate_id=self.server_id,
                last_log_index=len(self.log) - 1,
                last_log_term=self.log[-1].term if self.log else 0
            )
            if vote_granted:
                votes_received += 1

        if votes_received > len(all_servers) // 2:
            self.become_leader()
        else:
            self.become_follower()

    def request_vote(self, term, candidate_id, last_log_index, last_log_term):
        # Only vote if:
        # 1. Haven't voted in this term, or voted for this candidate
        # 2. Candidate's log is at least as up-to-date as ours
        if (term > self.current_term and
            (self.voted_for is None or self.voted_for == candidate_id) and
            self.log_is_up_to_date(last_log_index, last_log_term)):
            self.voted_for = candidate_id
            self.current_term = term
            return True
        return False
```

### Log Replication:

#### **Replication Process:**

```
1. Client sends command to leader
2. Leader appends to local log
3. Leader sends AppendEntries RPC to followers
4. Leader waits for majority acknowledgment
5. Leader commits entry and responds to client
6. Leader notifies followers of commitment
```

#### **Log Consistency:**

```python
class LogEntry:
    def __init__(self, term, command):
        self.term = term
        self.command = command

class RaftLeader:
    def replicate_entry(self, command):
        # Append to local log
        entry = LogEntry(self.current_term, command)
        self.log.append(entry)

        # Send to followers
        responses = []
        for follower in self.followers:
            response = follower.append_entries(
                term=self.current_term,
                leader_id=self.server_id,
                prev_log_index=len(self.log) - 2,
                prev_log_term=self.log[-2].term if len(self.log) > 1 else 0,
                entries=[entry],
                leader_commit=self.commit_index
            )
            responses.append(response)

        # Check for majority
        success_count = sum(1 for r in responses if r.success) + 1  # +1 for leader
        if success_count > len(self.all_servers) // 2:
            self.commit_index = len(self.log) - 1
            return True
        return False
```

### Safety Properties:

#### **Key Guarantees:**

- **Election Safety**: At most one leader per term
- **Leader Append-Only**: Leader never overwrites/deletes log entries
- **Log Matching**: If two logs contain entry with same index/term, logs
  identical up to that point
- **Leader Completeness**: If entry committed in term, present in logs of
  leaders for higher terms
- **State Machine Safety**: If server applies entry at index, no other server
  applies different entry at same index

#### **Network Partition Handling:**

```
Scenario: 5-server cluster splits into groups of 3 and 2

Group with 3 servers:
- Can elect leader (3 > 5/2)
- Can commit entries (3 > 5/2)
- Continues operating normally

Group with 2 servers:
- Cannot elect leader (2 ≤ 5/2)
- Cannot commit entries
- Remains unavailable until partition heals

When partition heals:
- Minority group adopts majority group's log
- System returns to normal operation
```

## DWIM - Do What I Mean

[DWIM - The Jargon File](http://www.catb.org/~esr/jargon/html/D/DWIM.html)

Computing philosophy emphasizing intelligent interpretation of user intent:

### Core Philosophy:

#### **Historical Context:**

- **Origin**: Warren Teitelman's BBN-LISP system (1960s-70s)
- **Goal**: Systems that understand user intent even with imperfect input
- **Trade-off**: Convenience vs. predictability

#### **Implementation Challenges:**

```lisp
;; Original DWIM in LISP
;; If user types (CAR X Y) instead of (CAR (X Y))
;; System might auto-correct to intended meaning

;; But ambiguity arises:
(SETQ FOO (CAR X Y))  ; What did user mean?
;; Option 1: (SETQ FOO (CAR (X Y)))
;; Option 2: (SETQ FOO (CAR X) Y)
;; Option 3: Syntax error
```

### Modern DWIM Examples:

#### **Successful DWIM:**

```python
# Python's flexible type system
def add_items(items):
    # Works with lists, tuples, strings, etc.
    result = []
    for item in items:  # DWIM: iterate over any iterable
        result.append(item)
    return result

# Shell command completion
$ git co<TAB>     # Expands to 'git commit' or 'git checkout'
$ ls /us/lo<TAB>  # Expands to '/usr/local'

# URL autocomplete in browsers
"github.com/user/repo" → "https://github.com/user/repo"
```

#### **Problematic DWIM:**

```javascript
// JavaScript's type coercion (too much DWIM)
"5" + 3    // "53" (string concatenation)
"5" - 3    // 2 (numeric subtraction)
[] + []    // "" (empty string)
[] + {}    // "[object Object]"
{} + []    // 0 (in some contexts)

// PHP's magic (inconsistent DWIM)
$array = [1, 2, 3];
echo $array;        // "Array" (not very helpful)
echo json_encode($array);  // "[1,2,3]" (more useful)
```

### Design Principles:

#### **Good DWIM Characteristics:**

1. **Predictable**: Users can learn and predict behavior
2. **Consistent**: Similar contexts produce similar interpretations
3. **Reversible**: Easy to undo or override automatic behavior
4. **Transparent**: Clear about what interpretation was made
5. **Conservative**: Err on side of asking rather than guessing

#### **Modern Examples:**

```python
# pandas DataFrame - good DWIM
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# These all "do what you mean" intuitively:
df['A']           # Column access
df[0:2]           # Row slicing
df[df['A'] > 1]   # Boolean indexing
df['A'] + df['B'] # Element-wise addition

# Git - good DWIM examples
git add .              # Add all changed files
git commit -am "msg"   # Add all and commit
git push              # Push to tracked upstream branch
git checkout main     # Switch to main branch
```

## The Jargon File

[The Jargon File](http://www.catb.org/~esr/jargon/html/index.html)

Comprehensive glossary of hacker slang and computing culture:

### Historical Significance:

#### **Cultural Documentation:**

- **Origins**: MIT AI Lab, Stanford, CMU hacker communities
- **Evolution**: From 1975 to present, maintained by Eric S. Raymond
- **Purpose**: Preserve and explain hacker culture terminology
- **Influence**: Shaped understanding of computing subculture

### Notable Entries:

#### **Technical Terms:**

```
Hack: (n.) 1. An elegant, clever, or inspired solution to a programming problem
      2. A quick-and-dirty fix or modification
      (v.) To program enthusiastically or obsessively

Kludge: A poorly-designed solution that works despite itself
       Etymology: From German "klug" (clever) + "fudge"

Grok: To understand something completely and intuitively
      From Robert Heinlein's "Stranger in a Strange Land"

Cruft: Accumulated junk, bugs, or poorly-designed code
       "This codebase has too much cruft"
```

#### **Cultural Concepts:**

```
Real Programmer: Mythical figure who codes in assembly language,
                 drinks coffee, and works through the night

Wizard: Programmer with deep system knowledge and seemingly
        magical abilities to fix complex problems

Guru: Expert who others consult for difficult technical problems

Mundane: Non-hacker; someone outside the computing community
```

### Programming Philosophy:

#### **Hacker Ethics (from the Jargon File):**

1. **Information wants to be free**: Open access to information and code
2. **Mistrust authority**: Decentralized decision-making
3. **Judge by hacking ability**: Meritocracy based on technical skill
4. **Computers can change life**: Technology as force for positive change
5. **Create beautiful, elegant solutions**: Aesthetic appreciation of code

#### **Design Values:**

```python
# Examples of hacker aesthetic values:

# Elegance - simple, clean solution
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

# vs. verbose alternative
def factorial_verbose(n):
    if n < 0:
        raise ValueError("Negative input not allowed")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result = result * i
    return result

# Cleverness - non-obvious but brilliant
def reverse_bits(n):
    return int(bin(n)[2:].zfill(32)[::-1], 2)

# Orthogonality - tools that compose well
# Unix philosophy: do one thing well
cat file.txt | grep "pattern" | sort | uniq -c | head -10
```

### Modern Relevance:

#### **Continuing Traditions:**

- **Open Source Movement**: Direct descendant of hacker ethics
- **Stack Overflow Culture**: Modern Q&A inherits hacker help traditions
- **Code Golf**: Competitive programming for shortest solutions
- **Easter Eggs**: Hidden features in software
- **RFC Humor**: April Fools' RFCs (like RFC 1149 - IP over Avian Carriers)

#### **Evolution of Terms:**

```
Historical: "Hacker" meant skilled programmer
Modern: Often conflated with "cracker" (malicious attacker)

Historical: "Guru" was revered expert
Modern: "Tech lead" or "Staff engineer"

Historical: "Wizard" had magical programming abilities
Modern: "10x engineer" (controversial term)

New terms: "Code smell", "Technical debt", "Yak shaving"
```

These resources represent different aspects of computing culture and
methodology - systematic program design, elegant distributed algorithms,
user-centered design philosophy, and the rich cultural history of computing
communities. Together they illustrate how technical and cultural evolution
intertwine in the computing field.
