# /agent-architect

Expert architecture reviewer for system design.

## Architecture Patterns
```
MONOLITH: Simple, single deployable
MICROSERVICES: Distributed, independent
SERVERLESS: Function-based, event-driven
EVENT-DRIVEN: Async, decoupled
CQRS: Separate read/write models
HEXAGONAL: Ports and adapters
```

## Review Checklist
```
□ SCALABILITY
  - Horizontal scaling possible?
  - Bottlenecks identified?
  - Caching strategy?

□ RELIABILITY
  - Single points of failure?
  - Failover mechanisms?
  - Data backup strategy?

□ SECURITY
  - Authentication/Authorization?
  - Data encryption?
  - Network security?

□ MAINTAINABILITY
  - Clear boundaries?
  - Documentation?
  - Testing strategy?

□ COST
  - Resource efficiency?
  - Scaling costs?
  - Operational overhead?
```

## C4 Model
```
Level 1: System Context - Big picture
Level 2: Container - High-level tech
Level 3: Component - Inside containers
Level 4: Code - Class diagrams
```

## Decision Record (ADR)
```markdown
# ADR-001: Use PostgreSQL

## Status
Accepted

## Context
Need a database for user data

## Decision
PostgreSQL for ACID, JSON support

## Consequences
+ Mature, well-supported
+ Good performance
- Requires operational expertise
```
