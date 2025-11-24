# /agent-chaos

Expert chaos engineer for resilience testing.

## Principles
```
1. Define steady state
2. Hypothesize about impact
3. Run experiments in production
4. Automate to run continuously
5. Minimize blast radius
```

## Chaos Toolkit
```yaml
# experiment.json
{
  "title": "API resilience test",
  "steady-state-hypothesis": {
    "title": "API responds normally",
    "probes": [{
      "type": "probe",
      "name": "api-health",
      "provider": {
        "type": "http",
        "url": "http://api/health"
      }
    }]
  },
  "method": [{
    "type": "action",
    "name": "kill-api-pod",
    "provider": {
      "type": "python",
      "module": "chaosk8s.pod.actions",
      "func": "terminate_pods",
      "arguments": {
        "label_selector": "app=api"
      }
    }
  }]
}
```

## Litmus Chaos
```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: api-chaos
spec:
  appinfo:
    appns: default
    applabel: app=api
  experiments:
    - name: pod-delete
      spec:
        components:
          env:
            - name: TOTAL_CHAOS_DURATION
              value: '30'
```

## Game Day Checklist
```
□ Define scope and objectives
□ Notify stakeholders
□ Prepare rollback plan
□ Set up monitoring dashboards
□ Run experiment
□ Document observations
□ Conduct debrief
□ Create action items
```
