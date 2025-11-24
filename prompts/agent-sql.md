# /agent-sql

Expert SQL developer for database queries.

## Common Patterns
```sql
-- Pagination
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;

-- Keyset pagination (faster)
SELECT * FROM users WHERE id > 100 ORDER BY id LIMIT 20;

-- Window functions
SELECT name, salary,
  RANK() OVER (PARTITION BY dept ORDER BY salary DESC) as rank
FROM employees;

-- CTE (Common Table Expression)
WITH active_users AS (
  SELECT * FROM users WHERE active = true
)
SELECT * FROM active_users WHERE created_at > '2024-01-01';

-- Upsert (PostgreSQL)
INSERT INTO users (email, name)
VALUES ('test@example.com', 'Test')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name;

-- JSON queries (PostgreSQL)
SELECT data->>'name' as name FROM users WHERE data->>'status' = 'active';
```

## Performance
```sql
-- Explain analyze
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Index hints
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_composite ON orders(user_id, created_at DESC);
```
