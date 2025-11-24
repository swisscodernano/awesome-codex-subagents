# Complete Setup Guide - AI SRE/DevOps Autopilot

**Repository:** `github.com/swisscodernano/awesome-codex-subagents`

This guide provides step-by-step instructions to configure **3 AI CLI tools** as SRE/DevOps autopilots:
1. **Codex CLI** (OpenAI)
2. **Gemini CLI** (Google)
3. **Claude Code** (Anthropic)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Codex CLI Setup](#codex-cli-setup)
3. [Gemini CLI Setup](#gemini-cli-setup)
4. [Claude Code Setup](#claude-code-setup)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Project-Specific Configuration](#project-specific-configuration)

---

## Quick Start

### Prerequisites

```bash
# Install AI CLI tools (if not already installed)
# Codex CLI: https://openai.com/codex-cli
# Gemini CLI: npm install -g @google/generative-ai-cli
# Claude Code: https://claude.ai/download

# Install Python dependencies for MCP servers
pip install mcp psycopg2-binary redis httpx boto3
```

### Clone Repository

```bash
git clone git@github.com:swisscodernano/awesome-codex-subagents.git
cd awesome-codex-subagents
```

---

## Codex CLI Setup

### 1. Install Configuration

```bash
# Create directories
mkdir -p ~/.codex/{prompts,mcp-servers}

# Copy agent prompts (97 files)
cp -r prompts/* ~/.codex/prompts/

# Copy global persona
cp AGENTS.md ~/.codex/

# Copy MCP servers
cp mcp-servers/*.py ~/.codex/mcp-servers/

# Merge config (careful not to overwrite existing!)
cat config.toml >> ~/.codex/config.toml
```

### 2. Configure MCP Servers

Edit `~/.codex/config.toml` and adjust environment variables:

```toml
[mcp_servers.postgres.env]
DATABASE_URL = "postgresql://localhost/your_db"  # Change this

[mcp_servers.slack.env]
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/xxx"  # Add yours

[mcp_servers.aws.env]
AWS_REGION = "eu-central-1"  # Change if needed
```

### 3. Add Bash Aliases

```bash
cat >> ~/.bashrc << 'EOF'

# Codex CLI Aliases
alias cdx='codex --model gpt-5.1-codex --full-auto'
alias cdxmax='codex --model gpt-5.1-codex-max --full-auto'
alias cdxdebug='codex --model gpt-5.1-codex --full-auto -q'
EOF

source ~/.bashrc
```

### 4. Test

```bash
cd ~
cdx
# Try: "List the agent prompts available"
```

---

## Gemini CLI Setup

### 1. Install Configuration

```bash
# Create directories
mkdir -p ~/.gemini/{commands/sre,policies/user}

# Copy settings
cp gemini/settings.json ~/.gemini/

# Copy global persona
cp gemini/GEMINI.md ~/.gemini/

# Copy slash commands
cp -r gemini/commands/* ~/.gemini/commands/

# Copy policies
cp -r gemini/policies/* ~/.gemini/policies/
```

### 2. Configure API Key

```bash
# If not already configured
gemini config set apiKey YOUR_GEMINI_API_KEY
```

### 3. Add Bash Aliases

```bash
cat >> ~/.bashrc << 'EOF'

# Gemini CLI Aliases
alias gem='gemini'
alias gemsre='cd /var/www/abtrading && gemini'
alias gemapi='gemini'
alias gemincident='gemini /sre:health-check'
EOF

source ~/.bashrc
```

### 4. Test

```bash
cd ~
gem
# Try: "/sre:health-check"
```

---

## Claude Code Setup

### 1. Install Configuration

```bash
# Create directories
mkdir -p ~/.claude/commands

# Copy global persona
cp claude/CLAUDE.md ~/.claude/

# Copy MCP settings
cp claude/mcp_settings.json ~/.claude/

# Copy commands info
cp claude/commands-README.md ~/.claude/commands/README.md
```

### 2. Configure MCP Servers

Edit `~/.claude/mcp_settings.json` and adjust paths/credentials:

```json
{
  "mcpServers": {
    "postgres": {
      "env": {
        "DATABASE_URL": "postgresql://localhost/your_db"
      }
    }
  }
}
```

### 3. Add Bash Aliases

```bash
cat >> ~/.bashrc << 'EOF'

# Claude Code Aliases
alias cld='claude'
alias cldsre='cd /var/www/abtrading && claude'
alias cldapi='claude'
alias cldincident='claude --quick-start'
EOF

source ~/.bashrc
```

### 4. Test

```bash
cd ~
cld
# Try: "Explain what CLAUDE.md file does"
```

---

## Project-Specific Configuration

### For Your Trading Bot (abtrading)

```bash
# Copy all 3 project contexts
cp gemini/projects/abtrading-GEMINI.md /var/www/abtrading/GEMINI.md
cp claude/abtrading-CLAUDE.md /var/www/abtrading/CLAUDE.md
cp projects/abtrading/AGENTS.md /var/www/abtrading/AGENTS.md

# Now all 3 AI tools will load project-specific context automatically!
```

### For Your API (aiagens.ch)

```bash
cp gemini/projects/aiagens-GEMINI.md /var/www/aiagens.ch/GEMINI.md
# CLAUDE.md already exists in aiagens.ch
cp projects/aiagens/AGENTS.md /var/www/aiagens.ch/AGENTS.md
```

### For Other Projects

Use the templates in `projects/` as starting points:
- `projects/abtrading/AGENTS.md` - Python trading bot
- `projects/aiagens/AGENTS.md` - Flask API
- `projects/ladymary/AGENTS.md` - WordPress
- `projects/bestwasabi/AGENTS.md` - Static site

---

## Verification

### Test All 3 Tools

```bash
# Test Codex
cd /var/www/abtrading
cdx
# Message: "Show me project structure"
# Expected: Uses Glob/Read tools to explore

# Test Gemini
cd /var/www/abtrading
gem
# Message: "/sre:systemd-debug abtrading.service"
# Expected: Runs systemctl + journalctl autonomously

# Test Claude Code
cd /var/www/abtrading
cld
# Message: "Check if there are any Python errors in logs"
# Expected: Creates TodoList, uses Bash/Read/Grep tools
```

### Verify MCP Servers

**Codex:**
```bash
# Check config
grep -A 5 "mcp_servers" ~/.codex/config.toml
# Should show 11 servers (aiagens_rag + 10 enterprise)
```

**Claude Code:**
```bash
# Check config
cat ~/.claude/mcp_settings.json
# Should show 5 servers
```

---

## Troubleshooting

### Codex: "MCP server failed to start"

```bash
# Test MCP server manually
python3 ~/.codex/mcp-servers/postgres_server.py
# Should not error

# Check dependencies
pip list | grep -E "mcp|psycopg2|redis|httpx"
```

### Gemini: "Invalid sandbox command"

```bash
# Check settings.json doesn't have invalid options
grep -E "theme|sandbox" ~/.gemini/settings.json
# Should return nothing (those lines should be removed)
```

### Claude Code: "MCP tools not available"

```bash
# Restart Claude Code to reload mcp_settings.json
# Or check logs in ~/.claude/debug/
```

---

## Architecture Summary

| Tool | Strengths | Use Case |
|------|-----------|----------|
| **Codex** | 10 MCP servers, 97 agent prompts | Full-stack operations, database queries |
| **Gemini** | Policy engine, autonomous execution | Quick incident response, systemd debugging |
| **Claude** | 120+ built-in subagents, TodoWrite | Complex debugging, multi-step tasks |

---

## What Each Tool Does

### Codex CLI
- Uses **agent prompts** as personas (97 available)
- Has **10 MCP servers** for enterprise operations
- Best for: Database queries, Docker ops, AWS management

### Gemini CLI
- Uses **slash commands** for playbooks (6 SRE commands)
- Has **policy engine** (40+ rules: allow/ask/deny)
- Best for: Fast incident response, autonomous log analysis

### Claude Code
- Uses **120+ built-in subagents** (Explore, Debugger, Security, etc.)
- Has **5 MCP servers** (focused on essentials)
- Best for: Complex debugging, multi-file analysis, planning mode

---

## Advanced Configuration

### Adding Custom MCP Servers

All 3 tools can use the same MCP servers. Create once, configure in:
- `~/.codex/config.toml`
- `~/.claude/mcp_settings.json`
- Gemini CLI doesn't support custom MCP yet (built-in only)

### Creating Custom Slash Commands

**Codex:** Add `.md` files to `~/.codex/prompts/`
**Gemini:** Add `.toml` files to `~/.gemini/commands/sre/`
**Claude:** Uses built-in subagents (no custom slash commands)

### Multi-Server Deployment

```bash
# On each server, clone and install
git clone git@github.com:swisscodernano/awesome-codex-subagents.git
cd awesome-codex-subagents
./install.sh  # (create this script for automation)
```

---

## Files Structure in Repository

```
awesome-codex-subagents/
├── README.md                    # Main documentation
├── SETUP_GUIDE.md               # This file
│
├── codex/
│   ├── config.toml              # Codex configuration
│   ├── AGENTS.md                # Global persona
│   ├── prompts/                 # 97 agent prompts
│   └── mcp-servers/             # 10 MCP servers
│
├── gemini/
│   ├── settings.json            # Gemini configuration
│   ├── GEMINI.md                # Global persona
│   ├── commands/sre/            # 6 slash commands
│   ├── policies/user/           # Policy rules
│   └── projects/                # Project templates
│
├── claude/
│   ├── CLAUDE.md                # Global persona
│   ├── mcp_settings.json        # MCP configuration
│   ├── abtrading-CLAUDE.md      # Project template
│   └── commands-README.md       # Info file
│
└── projects/
    ├── abtrading/AGENTS.md      # Trading bot context
    ├── aiagens/AGENTS.md        # API context
    └── ...
```

---

## Contributing

1. Fork the repository
2. Add your custom agents/commands/servers
3. Update documentation
4. Submit PR

---

## License

MIT

---

## Support

- GitHub Issues: https://github.com/swisscodernano/awesome-codex-subagents/issues
- Documentation: See README.md for full details
