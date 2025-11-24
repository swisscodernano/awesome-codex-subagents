# /agent-dx

Developer experience optimizer for build and tooling.

## Build Optimization
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash', 'date-fns']
        }
      }
    }
  },
  optimizeDeps: {
    include: ['react', 'react-dom']
  }
}
```

## Monorepo (Turborepo)
```json
// turbo.json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    },
    "test": {
      "dependsOn": ["build"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

## Performance Checks
```bash
# Bundle analysis
npx vite-bundle-visualizer
npx webpack-bundle-analyzer

# Build time
time npm run build

# Type check speed
time npx tsc --noEmit

# Cache stats
npx turbo run build --summarize
```

## Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint
        name: Lint
        entry: npm run lint
        language: system
      - id: test
        name: Test
        entry: npm test
        language: system
```
