# /health

Health check completo di tutti i servizi del server.

## Istruzioni

Esegui un health check completo del sistema:

### System Resources

```bash
echo "=== SYSTEM RESOURCES ==="
uptime
free -h
df -h / /var
```

### Services Status

```bash
echo "=== SERVICES STATUS ==="
systemctl is-active api.service nginx postgresql redis-server mcp-server.service
```

### Detailed Service Health

Per ogni servizio attivo, verifica:

```bash
# API
curl -s -w "\nResponse time: %{time_total}s\n" http://127.0.0.1:5002/health 2>/dev/null || echo "API: DOWN"

# Nginx
nginx -t 2>&1 | tail -1

# PostgreSQL
sudo -u postgres psql -c "SELECT 1;" -t 2>/dev/null && echo "PostgreSQL: OK" || echo "PostgreSQL: DOWN"

# Redis
redis-cli ping 2>/dev/null || echo "Redis: DOWN"

# MCP Server
curl -s http://127.0.0.1:5556/health 2>/dev/null || echo "MCP: DOWN"
```

### Network Ports

```bash
echo "=== LISTENING PORTS ==="
ss -tlnp | grep -E ':(80|443|5002|5556|5432|6379)\s'
```

### Recent Errors

```bash
echo "=== RECENT ERRORS (last 5 min) ==="
journalctl --since "5 minutes ago" -p err --no-pager | tail -20
```

## Output Format

```
## Server Health Report

### System
- **Uptime**: X days
- **Load**: X.XX
- **Memory**: XX% used
- **Disk**: XX% used

### Services
| Service | Status | Response Time |
|---------|--------|---------------|
| API | OK/DOWN | Xms |
| Nginx | OK/DOWN | - |
| PostgreSQL | OK/DOWN | - |
| Redis | OK/DOWN | - |
| MCP | OK/DOWN | Xms |

### Issues Found
- [Lista problemi se presenti]

### Recommendations
- [Suggerimenti se necessario]
```
