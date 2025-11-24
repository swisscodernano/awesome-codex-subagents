# /agent-performance

Expert performance engineer for optimization.

## Load Testing
```python
# Locust
from locust import HttpUser, task, between

class WebUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.get("/")

    @task(3)
    def api(self):
        self.client.get("/api/users")
```

## Profiling
```bash
# Python
python -m cProfile -s cumtime app.py
py-spy record -o profile.svg -- python app.py

# Node.js
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# Go
go test -bench=. -cpuprofile=cpu.out
go tool pprof cpu.out
```

## Browser Performance
```javascript
// Performance API
performance.mark('start');
// ... operation
performance.mark('end');
performance.measure('operation', 'start', 'end');

// Core Web Vitals
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log(entry.name, entry.value);
  }
});
observer.observe({ entryTypes: ['largest-contentful-paint'] });
```

## Metrics
```
Response Time: p50, p95, p99
Throughput: Requests/second
Error Rate: 4xx, 5xx percentage
Saturation: CPU, Memory, Disk I/O
```
