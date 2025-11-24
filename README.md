# Awesome AI CLI Agents

A comprehensive collection for **OpenAI Codex CLI** and **Gemini CLI**:
- **97 specialized agent prompts** (Codex)
- **10 enterprise MCP servers** (Codex)
- **SRE/DevOps autopilot config** (Gemini CLI)

## Quick Install

```bash
# Clone the repo
git clone git@github.com:swisscodernano/awesome-codex-subagents.git

# Run install script
cd awesome-codex-subagents
./install.sh
```

## Manual Install

```bash
# Copy prompts to ~/.codex/prompts/
mkdir -p ~/.codex/prompts
cp -r prompts/* ~/.codex/prompts/

# Copy global AGENTS.md
cp AGENTS.md ~/.codex/

# Update config.toml (merge with existing)
cat config/config.toml >> ~/.codex/config.toml
```

## Usage

### Slash Commands (Operations)

```bash
/health                    # Full system health check
/logs api 100              # View last 100 logs
/sre-debug api.service     # Debug a service
/incident "502 errors"     # Incident response
/restart nginx             # Safe restart
/deploy /var/www/app       # Deploy with checklist
```

### Agent Modes (Specialists)

```bash
/agent-sre                 # SRE/DevOps mode
/agent-devops              # DevOps mode
/agent-python              # Python expert
/agent-frontend            # Frontend specialist
/agent-debugger            # Debug mode
/agent-explorer            # Codebase exploration
/agent-security            # Security engineer
/agent-kubernetes          # K8s specialist
/agent-terraform           # IaC expert
# ... and 88 more!
```

## Agent Categories

### Development (30+)
- `agent-python`, `agent-javascript`, `agent-typescript`
- `agent-golang`, `agent-rust`, `agent-java`, `agent-cpp`
- `agent-react`, `agent-vue`, `agent-nextjs`, `agent-flutter`
- `agent-django`, `agent-rails`, `agent-laravel`, `agent-spring`

### DevOps & Infrastructure (15+)
- `agent-devops`, `agent-sre`, `agent-kubernetes`
- `agent-terraform`, `agent-docker`, `agent-cloud`
- `agent-deployment`, `agent-incident-responder`

### Security (10+)
- `agent-security`, `agent-pentest`, `agent-bug-bounty`
- `agent-red-team`, `agent-osint`, `agent-compliance`

### Data & AI (10+)
- `agent-data-scientist`, `agent-data-engineer`
- `agent-ai`, `agent-llm`, `agent-mlops`, `agent-nlp`

### Architecture & Design (10+)
- `agent-architect`, `agent-microservices`
- `agent-api-designer`, `agent-graphql`
- `agent-ui-designer`, `agent-ux-researcher`

### Business & Operations (10+)
- `agent-product`, `agent-business`, `agent-scrum-master`
- `agent-legal`, `agent-risk`, `agent-compliance`

## Project Templates

The `projects/` folder contains AGENTS.md templates for different tech stacks:

- `projects/aiagens/` - Flask + Gunicorn + PostgreSQL
- `projects/abtrading/` - Python trading bot
- `projects/exatoshi/` - Astro + Tailwind
- `projects/ladymary/` - WordPress
- `projects/bestwasabi/` - Static + Tailwind

Copy and customize for your projects.

## MCP Servers (Enterprise)

**10 custom MCP servers** for enterprise-grade capabilities:

| Server | Tools | Purpose |
|--------|-------|---------|
| **PostgreSQL** | `pg_query`, `pg_schema`, `pg_tables`, `pg_stats` | Database access with safety controls |
| **GitHub** | `gh_pr_list`, `gh_pr_view`, `gh_issue_list`, `gh_api` | GitHub operations via gh CLI |
| **HTTP** | `http_get`, `http_post`, `http_head`, `api_health_check` | API calls and health checks |
| **Redis** | `redis_get`, `redis_keys`, `redis_info`, `redis_hgetall` | Cache and pub/sub operations |
| **Docker** | `docker_ps`, `docker_logs`, `docker_stats`, `docker_exec` | Container management |
| **Slack** | `slack_alert`, `slack_incident`, `slack_send_message` | Notifications and alerts |
| **Prometheus** | `prom_query`, `prom_alerts`, `prom_targets`, `prom_rules` | Metrics and alerting |
| **Elasticsearch** | `es_search`, `es_logs`, `es_indices`, `es_aggregation` | Log search and analytics |
| **AWS** | `aws_ec2_list`, `aws_s3_list`, `aws_lambda_list`, `aws_cloudwatch` | Cloud operations via boto3 |
| **Kubernetes** | `k8s_get_pods`, `k8s_logs`, `k8s_describe`, `k8s_scale` | K8s operations via kubectl |

### Quick MCP Setup

```bash
# Copy MCP servers
mkdir -p ~/.codex/mcp-servers
cp mcp-servers/*.py ~/.codex/mcp-servers/

# Install dependencies
pip install mcp psycopg2-binary redis httpx boto3
```

### MCP Config Example

```toml
[mcp_servers.postgres]
command = "python3"
args = ["/home/user/.codex/mcp-servers/postgres_server.py"]

[mcp_servers.postgres.env]
DATABASE_URL = "postgresql://localhost/mydb"
MCP_POSTGRES_READONLY = "true"

[mcp_servers.slack]
command = "python3"
args = ["/home/user/.codex/mcp-servers/slack_server.py"]

[mcp_servers.slack.env]
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/xxx"
```

### Safety Features

All MCP servers include:
- **READONLY modes** - Prevent accidental writes
- **Row/key limits** - Prevent data overload
- **Timeouts** - Prevent hanging operations
- **Error handling** - Graceful failure messages

---

## Gemini CLI Configuration (SRE/DevOps Autopilot)

**Google's Gemini CLI** with ReAct architecture, shell access, and built-in MCP support.

### Quick Setup

```bash
# Copy Gemini configs
mkdir -p ~/.gemini/{commands/sre,policies/user}
cp gemini/settings.json ~/.gemini/
cp gemini/GEMINI.md ~/.gemini/
cp -r gemini/commands/* ~/.gemini/commands/
cp -r gemini/policies/* ~/.gemini/policies/
```

### Features

| Component | Purpose |
|-----------|---------|
| **settings.json** | Auto-accept safe commands, tool whitelist/blacklist |
| **GEMINI.md** | Global SRE persona, incident workflow, site inventory |
| **commands/sre/*.toml** | 6 slash commands for incident response |
| **policies/user/sre-safe.toml** | Policy engine (allow/deny/ask rules) |
| **projects/*.md** | Project-specific contexts (abtrading, aiagens) |

### Slash Commands

```bash
gemini  # Enter in project directory

/sre:systemd-debug api.service    # Analyze systemd service
/sre:pm2-incident my-app           # Debug PM2 process
/sre:nginx-5xx aiagens.ch          # Analyze nginx 5xx errors
/sre:health-check                  # Full system health check
/sre:logs-tail api.service         # Tail and analyze logs
/sre:disk-usage                    # Find disk space hogs
```

### Policy Engine

**Automatic execution (no confirmation):**
- `journalctl`, `systemctl status`, `pm2 status/logs`
- `cat`, `tail`, `grep`, `df`, `free`, `ps`
- `nginx -t`, `curl`, `git status`

**Ask confirmation:**
- `systemctl restart/stop`, `pm2 restart/stop`
- `nginx -s reload`, `rm`, `mv`, `write_file`

**Always deny:**
- `rm -rf /`, `dd`, `shutdown`, `reboot`

### Workflow Example

```bash
cd /var/www/abtrading
gemini

# You: "I'm getting 502 errors on the bot"

# Gemini (autonomously):
# - Runs systemctl status abtrading.service
# - Analyzes logs with journalctl
# - Identifies Python traceback
# - Proposes fix: "Missing dependency 'ccxt'"
# - Asks: "Install ccxt and restart?"
```

### Project Contexts

The repo includes 2 project GEMINI.md templates:
- **abtrading-GEMINI.md** - Python trading bot with critical safety rules
- **aiagens-GEMINI.md** - Flask/Gunicorn API with multi-tenant database

Copy and customize for your projects.

---

## Claude Code Configuration (Enterprise)

**Anthropic's Claude Code** with 120+ built-in subagents, native tools, and MCP support.

### Quick Setup

```bash
# Copy Claude configs
cp claude/CLAUDE.md ~/.claude/
cp claude/mcp_settings.json ~/.claude/
cp claude/abtrading-CLAUDE.md /var/www/abtrading/CLAUDE.md
```

### Features

| Component | Purpose |
|-----------|---------|
| **CLAUDE.md** | Global SRE persona, workflow rules, server inventory |
| **mcp_settings.json** | 5 MCP servers (postgres, redis, docker, github, rag) |
| **Project CLAUDE.md** | Auto-loaded context (abtrading template included) |

### Built-in Subagents

Claude Code has 120+ specialized subagents:
- **Explore** - Codebase exploration
- **Plan** - Multi-step task planning
- **Security** - Code security review
- **Performance** - Optimization analysis
- **Debugger** - Complex debugging
- **and 115+ more...**

### MCP Servers Added

```json
{
  "aiagens-rag": "Project knowledge base",
  "postgres": "Database queries (readonly)",
  "redis": "Cache operations",
  "docker": "Container management",
  "github": "PR/issue operations"
}
```

### Usage

```bash
cd /var/www/abtrading
cld  # Alias for 'claude'

# Claude Code automatically:
# - Reads CLAUDE.md (global + project)
# - Loads 5 MCP servers
# - Uses 120+ built-in subagents
# - Plans complex tasks with TodoWrite

# You: "The trading bot crashed, investigate"
# Claude:
# - Uses Bash tool for systemctl/journalctl
# - Uses Read tool for logs
# - Uses Grep tool for errors
# - Creates Todo list for incident steps
# - Proposes fix with risk assessment
```

### Workflow Example

```bash
cd /var/www/aiagens.ch
cld

# Incident: "502 errors on the API"

# Claude Code will:
# 1. Create TodoList (check status, analyze logs, identify cause, propose fix)
# 2. Run: systemctl status api.service
# 3. Run: journalctl -u api.service -n 200
# 4. Analyze Gunicorn errors
# 5. Propose: "Worker timeout - increase timeout in gunicorn config"
# 6. Ask: "Shall I edit the config and restart?"
```

### Bash Aliases

```bash
cld          # Launch Claude Code
cldsre       # Claude in abtrading project
cldapi       # Claude for API work
cldincident  # Quick start mode
```

---

## Configuration

### config.toml

```toml
model = "gpt-5.1-codex"
model_reasoning_effort = "high"
project_doc_fallback_filenames = ["AGENTS.md", "codex.yaml"]
project_doc_max_bytes = 65536
approval_policy = "on-failure"
```

### Bash Aliases

Add to `~/.bashrc`:

```bash
alias cdx='codex --model gpt-5.1-codex --full-auto'
alias cdxmax='codex --model gpt-5.1-codex-max --full-auto'
```

## Contributing

1. Fork the repo
2. Add your agent to `prompts/agent-{name}.md`
3. Update this README
4. Submit PR

## License

MIT
