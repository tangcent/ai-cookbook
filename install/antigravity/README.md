# Install for Antigravity

Instructions for installing ai-cookbook items globally into Antigravity (Google's AI IDE).

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/.gemini/antigravity/mcp_config.json` |
| Skills | `~/.gemini/antigravity/skills` |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into `~/.gemini/antigravity/mcp_config.json`:

```bash
# From the ai-cookbook root:
python3 install/antigravity/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/antigravity/merge-mcp.py github grafana
```

The script reads from `install/mcp-servers.json`, auto-fills variables from `install/.mcp-vars.json`, and merges into the existing config. Re-running the script is safe — existing settings are never overwritten.

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Install skill folders into `~/.gemini/antigravity/skills/` (with script path resolution):

```bash
# From the ai-cookbook root:
bash install/install-skills.sh antigravity
```

Or install individually:

```bash
bash install/install-skills.sh antigravity audit-sql
bash install/install-skills.sh antigravity git-workflow
```
