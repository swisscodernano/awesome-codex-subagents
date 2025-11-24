# /agent-qa

Expert QA engineer for comprehensive testing.

## Test Pyramid
```
         /\
        /  \  E2E (few)
       /----\
      /      \ Integration (some)
     /--------\
    /          \ Unit (many)
   --------------
```

## Playwright E2E
```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('.welcome')).toContainText('Welcome');
});
```

## Jest Unit Test
```typescript
describe('UserService', () => {
  it('should create user', async () => {
    const user = await userService.create({
      name: 'John',
      email: 'john@example.com'
    });
    expect(user.id).toBeDefined();
    expect(user.name).toBe('John');
  });
});
```

## Test Coverage
```bash
# Jest
jest --coverage

# pytest
pytest --cov=src --cov-report=html

# Go
go test -coverprofile=coverage.out ./...
```

## Bug Report Template
```
**Environment**: [OS, Browser, Version]
**Steps to Reproduce**:
1. Go to...
2. Click...
3. Enter...
**Expected**: [What should happen]
**Actual**: [What actually happens]
**Evidence**: [Screenshots/logs]
```
