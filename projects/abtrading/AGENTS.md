# ABTrading - Project Instructions

> PerpFoundry Trading Agent - Automated cryptocurrency trading bot

---

## Stack Tecnico

| Component | Technology | Details |
|-----------|------------|---------|
| Backend | Flask + Flask-RESTX | REST API with Swagger |
| Trading | CCXT | Multi-exchange support |
| ML/Analysis | Prophet, Pandas, NumPy | Time series forecasting |
| Logging | Structlog | Structured JSON logging |
| API Docs | Swagger UI | `/swagger-ui` |

---

## File Principali

```
/var/www/abtrading/
├── app.py                    # Flask API entry point
├── trading_service.py        # Core trading logic
├── config.py                 # Configuration management
├── logger_config.py          # Structured logging setup
├── agents.json               # Agent configurations
├── system_prompts.json       # AI prompts for trading
└── requirements.txt          # Python dependencies
```

---

## Comandi Rapidi

```bash
# Activate venv
source /var/www/abtrading/venv/bin/activate

# Run locally
python app.py

# Check service (if systemd)
systemctl status abtrading.service

# View logs
journalctl -u abtrading.service -n 100 --no-pager

# Test API
curl http://localhost:5000/
curl -X POST http://localhost:5000/trading/run_cycle
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/trading/run_cycle` | Execute trading decision cycle |
| GET | `/swagger-ui` | API documentation |

---

## Trading Decision Model

```python
{
    'operation': 'buy|sell|hold',
    'symbol': 'BTC|ETH|...',
    'direction': 'long|short',
    'target_portion_of_balance': 0.0-1.0,
    'leverage': 1-100,
    'reason': 'Analysis explanation'
}
```

---

## Configuration

Key config in `config.py`:
- Exchange credentials (from env)
- Trading pairs
- Risk parameters
- API keys

---

## Safety Rules

- **NEVER** expose API keys in logs or responses
- **ALWAYS** validate trading decisions before execution
- **LIMIT** leverage according to risk parameters
- **LOG** all trading decisions with full context

---

## Debug Trading Issues

```bash
# Check exchange connectivity
python -c "from trading_service import *; print('OK')"

# Verify config
python -c "from config import config; print(config)"

# Test with dry run (if available)
curl -X POST http://localhost:5000/trading/run_cycle?dry_run=true
```

---

## Dependencies

Key packages:
- `ccxt` - Exchange abstraction
- `prophet` - Time series forecasting
- `flask-restx` - REST API with Swagger
- `structlog` - Structured logging
- `pandas`, `numpy` - Data analysis
