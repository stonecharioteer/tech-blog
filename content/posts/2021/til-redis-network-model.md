---
date: 2021-02-20T10:00:00+05:30
draft: false
title: "TIL: Redis Network Model and Internal Architecture"
description:
  "Today I learned about Redis's sophisticated network model, event-driven
  architecture, and internal implementation details that make it one of the
  fastest in-memory data stores."
tags:
  - TIL
  - Redis
  - Networking
  - Architecture
  - Performance
  - Event-driven
---

## Redis Network Model Analysis

[Detailed analysis on the source code of redis network model](https://developpaper.com/detailed-analysis-on-the-source-code-of-redis-network-model/)

Deep dive into how Redis achieves exceptional performance through its network
architecture:

### Event-Driven Architecture:

#### **Single-Threaded Event Loop:**

- **Main Thread**: All Redis operations run in a single thread
- **Non-blocking I/O**: Uses epoll/kqueue for efficient I/O multiplexing
- **Event Processing**: Commands processed sequentially without context
  switching
- **Atomicity**: Single-threaded nature ensures atomic operations

#### **Event Types:**

```c
// File events for network I/O
#define AE_READABLE     1   // Socket ready for reading
#define AE_WRITABLE     2   // Socket ready for writing

// Time events for periodic tasks
typedef struct aeTimeEvent {
    long long id;           // Time event identifier
    long when_sec;          // When to fire (seconds)
    long when_ms;           // When to fire (milliseconds)
    aeTimeProc *timeProc;   // Time event handler
} aeTimeEvent;
```

### Network I/O Implementation:

#### **Client Connection Handling:**

1. **Accept Phase**: New client connections accepted
2. **Read Phase**: Commands read from client sockets
3. **Process Phase**: Commands executed in Redis core
4. **Write Phase**: Responses written back to clients
5. **Cleanup Phase**: Closed connections handled

#### **Buffer Management:**

```c
typedef struct client {
    int fd;                 // Client socket file descriptor
    sds querybuf;           // Input buffer for commands
    list *reply;            // Output buffer list
    unsigned long reply_bytes; // Bytes in output buffer
    size_t querybuf_peak;   // Peak query buffer size
} client;
```

### Performance Optimizations:

#### **Pipeline Support:**

- **Batch Processing**: Multiple commands in single network round-trip
- **Reduced Latency**: Fewer network calls for better performance
- **Buffer Reuse**: Efficient memory management for pipelined requests

#### **Memory Efficiency:**

- **Zero-Copy**: Direct buffer manipulation where possible
- **Pooled Buffers**: Reuse of network buffers
- **Lazy Deletion**: Deferred cleanup of large objects

## Redis Under the Hood

[Redis: under the hood](https://www.pauladamsmith.com/articles/redis-under-the-hood.html)

Comprehensive exploration of Redis internal data structures and algorithms:

### Core Data Structures:

#### **String Implementation:**

```c
struct sdshdr {
    int len;        // String length
    int free;       // Available space
    char buf[];     // Actual string data
};
```

**Features:**

- **Dynamic Sizing**: Automatic growth and shrinkage
- **Binary Safe**: Can store any byte sequence
- **Memory Efficient**: Minimal overhead compared to C strings
- **O(1) Length**: Length stored, not calculated

#### **Hash Table (Dict):**

```c
typedef struct dict {
    dictType *type;     // Type-specific functions
    void *privdata;     // Private data
    dictht ht[2];       // Two hash tables for rehashing
    int rehashidx;      // Rehashing progress (-1 if not rehashing)
} dict;
```

**Rehashing Strategy:**

- **Incremental Rehashing**: Gradual migration to avoid blocking
- **Progressive**: Few entries moved per operation
- **Dual Tables**: Old and new tables coexist during rehashing

### Advanced Features:

#### **Expiration Mechanism:**

```c
// Expiration strategies
#define EXPIRE_STRATEGY_ACTIVE    1  // Active expiration
#define EXPIRE_STRATEGY_PASSIVE   2  // Lazy expiration

// Expire dictionary tracks TTL
dict *expires;  // Maps keys to expiration times
```

**Implementation:**

- **Active Expiration**: Background task removes expired keys
- **Passive Expiration**: Keys checked on access
- **Sampling**: Random sampling to find expired keys efficiently

#### **Memory Management:**

- **Object Encoding**: Different encodings for memory efficiency
- **Reference Counting**: Shared objects for memory savings
- **Copy-on-Write**: Efficient forking for persistence

### Persistence Models:

#### **RDB (Redis Database) Snapshots:**

- **Fork-based**: Child process handles disk I/O
- **Compressed**: Efficient binary format
- **Point-in-time**: Consistent snapshots
- **Configurable**: Various trigger conditions

#### **AOF (Append Only File):**

- **Command Logging**: Every write command logged
- **Replayable**: Reconstruct state by replaying commands
- **Rewriting**: Periodic compaction of log files
- **Fsync Options**: Different durability guarantees

### Scaling Patterns:

#### **Replication:**

```
Master ──┬── Slave 1
         ├── Slave 2
         └── Slave N
```

**Features:**

- **Asynchronous**: Non-blocking replication
- **Partial Resync**: Resume from disconnection point
- **Read Scaling**: Distribute read load across replicas

#### **Clustering:**

```
Cluster Node 1 ─┬─ Hash Slots 0-5460
Cluster Node 2 ─┼─ Hash Slots 5461-10922
Cluster Node 3 ─┴─ Hash Slots 10923-16383
```

**Implementation:**

- **Hash Slots**: 16384 slots distributed across nodes
- **Client-side Routing**: Clients calculate target node
- **Automatic Failover**: Master failures handled automatically
- **Resharding**: Live migration of slots between nodes

### Performance Characteristics:

#### **Operation Complexity:**

```
GET/SET:        O(1)
LPUSH/RPUSH:    O(1)
LRANGE:         O(S+N) where S=start, N=elements
SADD:           O(1)
SINTER:         O(N*M) where N=smallest set
ZADD:           O(log(N))
ZRANGE:         O(log(N)+M) where M=elements returned
```

#### **Memory Usage:**

- **Overhead**: ~20-30% overhead for Redis objects
- **Encoding Optimization**: Automatic selection of efficient encodings
- **Compression**: Option to trade CPU for memory savings

### Production Considerations:

#### **Configuration Tuning:**

```
# Memory
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1      # Save if 1 key changed in 900 seconds
save 300 10     # Save if 10 keys changed in 300 seconds
save 60 10000   # Save if 10000 keys changed in 60 seconds

# Network
tcp-backlog 511
timeout 0
tcp-keepalive 300
```

#### **Monitoring Metrics:**

- **Memory Usage**: Watch for memory pressure
- **Command Latency**: Monitor P99 latencies
- **Connection Count**: Track client connections
- **Persistence Metrics**: RDB/AOF performance
- **Replication Lag**: Master-slave synchronization delay

Redis's architecture demonstrates how careful design of data structures, memory
management, and I/O handling can create exceptionally high-performance systems
while maintaining simplicity and reliability.
