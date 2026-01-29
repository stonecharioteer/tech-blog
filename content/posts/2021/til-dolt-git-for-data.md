---
date: 2021-03-05T10:00:00+05:30
draft: false
title: "TIL: Dolt - Git for Data and Database Version Control"
description:
  "Today I learned about Dolt, a revolutionary SQL database that combines
  Git-style version control with relational database functionality, enabling
  true data versioning and collaboration."
tags:
  - "til"
  - "database"
  - "version-control"
  - "data-management"
  - "sql"
---

## Dolt - Version Control for Data

[GitHub - dolthub/dolt: Dolt – It's Git for Data](https://github.com/dolthub/dolt)

A SQL database with Git-style version control built into the core:

### Core Concept:

- **Git + SQL**: Combines familiar Git workflows with SQL database operations
- **Data Versioning**: Track changes to data like you track changes to code
- **Collaboration**: Multiple people can work on the same dataset simultaneously
- **Audit Trail**: Complete history of who changed what and when

### Key Features:

#### **Git-Style Operations:**

```bash
# Clone a database
dolt clone dolthub/ip-to-country

# Make changes to data
dolt sql -q "INSERT INTO countries VALUES ('XX', 'Test Country')"

# Stage changes
dolt add .

# Commit changes
dolt commit -m "Added test country"

# Push to remote
dolt push origin main
```

#### **SQL Database Functionality:**

- **Standard SQL**: Full MySQL-compatible SQL interface
- **ACID Transactions**: Complete transaction support
- **Indexes**: Performance optimization with standard database indexes
- **Constraints**: Primary keys, foreign keys, unique constraints

### Unique Capabilities:

#### **Branch and Merge Data:**

```bash
# Create feature branch
dolt checkout -b feature/cleanup-data

# Make data changes
dolt sql -q "DELETE FROM users WHERE last_login < '2020-01-01'"

# Merge back to main
dolt checkout main
dolt merge feature/cleanup-data
```

#### **Time Travel Queries:**

```sql
-- Query data as of specific commit
SELECT * FROM users AS OF 'abc123';

-- Compare data between commits
SELECT * FROM diff('main', 'feature/cleanup', 'users');

-- Show history of specific row
SELECT * FROM dolt_history_users WHERE id = 123;
```

### Use Cases:

#### **Data Analytics:**

- **Experiment Tracking**: Different feature engineering approaches
- **Model Versioning**: Track training data versions with model performance
- **Reproducible Research**: Exact data state for research papers
- **A/B Testing**: Compare dataset variants and results

#### **Data Engineering:**

- **ETL Pipeline Versioning**: Track data transformation steps
- **Data Quality**: Rollback corrupted data changes
- **Collaboration**: Multiple analysts working on same dataset
- **Audit Compliance**: Complete change history for regulations

#### **Application Development:**

- **Schema Evolution**: Version database schema alongside data
- **Feature Flags**: Different data configurations for different features
- **Testing**: Isolated test data environments
- **Rollback Safety**: Safe deployment with easy rollback

### Architecture Benefits:

#### **Storage Efficiency:**

- **Content Addressable**: Deduplication of identical data blocks
- **Incremental Changes**: Only store what actually changed
- **Compression**: Efficient storage of large datasets
- **Remote Sync**: Only transfer changed data

#### **Concurrent Access:**

- **MVCC**: Multiple version concurrency control
- **Branch Isolation**: Changes don't interfere until merge
- **Conflict Resolution**: Merge conflict handling for data
- **Distributed**: Clone and work offline

### Comparison with Traditional Approaches:

#### **vs Database Backups:**

- **Granular Changes**: See individual row changes, not just snapshots
- **Efficient Storage**: Don't duplicate unchanged data
- **Branch Support**: Multiple parallel data versions
- **Merge Capability**: Combine changes intelligently

#### **vs Data Lakes:**

- **Structured Data**: SQL interface with schema enforcement
- **ACID Properties**: Transactional consistency
- **Version Control**: Built-in change tracking
- **Query Performance**: Optimized for relational queries

### Getting Started:

#### **Installation:**

```bash
# Install Dolt
curl -L https://github.com/dolthub/dolt/releases/latest/download/install.sh | bash

# Initialize new database
mkdir my-database && cd my-database
dolt init

# Create table and add data
dolt sql -q "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100))"
dolt sql -q "INSERT INTO users VALUES (1, 'Alice'), (2, 'Bob')"

# Track changes
dolt add .
dolt commit -m "Initial users"
```

#### **Connect Existing Tools:**

```bash
# Start SQL server
dolt sql-server

# Connect with any MySQL client
mysql -h 127.0.0.1 -P 3306 -u root my-database
```

### Enterprise Features:

- **DoltHub**: GitHub-like hosting for Dolt databases
- **Access Control**: User permissions and authentication
- **API Access**: REST and GraphQL APIs
- **Integration**: Works with existing BI and analytics tools

### Limitations and Considerations:

- **Performance**: Not optimized for high-throughput OLTP
- **Ecosystem**: Newer tool with growing ecosystem
- **Learning Curve**: New concepts for traditional database users
- **Storage**: Version history can grow large over time

Dolt represents a paradigm shift in how we think about data management, bringing
software engineering best practices to database operations and making data
collaboration as natural as code collaboration.
