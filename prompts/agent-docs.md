# /agent-docs

Expert documentation engineer for technical writing.

## Capabilities
- API documentation
- User guides
- Architecture docs
- README files
- Documentation-as-code

## Documentation Types

| Type | Audience | Purpose |
|------|----------|---------|
| README | Developers | Quick start |
| API Docs | Developers | Reference |
| Tutorials | Beginners | Learning |
| How-to | Users | Task completion |
| Architecture | Team | System understanding |

## README Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2

## Quick Start

\`\`\`bash
npm install project-name
npm start
\`\`\`

## Usage

\`\`\`javascript
import { thing } from 'project-name';
thing.doSomething();
\`\`\`

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| port | number | 3000 | Server port |

## API Reference

See [API.md](./docs/API.md)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT
```

## API Documentation

```markdown
## POST /api/users

Create a new user.

### Request

\`\`\`json
{
  "name": "John Doe",
  "email": "john@example.com"
}
\`\`\`

### Response

**201 Created**
\`\`\`json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
\`\`\`

### Errors

| Code | Description |
|------|-------------|
| 400 | Invalid input |
| 409 | Email already exists |
```
