# /agent-tooling

Expert tooling engineer for developer productivity.

## CLI Framework (Node.js)
```javascript
#!/usr/bin/env node
import { Command } from 'commander';

const program = new Command()
  .name('mytool')
  .version('1.0.0')
  .description('My awesome tool');

program
  .command('init')
  .option('-n, --name <name>', 'Project name')
  .action((options) => {
    console.log(`Creating ${options.name}`);
  });

program.parse();
```

## VS Code Extension
```json
{
  "contributes": {
    "commands": [{
      "command": "extension.myCommand",
      "title": "My Command"
    }]
  }
}
```

## Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint
        name: Lint
        entry: npm run lint
        language: system
```

## Makefile
```makefile
.PHONY: build test deploy

build:
	npm run build

test:
	npm test

deploy: build test
	./deploy.sh
```
