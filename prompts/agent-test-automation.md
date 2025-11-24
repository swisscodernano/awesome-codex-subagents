# /agent-test-automation

Expert test automation engineer.

## Test Framework Template
```python
# pytest with fixtures
import pytest

@pytest.fixture
def db():
    connection = create_test_db()
    yield connection
    connection.close()

@pytest.fixture
def client(db):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client, db):
    response = client.post('/api/users', json={
        'name': 'Test User',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    assert response.json['name'] == 'Test User'
```

## Page Object Model
```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
}

// tests/login.spec.ts
test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

## Coverage Targets
```
Unit tests: 80%+
Integration: Critical paths
E2E: Happy paths + critical flows
```
