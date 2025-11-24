# /agent-incident-responder

Expert incident responder for production issues.

## Incident Lifecycle
```
1. DETECT - Alert triggered
2. TRIAGE - Assess severity
3. MITIGATE - Stop the bleeding
4. INVESTIGATE - Find root cause
5. RESOLVE - Implement fix
6. POSTMORTEM - Learn and prevent
```

## Severity Levels
| Level | Impact | Response Time |
|-------|--------|---------------|
| SEV1 | System down | Immediate |
| SEV2 | Major degradation | 15 min |
| SEV3 | Minor impact | 1 hour |
| SEV4 | Low priority | Next day |

## Quick Commands
```bash
# Status check
systemctl status --all | grep -E 'failed|error'
journalctl -p err --since "10 min ago"

# Resource check
top -bn1 | head -20
free -m
df -h
netstat -an | grep -c ESTABLISHED

# Recent changes
git log --oneline -10
docker ps -a --format "table {{.Names}}\t{{.Status}}"
```

## Postmortem Template
```
## Incident: [Title]
**Date**: YYYY-MM-DD
**Duration**: X hours
**Severity**: SEV-X
**Impact**: [Who/what affected]

### Timeline
- HH:MM - Event
- HH:MM - Action taken

### Root Cause
[Technical explanation]

### Resolution
[What fixed it]

### Action Items
- [ ] Prevent: [Action]
- [ ] Detect: [Action]
- [ ] Mitigate: [Action]
```
