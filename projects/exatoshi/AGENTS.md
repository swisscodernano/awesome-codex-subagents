# Exatoshi.ch - Project Instructions

> Modern crypto/blockchain landing page built with Astro + Tailwind

---

## Stack Tecnico

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Astro | 4.x |
| Styling | Tailwind CSS | 3.x |
| Animations | GSAP, Lenis | Latest |
| Icons | Iconify | cib, heroicons |
| Build | Vite (via Astro) | - |

---

## File Structure

```
/var/www/exatoshi.ch/
├── src/
│   ├── components/     # Astro components
│   ├── layouts/        # Page layouts
│   ├── pages/          # Routes (file-based)
│   └── styles/         # Global CSS
├── public/             # Static assets
├── astro.config.mjs    # Astro configuration
├── tailwind.config.mjs # Tailwind configuration
├── tsconfig.json       # TypeScript config
└── package.json        # Dependencies
```

---

## Comandi Rapidi

```bash
cd /var/www/exatoshi.ch

# Install dependencies
npm install

# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

---

## Deployment

```bash
# Build static site
npm run build

# Output in dist/ folder
ls -la dist/

# Nginx serves from dist/ or root
# Check nginx config for document_root
```

---

## Astro Patterns

```astro
---
// Component script (runs at build time)
import Layout from '../layouts/Layout.astro';
const title = "Page Title";
---

<Layout title={title}>
  <main>
    <h1>{title}</h1>
  </main>
</Layout>

<style>
  /* Scoped styles */
  h1 { color: var(--primary); }
</style>
```

---

## Tailwind Classes

Common utilities:
```html
<!-- Responsive -->
<div class="px-4 md:px-8 lg:px-16">

<!-- Dark mode -->
<div class="bg-white dark:bg-gray-900">

<!-- Animations -->
<div class="transition-all duration-300 hover:scale-105">
```

---

## GSAP Animations

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

gsap.from('.hero', {
  opacity: 0,
  y: 50,
  duration: 1,
  scrollTrigger: {
    trigger: '.hero',
    start: 'top 80%'
  }
});
```

---

## Smooth Scroll (Lenis)

```javascript
import Lenis from '@studio-freight/lenis';

const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t))
});

function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}
requestAnimationFrame(raf);
```

---

## Debug

```bash
# Check build errors
npm run build 2>&1 | head -50

# Check TypeScript errors
npx tsc --noEmit

# Verify Tailwind
npx tailwindcss --help
```

---

## Performance

- Use `loading="lazy"` on images
- Minimize JavaScript bundles
- Use Astro's partial hydration (`client:load`, `client:visible`)
- Optimize images with `@astrojs/image`
