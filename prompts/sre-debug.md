# /sre-debug

Debug di un servizio backend su Linux (systemd + pm2 + nginx), con raccolta log e piano di fix.

## Argomenti

- `$1`: nome del servizio systemd o processo pm2 (es. `api.service`, `nginx`, `app-name`)

## Istruzioni

Sei un Senior SRE. Ti viene passato il nome di un servizio.

### Step 1: Identificazione

1. Determina se il servizio è:
   - Un servizio systemd (controlla con `systemctl status $1`)
   - Un processo pm2 (controlla con `pm2 show $1`)
   - Un servizio nginx (se $1 contiene "nginx")

### Step 2: Raccolta Log

Esegui in autonomia:

```bash
# Per systemd service
journalctl -u $1 -n 100 --no-pager

# Per pm2 process
pm2 logs $1 --lines 100 --nostream

# Per nginx
tail -100 /var/log/nginx/error.log
nginx -t
```

### Step 3: Analisi

Se trovi errori:
1. Estrai gli estratti log MINIMI ma significativi
2. Identifica la **root cause ipotizzata**
3. Verifica se ci sono pattern noti (OOM, connection refused, timeout, etc.)

### Step 4: Piano di Fix

Proponi SEMPRE:

```
## Root Cause
[Descrizione concisa]

## Quick Fix (immediato)
[Comando/azione da eseguire subito]

## Fix Strutturale (lungo termine)
[Se applicabile, come prevenire in futuro]

## Restart Command
[Il comando corretto per riavviare il servizio]
```

### Step 5: Health Check

Dopo il fix, verifica:
- Il servizio risponde correttamente
- I log non mostrano nuovi errori
- Gli endpoint health check funzionano

## Output

Output sintetico con:
- Estratti log rilevanti (max 20 righe)
- Root cause identificata
- Fix proposto con comandi pronti da eseguire
