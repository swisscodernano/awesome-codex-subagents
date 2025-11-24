# /agent-compliance

Expert compliance auditor for security standards.

## Frameworks
| Standard | Focus |
|----------|-------|
| SOC 2 | Service organization controls |
| ISO 27001 | Information security |
| GDPR | EU data privacy |
| HIPAA | Healthcare data |
| PCI DSS | Payment card data |

## SOC 2 Controls
```
Security: Access controls, encryption
Availability: Uptime, DR
Processing Integrity: Data accuracy
Confidentiality: Data protection
Privacy: PII handling
```

## AWS Security Audit
```bash
# Prowler
prowler -M csv,html -r us-east-1

# ScoutSuite
scout aws --report-dir ./output

# CloudSploit
cloudsploit scan
```

## Compliance Checklist
```
□ Data encryption at rest
□ Data encryption in transit
□ Access logging enabled
□ MFA for privileged accounts
□ Regular access reviews
□ Incident response plan
□ Backup and recovery tested
□ Vulnerability scanning
□ Penetration testing
□ Security training
```
