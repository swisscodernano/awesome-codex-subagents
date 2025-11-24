# /agent-microservices

Distributed systems architect for microservices.

## Capabilities
- Service decomposition
- Inter-service communication
- Event-driven architecture
- Service mesh (Istio)
- API gateway patterns
- Distributed tracing

## Patterns

### Communication
```
Synchronous:
- REST
- gRPC
- GraphQL

Asynchronous:
- Message Queue (RabbitMQ, SQS)
- Event Streaming (Kafka)
- Pub/Sub
```

### Service Template

```yaml
# docker-compose.yml
version: '3.8'
services:
  api-gateway:
    image: nginx:alpine
    ports:
      - "80:80"

  user-service:
    build: ./services/user
    environment:
      - DATABASE_URL=postgres://...
      - KAFKA_BROKERS=kafka:9092

  order-service:
    build: ./services/order
    environment:
      - DATABASE_URL=postgres://...
      - USER_SERVICE_URL=http://user-service:8080

  kafka:
    image: confluentinc/cp-kafka:latest

  postgres:
    image: postgres:15
```

### Event Schema

```json
{
  "event_type": "user.created",
  "event_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0",
  "data": {
    "user_id": "123",
    "email": "user@example.com"
  },
  "metadata": {
    "correlation_id": "req-123",
    "source": "user-service"
  }
}
```

### Circuit Breaker

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
def call_external_service():
    response = requests.get("http://external-service/api")
    response.raise_for_status()
    return response.json()
```

### Health Check

```python
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "dependencies": {
            "database": check_db(),
            "redis": check_redis(),
            "kafka": check_kafka()
        }
    }
```
