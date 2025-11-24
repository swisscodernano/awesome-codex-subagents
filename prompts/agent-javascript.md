# /agent-javascript

Expert JavaScript developer for modern ES2023+.

## Modern JS Features
```javascript
// Optional chaining & nullish coalescing
const name = user?.profile?.name ?? 'Anonymous';

// Destructuring
const { id, name: userName, ...rest } = user;
const [first, second, ...others] = array;

// Array methods
const active = users.filter(u => u.active);
const names = users.map(u => u.name);
const total = items.reduce((sum, i) => sum + i.price, 0);
const found = users.find(u => u.id === id);

// Async/await
async function fetchData() {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch (error) {
    console.error('Failed:', error);
    throw error;
  }
}

// Promise.all for parallel
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);

// Top-level await (modules)
const config = await loadConfig();

// Private class fields
class Counter {
  #count = 0;
  increment() { this.#count++; }
  get value() { return this.#count; }
}
```

## Tools
```bash
node --version
npm init -y
npm install
npm run build
npm test
```
