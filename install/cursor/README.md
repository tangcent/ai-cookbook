# Install for Cursor

Instructions for installing ai-cookbook items globally into Cursor.

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/.cursor/mcp.json` (key: `mcpServers`) |
| Skills | `~/.cursor/skills/` |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into `~/.cursor/mcp.json`:

```bash
# From the ai-cookbook root:
python3 install/cursor/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/cursor/merge-mcp.py github grafana
```

The script reads from `install/mcp-servers.json`, auto-fills variables from `install/.mcp-vars.json`, and merges into the existing `~/.cursor/mcp.json` (preserving other keys). Re-running the script is safe — existing settings are never overwritten.

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Install skill folders into `~/.cursor/skills/` (with script path resolution):

```bash
# From the ai-cookbook root:
bash install/install-skills.sh cursor
```

Or install individually:

```bash
bash install/install-skills.sh cursor audit-sql
bash install/install-skills.sh cursor git-workflow
```
