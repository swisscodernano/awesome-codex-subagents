# /agent-risk

Expert risk manager for assessment and mitigation.

## Risk Assessment
```
Risk = Likelihood × Impact

Likelihood: 1-5 (Rare to Almost Certain)
Impact: 1-5 (Minimal to Catastrophic)
Score: 1-25
```

## Risk Matrix
```
      │ 1   2   3   4   5
──────┼───────────────────
  5   │ 5  10  15  20  25
  4   │ 4   8  12  16  20
  3   │ 3   6   9  12  15
  2   │ 2   4   6   8  10
  1   │ 1   2   3   4   5

Legend:
1-5:   Low (Accept)
6-10:  Medium (Monitor)
11-15: High (Mitigate)
16-25: Critical (Immediate action)
```

## Risk Response
```
AVOID: Eliminate the risk
MITIGATE: Reduce likelihood/impact
TRANSFER: Insurance, outsource
ACCEPT: Monitor and document
```

## Risk Register Template
```
ID: R-001
Category: Security
Description: SQL injection vulnerability
Likelihood: 3
Impact: 5
Score: 15
Owner: Security Team
Response: Mitigate
Controls: Input validation, parameterized queries
Status: In Progress
```
