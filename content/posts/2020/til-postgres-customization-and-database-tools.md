---
date: 2020-11-08T17:00:00+05:30
draft: false
title: "TIL: PostgreSQL Customization and Advanced Database Management"
description:
  "Today I learned about customizing PostgreSQL shell environments, advanced
  psql configurations, and database administration best practices for enhanced
  productivity."
tags:
  - "til"
  - "postgresql"
  - "database"
  - "psql"
  - "sql"
  - "database"
  - "productivity"
---

Today I discovered comprehensive techniques for customizing PostgreSQL
environments and learned advanced database management practices that
significantly improve developer and DBA productivity.

## PostgreSQL Shell Customization with .psqlrc

### Advanced .psqlrc Configuration

[Customizing PostgreSQL shell using psqlrc](https://www.citusdata.com/blog/2017/07/16/customizing-my-postgres-shell-using-psqlrc/)
reveals powerful techniques for creating a more productive database environment:

```sql
-- ~/.psqlrc - PostgreSQL shell customization

-- Set better default formatting
\set QUIET 1
\pset null '[NULL]'
\pset linestyle unicode
\pset border 2
\pset format wrapped
\set COMP_KEYWORD_CASE upper
\set HISTSIZE 10000
\set PROMPT1 '%[%033[1m%]%M %n@%/%R%[%033[0m%]%# '
\set PROMPT2 '[more] %R > '
\unset QUIET

-- Timing for performance monitoring
\timing

-- Show expanded output for wide tables
\x auto

-- Better error handling
\set ON_ERROR_ROLLBACK interactive
\set ON_ERROR_STOP on

-- Helpful shortcuts and aliases
\set version 'SELECT version();'
\set extensions 'SELECT * FROM pg_available_extensions ORDER BY name;'
\set settings 'SELECT name, setting, unit, context FROM pg_settings ORDER BY name;'
\set locks 'SELECT * FROM pg_locks ORDER BY pid;'
\set activity 'SELECT pid, usename, application_name, client_addr, state, query_start, query FROM pg_stat_activity ORDER BY query_start DESC;'
\set blocking 'SELECT blocked_locks.pid AS blocked_pid, blocked_activity.usename AS blocked_user, blocking_locks.pid AS blocking_pid, blocking_activity.usename AS blocking_user, blocked_activity.query AS blocked_statement, blocking_activity.query AS current_statement_in_blocking_process FROM pg_catalog.pg_locks blocked_locks JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype AND blocking_locks.DATABASE IS NOT DISTINCT FROM blocked_locks.DATABASE AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid AND blocking_locks.pid != blocked_locks.pid JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid WHERE NOT blocked_locks.GRANTED;'

-- Database size information
\set dbsize 'SELECT datname, pg_size_pretty(pg_database_size(datname)) as size FROM pg_database ORDER BY pg_database_size(datname) DESC;'
\set tablesize 'SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||''.''||tablename)) as size FROM pg_tables ORDER BY pg_total_relation_size(schemaname||''.''||tablename) DESC;'

-- Index usage statistics
\set indexusage 'SELECT schemaname, tablename, attname, n_distinct, correlation FROM pg_stats WHERE schemaname = ''public'' ORDER BY n_distinct DESC;'
\set indexsize 'SELECT schemaname, tablename, indexname, pg_size_pretty(pg_relation_size(indexname::regclass)) as size FROM pg_indexes WHERE schemaname = ''public'' ORDER BY pg_relation_size(indexname::regclass) DESC;'

-- Connection information
\set conninfo 'SELECT usename, count(*) FROM pg_stat_activity GROUP BY usename ORDER BY count DESC;'

-- Slow queries (requires pg_stat_statements)
\set slowqueries 'SELECT query, calls, total_time, mean_time, rows FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;'

-- Replication status
\set replication 'SELECT * FROM pg_stat_replication;'

-- Vacuum and analyze status
\set vacuum_stats 'SELECT schemaname, tablename, last_vacuum, last_autovacuum, last_analyze, last_autoanalyze FROM pg_stat_user_tables ORDER BY last_vacuum DESC NULLS LAST;'
```

### Interactive PostgreSQL Development

Enhanced psql environment for database development:

```sql
-- Development-specific shortcuts in .psqlrc

-- Quick table inspection
\set desc '\\d+'
\set tables '\\dt'
\set sequences '\\ds'
\set views '\\dv'
\set functions '\\df'
\set schemas '\\dn'

-- Development queries
\set missing_indexes 'SELECT schemaname, tablename, attname, n_distinct, correlation FROM pg_stats WHERE schemaname = ''public'' AND n_distinct > 100 AND correlation < 0.1;'

\set duplicate_indexes 'SELECT pg_size_pretty(SUM(pg_relation_size(idx))::BIGINT) AS SIZE, (array_agg(indexrelname))[1] AS idx1, (array_agg(indexrelname))[2] AS idx2, (array_agg(indexrelname))[3] AS idx3, (array_agg(indexrelname))[4] AS idx4 FROM (SELECT indexrelname, regexp_split_to_array(indexdef, E''\\\('') AS parts FROM pg_indexes WHERE schemaname = ''public'') t GROUP BY parts[2] HAVING COUNT(*) > 1;'

-- Performance monitoring
\set cache_hit_ratio 'SELECT ''index hit rate'' as name, (sum(idx_blks_hit)) / sum(idx_blks_hit + idx_blks_read) as ratio FROM pg_statio_user_indexes union all SELECT ''cache hit rate'' as name, sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio FROM pg_statio_user_tables;'

-- Transaction and connection monitoring
\set long_running_queries 'SELECT pid, usename, datname, query_start, now() - query_start AS duration, state, query FROM pg_stat_activity WHERE (now() - query_start) > interval ''5 minutes'' AND state != ''idle'' ORDER BY duration DESC;'

-- Security and permissions
\set user_permissions 'SELECT grantee, privilege_type, table_schema, table_name FROM information_schema.role_table_grants WHERE grantee = current_user;'
```

## Advanced Database Monitoring and Management

### Database Performance Analysis

```sql
-- Comprehensive database health check queries

-- 1. Database size and growth trends
WITH db_size AS (
    SELECT
        datname,
        pg_size_pretty(pg_database_size(datname)) as current_size,
        pg_database_size(datname) as size_bytes
    FROM pg_database
    WHERE datistemplate = false
)
SELECT * FROM db_size ORDER BY size_bytes DESC;

-- 2. Table bloat analysis
WITH table_bloat AS (
    SELECT
        schemaname,
        tablename,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as table_size,
        pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as data_size,
        pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) -
                      pg_relation_size(schemaname||'.'||tablename)) as index_size,
        ROUND(
            100.0 * (pg_total_relation_size(schemaname||'.'||tablename) -
                    pg_relation_size(schemaname||'.'||tablename)) /
                    NULLIF(pg_total_relation_size(schemaname||'.'||tablename), 0), 2
        ) as index_ratio
    FROM pg_tables
    WHERE schemaname = 'public'
)
SELECT * FROM table_bloat
ORDER BY pg_size_bytes(regexp_replace(table_size, '[^0-9]', '', 'g')::bigint) DESC;

-- 3. Index usage effectiveness
WITH index_usage AS (
    SELECT
        schemaname,
        tablename,
        indexname,
        idx_tup_read,
        idx_tup_fetch,
        CASE
            WHEN idx_tup_read = 0 THEN 0
            ELSE ROUND(100.0 * idx_tup_fetch / idx_tup_read, 2)
        END as hit_rate,
        pg_size_pretty(pg_relation_size(indexname::regclass)) as index_size
    FROM pg_stat_user_indexes psi
    JOIN pg_indexes pi ON psi.indexrelname = pi.indexname
    WHERE schemaname = 'public'
)
SELECT * FROM index_usage
WHERE idx_tup_read > 0
ORDER BY hit_rate ASC, idx_tup_read DESC;

-- 4. Query performance analysis (requires pg_stat_statements)
SELECT
    query,
    calls,
    total_time,
    mean_time,
    max_time,
    stddev_time,
    rows,
    100.0 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0) AS hit_percent,
    pg_size_pretty(temp_blks_written * 8192::bigint) as temp_written
FROM pg_stat_statements
WHERE calls > 100  -- Focus on frequently called queries
ORDER BY total_time DESC
LIMIT 20;
```

### Automated Maintenance Procedures

```sql
-- Database maintenance automation

-- 1. Comprehensive vacuum and analyze
DO $$
DECLARE
    table_record RECORD;
    vacuum_cmd TEXT;
BEGIN
    -- Loop through all user tables
    FOR table_record IN
        SELECT schemaname, tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        -- Build vacuum analyze command
        vacuum_cmd := 'VACUUM ANALYZE ' ||
                     quote_ident(table_record.schemaname) || '.' ||
                     quote_ident(table_record.tablename);

        RAISE NOTICE 'Executing: %', vacuum_cmd;
        EXECUTE vacuum_cmd;

        -- Add delay to prevent overwhelming the system
        PERFORM pg_sleep(0.1);
    END LOOP;

    RAISE NOTICE 'Vacuum analyze completed for all tables';
END
$$;

-- 2. Index maintenance and optimization
WITH unused_indexes AS (
    SELECT
        schemaname,
        tablename,
        indexname,
        pg_size_pretty(pg_relation_size(indexname::regclass)) as size,
        idx_scan
    FROM pg_stat_user_indexes
    WHERE idx_scan = 0
    AND schemaname = 'public'
    AND pg_relation_size(indexname::regclass) > 1024 * 1024  -- Larger than 1MB
)
SELECT
    'DROP INDEX ' || quote_ident(schemaname) || '.' || quote_ident(indexname) || ';' as drop_command,
    size,
    'Unused index on ' || tablename as reason
FROM unused_indexes
ORDER BY pg_size_bytes(size) DESC;

-- 3. Connection monitoring and cleanup
WITH connection_stats AS (
    SELECT
        datname,
        usename,
        application_name,
        client_addr,
        state,
        COUNT(*) as connection_count,
        MAX(query_start) as last_query,
        SUM(CASE WHEN state = 'idle' THEN 1 ELSE 0 END) as idle_connections,
        SUM(CASE WHEN state = 'active' THEN 1 ELSE 0 END) as active_connections
    FROM pg_stat_activity
    WHERE pid != pg_backend_pid()  -- Exclude current connection
    GROUP BY datname, usename, application_name, client_addr, state
)
SELECT
    *,
    CASE
        WHEN idle_connections > 10 AND last_query < NOW() - INTERVAL '1 hour'
        THEN 'Consider terminating idle connections'
        WHEN active_connections > 50
        THEN 'High active connection count - investigate'
        ELSE 'Normal'
    END as recommendation
FROM connection_stats
ORDER BY connection_count DESC;
```

## Database Security and Best Practices

### User Management and Security

```sql
-- PostgreSQL security configuration

-- 1. User and role management
-- Create application-specific roles
CREATE ROLE app_reader;
CREATE ROLE app_writer;
CREATE ROLE app_admin;

-- Grant appropriate permissions
GRANT CONNECT ON DATABASE myapp TO app_reader, app_writer, app_admin;
GRANT USAGE ON SCHEMA public TO app_reader, app_writer, app_admin;

-- Reader permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO app_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO app_reader;

-- Writer permissions (includes reader)
GRANT app_reader TO app_writer;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_writer;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT INSERT, UPDATE, DELETE ON TABLES TO app_writer;

-- Admin permissions (includes writer)
GRANT app_writer TO app_admin;
GRANT CREATE ON SCHEMA public TO app_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO app_admin;

-- 2. Create specific users
CREATE USER app_read_user WITH PASSWORD 'secure_password_here';
CREATE USER app_write_user WITH PASSWORD 'secure_password_here';
CREATE USER app_admin_user WITH PASSWORD 'secure_password_here';

-- Assign roles
GRANT app_reader TO app_read_user;
GRANT app_writer TO app_write_user;
GRANT app_admin TO app_admin_user;

-- 3. Security audit queries
\set security_audit 'SELECT usename, passwd, valuntil, usesuper, usecreatedb, usebypassrls FROM pg_user ORDER BY usename;'
\set role_memberships 'SELECT r.rolname, m.rolname as member FROM pg_roles r JOIN pg_auth_members am ON r.oid = am.roleid JOIN pg_roles m ON am.member = m.oid ORDER BY r.rolname;'
\set table_permissions 'SELECT grantee, table_schema, table_name, privilege_type FROM information_schema.role_table_grants WHERE table_schema = ''public'' ORDER BY grantee, table_name;'
```

### Backup and Recovery Procedures

```bash
#!/bin/bash
# Advanced PostgreSQL backup script

DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="myapp"
DB_USER="postgres"
BACKUP_DIR="/var/backups/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Full database backup with compression
echo "Starting full database backup..."
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    --verbose --clean --create --format=custom \
    --file="${BACKUP_DIR}/full_backup_${DATE}.dump"

# Schema-only backup for quick structure reference
echo "Creating schema-only backup..."
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    --schema-only --verbose \
    --file="${BACKUP_DIR}/schema_backup_${DATE}.sql"

# Data-only backup for large tables (if needed)
echo "Creating data-only backup..."
pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
    --data-only --verbose --format=custom \
    --file="${BACKUP_DIR}/data_backup_${DATE}.dump"

# Table-specific backups for critical tables
CRITICAL_TABLES=("users" "orders" "products")
for table in "${CRITICAL_TABLES[@]}"; do
    echo "Backing up critical table: ${table}"
    pg_dump -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" -d "${DB_NAME}" \
        --table="${table}" --verbose --format=custom \
        --file="${BACKUP_DIR}/table_${table}_${DATE}.dump"
done

# Cleanup old backups
echo "Cleaning up backups older than ${RETENTION_DAYS} days..."
find "${BACKUP_DIR}" -type f -name "*.dump" -mtime +${RETENTION_DAYS} -delete
find "${BACKUP_DIR}" -type f -name "*.sql" -mtime +${RETENTION_DAYS} -delete

# Verify backup integrity
echo "Verifying backup integrity..."
pg_restore --list "${BACKUP_DIR}/full_backup_${DATE}.dump" > /dev/null
if [ $? -eq 0 ]; then
    echo "Backup verification successful"

    # Log backup completion
    echo "$(date): Backup completed successfully - ${BACKUP_DIR}/full_backup_${DATE}.dump" >> "${BACKUP_DIR}/backup.log"
else
    echo "Backup verification failed!"
    echo "$(date): Backup verification failed - ${BACKUP_DIR}/full_backup_${DATE}.dump" >> "${BACKUP_DIR}/backup.log"
    exit 1
fi

echo "Backup process completed"
```

## Performance Optimization Techniques

### Query Optimization

```sql
-- Query optimization and performance tuning

-- 1. Identify slow queries with detailed analysis
WITH slow_queries AS (
    SELECT
        query,
        calls,
        total_time,
        mean_time,
        max_time,
        stddev_time,
        rows,
        100.0 * shared_blks_hit / NULLIF(shared_blks_hit + shared_blks_read, 0) AS cache_hit_ratio,
        shared_blks_read,
        shared_blks_written,
        temp_blks_read,
        temp_blks_written
    FROM pg_stat_statements
    WHERE mean_time > 100  -- Queries averaging more than 100ms
    OR total_time > 10000  -- Queries with high total time
    ORDER BY total_time DESC
)
SELECT
    LEFT(query, 100) as query_snippet,
    calls,
    ROUND(total_time::numeric, 2) as total_time_ms,
    ROUND(mean_time::numeric, 2) as mean_time_ms,
    ROUND(max_time::numeric, 2) as max_time_ms,
    rows,
    ROUND(cache_hit_ratio::numeric, 2) as cache_hit_pct,
    CASE
        WHEN temp_blks_written > 0 THEN 'Uses temp files'
        WHEN cache_hit_ratio < 95 THEN 'Poor cache utilization'
        WHEN mean_time > 1000 THEN 'Very slow average'
        ELSE 'Review for optimization'
    END as optimization_hint
FROM slow_queries
LIMIT 20;

-- 2. Index recommendations based on query patterns
WITH table_scans AS (
    SELECT
        schemaname,
        tablename,
        seq_scan,
        seq_tup_read,
        idx_scan,
        idx_tup_fetch,
        n_tup_ins + n_tup_upd + n_tup_del as modifications
    FROM pg_stat_user_tables
    WHERE schemaname = 'public'
),
index_candidates AS (
    SELECT
        schemaname,
        tablename,
        seq_scan,
        seq_tup_read,
        CASE
            WHEN seq_scan > 0 THEN seq_tup_read / seq_scan
            ELSE 0
        END as avg_seq_read,
        idx_scan,
        modifications,
        CASE
            WHEN seq_scan > idx_scan AND seq_tup_read > 10000
            THEN 'High sequential scan activity - consider indexing'
            WHEN modifications > (idx_scan + seq_scan) * 10
            THEN 'High modification rate - index overhead may be significant'
            ELSE 'Normal access pattern'
        END as recommendation
    FROM table_scans
)
SELECT * FROM index_candidates
WHERE recommendation LIKE 'High%'
ORDER BY avg_seq_read DESC;

-- 3. Connection and lock analysis
WITH connection_analysis AS (
    SELECT
        datname,
        usename,
        application_name,
        state,
        COUNT(*) as connection_count,
        AVG(EXTRACT(EPOCH FROM (now() - query_start))) as avg_query_duration,
        MAX(EXTRACT(EPOCH FROM (now() - query_start))) as max_query_duration,
        SUM(CASE WHEN state = 'idle in transaction' THEN 1 ELSE 0 END) as idle_in_transaction
    FROM pg_stat_activity
    WHERE pid != pg_backend_pid()
    GROUP BY datname, usename, application_name, state
)
SELECT
    *,
    CASE
        WHEN idle_in_transaction > 0 THEN 'Idle transactions detected - may cause blocking'
        WHEN max_query_duration > 300 THEN 'Long-running queries detected'
        WHEN connection_count > 100 THEN 'High connection count'
        ELSE 'Normal'
    END as alert
FROM connection_analysis
ORDER BY connection_count DESC;
```

## Key PostgreSQL Productivity Tips

### Essential psql Commands and Shortcuts

{{< tip title="Advanced psql Usage" >}} **Navigation and Information:**

- `\l` - List databases
- `\dt` - List tables
- `\d+ table_name` - Describe table with details
- `\df` - List functions
- `\dv` - List views
- `\dn` - List schemas

**Query Management:**

- `\e` - Edit last query in external editor
- `\g` - Re-run last query
- `\s` - Show command history
- `\i filename.sql` - Execute SQL file

**Output Control:**

- `\x` - Toggle expanded output
- `\a` - Toggle aligned output
- `\t` - Toggle tuples-only mode
- `\pset format html` - HTML output format {{< /tip >}}

### Database Health Monitoring

```sql
-- Daily health check queries for .psqlrc
\set daily_health 'WITH db_stats AS (SELECT datname, numbackends, xact_commit, xact_rollback, blks_read, blks_hit, temp_files, temp_bytes FROM pg_stat_database WHERE datname = current_database()), table_stats AS (SELECT COUNT(*) as table_count, SUM(n_tup_ins + n_tup_upd + n_tup_del) as total_modifications, SUM(seq_scan) as total_seq_scans FROM pg_stat_user_tables), index_stats AS (SELECT COUNT(*) as index_count, SUM(idx_scan) as total_index_scans FROM pg_stat_user_indexes) SELECT d.datname, d.numbackends as connections, d.xact_commit as commits, d.xact_rollback as rollbacks, ROUND(100.0 * d.blks_hit / NULLIF(d.blks_hit + d.blks_read, 0), 2) as cache_hit_ratio, t.table_count, t.total_modifications, t.total_seq_scans, i.index_count, i.total_index_scans FROM db_stats d CROSS JOIN table_stats t CROSS JOIN index_stats i;'

\set weekly_maintenance 'SELECT ''Run VACUUM ANALYZE on all tables'' as task, CASE WHEN MAX(last_autovacuum) < NOW() - INTERVAL ''7 days'' OR MAX(last_autovacuum) IS NULL THEN ''URGENT'' ELSE ''OK'' END as status FROM pg_stat_user_tables UNION ALL SELECT ''Check for unused indexes'', CASE WHEN COUNT(*) > 0 THEN ''REVIEW NEEDED'' ELSE ''OK'' END FROM pg_stat_user_indexes WHERE idx_scan = 0 AND pg_relation_size(indexrelname::regclass) > 1024*1024 UNION ALL SELECT ''Monitor connection count'', CASE WHEN COUNT(*) > 80 THEN ''HIGH'' WHEN COUNT(*) > 50 THEN ''MEDIUM'' ELSE ''OK'' END FROM pg_stat_activity WHERE pid != pg_backend_pid();'
```

This comprehensive exploration of PostgreSQL customization and management
demonstrates how proper configuration and monitoring can transform database
administration from reactive troubleshooting to proactive optimization.

---

_These PostgreSQL insights from my archive showcase the evolution from basic
database usage to advanced administration practices, emphasizing the importance
of proper tooling and systematic monitoring for database reliability and
performance._
