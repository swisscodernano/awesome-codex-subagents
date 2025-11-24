# ABTrading - Trading Bot

**Stack:** Python 3.11+ | Custom trading bot | Systemd service

## Critical Safety Rules

⚠️ **BEFORE ANY ACTION:**
1. **NEVER restart bot during active trade**
2. **ALWAYS check DRY_RUN mode** before restart
3. **STOP bot IMMEDIATELY** if trading anomaly detected
4. **VERIFY exchange balance** before allowing trades
5. **NEVER show API keys** in output

## Architecture

```
/var/www/abtrading/
├── main.py              # Entry point
├── strategies/          # Trading strategies
├── indicators/          # Technical indicators
├── exchanges/           # Exchange connectors (CCXT)
├── logs/                # Application logs
│   ├── trading.log      # Main log
│   └── error.log        # Error log
├── data/                # Market data cache
├── config/              # Configuration
├── .env                 # API keys (NEVER commit!)
└── venv/                # Python virtual environment
```

## Service Management

### Systemd Service
```bash
# Status (use this first!)
systemctl status abtrading.service
journalctl -u abtrading.service -n 200 --no-pager

# Control (ASK USER FIRST!)
sudo systemctl start abtrading.service
sudo systemctl stop abtrading.service
sudo systemctl restart abtrading.service
```

### Pre-Restart Checklist
Run this BEFORE ANY restart:
```bash
# 1. Check for active trades
tail -20 /var/www/abtrading/logs/trading.log | grep -i "trade\|position"

# 2. Check exchange balance
# (requires user confirmation)

# 3. Verify DRY_RUN mode
grep "DRY_RUN" /var/www/abtrading/.env

# 4. Backup config if changed
cp .env .env.backup-$(date +%Y%m%d-%H%M%S)
```

## Common Issues

### 1. Bot Crashed
**Symptoms:** Service inactive, no recent logs

**Diagnostic:**
```bash
# Check logs for Python traceback
journalctl -u abtrading.service -n 500 | grep -A 20 "Traceback"

# Check last 50 lines of error log
tail -50 /var/www/abtrading/logs/error.log

# Check system resources (OOM kill?)
journalctl -n 100 | grep -i "out of memory\|killed"
```

**Common causes:**
- Missing/outdated dependencies (ccxt, pandas, numpy, talib)
- Exchange API connection failure
- Invalid API keys
- OOM killed (high memory usage)

### 2. Trading Anomaly
**Symptoms:** Unexpected trades, losses, wrong positions

**IMMEDIATE ACTION:**
```bash
# STOP BOT IMMEDIATELY
sudo systemctl stop abtrading.service

# DON'T restart until:
# 1. User reviews recent trades
# 2. Strategy verified
# 3. Market conditions checked
# 4. Root cause understood
```

### 3. Exchange API Errors
**Symptoms:** 401, 403, 429, 500 errors in logs

**Diagnostic:**
```bash
# Check API errors
grep -i "401\|403\|429\|api.*error" /var/www/abtrading/logs/trading.log | tail -20

# Test exchange connectivity
cd /var/www/abtrading && source venv/bin/activate
python3 -c "import ccxt; exchange = ccxt.binance(); print(exchange.fetch_status())"
```

**Fixes:**
- **401/403:** API key invalid → Check .env
- **429:** Rate limit → Increase delays or enable rate limiter
- **500:** Exchange issue → Check exchange status page

### 4. Dependency Issues
**Symptoms:** ModuleNotFoundError, ImportError

**Fix:**
```bash
cd /var/www/abtrading
source venv/bin/activate

# Check what's installed
pip list

# Re-install requirements
pip install -r requirements.txt

# Test imports
python3 -c "import ccxt, pandas, numpy, talib; print('OK')"
```

## Environment Variables

**Location:** `/var/www/abtrading/.env` (NEVER commit to git!)

**Critical variables:**
```bash
EXCHANGE=binance              # Exchange name
API_KEY=xxx                   # KEEP SECRET
API_SECRET=xxx                # KEEP SECRET
TRADING_PAIR=BTC/USDT         # Trading pair
STRATEGY=scalping             # Strategy name
DRY_RUN=false                 # ⚠️ false = REAL TRADING!
MAX_POSITION_SIZE=1000        # Max $ per trade
STOP_LOSS_PCT=2.0             # Stop loss %
```

## Logs Location

```bash
# Main trading log
tail -f /var/www/abtrading/logs/trading.log

# Error log
tail -f /var/www/abtrading/logs/error.log

# Systemd log
journalctl -u abtrading.service -f

# Find specific errors
grep -i "error\|exception\|traceback" /var/www/abtrading/logs/*.log
```

## Update & Deploy

```bash
cd /var/www/abtrading

# 1. Pull latest code
git pull origin main

# 2. Activate venv
source venv/bin/activate

# 3. Update dependencies
pip install -r requirements.txt

# 4. Check config changes
git diff HEAD~1 .env.example

# 5. Test (if available)
python3 -m pytest tests/

# 6. Restart (ONLY if safe!)
sudo systemctl restart abtrading.service

# 7. Verify
systemctl status abtrading.service
tail -50 /var/www/abtrading/logs/trading.log
```

## Monitoring

**Suggested cron job:**
```bash
# Check bot is running every 5 minutes
*/5 * * * * systemctl is-active abtrading.service || echo "ABTrading DOWN" | mail -s "ALERT" admin@email.com
```

## Debug Session Example

```bash
# 1. Enter project
cd /var/www/abtrading

# 2. Activate venv
source venv/bin/activate

# 3. Check status
systemctl status abtrading.service

# 4. View recent logs
journalctl -u abtrading.service -n 100

# 5. Check for errors
grep -i "error" logs/trading.log | tail -20

# 6. Test exchange connection
python3 -c "import ccxt; print(ccxt.binance().fetch_ticker('BTC/USDT'))"

# 7. If all OK, consider restart
# (but ASK USER FIRST!)
```

## Incident Response Priority

**P1 - CRITICAL (Act immediately):**
- Trading anomaly detected → **STOP BOT**
- Unexpected losses → **STOP BOT**
- API keys compromised → **STOP BOT + ROTATE KEYS**

**P2 - HIGH (Investigate first):**
- Bot crashed → Analyze logs, propose fix
- Exchange API errors → Check connectivity
- OOM killed → Investigate memory usage

**P3 - MEDIUM (Plan fix):**
- Missing dependencies → Reinstall
- Performance degradation → Profile code
- Log file too large → Rotate logs

**P4 - LOW (Schedule):**
- Code refactoring needed
- Minor bugs
- Documentation updates

## Contact/Escalation

- **Always notify user** before restarting bot
- **Never restart** without understanding crash cause
- **Document all actions** in incident notes
- **Preserve logs** before restart (they rotate!)

---

**Remember:** This is REAL MONEY. Safety first, always.
