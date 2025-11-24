# /agent-postgres

Expert PostgreSQL administrator.

## Admin Commands
```sql
-- Database info
\l                    -- List databases
\dt                   -- List tables
\d+ table_name        -- Describe table
\du                   -- List users

-- Performance
SELECT * FROM pg_stat_activity;
SELECT * FROM pg_stat_user_tables;
SELECT * FROM pg_stat_user_indexes;

-- Locks
SELECT * FROM pg_locks WHERE granted = false;

-- Table sizes
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;

-- Vacuum
VACUUM ANALYZE table_name;
VACUUM FULL table_name;
```

## Backup/Restore
```bash
# Backup
pg_dump -Fc dbname > backup.dump
pg_dumpall > all_databases.sql

# Restore
pg_restore -d dbname backup.dump
psql -f all_databases.sql postgres
```

## Replication
```sql
-- Check replication status
SELECT * FROM pg_stat_replication;
SELECT * FROM pg_replication_slots;
```
