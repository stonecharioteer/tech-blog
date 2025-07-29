---
date: 2020-11-08T10:00:00+05:30
draft: false
title: "TIL: Customizing PostgreSQL Shell with psqlrc Configuration"
description: "Today I learned how to customize the PostgreSQL command-line interface using psqlrc configuration files to improve productivity and user experience."
tags:
  - til
  - postgresql
  - database
  - productivity
  - configuration
  - sql
---

Today I discovered how to transform the PostgreSQL command-line experience through custom psqlrc configuration, making database work more efficient and user-friendly.

## PostgreSQL Shell Customization

[Customizing Postgres shell using psqlrc](https://www.citusdata.com/blog/2017/07/16/customizing-my-postgres-shell-using-psqlrc/) demonstrates how to create a personalized and productive PostgreSQL environment.

### Basic psqlrc Configuration

Create `~/.psqlrc` to customize your PostgreSQL shell:

```sql
-- ~/.psqlrc configuration

-- Display settings
\set QUIET 1
\pset null '[NULL]'
\pset border 2
\pset format wrapped
\x auto
\set QUIET 0

-- Prompt customization
\set PROMPT1 '%[%033[1;32m%]%n@%M:%> %[%033[1;33m%]%/%[%033[0m%]%R%[%033[K%]%# '
\set PROMPT2 '%[%033[1;33m%]%/%[%033[0m%]%R%[%033[K%]%# '

-- History settings
\set HISTFILE ~/.psql_history- :DBNAME
\set HISTCONTROL ignoredups
\set HISTSIZE 5000

-- Timing and verbosity
\timing on
\set VERBOSITY verbose
\set COMP_KEYWORD_CASE upper
```

### Advanced Customization Features

#### **Custom Shortcuts and Macros:**
```sql
-- Useful shortcuts
\set conninfo 'SELECT usename, application_name, client_addr, state FROM pg_stat_activity;'
\set activity 'SELECT datname, pid, usename, application_name, client_addr, state, query FROM pg_stat_activity ORDER BY query_start DESC;'
\set locks 'SELECT mode, locktype, database, relation, page, tuple, classid, granted, query FROM pg_locks pl LEFT JOIN pg_stat_activity psa ON pl.pid = psa.pid;'
\set waits 'SELECT pg_stat_activity.pid, pg_stat_activity.query, pg_stat_activity.waiting, now() - pg_stat_activity.query_start AS \"totaltime\", pg_stat_activity.backend_start FROM pg_stat_activity WHERE pg_stat_activity.query !~ \'%IDLE%\'::text AND pg_stat_activity.waiting = true;'

-- Database size information
\set dbsize 'SELECT datname, pg_size_pretty(pg_database_size(datname)) as size FROM pg_database ORDER BY pg_database_size(datname) DESC;'
\set tablesize 'SELECT schemaname,tablename,pg_size_pretty(size) as size, pg_size_pretty(total_size) as total_size FROM (SELECT schemaname,tablename,pg_relation_size(schemaname||''.''||tablename) as size, pg_total_relation_size(schemaname||''.''||tablename) as total_size FROM pg_tables) as TABLES ORDER BY total_size DESC;'

-- Index usage statistics
\set unused_indexes 'SELECT schemaname, tablename, attname, n_distinct, correlation FROM pg_stats WHERE schemaname = ''public'' ORDER BY n_distinct DESC;'
\set index_usage 'SELECT relname, 100 * idx_scan / (seq_scan + idx_scan) percent_of_times_index_used, n_tup_upd + n_tup_ins + n_tup_del as num_writes, indexrelname as index_name FROM pg_stat_user_tables JOIN pg_stat_user_indexes USING (relid) ORDER BY percent_of_times_index_used;'
```

#### **Performance Monitoring Shortcuts:**
```sql
-- Query performance
\set slow_queries 'SELECT query, calls, total_time, mean_time, (100.0 * total_time / sum(total_time) OVER()) AS percentage_cpu FROM pg_stat_statements ORDER BY total_time DESC LIMIT 20;'

-- Connection monitoring  
\set blocking 'SELECT bl.pid as blocked_pid, a.usename as blocked_user, ka.query as current_statement_in_blocking_process, now() - ka.query_start as blocking_duration, ka.pid as blocking_pid, ka.usename as blocking_user, a.query as blocked_statement, now() - a.query_start as blocked_duration FROM pg_catalog.pg_locks bl JOIN pg_catalog.pg_stat_activity a ON bl.pid = a.pid JOIN pg_catalog.pg_locks kl ON bl.transactionid = kl.transactionid AND bl.pid != kl.pid JOIN pg_catalog.pg_stat_activity ka ON kl.pid = ka.pid WHERE NOT bl.granted;'

-- Cache hit ratio
\set cache_hit 'SELECT ''index hit rate'' as name, (sum(idx_blks_hit)) / sum(idx_blks_hit + idx_blks_read) as ratio FROM pg_statio_user_indexes UNION ALL SELECT ''cache hit rate'' as name, sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio FROM pg_statio_user_tables;'
```

### Productivity Enhancements

#### **Enhanced Display Settings:**
```sql
-- Better null representation
\pset null '¤'

-- Automatic extended display for wide results
\x auto

-- Unicode line drawing
\pset linestyle unicode

-- Show execution time for all queries
\timing on

-- More detailed error messages
\set VERBOSITY verbose
\set SHOW_CONTEXT always

-- Case-insensitive tab completion with uppercase keywords
\set COMP_KEYWORD_CASE upper
```

#### **Development Helpers:**
```sql
-- Transaction shortcuts
\set commit 'COMMIT;'
\set rollback 'ROLLBACK;'
\set autocommit_off '\set AUTOCOMMIT off'
\set autocommit_on '\set AUTOCOMMIT on'

-- Schema exploration
\set desc_table 'SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_name = '
\set list_tables '\dt'
\set list_views '\dv'  
\set list_functions '\df'
\set list_indexes '\di'

-- Quick table stats
\set table_stats 'SELECT n_tup_ins as inserts, n_tup_upd as updates, n_tup_del as deletes, n_live_tup as live_tuples, n_dead_tup as dead_tuples FROM pg_stat_user_tables WHERE relname = '
```

### Usage Examples

#### **Using Custom Shortcuts:**
```sql
-- Check database connections
:conninfo

-- Monitor slow queries
:slow_queries

-- Check table sizes
:tablesize

-- View blocking queries
:blocking

-- Get cache hit ratios
:cache_hit
```

#### **Environment-Specific Configurations:**
```sql
-- Different settings for different environments
\if :{?PRODUCTION}
    \echo 'PRODUCTION DATABASE - BE CAREFUL!'
    \set PROMPT1 '%[%033[1;31m%][PROD] %n@%M:%> %[%033[1;33m%]%/%[%033[0m%]%R%[%033[K%]%# '
\else
    \set PROMPT1 '%[%033[1;32m%][DEV] %n@%M:%> %[%033[1;33m%]%/%[%033[0m%]%R%[%033[K%]%# '
\endif
```

### Benefits

- **Improved readability**: Better formatting and color coding
- **Faster debugging**: Quick access to performance and system information
- **Reduced typing**: Shortcuts for common administrative tasks
- **Environment awareness**: Visual cues for different database environments
- **Enhanced history**: Better command history management

This configuration transforms PostgreSQL from a basic command-line tool into a powerful, user-friendly database administration interface.