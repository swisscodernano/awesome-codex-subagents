# BestWasabiCoordinators.com - Project Instructions

> Static website for Wasabi Wallet coordinators with Tailwind CSS

---

## Stack Tecnico

| Component | Technology |
|-----------|------------|
| Type | Static HTML |
| Styling | Tailwind CSS 3.x |
| Build | Tailwind CLI |
| Server | Nginx (static files) |

---

## File Structure

```
/var/www/bestwasabicoordinators.com/
├── src/
│   └── input.css       # Tailwind input file
├── assets/
│   └── css/
│       └── styles.css  # Compiled Tailwind output
├── api/                # Static API responses (if any)
├── index.html          # Main page
├── package.json        # npm scripts
└── tailwind.config.js  # Tailwind configuration
```

---

## Comandi Rapidi

```bash
cd /var/www/bestwasabicoordinators.com

# Install dependencies
npm install

# Build CSS (production)
npm run build-css

# Watch mode (development)
npm run watch-css
```

---

## NPM Scripts

```json
{
  "build-css": "tailwindcss -i ./src/input.css -o ./assets/css/styles.css --minify",
  "watch-css": "tailwindcss -i ./src/input.css -o ./assets/css/styles.css --watch"
}
```

---

## Development Workflow

1. Edit HTML files directly
2. Run `npm run watch-css` for live Tailwind compilation
3. Refresh browser to see changes
4. For production: `npm run build-css` (minified)

---

## Tailwind Configuration

Check `tailwind.config.js` for:
- Custom colors
- Font families
- Content paths (which files to scan for classes)

```javascript
module.exports = {
  content: [
    './*.html',
    './src/**/*.{html,js}'
  ],
  theme: {
    extend: {
      // Custom theme extensions
    }
  }
}
```

---

## Adding New Pages

1. Create new `.html` file in root
2. Use same structure as `index.html`
3. Link to `assets/css/styles.css`
4. Rebuild CSS if using new Tailwind classes

---

## Deployment

Static files served directly by Nginx:

```bash
# No build step needed for HTML
# Only rebuild CSS if Tailwind classes changed:
npm run build-css

# Clear nginx cache if needed
sudo find /var/cache/nginx -type f -delete
sudo systemctl reload nginx
```

---

## Nginx Config

Location: `/etc/nginx/sites-enabled/bestwasabicoordinators.com`

Typical static site config:
```nginx
server {
    listen 80;
    server_name bestwasabicoordinators.com;
    root /var/www/bestwasabicoordinators.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## Troubleshooting

### CSS Not Updating
```bash
# Rebuild CSS
npm run build-css

# Check output file
ls -la assets/css/styles.css

# Clear browser cache (Ctrl+Shift+R)
```

### Missing Tailwind Classes
- Ensure class is in a file scanned by `content` in config
- Run `npm run build-css` after adding new classes
- Check for typos in class names
