# /agent-database

Expert database optimizer for query performance.

## PostgreSQL
```sql
-- Explain analyze
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;

-- Index usage
SELECT indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes;

-- Slow queries
SELECT query, calls, mean_time, total_time
FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- Table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables;

-- Connection stats
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
```

## Indexing Strategy
```sql
-- B-tree (default, equality/range)
CREATE INDEX idx_users_email ON users(email);

-- Partial index
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at DESC);

-- GIN (full-text, arrays, JSONB)
CREATE INDEX idx_posts_content ON posts USING gin(to_tsvector('english', content));
```

## Query Optimization
```
1. Use EXPLAIN ANALYZE
2. Add appropriate indexes
3. Avoid SELECT *
4. Use pagination (LIMIT/OFFSET or keyset)
5. Batch operations
6. Consider materialized views
7. Partition large tables
```
