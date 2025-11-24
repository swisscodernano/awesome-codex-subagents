# /incident

Gestione incident di produzione con protocollo strutturato.

## Argomenti

- `$1`: Descrizione breve dell'incident (es. "502 errors", "service down", "high latency")

## Istruzioni

Sei l'Incident Commander. Segui questo protocollo:

### Phase 1: ASSESS (30 secondi)

```bash
# Quick status di tutti i servizi critici
systemctl status api.service nginx postgresql redis-server --no-pager

# Check load e risorse
uptime && free -h && df -h /
```

### Phase 2: IDENTIFY (2 minuti)

In base all'incident "$1", esegui diagnostica mirata:

**Per 502/503 errors:**
```bash
journalctl -u api.service -n 50 --no-pager
journalctl -u nginx -n 50 --no-pager
curl -I http://127.0.0.1:5002/health 2>/dev/null || echo "API non risponde"
```

**Per "service down":**
```bash
systemctl status $SERVICE --no-pager
journalctl -u $SERVICE -n 100 --no-pager
```

**Per "high latency":**
```bash
# Check database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
# Check redis
redis-cli ping
# Check API response time
curl -w "%{time_total}\n" -o /dev/null -s http://127.0.0.1:5002/health
```

### Phase 3: MITIGATE (immediato)

Proponi SEMPRE una mitigazione temporanea prima del fix completo:
- Restart del servizio se safe
- Failover se disponibile
- Rate limiting temporaneo
- Maintenance page

### Phase 4: FIX

Proponi il fix strutturale con:
1. Comando/codice esatto
2. Rollback plan se il fix fallisce
3. Tempo stimato di implementazione

### Phase 5: VERIFY

```bash
# Health check completo
curl -s http://127.0.0.1:5002/health | jq
systemctl is-active api.service nginx
```

## Output Format

```
## INCIDENT: $1
**Status**: [INVESTIGATING|IDENTIFIED|MITIGATING|RESOLVED]
**Impact**: [Descrizione impatto utenti]

## Timeline
- HH:MM - Incident detected
- HH:MM - Root cause identified
- HH:MM - Mitigation applied

## Root Cause
[Spiegazione]

## Mitigation (immediata)
[Cosa fare ORA per ripristinare il servizio]

## Fix (definitivo)
[Soluzione permanente]

## Prevention
[Come evitare in futuro]
```
