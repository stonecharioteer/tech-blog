---
date: 2021-03-02T10:00:00+05:30
draft: false
title: "TIL: Comprehensive Distributed Systems Reading List"
description:
  "Today I learned about a curated reading list for understanding distributed
  systems, covering essential papers, books, and resources for building
  scalable, fault-tolerant systems."
tags:
  - TIL
  - Distributed Systems
  - System Design
  - Research Papers
  - Architecture
---

## Distributed Systems Reading List

[Distributed Systems Reading List](https://dancres.github.io/Pages/)

Curated collection of essential resources for understanding distributed systems:

### Why Study Distributed Systems:

- **Scale Requirements**: Modern applications require distribution across
  multiple machines
- **Fault Tolerance**: Systems must continue operating despite component
  failures
- **Performance**: Distribution enables parallel processing and reduced latency
- **Availability**: Geographic distribution improves service availability

### Core Topics Covered:

#### **Foundational Papers:**

- **Time and Ordering**: Lamport timestamps and vector clocks
- **Consensus**: Paxos, Raft, and Byzantine fault tolerance
- **Consistency Models**: CAP theorem, ACID vs BASE properties
- **Failure Detection**: Detecting node failures in distributed environments

#### **Distributed Data Management:**

- **Replication**: Primary-backup, multi-master, and quorum-based systems
- **Partitioning**: Sharding strategies and partition tolerance
- **Distributed Transactions**: Two-phase commit, saga pattern
- **Eventually Consistent Systems**: CRDTs and conflict resolution

### Essential Reading Categories:

#### **Classic Papers:**

1. **"Time, Clocks, and the Ordering of Events"** - Leslie Lamport
   - Fundamental concepts of distributed system ordering
   - Logical timestamps and causality

2. **"The Byzantine Generals Problem"** - Lamport, Shostak, Pease
   - Fault tolerance in the presence of malicious actors
   - Foundation for blockchain consensus algorithms

3. **"Impossibility of Distributed Consensus"** - Fischer, Lynch, Paterson
   - Theoretical limits of distributed agreement
   - FLP impossibility result

#### **Modern System Papers:**

1. **"The Google File System"** - Ghemawat, Gobioff, Leung
   - Large-scale distributed file system design
   - Principles applied in HDFS and other systems

2. **"MapReduce: Simplified Data Processing"** - Dean & Ghemawat
   - Programming model for large-scale data processing
   - Foundation for modern big data systems

3. **"Dynamo: Amazon's Highly Available Key-value Store"**
   - Eventually consistent distributed storage
   - Influenced Cassandra, Riak, and other NoSQL systems

### Practical System Design:

#### **Consistency Patterns:**

- **Strong Consistency**: All nodes see the same data simultaneously
- **Eventual Consistency**: Nodes will eventually converge to the same state
- **Weak Consistency**: No guarantees about when consistency will be achieved
- **Causal Consistency**: Related operations maintain their causal order

#### **Availability Patterns:**

- **Fail-over**: Active-passive and active-active configurations
- **Replication**: Master-slave and master-master setups
- **Load Balancing**: Distributing traffic across multiple servers
- **Circuit Breakers**: Preventing cascade failures

### Modern Distributed Systems:

#### **Microservices Architecture:**

- **Service Discovery**: How services find and communicate with each other
- **API Gateway**: Single entry point for client requests
- **Event Sourcing**: State changes as sequence of events
- **CQRS**: Command Query Responsibility Segregation

#### **Container Orchestration:**

- **Kubernetes**: Container orchestration and service mesh
- **Service Mesh**: Infrastructure layer for service communication
- **Observability**: Monitoring, logging, and tracing in distributed systems

### Implementation Challenges:

#### **Network Partitions:**

- **Split-brain**: When network partition creates multiple active leaders
- **Quorum Systems**: Majority-based decision making
- **Partition Tolerance**: System continues operating during network splits

#### **Data Consistency:**

- **Read Repair**: Fixing inconsistencies during read operations
- **Anti-entropy**: Background processes to synchronize replicas
- **Version Vectors**: Tracking causality in distributed updates

### Learning Path:

#### **Beginner Level:**

1. Understand CAP theorem and its implications
2. Learn about basic replication strategies
3. Study simple consensus algorithms like Raft

#### **Intermediate Level:**

1. Deep dive into Paxos and its variants
2. Understand distributed transaction protocols
3. Learn about conflict-free replicated data types (CRDTs)

#### **Advanced Level:**

1. Study Byzantine fault tolerance algorithms
2. Understand advanced consistency models
3. Learn about cutting-edge research in distributed systems

### Practical Applications:

- **Database Systems**: Distributed databases like Cassandra, MongoDB
- **Message Queues**: Apache Kafka, RabbitMQ clustering
- **Caching Systems**: Redis clustering, Memcached
- **Storage Systems**: Distributed file systems, object storage

This reading list provides a structured approach to understanding the
theoretical foundations and practical implementations of distributed systems,
essential knowledge for building modern scalable applications.
