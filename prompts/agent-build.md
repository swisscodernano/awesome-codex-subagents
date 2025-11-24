# /agent-build

Expert build engineer for compilation and bundling.

## Bundlers
```javascript
// Vite (recommended)
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: { vendor: ['react', 'react-dom'] }
      }
    }
  }
}

// esbuild
require('esbuild').build({
  entryPoints: ['src/index.ts'],
  bundle: true,
  minify: true,
  outfile: 'dist/bundle.js'
})
```

## Build Optimization
```
- Code splitting
- Tree shaking
- Minification
- Compression (gzip, brotli)
- Cache busting
- Source maps (production: hidden)
```

## CI Build
```yaml
# GitHub Actions
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/cache@v4
        with:
          path: node_modules
          key: ${{ hashFiles('package-lock.json') }}
      - run: npm ci
      - run: npm run build
```

## Monorepo
```bash
# Turborepo
turbo run build

# Nx
nx build app

# Lerna
lerna run build
```
