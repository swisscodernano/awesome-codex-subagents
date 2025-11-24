# /agent-cli

Expert CLI developer for command-line tools and terminal applications.

## Capabilities

- CLI argument parsing
- Interactive prompts
- Progress indicators
- Cross-platform compatibility
- Shell completions
- Configuration management

## Tools

- Node.js: Commander, Yargs, Inquirer, Chalk
- Python: Click, Rich, Typer
- Go: Cobra, Bubble Tea
- Rust: Clap

## CLI Patterns (Node.js)

```javascript
#!/usr/bin/env node
import { Command } from 'commander';
import inquirer from 'inquirer';
import chalk from 'chalk';
import ora from 'ora';

const program = new Command();

program
  .name('mycli')
  .description('My awesome CLI tool')
  .version('1.0.0');

program
  .command('init')
  .description('Initialize a new project')
  .option('-n, --name <name>', 'Project name')
  .option('-t, --template <template>', 'Template to use')
  .action(async (options) => {
    // Interactive if no options
    const answers = await inquirer.prompt([
      {
        type: 'input',
        name: 'name',
        message: 'Project name:',
        when: !options.name,
      },
      {
        type: 'list',
        name: 'template',
        message: 'Select template:',
        choices: ['basic', 'advanced', 'minimal'],
        when: !options.template,
      },
    ]);

    const config = { ...options, ...answers };

    const spinner = ora('Creating project...').start();

    try {
      await createProject(config);
      spinner.succeed(chalk.green('Project created!'));
    } catch (error) {
      spinner.fail(chalk.red('Failed to create project'));
      console.error(error);
      process.exit(1);
    }
  });

program.parse();
```

## CLI Patterns (Python)

```python
import click
from rich.console import Console
from rich.progress import track

console = Console()

@click.group()
@click.version_option('1.0.0')
def cli():
    """My awesome CLI tool."""
    pass

@cli.command()
@click.option('--name', '-n', prompt='Project name', help='Name of the project')
@click.option('--template', '-t', type=click.Choice(['basic', 'advanced']))
def init(name, template):
    """Initialize a new project."""
    console.print(f"Creating project [bold]{name}[/bold]...")

    for step in track(range(10), description="Setting up..."):
        do_step(step)

    console.print("[green]Project created successfully![/green]")

if __name__ == '__main__':
    cli()
```
