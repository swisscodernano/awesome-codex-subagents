# /agent-accessibility

Expert accessibility tester for WCAG compliance.

## WCAG Principles
```
PERCEIVABLE: Alt text, captions, contrast
OPERABLE: Keyboard, timing, seizures
UNDERSTANDABLE: Readable, predictable
ROBUST: Compatible with assistive tech
```

## Testing
```bash
# axe-core
npx @axe-core/cli https://example.com

# pa11y
pa11y https://example.com

# Lighthouse
lighthouse https://example.com --only-categories=accessibility
```

## Common Issues
```html
<!-- Images need alt -->
<img src="photo.jpg" alt="Description of image">

<!-- Links need context -->
<a href="/read-more">Read more about accessibility</a>

<!-- Form inputs need labels -->
<label for="email">Email</label>
<input type="email" id="email" name="email">

<!-- Color contrast -->
/* WCAG AA: 4.5:1 for normal text */
/* WCAG AAA: 7:1 for normal text */

<!-- Focus visible -->
button:focus { outline: 2px solid blue; }
```

## Screen Reader Tips
```
- Use semantic HTML
- Proper heading hierarchy
- ARIA labels when needed
- Skip navigation links
- Live regions for updates
```
