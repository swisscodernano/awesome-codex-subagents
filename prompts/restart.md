# /restart

Restart sicuro di un servizio con pre-check e post-check.

## Argomenti

- `$1`: nome del servizio (es. `api`, `nginx`, `mcp-server`)

## Service Mapping

| Input | Systemd Service |
|-------|-----------------|
| api | api.service |
| nginx | nginx |
| mcp | mcp-server.service |
| mcp-server | mcp-server.service |
| postgresql | postgresql |
| redis | redis-server |

## Istruzioni

### Pre-Flight Check

```bash
echo "=== PRE-RESTART CHECK ==="

# 1. Verifica stato attuale
systemctl status $SERVICE --no-pager | head -10

# 2. Per nginx, verifica config
if [ "$SERVICE" = "nginx" ]; then
    nginx -t
fi

# 3. Salva PID attuale per verifica
systemctl show $SERVICE -p MainPID --value
```

### Restart

```bash
echo "=== RESTARTING $SERVICE ==="
sudo systemctl restart $SERVICE
```

### Post-Restart Verification

```bash
echo "=== POST-RESTART CHECK ==="

# 1. Attendi 3 secondi per startup
sleep 3

# 2. Verifica nuovo stato
systemctl status $SERVICE --no-pager | head -10

# 3. Verifica health endpoint se applicabile
case $SERVICE in
    api.service)
        curl -s http://127.0.0.1:5002/health | head -5
        ;;
    mcp-server.service)
        curl -s http://127.0.0.1:5556/health | head -5
        ;;
    nginx)
        curl -sI http://127.0.0.1/ | head -3
        ;;
esac

# 4. Check log per errori immediati
journalctl -u $SERVICE --since "10 seconds ago" --no-pager
```

## Output

```
## Restart: $1

### Pre-Check
- Status: [active/inactive/failed]
- PID: XXXX

### Restart
- Command: `systemctl restart $SERVICE`
- Result: [success/failed]

### Post-Check
- New Status: [active/inactive/failed]
- New PID: XXXX
- Health: [OK/FAILED]
- Errors: [none/list]
```

## Safety Rules

- NON riavviare `postgresql` senza conferma esplicita (rischio perdita connessioni)
- Per nginx, SEMPRE fare `nginx -t` prima
- Se il servizio non parte, mostra i log e NON ritentare automaticamente
