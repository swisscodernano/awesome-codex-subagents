# AIAgens - Project-Specific Instructions

> Questo file viene caricato da Codex CLI quando lavori nella directory AIAgens.
> Integra le istruzioni globali di `~/.codex/AGENTS.md` con context specifico del progetto.

---

## Stack Tecnico

| Component | Technology | Port | Service |
|-----------|------------|------|---------|
| Web Server | Nginx | 80/443 | nginx |
| API | Flask + Gunicorn (gevent) | 5002 | api.service |
| Database | PostgreSQL 14 | 5432 | postgresql |
| Cache | Redis | 6379 | redis-server |
| MCP Server | FastAPI + Uvicorn | 5556 | mcp-server.service |

---

## File Critici

### Configurazione
- `/etc/nginx/sites-enabled/aiagens.ch` - Nginx config
- `/etc/systemd/system/api.service` - Gunicorn service
- `/etc/systemd/system/mcp-server.service` - MCP service
- `/etc/aiagens/secrets.conf` - Credentials (0400 root)
- `/var/www/aiagens.ch/.env` - Non-sensitive config

### Log
- `/var/log/aiagens/gunicorn-error.log` - API errors
- `/var/log/aiagens/gunicorn-access.log` - API access
- `/var/log/nginx/error.log` - Nginx errors
- `/var/log/nginx/access.log` - Nginx access

### Codice Principale
- `/var/www/aiagens.ch/api/app.py` - Main Flask app
- `/var/www/aiagens.ch/api/routes/` - Blueprint routes
- `/var/www/aiagens.ch/services/` - Business logic

---

## Comandi Rapidi

### Debug API
```bash
# Status
systemctl status api.service --no-pager

# Log recenti
journalctl -u api.service -n 100 --no-pager

# Health check
curl -s http://127.0.0.1:5002/health | jq

# Restart
sudo systemctl restart api.service
```

### Debug Nginx
```bash
# Test config
nginx -t

# Log errori
tail -100 /var/log/nginx/error.log

# Reload (dopo fix config)
sudo systemctl reload nginx

# Clear cache
sudo find /var/cache/nginx -type f -delete && sudo systemctl reload nginx
```

### Debug Database
```bash
# Connessione
sudo -u postgres psql -d aiagens

# Query attive
sudo -u postgres psql -c "SELECT pid, state, query FROM pg_stat_activity WHERE state != 'idle';"

# Connessioni totali
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
```

### Debug MCP Server
```bash
# Status
systemctl status mcp-server.service --no-pager

# Log
journalctl -u mcp-server.service -n 100 --no-pager

# Health
curl -s http://127.0.0.1:5556/health | jq
```

---

## Architettura Blueprint

Il progetto usa Flask Blueprints (Nov 2025):

| Blueprint | Prefix | File |
|-----------|--------|------|
| admin_bp | /admin | api/routes/admin_routes.py |
| client_bp | /client | api/routes/client_routes.py |
| widget_bp | /widget | api/routes/widget_routes.py |
| public_bp | / | api/routes/public_routes.py |
| auth_bp | / | api/routes/auth_routes.py |

**IMPORTANTE:** Usa sempre `url_for('blueprint.endpoint')`:
```python
# Corretto
url_for('auth.login')
url_for('admin.admin_dashboard')

# SBAGLIATO (BuildError)
url_for('login')
```

---

## Regole Critiche (da CLAUDE.md)

1. **B2C ≠ B2B** - `customer_bookings` è SOLO B2B, mai usare in client dashboard
2. **Multi-tenant** - SEMPRE filtrare per `customer_id`
3. **Gevent** - Patchare psycopg2 PRIMA di importarlo:
   ```python
   from psycogreen.gevent import patch_psycopg
   patch_psycopg()
   import psycopg2
   ```
4. **Credits** - Richiedono DUE webhook: `conversation:init` E `conversation:end`
5. **day_of_week** - Usa convenzione Python: 0 = Monday (non 1!)

---

## Troubleshooting Comune

### 502 Bad Gateway
1. Check api.service: `systemctl status api.service`
2. Check gunicorn log: `tail -50 /var/log/aiagens/gunicorn-error.log`
3. Check port: `ss -tlnp | grep 5002`
4. Restart: `sudo systemctl restart api.service`

### Credits non scalati
1. Verifica webhook: `journalctl -u api.service | grep conversation`
2. Fix webhook: `./venv/bin/python3 scripts/fix_agent_webhooks.py <agent_id>`

### Translation keys visibili (nav_xxx)
1. Controlla `/assets/js/app.js` linee 113-128
2. Aggiungi path matcher per nuova pagina
3. Incrementa versione: `app.js?v=XX`
4. Clear cache: `sudo find /var/cache/nginx -type f -delete && sudo systemctl reload nginx`

### CSP Violation
1. Modifica `/api/middleware/security_headers.py`
2. Aggiungi dominio a `script-src` E `connect-src`

---

## Deploy Checklist

1. `git status` - verifica branch e modifiche
2. `git pull origin main`
3. `source venv/bin/activate && pip install -r requirements.txt`
4. `sudo systemctl restart api.service`
5. `curl http://127.0.0.1:5002/health` - verifica API
6. `journalctl -u api.service -n 20` - check errori

---

## RAG Tools

Il progetto ha RAG tools configurati in `codex.yaml`:

```bash
# Query knowledge base
codex-rag query "come funziona il wizard setup"

# Store nuove informazioni
codex-rag store "nuova implementazione..."

# Info progetto
codex-rag info
```

---

## Documentazione

- `CLAUDE.md` - Quick reference (leggi sempre prima)
- `docs/CLAUDE.md.legacy-20251102` - Documentazione completa
- `docs/blueprints/CLIENT_DASHBOARD_BLUEPRINT.md` - Dashboard architecture
