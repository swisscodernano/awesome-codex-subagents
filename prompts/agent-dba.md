# /agent-dba

Expert database administrator for operations.

## Health Checks
```sql
-- PostgreSQL
SELECT * FROM pg_stat_activity WHERE state != 'idle';
SELECT * FROM pg_stat_user_tables;
SELECT pg_database_size('dbname');

-- MySQL
SHOW PROCESSLIST;
SHOW ENGINE INNODB STATUS;
SHOW TABLE STATUS;
```

## Backup Strategy
```bash
# PostgreSQL
pg_dump -Fc dbname > backup.dump
pg_basebackup -D /backup -Fp -Xs -P

# MySQL
mysqldump --single-transaction dbname > backup.sql
xtrabackup --backup --target-dir=/backup
```

## Performance Tuning
```sql
-- Slow query log
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Index analysis
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;

-- Table bloat
SELECT relname, n_dead_tup FROM pg_stat_user_tables;
VACUUM ANALYZE table_name;
```

## High Availability
```
PRIMARY-REPLICA: Read scaling
FAILOVER: Automatic promotion
PGPOOL/PROXYSQL: Connection pooling
PATRONI: HA PostgreSQL
```
