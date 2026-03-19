# Install for OpenCode

Instructions for installing ai-cookbook items globally into OpenCode.

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/.config/opencode/opencode.json` (key: `mcp`) |
| Skills | `~/.config/opencode/skills/` (unverified) |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into `~/.config/opencode/opencode.json`:

```bash
# From the ai-cookbook root:
python3 install/opencode/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/opencode/merge-mcp.py github grafana
```

The script reads from `install/mcp-servers.json`, converts to OpenCode format (`mcp` key, `command` as array, `environment` instead of `env`, `type: "local"`), auto-fills variables from `install/.mcp-vars.json`, and merges into the existing config. Re-running the script is safe — existing settings are never overwritten.

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Install skill folders into `~/.config/opencode/skills/` (with script path resolution):

```bash
# From the ai-cookbook root:
bash install/install-skills.sh opencode
```

Or install individually:

```bash
bash install/install-skills.sh opencode audit-sql
```
