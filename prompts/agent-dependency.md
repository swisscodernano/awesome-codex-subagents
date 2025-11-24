# /agent-dependency

Expert dependency manager for package security.

## Security Audit
```bash
# npm
npm audit
npm audit fix

# pip
pip-audit
safety check

# Snyk
snyk test
```

## Version Management
```bash
# npm
npm outdated
npm update
npx npm-check-updates -u

# pip
pip list --outdated
pip install --upgrade package

# Renovate config
{
  "extends": ["config:base"],
  "schedule": ["every weekend"]
}
```

## Lock Files
```
npm: package-lock.json
yarn: yarn.lock
pip: requirements.txt + pip-tools
poetry: poetry.lock
go: go.sum
rust: Cargo.lock
```

## Dependabot
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
    groups:
      dev-dependencies:
        patterns: ["*"]
        update-types: ["minor", "patch"]
```
