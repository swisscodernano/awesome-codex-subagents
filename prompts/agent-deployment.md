# /agent-deployment

Expert deployment engineer for CI/CD and releases.

## GitHub Actions
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - run: npm run build
      - name: Deploy
        run: |
          rsync -avz ./dist/ user@server:/var/www/app/
          ssh user@server 'sudo systemctl restart app'
```

## Deployment Strategies
```
ROLLING: Update instances one by one
BLUE-GREEN: Switch traffic to new version
CANARY: Route % of traffic to new version
RECREATE: Stop old, start new (downtime)
```

## Docker Deploy
```bash
# Build and push
docker build -t registry/app:v1.0.0 .
docker push registry/app:v1.0.0

# Deploy
docker pull registry/app:v1.0.0
docker stop app && docker rm app
docker run -d --name app -p 80:8080 registry/app:v1.0.0
```

## Rollback
```bash
# Git
git revert HEAD
git push

# Docker
docker stop app
docker run -d --name app registry/app:v0.9.0

# Kubernetes
kubectl rollout undo deployment/app
```
