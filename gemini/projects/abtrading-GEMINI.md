# ABTrading - Trading Bot Context

## Stack Tecnico

- **Linguaggio:** Python 3.11+
- **Framework:** Custom trading bot
- **Dependencies:** NumPy, Pandas, TA-Lib, CCXT, requests
- **Ambiente:** Virtualenv `/var/www/abtrading/venv/`
- **Esecuzione:** Systemd service `abtrading.service` oppure manuale
- **Configurazione:** `.env` file (API keys, exchange config)

## Architettura

```
/var/www/abtrading/
├── venv/                    # Virtual environment
├── main.py                  # Entry point
├── strategies/              # Trading strategies
├── indicators/              # Technical indicators
├── exchanges/               # Exchange connectors
├── config/                  # Configuration files
├── logs/                    # Trading logs
├── data/                    # Market data cache
└── .env                     # Environment variables (API keys)
```

## Log Principali

- **Application logs:** `/var/www/abtrading/logs/trading.log`
- **Systemd logs:** `journalctl -u abtrading.service`
- **Error logs:** `/var/www/abtrading/logs/error.log`

## Comandi Diagnostici

### Status Bot
```bash
# Se gestito da systemd
systemctl status abtrading.service
journalctl -u abtrading.service -n 200 --no-pager

# Se running manualmente
ps aux | grep main.py
lsof -i :PORT  # Se usa API HTTP
```

### Check Dependencies
```bash
cd /var/www/abtrading
source venv/bin/activate
pip list
python -c "import ccxt, pandas, numpy, talib; print('OK')"
```

### Logs Analysis
```bash
tail -f /var/www/abtrading/logs/trading.log
grep -i "error\|exception\|traceback" /var/www/abtrading/logs/trading.log | tail -20
```

### Database/Redis (se usati)
```bash
redis-cli ping
redis-cli keys "abtrading:*"
```

## Politica Incident

### 1. Bot Crashed
**Azioni:**
1. Controlla logs per traceback Python
2. Verifica connessione exchange (API keys, rate limits)
3. Controlla memoria/CPU (bot potrebbe essere OOM killed)
4. Verifica data/cache integrity
5. Restart bot SOLO dopo aver capito la causa

### 2. Trading Anomalo
**Azioni:**
1. **STOP IMMEDIATO** il bot (via systemctl stop o kill)
2. Analizza ultimi trade nei log
3. Controlla balance exchange
4. Verifica strategia attiva e parametri
5. NON riavviare senza conferma esplicita utente

### 3. Exchange API Errors
**Azioni:**
1. Verifica status exchange (`curl https://status.binance.com/api/v1/status`)
2. Controlla API key validity/permissions
3. Verifica rate limits
4. Test connessione con script minimale

### 4. Dependency Issues
**Azioni:**
1. Verifica venv integrity: `which python` (deve puntare a venv)
2. Re-install dependencies: `pip install -r requirements.txt`
3. Check version conflicts: `pip check`

## Comandi Standard

### Start/Stop
```bash
# Via systemd
sudo systemctl start abtrading.service
sudo systemctl stop abtrading.service
sudo systemctl restart abtrading.service

# Manuale (solo per test!)
cd /var/www/abtrading
source venv/bin/activate
python main.py
```

### Update Code
```bash
cd /var/www/abtrading
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart abtrading.service
```

### Backup Config/Data
```bash
cp /var/www/abtrading/.env /var/www/abtrading/.env.backup
tar -czf /var/www/abtrading/backup-$(date +%Y%m%d).tar.gz data/ config/
```

## Variabili Ambiente Critiche

**`.env` file:**
```bash
EXCHANGE=binance
API_KEY=xxx
API_SECRET=xxx
TRADING_PAIR=BTC/USDT
STRATEGY=scalping
DRY_RUN=false  # ATTENZIONE: false = trading reale!
```

## Sicurezza

### CRITICAL RULES:
1. **NEVER commit .env to git**
2. **NEVER show API keys in logs/output**
3. **ALWAYS check DRY_RUN mode before restart**
4. **ALWAYS verify balance before trading**
5. **NEVER restart bot during active trade**

### Pre-Restart Checklist:
- [ ] Verifica nessun trade aperto
- [ ] Check exchange balance
- [ ] Conferma configurazione corretta
- [ ] Backup .env se modificato
- [ ] Dry-run test se strategia cambiata

## Debugging Common Issues

### ModuleNotFoundError
```bash
# Fix: reinstall in venv
cd /var/www/abtrading
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### API Key Invalid
```bash
# Test API connectivity
python -c "import ccxt; exchange = ccxt.binance({'apiKey': 'xxx', 'secret': 'xxx'}); print(exchange.fetch_balance())"
```

### Rate Limit Exceeded
```bash
# Check logs for 429 errors
grep "429" /var/www/abtrading/logs/trading.log
# Soluzione: aumenta delay tra richieste o usa exchange.enableRateLimit = True
```

### OOM Killed
```bash
# Check memoria disponibile
free -h
# Check process memory usage
ps aux --sort=-%mem | head -10
# Soluzione: ottimizza data caching o aumenta RAM
```

## Monitoring Setup

**Suggerito (se non già fatto):**
```bash
# Cron job per monitoring
*/5 * * * * systemctl is-active abtrading.service || echo "ABTrading DOWN" | mail -s "ALERT" admin@example.com
```

## Contact/Escalation

- **Log analysis priority:** trading.log → error.log → systemd journal
- **Critical errors:** STOP bot immediately, notify user
- **Non-critical:** Proponi fix, chiedi conferma per restart
