---
date: 2020-12-17T10:00:00+05:30
draft: false
title:
  "TIL: Zettelkasten Knowledge Management, Tmuxinator Templates, and Engineering
  Napkin Math"
description:
  "Today I learned about the Zettelkasten method for building interconnected
  knowledge systems, using Tmuxinator for tmux session templating, and advanced
  napkin math techniques for system estimation."
tags:
  - "til"
  - "knowledge-management"
  - "zettelkasten"
  - "tmux"
  - "tmuxinator"
  - "system-design"
  - "estimation"
  - "sre"
---

## Zettelkasten Knowledge Management System

[Zettelkasten knowledge and info management • Zettelkasten Method](https://zettelkasten.de/)

Revolutionary approach to building interconnected knowledge systems:

### Core Principles:

#### **Atomic Notes:**

- **One Idea Per Note**: Each note should contain exactly one concept
- **Unique Identifiers**: Every note gets a permanent, unique ID
- **Self-Contained**: Notes should be understandable without context
- **Evergreen**: Notes are continuously refined and updated

#### **Interconnected Structure:**

```
Note ID: 202012171030
Title: Python Memory Management
Content: Python uses reference counting combined with cycle detection...
Links: [[202012150945 - Garbage Collection]], [[202012160800 - CPython Internals]]
Tags: #python #memory #performance

Note ID: 202012150945
Title: Garbage Collection Algorithms
Content: Garbage collection algorithms can be categorized into...
Links: [[202012171030 - Python Memory Management]], [[202012140630 - JVM Memory]]
Tags: #algorithms #memory #gc
```

### Implementation Strategies:

#### **Digital Zettelkasten:**

```markdown
# 202012171030 - Python Memory Management

Python's memory management combines several strategies:

## Reference Counting

- Each object maintains a count of references
- When count reaches zero, object is immediately freed
- **Problem**: Cannot handle circular references

## Cycle Detection

- Periodic scan for unreachable circular references
- Uses mark-and-sweep algorithm
- **Trade-off**: Introduces pause times

## Memory Pools

- Small objects use pymalloc for efficiency
- Reduces fragmentation for common allocation patterns
- **Benefit**: Faster allocation/deallocation

**Connected Ideas:**

- [[202012150945]] - General GC algorithms
- [[202012160800]] - CPython implementation details
- [[202012180900]] - Memory profiling techniques

**References:**

- CPython source: Objects/obmalloc.c
- PEP 442: Safe object finalization
```

#### **Linking Strategies:**

- **Progressive Summarization**: Highlight key insights in existing notes
- **Index Notes**: Create overview notes that link to related concepts
- **Concept Maps**: Visual representation of note relationships
- **Tag Systems**: Multiple categorization schemes

### Tools and Workflows:

#### **Popular Zettelkasten Tools:**

```bash
# Obsidian - Graph-based note taking
# Features: Link visualization, backlinks, graph view

# Roam Research - Bi-directional linking
# Features: Block references, daily notes, query system

# Zettlr - Academic writing focus
# Features: Citation management, LaTeX support

# Plain text + scripts
mkdir zettelkasten
cd zettelkasten

# Create new note with timestamp ID
new_note() {
    local id=$(date +%Y%m%d%H%M)
    local title="$1"
    local filename="${id}-${title// /-}.md"

    cat > "$filename" << EOF
# $id - $title

## Content



## Links
-

## Tags
#

## References
-
EOF

    echo "Created: $filename"
    $EDITOR "$filename"
}
```

#### **Maintenance Practices:**

```bash
# Regular review and connection script
#!/bin/bash
# find-orphans.sh

echo "=== Orphaned Notes (no incoming links) ==="
for note in *.md; do
    note_id=$(basename "$note" .md | cut -d'-' -f1)
    if ! grep -l "\[\[$note_id\]\]" *.md > /dev/null 2>&1; then
        echo "Orphan: $note"
    fi
done

echo -e "\n=== Notes with few connections ==="
for note in *.md; do
    link_count=$(grep -o "\[\[[0-9]*\]\]" "$note" | wc -l)
    if [ "$link_count" -lt 2 ]; then
        echo "Few links: $note ($link_count connections)"
    fi
done
```

### Benefits for Developers:

#### **Technical Knowledge Building:**

- **API Documentation**: Personal notes on libraries and frameworks
- **Problem Solutions**: Reusable solutions to common problems
- **Architecture Patterns**: Design patterns and their applications
- **Learning Journal**: Track understanding of complex concepts

#### **Example Developer Zettelkasten:**

```
202012171100 - Docker Container Networking
├── Links to: Bridge Networks, Host Networking, Docker Compose
├── Tags: #docker #networking #containers
└── Contains: Network types, port mapping, service discovery

202012171115 - Kubernetes Service Types
├── Links to: Docker Networking, Load Balancing, Ingress
├── Tags: #kubernetes #services #networking
└── Contains: ClusterIP, NodePort, LoadBalancer, ExternalName

202012171130 - Load Balancing Algorithms
├── Links to: Kubernetes Services, System Design, Performance
├── Tags: #algorithms #networking #performance
└── Contains: Round-robin, least connections, weighted, consistent hashing
```

## Tmuxinator - Tmux Session Templates

[Templating tmux with tmuxinator](https://thoughtbot.com/blog/templating-tmux-with-tmuxinator)

Powerful tool for creating and managing complex tmux session layouts:

### Installation and Setup:

#### **Installation:**

```bash
# Install tmuxinator
gem install tmuxinator

# Or with bundler
echo 'gem "tmuxinator"' >> Gemfile
bundle install

# Set up shell completion (zsh)
echo 'source ~/.gem/gems/tmuxinator-*/completion/tmuxinator.zsh' >> ~/.zshrc

# Set editor for configuration
export EDITOR='vim'  # or your preferred editor
```

### Project Configuration:

#### **Basic Project Template:**

```yaml
# ~/.tmuxinator/web-development.yml
name: web-development
root: ~/projects/my-website

# Optional: Run commands before starting
pre_window: cd ~/projects/my-website

# Terminal windows configuration
windows:
  - editor:
      layout: main-vertical
      panes:
        - vim
        -  # empty pane for terminal commands
  - server:
      panes:
        - npm run dev
        -  # empty pane for server monitoring
  - database:
      panes:
        - mysql -u root -p
        - redis-cli
  - monitoring:
      layout: tiled
      panes:
        - htop
        - tail -f logs/development.log
        - watch -n 1 'ps aux | grep node'
        -  # empty pane for additional monitoring
```

#### **Advanced Configuration:**

```yaml
# ~/.tmuxinator/microservices.yml
name: microservices
root: ~/work/microservices

# Pre-execution commands
pre: docker-compose up -d postgres redis
post: echo "Development environment ready!"

# Environment variables
pre_window: export NODE_ENV=development

windows:
  - api:
      root: ~/work/microservices/api
      layout: main-horizontal
      panes:
        -  # Main development pane
        - npm run dev:watch
        - npm run test:watch

  - frontend:
      root: ~/work/microservices/frontend
      layout: main-vertical
      panes:
        - npm run serve
        - npm run test:unit -- --watch
        -  # Static analysis

  - services:
      root: ~/work/microservices
      layout: tiled
      panes:
        - cd auth-service && npm run dev
        - cd notification-service && npm run dev
        - cd payment-service && npm run dev
        - docker-compose logs -f

  - monitoring:
      layout: even-horizontal
      panes:
        - curl -s http://localhost:3000/health | jq
        - watch -n 5 'docker ps --format "table
          {{.Names}}\t{{.Status}}\t{{.Ports}}"'
```

### Advanced Features:

#### **Custom Commands and Hooks:**

```yaml
# ~/.tmuxinator/data-pipeline.yml
name: data-pipeline
root: ~/data-pipeline

# Startup sequence
pre:
  - docker-compose up -d kafka zookeeper elasticsearch
  - sleep 10 # Wait for services to be ready

# Custom window startup commands
pre_window:
  - source venv/bin/activate
  - export PYTHONPATH=$PWD

windows:
  - kafka:
      panes:
        - kafka-console-consumer --topic events --bootstrap-server
          localhost:9092
        - kafka-console-producer --topic events --bootstrap-server
          localhost:9092
        - kafka-topics --list --bootstrap-server localhost:9092

  - pipeline:
      panes:
        - python -m pipeline.consumer
        - python -m pipeline.producer
        - python -m pipeline.monitor

  - analysis:
      panes:
        - jupyter notebook --port=8888 --no-browser
        - python -c "import pandas as pd; import numpy as np; print('Ready for
          analysis')"

# Cleanup on exit
post: docker-compose down
```

#### **Session Management:**

```bash
# Create new project configuration
tmuxinator new myproject

# Start a project session
tmuxinator start web-development
tmuxinator s web-development  # short form

# List available projects
tmuxinator list

# Edit existing project
tmuxinator edit web-development

# Copy project configuration
tmuxinator copy web-development mobile-development

# Delete project
tmuxinator delete old-project

# Debug configuration
tmuxinator debug web-development
```

### Integration with Development Workflow:

#### **Git Hooks Integration:**

```bash
# .git/hooks/post-checkout
#!/bin/bash
# Start development environment after branch checkout

branch_name=$(git symbolic-ref --short HEAD)

case "$branch_name" in
    "feature/"*)
        tmuxinator start feature-development
        ;;
    "hotfix/"*)
        tmuxinator start hotfix-environment
        ;;
    "main"|"master")
        tmuxinator start production-monitoring
        ;;
esac
```

## Advanced Napkin Math for System Estimation

[Advanced Napkin Math: Estimating System Performance - SREcon19](https://www.youtube.com/watch?v=IxkSlnrRFqc)
[Napkin Math - Simon Eskildsen](https://sirupsen.com/napkin/)

Essential skills for back-of-the-envelope system calculations:

### Fundamental Constants:

#### **Computer Performance Numbers:**

```
CPU Operations:
- L1 cache reference: 0.5 ns
- Branch mispredict: 5 ns
- L2 cache reference: 7 ns
- Mutex lock/unlock: 25 ns
- Main memory reference: 100 ns
- Context switch: 3,000 ns

Storage Operations:
- SSD sequential read: 25 MB/s per 1 GB
- SSD random read: 4KB in 150 μs
- HDD sequential read: 100 MB/s
- HDD seek: 10 ms
- Network round trip (same datacenter): 0.5 ms
- Network round trip (cross-continental): 150 ms
```

#### **Capacity Planning Numbers:**

```
Memory:
- Typical server: 64-256 GB RAM
- Database connection: ~10 MB overhead
- Web server process: ~50-200 MB
- Container overhead: ~5-50 MB

Network:
- Gigabit ethernet: 125 MB/s theoretical max
- Typical utilization: 70% = 87.5 MB/s
- TCP overhead: ~5-10%
- Load balancer overhead: ~5%
```

### Estimation Techniques:

#### **Request Capacity Calculation:**

```python
# Example: Web server capacity estimation
def calculate_web_capacity():
    # Server specifications
    cpu_cores = 8
    memory_gb = 32

    # Application characteristics
    avg_request_time_ms = 100
    memory_per_request_mb = 2
    cpu_utilization_target = 0.7

    # CPU-bound calculation
    requests_per_second_cpu = (cpu_cores * 1000 / avg_request_time_ms) * cpu_utilization_target
    print(f"CPU limit: {requests_per_second_cpu:.0f} req/s")

    # Memory-bound calculation
    concurrent_requests_memory = (memory_gb * 1024) / memory_per_request_mb * 0.8  # 80% utilization
    requests_per_second_memory = concurrent_requests_memory / (avg_request_time_ms / 1000)
    print(f"Memory limit: {requests_per_second_memory:.0f} req/s")

    # Bottleneck is the lower value
    capacity = min(requests_per_second_cpu, requests_per_second_memory)
    print(f"Estimated capacity: {capacity:.0f} req/s")

    return capacity

calculate_web_capacity()
```

#### **Database Sizing:**

```python
def estimate_database_size():
    # Business metrics
    daily_active_users = 100_000
    actions_per_user_per_day = 50
    data_retention_days = 2555  # ~7 years

    # Technical metrics
    avg_record_size_bytes = 1024  # 1KB per record
    index_overhead_multiplier = 1.5
    replication_factor = 3

    # Calculate storage requirements
    daily_records = daily_active_users * actions_per_user_per_day
    total_records = daily_records * data_retention_days

    raw_data_gb = (total_records * avg_record_size_bytes) / (1024**3)
    with_indexes_gb = raw_data_gb * index_overhead_multiplier
    with_replication_gb = with_indexes_gb * replication_factor

    print(f"Daily records: {daily_records:,}")
    print(f"Total records: {total_records:,}")
    print(f"Raw data: {raw_data_gb:.1f} GB")
    print(f"With indexes: {with_indexes_gb:.1f} GB")
    print(f"With replication: {with_replication_gb:.1f} GB")

    # Growth planning (20% annual growth)
    annual_growth = 1.2
    five_year_size = with_replication_gb * (annual_growth ** 5)
    print(f"5-year projection: {five_year_size:.1f} GB")

estimate_database_size()
```

#### **Network Bandwidth Estimation:**

```python
def estimate_network_bandwidth():
    # Application characteristics
    peak_requests_per_second = 10_000
    avg_response_size_kb = 50
    static_content_ratio = 0.6  # 60% cached/CDN

    # Calculate bandwidth needs
    dynamic_requests_per_second = peak_requests_per_second * (1 - static_content_ratio)
    bandwidth_mbps = (dynamic_requests_per_second * avg_response_size_kb * 8) / 1024  # Convert to Mbps

    # Add safety margins
    tcp_overhead = 1.1  # 10% TCP overhead
    burst_capacity = 2.0  # Handle 2x peak traffic

    required_bandwidth = bandwidth_mbps * tcp_overhead * burst_capacity

    print(f"Peak requests/s: {peak_requests_per_second:,}")
    print(f"Dynamic requests/s: {dynamic_requests_per_second:,}")
    print(f"Base bandwidth: {bandwidth_mbps:.1f} Mbps")
    print(f"With overhead & burst: {required_bandwidth:.1f} Mbps")

    # Server recommendations
    if required_bandwidth < 100:
        print("Recommendation: Single server with gigabit connection")
    elif required_bandwidth < 1000:
        print("Recommendation: Load balancer with multiple servers")
    else:
        print("Recommendation: CDN + multiple regions")

estimate_network_bandwidth()
```

### Quick Reference Formulas:

#### **Common Calculations:**

```
Database Connections:
- connections = (concurrent_users / avg_request_time) * connection_multiplier
- connection_multiplier = 1.2-2.0 depending on pooling efficiency

Cache Hit Ratio Impact:
- effective_latency = hit_ratio * cache_latency + (1 - hit_ratio) * backend_latency

Queue Depth:
- queue_depth = arrival_rate * avg_processing_time
- utilization = arrival_rate / service_rate (should be < 0.8)

Scale Factor:
- horizontal: cost grows linearly, complexity grows exponentially
- vertical: cost grows exponentially, complexity stays constant
```

These tools and techniques represent essential skills for modern software
development - building knowledge systems, managing development environments
efficiently, and making informed architectural decisions through quantitative
analysis.
