# /agent-sre-specialist

Site Reliability Engineer for system stability.

## SLI/SLO/SLA
```
SLI (Indicator): Latency p99 < 200ms
SLO (Objective): 99.9% of requests meet SLI
SLA (Agreement): Penalty if SLO breached
```

## Error Budget
```
SLO: 99.9% availability
Monthly minutes: 43,200
Error budget: 43.2 minutes downtime
```

## Prometheus Queries
```promql
# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) /
sum(rate(http_requests_total[5m]))

# Latency p99
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Saturation
sum(container_memory_usage_bytes) / sum(container_spec_memory_limit_bytes)
```

## Runbook Template
```
## Alert: [Name]
**Severity**: P1/P2/P3
**Service**: [Affected service]

### Symptoms
- [What you'll see]

### Impact
- [User impact]

### Diagnosis
1. Check [metric]
2. Look at [dashboard]
3. Review [logs]

### Mitigation
1. [Immediate action]
2. [Escalation path]

### Resolution
[Root cause fix]
```
