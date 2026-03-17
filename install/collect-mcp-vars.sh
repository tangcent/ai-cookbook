#!/usr/bin/env bash
# Scan all AI tool MCP configs and collect existing variable values.
# Outputs a JSON file (install/.mcp-vars.json) with discovered values
# that can be reused when installing MCPs into other tools.
#
# Usage: bash install/collect-mcp-vars.sh [workspace_path]
#   workspace_path: optional, defaults to current directory

set -euo pipefail

WORKSPACE="${1:-.}"
OUTPUT="install/.mcp-vars.json"

# We'll collect values into associative-style temp files, then merge into JSON.
# Using a simple approach: grep known keys from all config files.

CONFIG_FILES=()

# --- Gather all possible MCP config file paths ---

# Cursor
for f in \
  "$HOME/.cursor/mcp.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# Kiro
for f in \
  "$HOME/.kiro/settings/mcp.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# Claude Code
for f in \
  "$HOME/.claude.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# Cline (VS Code extension)
for f in \
  "$HOME/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# OpenCode
for f in \
  "$HOME/.config/opencode/opencode.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# Tare (unverified path)
for f in \
  "$HOME/.tare/mcp.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# Antigravity
for f in \
  "$HOME/.gemini/antigravity/mcp_config.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# Trae
for f in \
  "$HOME/Library/Application Support/Trae/User/mcp.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

# Trae CN
for f in \
  "$HOME/Library/Application Support/Trae CN/User/mcp.json"; do
  [ -f "$f" ] && CONFIG_FILES+=("$f")
done

if [ ${#CONFIG_FILES[@]} -eq 0 ]; then
  echo "No MCP config files found."
  echo '{}' > "$OUTPUT"
  exit 0
fi

echo "Scanning ${#CONFIG_FILES[@]} config file(s)..."
for f in "${CONFIG_FILES[@]}"; do
  echo "  → $f"
done
echo ""

# --- Use python3 to parse JSON and extract variables ---
python3 - "${CONFIG_FILES[@]}" "$OUTPUT" << 'PYEOF'
import json
import sys
import os
import re

config_files = sys.argv[1:-1]
output_file = sys.argv[-1]

# Known variable keys we want to collect, grouped by MCP server name
# Maps: env_var_name -> friendly_key
KNOWN_VARS = {
    "GRAFANA_URL": "grafana_url",
    "GRAFANA_USERNAME": "grafana_username",
    "GRAFANA_PASSWORD": "grafana_password",
    "GRAFANA_ORG_ID": "grafana_org_id",
}

# Placeholder patterns to skip
PLACEHOLDER_RE = re.compile(
    r"^(<.*>|\[.*\]|/path/to/.*|your-.*|http://your-.*|<email>|<password>)$",
    re.IGNORECASE,
)

collected = {}  # friendly_key -> value
commands = {}   # mcp_name -> command path

for fpath in config_files:
    try:
        with open(fpath) as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        continue

    # Find mcpServers (could be top-level or nested under "mcp")
    servers = data.get("mcpServers", data.get("mcp", {}))
    if not isinstance(servers, dict):
        continue

    for server_name, server_cfg in servers.items():
        if not isinstance(server_cfg, dict):
            continue

        # Collect command paths (for github, grafana binaries)
        cmd = server_cfg.get("command", "")
        # Handle command as string or array
        if isinstance(cmd, list):
            cmd = cmd[0] if cmd else ""
        if cmd and cmd not in ("npx", "uvx", "node", "python3") and not PLACEHOLDER_RE.match(str(cmd)):
            key = f"{server_name}_command"
            if key not in collected:
                collected[key] = str(cmd)
                commands[server_name] = str(cmd)

        # Collect env vars (supports both "env" and "environment" keys)
        env = server_cfg.get("env", server_cfg.get("environment", {}))
        if isinstance(env, dict):
            for env_key, env_val in env.items():
                if env_key in KNOWN_VARS and env_val and not PLACEHOLDER_RE.match(str(env_val)):
                    friendly = KNOWN_VARS[env_key]
                    if friendly not in collected:
                        collected[friendly] = str(env_val)

result = {
    "source_files": config_files,
    "variables": collected,
}

with open(output_file, "w") as f:
    json.dump(result, f, indent=2)

# Print summary
if collected:
    print("Collected variables:")
    for k, v in collected.items():
        # Mask sensitive values
        if "pat" in k or "password" in k or "token" in k:
            display = v[:4] + "****" + v[-4:] if len(v) > 8 else "****"
        else:
            display = v
        print(f"  {k} = {display}")
    print(f"\nSaved to {output_file}")
else:
    print("No reusable variables found in existing configs.")
    print(f"Empty result saved to {output_file}")
PYEOF

echo ""
echo "Done. The agent can now read $OUTPUT to auto-fill MCP configs."
