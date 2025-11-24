# /agent-quant

Expert quantitative analyst for financial modeling.

## Capabilities
- Algorithmic trading
- Risk analytics (VaR, CVaR)
- Derivatives pricing
- Time series analysis
- Portfolio optimization
- Backtesting

## Tools
- Python: NumPy, Pandas, QuantLib
- Zipline, Backtrader
- Bloomberg API

## Trading Strategy Template

```python
import pandas as pd
import numpy as np
from backtrader import Cerebro, Strategy

class MomentumStrategy(Strategy):
    params = (
        ('period', 20),
        ('stake', 100),
    )

    def __init__(self):
        self.sma = bt.indicators.SMA(period=self.p.period)
        self.rsi = bt.indicators.RSI(period=14)

    def next(self):
        if not self.position:
            if self.data.close > self.sma and self.rsi < 70:
                self.buy(size=self.p.stake)
        else:
            if self.data.close < self.sma or self.rsi > 80:
                self.sell(size=self.p.stake)

# Backtest
cerebro = Cerebro()
cerebro.addstrategy(MomentumStrategy)
cerebro.adddata(data)
cerebro.broker.setcash(100000)
results = cerebro.run()
```

## Risk Metrics

```python
def calculate_var(returns, confidence=0.95):
    """Value at Risk"""
    return np.percentile(returns, (1 - confidence) * 100)

def calculate_sharpe(returns, risk_free=0.02):
    """Sharpe Ratio"""
    excess = returns.mean() * 252 - risk_free
    volatility = returns.std() * np.sqrt(252)
    return excess / volatility

def max_drawdown(equity_curve):
    """Maximum Drawdown"""
    peak = equity_curve.expanding(min_periods=1).max()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()
```
