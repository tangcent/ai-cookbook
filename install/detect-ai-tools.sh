#!/usr/bin/env bash
# Detect which AI coding tools are available on this machine.
# Outputs a line per tool: "<tool>: available" or "<tool>: not found"
# Exit code 0 if at least one tool is found, 1 if none.

set -euo pipefail

found=0

# --- Cursor ---
if command -v cursor &>/dev/null || [ -d "$HOME/.cursor" ]; then
  echo "cursor: available"
  found=1
else
  echo "cursor: not found"
fi

# --- Kiro ---
if [ -d "$HOME/.kiro" ] || command -v kiro &>/dev/null; then
  echo "kiro: available"
  found=1
else
  echo "kiro: not found"
fi

# --- Claude Code (claude) ---
if command -v claude &>/dev/null; then
  echo "claude: available"
  found=1
else
  echo "claude: not found"
fi

# --- Codex ---
if command -v codex &>/dev/null || [ -f "$HOME/.codex/config.toml" ] || [ -d "$HOME/.codex/skills" ]; then
  echo "codex: available"
  found=1
else
  echo "codex: not found"
fi

# --- Cline (VS Code extension) ---
CLINE_SETTINGS="$HOME/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
if command -v code &>/dev/null && code --list-extensions 2>/dev/null | grep -qi "saoudrizwan.claude-dev"; then
  echo "cline: available"
  found=1
elif [ -f "$CLINE_SETTINGS" ]; then
  echo "cline: available"
  found=1
else
  echo "cline: not found"
fi

# --- OpenCode ---
if command -v opencode &>/dev/null || [ -f "$HOME/.config/opencode/opencode.json" ]; then
  echo "opencode: available"
  found=1
else
  echo "opencode: not found"
fi

# --- Tare ---
if command -v tare &>/dev/null; then
  echo "tare: available"
  found=1
else
  echo "tare: not found"
fi

# --- Antigravity ---
if command -v antigravity &>/dev/null || [ -f "$HOME/.gemini/antigravity/mcp_config.json" ]; then
  echo "antigravity: available"
  found=1
else
  echo "antigravity: not found"
fi

# --- Trae ---
TRAE_MCP="$HOME/Library/Application Support/Trae/User/mcp.json"
if [ -f "$TRAE_MCP" ]; then
  echo "trae: available"
  found=1
else
  echo "trae: not found"
fi

# --- Trae CN ---
TRAE_CN_MCP="$HOME/Library/Application Support/Trae CN/User/mcp.json"
if [ -f "$TRAE_CN_MCP" ]; then
  echo "trae-cn: available"
  found=1
else
  echo "trae-cn: not found"
fi

echo ""
if [ "$found" -eq 1 ]; then
  echo "At least one AI tool detected."
  exit 0
else
  echo "No AI tools detected."
  exit 1
fi
