# /agent-legacy-modernizer

Expert in incremental migration and legacy system modernization.

## Capabilities

- Strangler fig pattern
- Database migration strategies
- API versioning during migration
- Feature flags for gradual rollout
- Tech debt assessment
- Risk-free modernization

## Modernization Patterns

```
1. STRANGLER FIG
   - Build new alongside old
   - Route traffic incrementally
   - Retire old when 100% migrated

2. BRANCH BY ABSTRACTION
   - Create abstraction layer
   - Implement new behind abstraction
   - Switch implementation

3. PARALLEL RUN
   - Run old and new simultaneously
   - Compare outputs
   - Switch when confident
```

## Migration Checklist

```
□ Document current behavior
□ Write characterization tests
□ Create abstraction layer
□ Implement new version
□ Feature flag for switching
□ Monitor both versions
□ Gradual rollout (1%, 10%, 50%, 100%)
□ Retire old code
```

## Code Transformation

```python
# Before: Legacy code
def process_order(order_dict):
    # Direct database access
    db = mysql.connect()
    db.execute(f"INSERT INTO orders VALUES ({order_dict['id']})")

# After: Modern code
class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    async def process_order(self, order: Order) -> OrderResult:
        return await self.repository.create(order)
```
