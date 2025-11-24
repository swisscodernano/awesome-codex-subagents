# AIAgens.ch - AI Voice Agent Platform Context

## Stack Tecnico

- **Framework:** Python 3.11 + Flask
- **Server:** Gunicorn (4 workers)
- **Database:** PostgreSQL 16
- **Cache:** Redis
- **Web Server:** Nginx (reverse proxy)
- **Services:** Systemd `api.service`, `mcp-server.service`
- **Frontend:** Vanilla JS + TailwindCSS
- **AI:** ElevenLabs Conversational AI + Gemini 2.0

## Architettura

```
/var/www/aiagens.ch/
├── api/
│   ├── app.py                    # Main Flask app (6,735 lines)
│   ├── routes/                   # Blueprint routes
│   │   ├── admin_routes.py       # Admin dashboard
│   │   ├── client_routes.py      # Client dashboard
│   │   ├── widget_routes.py      # Embeddable widget
│   │   ├── public_routes.py      # Public pages
│   │   └── auth_routes.py        # Authentication
│   ├── templates/                # Jinja2 templates
│   ├── static/                   # CSS/JS assets
│   ├── integrations/             # Google, Telegram, etc.
│   └── middleware/               # Auth, security headers
├── services/
│   ├── mcp-server/               # MCP tool server (port 5556)
│   ├── elevenlabs_agent_manager.py
│   └── credits_manager.py
├── scripts/                      # Utility scripts
├── venv/                         # Virtual environment
├── .env                          # Non-sensitive config
└── /etc/aiagens/secrets.conf     # SECRETS (0400 root)
```

## Services

### Main API (port 5002)
```bash
# Service: api.service
systemctl status api.service
journalctl -u api.service -n 200 --no-pager

# Gunicorn workers
ps aux | grep gunicorn
lsof -i :5002

# Restart (usa script!)
cd /var/www/aiagens.ch && ./restart_all.sh
# O manuale:
sudo systemctl restart api.service
```

### MCP Server (port 5556)
```bash
# Service: mcp-server.service
systemctl status mcp-server.service
journalctl -u mcp-server.service -n 200 --no-pager

# Health check
curl http://localhost:5556/health
```

### Nginx
```bash
# Config: /etc/nginx/sites-available/aiagens.ch
sudo nginx -t
sudo systemctl reload nginx

# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Database Schema (PostgreSQL)

### Core Tables
- `customer_agents` - Agent registry (1 customer → N agents)
- `agent_licenses` - License distribution (1 agent → M licenses)
- `customer_credits` - Credits system (1 credit = 1 second)
- `conversations` - Conversation logs
- `business_hours` - Working schedule
- `google_oauth_tokens` - Google Calendar integration
- `waitlist_entries` - Waitlist when no slots

**IMPORTANT:** B2C product. NEVER use `customer_bookings` table (B2B only!)

## Log Locations

```bash
# Application logs
/var/log/aiagens/gunicorn-error.log
/var/log/aiagens/gunicorn-access.log

# Systemd logs
journalctl -u api.service
journalctl -u mcp-server.service

# Nginx logs
/var/log/nginx/access.log
/var/log/nginx/error.log

# Database logs
/var/log/postgresql/postgresql-16-main.log
```

## Incident Playbook

### 1. 502 Bad Gateway (Nginx)
**Causa:** Gunicorn down o unreachable
**Azioni:**
```bash
systemctl status api.service
journalctl -u api.service -n 100
lsof -i :5002  # Should show gunicorn
sudo systemctl restart api.service
```

### 2. 500 Internal Server Error (Flask)
**Causa:** Python exception
**Azioni:**
```bash
tail -n 200 /var/log/aiagens/gunicorn-error.log | grep -i "error\|exception\|traceback"
# Se ModuleNotFoundError:
cd /var/www/aiagens.ch && source venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart api.service
```

### 3. Database Connection Issues
**Causa:** PostgreSQL down o connection pool exhausted
**Azioni:**
```bash
systemctl status postgresql
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"
# Check for blocking queries:
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
```

### 4. Credits Not Charged (ElevenLabs webhooks)
**Causa:** Missing webhooks configuration
**Fix:**
```bash
cd /var/www/aiagens.ch
./venv/bin/python3 scripts/fix_agent_webhooks.py <agent_id>

# Verify logs
journalctl -u api.service -f | grep "conversation"
# Should see BOTH: conversation:init AND conversation:end
```

### 5. Agent Not Calling Tools (MCP)
**Causa:** MCP server down o agent config wrong
**Ações:**
```bash
curl http://localhost:5556/health
systemctl status mcp-server.service
journalctl -u mcp-server.service -n 100
```

## Blueprint Architecture

**Status:** Production (Phase 1-6A Complete)

**5 Blueprints:**
- `admin_bp` → `/admin` (29 routes)
- `client_bp` → `/client` (10 routes)
- `widget_bp` → `/widget` (11 routes)
- `public_bp` → `/` (11 routes)
- `auth_bp` → `/` (4 routes)

**CRITICAL:** Always use Blueprint-prefixed `url_for()`:
```python
# ✅ CORRECT
redirect(url_for('auth.login'))
redirect(url_for('client.wizard_setup'))

# ❌ WRONG (BuildError!)
redirect(url_for('login'))
```

## Common Issues

### Translation Keys Showing
**Causa:** TranslationManager not loading required modules
**Fix:** Check `/assets/js/app.js` path matcher (line 113-128)

### Nested data-include Doesn't Work
**Causa:** `loader.js` loads ONLY first level
**Fix:** Always inline content in partials, use Jinja2 `{% include %}`

### War Room Chart Errors
**Causa:** Chart.js instances in reactive Alpine data
**Fix:** Charts OUTSIDE Alpine, data INSIDE

## Environment Variables

**Location:** `/etc/aiagens/secrets.conf` (0400 root:root)

**Required:**
```bash
DATABASE_URL=postgresql://...
GOOGLE_OAUTH_CLIENT_ID=...
GOOGLE_OAUTH_CLIENT_SECRET=...
ELEVENLABS_SYSTEM_API_KEY=...
ELEVENLABS_WEBHOOK_SECRET=...
STRIPE_SECRET_KEY=...
```

**NEVER:**
- ❌ Commit secrets to git
- ❌ Hardcode credentials
- ❌ Put secrets in .env

## Deployment Workflow

```bash
# 1. Pull latest code
cd /var/www/aiagens.ch
git pull origin main

# 2. Update dependencies (if requirements.txt changed)
source venv/bin/activate
pip install -r requirements.txt

# 3. Database migrations (if any)
# flask db upgrade  # (se usi Alembic)

# 4. Restart services
./restart_all.sh
# O manuale:
sudo systemctl restart api.service
sudo systemctl restart mcp-server.service

# 5. Verify
curl https://aiagens.ch
systemctl status api.service
journalctl -u api.service -n 50
```

## Performance Monitoring

```bash
# Gunicorn workers health
ps aux | grep gunicorn | wc -l  # Should be 5 (1 master + 4 workers)

# Database connections
sudo -u postgres psql -c "SELECT count(*) FROM pg_stat_activity;"

# Redis memory
redis-cli info memory | grep used_memory_human

# Disk usage
df -h | grep "/var/www"
```

## Security

### Multi-Tenant Isolation
**CRITICAL:** Always filter by `customer_id` in queries to prevent data leaks

### Gevent Compatibility
**ALWAYS patch BEFORE importing psycopg2:**
```python
from psycogreen.gevent import patch_psycopg
patch_psycopg()
import psycopg2
```

## Contact/Escalation

- **Priority 1 (P1):** Site down, database down → Restart immediately
- **Priority 2 (P2):** 500 errors, agent not working → Investigate logs first
- **Priority 3 (P3):** Performance issues, minor bugs → Plan fix during maintenance

**ALWAYS:**
1. Check logs before restart
2. Use `restart_all.sh` when available
3. Verify after restart (curl + status + logs)
4. Document what you did in incident notes
