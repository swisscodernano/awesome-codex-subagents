# /deploy

Deploy sicuro con git pull e restart servizi.

## Argomenti

- `$1`: path del progetto (es. `/var/www/aiagens.ch`)
- `$2`: (opzionale) branch da deployare (default: main)

## Istruzioni

### Pre-Deploy Check

```bash
cd $1

echo "=== PRE-DEPLOY CHECK ==="

# 1. Verifica branch corrente e stato
git status
git log --oneline -3

# 2. Verifica modifiche locali non committate
if ! git diff --quiet; then
    echo "WARNING: Uncommitted changes detected!"
    git diff --stat
fi

# 3. Backup timestamp
BACKUP_TS=$(date +%Y%m%d_%H%M%S)
echo "Backup timestamp: $BACKUP_TS"
```

### Deploy

```bash
echo "=== DEPLOYING ==="

# 1. Fetch e pull
git fetch origin
git pull origin ${2:-main}

# 2. Se Python: installa dipendenze
if [ -f "requirements.txt" ]; then
    source venv/bin/activate 2>/dev/null || true
    pip install -r requirements.txt --quiet
fi

# 3. Se Node: installa dipendenze
if [ -f "package.json" ]; then
    npm install --quiet
fi
```

### Restart Services

```bash
echo "=== RESTARTING SERVICES ==="

# Per AIAgens
if [ "$1" = "/var/www/aiagens.ch" ]; then
    sudo systemctl restart api.service
    sleep 3
    curl -s http://127.0.0.1:5002/health | jq -r '.status // "error"'
fi

# Clear nginx cache se presente
if [ -d "/var/cache/nginx" ]; then
    sudo find /var/cache/nginx -type f -delete 2>/dev/null
    sudo systemctl reload nginx
fi
```

### Post-Deploy Verification

```bash
echo "=== POST-DEPLOY CHECK ==="

# 1. Verifica commit deployato
git log --oneline -1

# 2. Verifica servizi
systemctl is-active api.service nginx

# 3. Health check
curl -s http://127.0.0.1:5002/health | jq

# 4. Check errori nei log (ultimi 30 sec)
journalctl -u api.service --since "30 seconds ago" -p err --no-pager
```

## Output Format

```
## Deploy Report

### Project
- Path: $1
- Branch: ${2:-main}

### Changes Deployed
[git log output]

### Services Restarted
- api.service: [OK/FAILED]
- nginx: [reloaded]

### Health Check
- API: [OK/FAILED]
- Response time: Xms

### Errors
[none o lista errori]
```

## Rollback

Se il deploy fallisce:

```bash
# Rollback all'ultimo commit funzionante
git reset --hard HEAD~1
sudo systemctl restart api.service
```
