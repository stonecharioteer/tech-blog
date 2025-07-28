---
date: 2021-01-13T10:00:00+05:30
draft: false
title: "TIL: Plain Text Accounting with Beancount, Ledger, and Fava"
description: "Today I learned about plain text accounting systems that use simple text files to track finances using double-entry bookkeeping principles, with tools like Beancount, Ledger, and the Fava web interface."
tags:
  - TIL
  - Accounting
  - Finance
  - Plain Text
  - Beancount
  - Double-entry Bookkeeping
  - Personal Finance
---

## Introduction to Plain Text Accounting

[Introduction to plain text accounting — sirodoht blog](https://sirodoht.com/blog/introduction-to-plain-text-accounting/)

Revolutionary approach to personal and business accounting using simple text files:

### Core Philosophy:
- **Human Readable**: Accounting records in plain text format
- **Version Control**: Track financial changes with Git
- **Durability**: Text files last forever, proprietary formats don't
- **Transparency**: Every transaction is visible and auditable
- **Scriptable**: Automate analysis with standard text processing tools

### Double-Entry Bookkeeping Principles:

#### **Fundamental Equation:**
```
Assets + Expenses = Liabilities + Equity + Income
```

#### **Every Transaction Has Two Sides:**
```beancount
2021-01-13 * "Grocery shopping"
  Expenses:Food:Groceries    45.67 USD
  Assets:Checking           -45.67 USD
```

**Explanation:**
- Money flows OUT of checking account (asset decreases)
- Money flows INTO grocery expense (expense increases)
- Total change = 0 (books balance)

### Benefits of Plain Text Accounting:

#### **Advantages Over Traditional Software:**
- **No Vendor Lock-in**: Your data remains accessible forever
- **Version Control**: Complete audit trail of changes
- **Automation**: Scripts can generate and analyze transactions
- **Customization**: Unlimited flexibility in categorization
- **Privacy**: Data stays on your computer
- **Cost**: Free and open source tools

#### **Developer-Friendly Features:**
```bash
# Version control your finances
git add finances.beancount
git commit -m "Added Q4 2021 expenses"

# Analyze with standard tools
grep "Expenses:Food" finances.beancount | wc -l
awk '/Expenses:Transport/ {sum += $2} END {print sum}' finances.beancount

# Backup and sync
rsync -av finances/ backup-server:/accounting/
```

## Beancount - Python-Based Accounting

[beancount: Double-Entry Accounting from Text Files](https://beancount.github.io/)

Modern, powerful plain text accounting system:

### Syntax and Structure:

#### **Basic Transaction Format:**
```beancount
; Account declarations
1900-01-01 open Assets:US:BofA:Checking         USD
1900-01-01 open Expenses:Food:Restaurant        USD
1900-01-01 open Expenses:Transport:Uber         USD
1900-01-01 open Income:US:Company:Salary        USD

; Transactions
2021-01-13 * "Lunch at Italian restaurant"
  Expenses:Food:Restaurant   28.50 USD
  Assets:US:BofA:Checking   -28.50 USD

2021-01-13 * "Uber ride to work"
  Expenses:Transport:Uber    12.45 USD
  Assets:US:BofA:Checking   -12.45 USD

2021-01-15 * "Salary deposit"
  Assets:US:BofA:Checking   3500.00 USD
  Income:US:Company:Salary -3500.00 USD
```

#### **Advanced Features:**
```beancount
; Price declarations
2021-01-13 price AAPL 150.00 USD

; Investment transactions
2021-01-13 * "Buy Apple stock"
  Assets:US:Schwab:AAPL     10 AAPL {150.00 USD}
  Assets:US:Schwab:Cash   -1500.00 USD

; Multi-currency support
2021-01-13 * "European vacation expense"
  Expenses:Travel:Hotel     120.00 EUR
  Assets:US:BofA:Checking  -142.80 USD @ 1.19 USD/EUR

; Budgets and forecasting
2021-01-01 budget Assets:US:BofA:Checking   "Monthly budget: 4000 USD"
```

### Command Line Tools:

#### **Basic Operations:**
```bash
# Validate file syntax
bean-check finances.beancount

# Generate balance sheet
bean-report finances.beancount balsheet

# Income statement
bean-report finances.beancount income

# Custom queries
bean-query finances.beancount "SELECT account, sum(position) WHERE date >= 2021-01-01"

# Export to other formats
bean-report finances.beancount holdings --format=csv > holdings.csv
```

### Data Validation and Error Checking:
```beancount
; Assertions to catch errors
2021-01-31 balance Assets:US:BofA:Checking  2847.55 USD

; Padding for unknown transactions
2021-01-01 pad Assets:US:BofA:Checking Equity:Opening-Balances

; Close accounts when no longer used
2021-12-31 close Assets:US:OldBank:Savings
```

## Fava - Web Interface for Beancount

[Welcome to Fava! — Fava documentation](https://beancount.github.io/fava/)

Beautiful web interface for Beancount files:

### Key Features:

#### **Interactive Dashboard:**
- **Real-time Updates**: Automatically reload when files change
- **Charts and Graphs**: Visual representation of financial data
- **Drill-down Analysis**: Click through from summaries to transactions
- **Multi-file Support**: Handle complex accounting setups

#### **Web Interface Benefits:**
```bash
# Start Fava server
fava finances.beancount

# Access at http://localhost:5000
# Features available:
# - Balance sheets and income statements
# - Account hierarchies and drill-downs
# - Transaction search and filtering
# - Import helpers for bank data
# - Budget vs actual reporting
```

### Advanced Analysis:

#### **Custom Reports:**
```beancount
; Custom reporting periods
2021-01-01 custom "fava-option" "fiscal-year-end" "03-31"

; Budget definitions
2021-01-01 custom "budget" Assets:US:BofA:Checking  "4000 USD"
2021-01-01 custom "budget" Expenses:Food            "800 USD"
```

#### **Import Automation:**
- **Bank CSV Import**: Convert bank statements to Beancount format
- **Duplicate Detection**: Automatic detection of duplicate transactions
- **Categorization**: Machine learning-based expense categorization
- **Reconciliation**: Match imported transactions with manual entries

## Ledger - The Original Plain Text Accounting

[ledger, a powerful command-line accounting system](https://www.ledger-cli.org/)

The pioneering plain text accounting system:

### Core Features:

#### **Simple Syntax:**
```ledger
2021/01/13 Grocery Store
    Expenses:Food:Groceries        $45.67
    Assets:Checking

2021/01/13 Salary
    Assets:Checking             $3,500.00
    Income:Salary

2021/01/15 Investment
    Assets:Brokerage:AAPL       10 AAPL @ $150.00
    Assets:Checking            $-1,500.00
```

#### **Powerful Queries:**
```bash
# Basic reports
ledger -f finances.ledger balance
ledger -f finances.ledger register

# Time-based analysis
ledger -f finances.ledger balance --period "this month"
ledger -f finances.ledger register --period "last year"

# Complex queries
ledger -f finances.ledger balance ^Expenses --depth 2
ledger -f finances.ledger register Expenses:Food --monthly
```

### Advanced Capabilities:

#### **Budgeting and Forecasting:**
```bash
# Budget vs actual
ledger -f finances.ledger balance --budget

# Forecast future cash flow
ledger -f finances.ledger register --forecast "next 6 months"

# Investment tracking
ledger -f finances.ledger balance --market --price-db prices.db
```

### Ecosystem and Tools:

#### **Supporting Applications:**
- **hledger**: Haskell implementation with additional features
- **PlainTextAccounting.org**: Community and resources
- **Mobile Apps**: Various mobile entry applications
- **Bank Integration**: Tools for automatic transaction import

## Practical Implementation:

### Getting Started Workflow:

#### **1. Set Up Account Structure:**
```beancount
1900-01-01 open Assets:US:BofA:Checking         USD
1900-01-01 open Assets:US:BofA:Savings          USD
1900-01-01 open Expenses:Food:Groceries         USD
1900-01-01 open Expenses:Food:Restaurant        USD
1900-01-01 open Expenses:Transport:Gas          USD
1900-01-01 open Expenses:Housing:Rent           USD
1900-01-01 open Income:Salary                   USD
```

#### **2. Import Historical Data:**
```bash
# Convert bank CSV to Beancount
bean-extract config.py statement.csv > imported.beancount

# Merge with main file
cat imported.beancount >> finances.beancount
```

#### **3. Establish Routine:**
```bash
#!/bin/bash
# Daily accounting routine
bean-check finances.beancount || exit 1
fava finances.beancount &
echo "Fava started at http://localhost:5000"
echo "Add today's transactions and review accounts"
```

### Best Practices:
- **Consistent Naming**: Establish and stick to account naming conventions
- **Regular Reconciliation**: Match against bank statements monthly
- **Backup Strategy**: Version control and offsite backups
- **Documentation**: Comment complex transactions and account purposes
- **Automation**: Script repetitive tasks like imports and reports

Plain text accounting represents a powerful paradigm shift in financial management, combining the rigor of double-entry bookkeeping with the flexibility and transparency of plain text files.