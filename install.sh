#!/bin/bash
set -e

echo "Installing Awesome Codex Subagents..."

# Create directories
mkdir -p ~/.codex/prompts

# Copy prompts
echo "Copying 97 agent prompts..."
cp -r prompts/* ~/.codex/prompts/

# Copy global AGENTS.md
echo "Installing global AGENTS.md..."
cp AGENTS.md ~/.codex/

# Backup existing config
if [ -f ~/.codex/config.toml ]; then
    echo "Backing up existing config.toml..."
    cp ~/.codex/config.toml ~/.codex/config.toml.backup
fi

# Merge config (append if not present)
if ! grep -q "project_doc_fallback_filenames" ~/.codex/config.toml 2>/dev/null; then
    echo "Adding autopilot config..."
    cat >> ~/.codex/config.toml << 'EOF'

# === AUTOPILOT CONFIG (from awesome-codex-subagents) ===
project_doc_fallback_filenames = ["AGENTS.md", "AGENTS.override.md", "codex.yaml", "codex.yml"]
project_doc_max_bytes = 65536
approval_policy = "on-failure"
EOF
fi

# Add bash aliases
if ! grep -q "alias cdx=" ~/.bashrc 2>/dev/null; then
    echo "Adding bash aliases..."
    cat >> ~/.bashrc << 'EOF'

# Codex CLI Aliases (from awesome-codex-subagents)
alias cdx='codex --model gpt-5.1-codex --full-auto'
alias cdxmax='codex --model gpt-5.1-codex-max --full-auto'
EOF
fi

echo ""
echo "Installation complete!"
echo ""
echo "Available commands:"
echo "  cdx     - Standard turbo mode"
echo "  cdxmax  - Max model + turbo"
echo ""
echo "Available slash commands:"
echo "  /health, /logs, /sre-debug, /incident, /restart, /deploy"
echo ""
echo "Available agents (97 total):"
echo "  /agent-sre, /agent-devops, /agent-python, /agent-frontend, ..."
echo ""
echo "Run 'source ~/.bashrc' to activate aliases."
