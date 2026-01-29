---
date: 2021-03-13T10:00:00+05:30
draft: false
title:
  "TIL: Camelot PDF Tables, PostgreSQL Row Level Security, Zerodha Varsity, and
  Write Yourself a Git"
description:
  "Today I learned about Camelot for PDF table extraction, PostgreSQL Row Level
  Security for multi-tenant isolation, Zerodha's free trading education
  platform, and building Git from scratch."
tags:
  - "til"
  - "pdf"
  - "postgresql"
  - "security"
  - "multi-tenancy"
  - "finance"
  - "trading"
  - "git"
  - "version-control"
---

## Camelot - PDF Table Extraction

[Camelot: PDF Table Extraction for Humans](https://camelot-py.readthedocs.io/en/master/)

Python library for extracting tables from PDF files with high accuracy:

### Key Features:

- **Multiple Parsing Methods**: Stream and Lattice parsers for different table
  types
- **High Accuracy**: Better results than traditional PDF parsing tools
- **Pandas Integration**: Direct conversion to pandas DataFrames
- **Visual Debugging**: Plot detected table areas for validation
- **Customizable**: Fine-tune detection parameters

### Usage Examples:

```python
import camelot

# Extract tables from PDF
tables = camelot.read_pdf('document.pdf')
print(f"Found {tables.n} tables")

# Convert to pandas DataFrame
df = tables[0].df

# Export to various formats
tables.export('output.csv', f='csv')
tables.export('output.xlsx', f='excel')
```

### When to Use:

- Financial reports with tabular data
- Research papers with data tables
- Government documents with statistics
- Any structured data trapped in PDFs

## PostgreSQL Row Level Security for Multi-Tenancy

[Multi-tenant data isolation with PostgreSQL Row Level Security](https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/)

Advanced PostgreSQL feature for implementing secure multi-tenant applications:

### What is Row Level Security (RLS):

- **Fine-Grained Access**: Control access at the row level within tables
- **Policy-Based**: Define security policies for different user types
- **Transparent**: Application code doesn't need complex filtering logic
- **Performance**: Database-level enforcement with optimized execution

### Implementation Pattern:

```sql
-- Enable RLS on table
ALTER TABLE customer_data ENABLE ROW LEVEL SECURITY;

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation ON customer_data
    FOR ALL TO tenant_user
    USING (tenant_id = current_setting('app.current_tenant')::integer);

-- Set tenant context in application
SET app.current_tenant = '123';
```

### Benefits:

- **Data Isolation**: Strong tenant boundaries
- **Security**: Prevents data leaks between tenants
- **Simplicity**: Reduces application complexity
- **Compliance**: Meets regulatory requirements

### Use Cases:

- SaaS applications with multiple customers
- Healthcare systems with patient data isolation
- Financial applications with account separation
- Any system requiring strict data boundaries

## Zerodha Varsity - Free Trading Education

[Varsity by Zerodha – Markets, Trading, and Investing Simplified](https://zerodha.com/varsity/)

Comprehensive free educational platform for learning about financial markets:

### What It Covers:

#### **Trading Fundamentals:**

- **Technical Analysis**: Chart patterns, indicators, candlesticks
- **Fundamental Analysis**: Financial statement analysis, valuation
- **Options Trading**: Strategies, Greeks, risk management
- **Futures Trading**: Contract specifications, margin requirements

#### **Investment Concepts:**

- **Portfolio Management**: Asset allocation, diversification
- **Risk Management**: Position sizing, stop losses
- **Market Psychology**: Behavioral finance concepts
- **Regulatory Framework**: SEBI guidelines and compliance

### Learning Approach:

- **Module-Based**: Structured progression from basics to advanced
- **Practical Examples**: Real market scenarios and case studies
- **Interactive Content**: Charts, calculators, and tools
- **Free Access**: No cost for high-quality financial education

### Value Proposition:

- Democratizes financial education
- Reduces dependence on expensive courses
- Provides practical, actionable knowledge
- Builds informed investor community

## Write Yourself a Git

[Write yourself a Git!](https://wyag.thb.lt/)

Educational project to understand Git internals by implementing it from scratch:

### Learning Objectives:

- **Version Control Concepts**: How distributed version control works
- **Git Internals**: Objects, references, and storage mechanisms
- **Data Structures**: Trees, graphs, and hash-based storage
- **File System Operations**: Blob storage and retrieval

### Key Components to Implement:

#### **Core Git Objects:**

- **Blobs**: File content storage
- **Trees**: Directory structure representation
- **Commits**: Snapshots with metadata
- **Tags**: Named references to commits

#### **Repository Operations:**

- **Initialize**: Create new repository structure
- **Add**: Stage files for commit
- **Commit**: Create snapshot with message
- **Checkout**: Switch between branches/commits

### Implementation Benefits:

- **Deep Understanding**: Learn Git's internal architecture
- **Debugging Skills**: Better troubleshoot Git issues
- **System Design**: Understand distributed system principles
- **Programming Practice**: File I/O, data structures, algorithms

### Technologies Used:

- Python for implementation simplicity
- File system operations for storage
- Hashing algorithms for content addressing
- Command-line interface design

Each resource provides deep technical knowledge in its domain - from practical
data extraction to advanced database security, financial literacy, and version
control system design.
