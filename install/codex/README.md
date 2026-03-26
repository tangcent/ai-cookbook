# Install for Codex

Instructions for installing ai-cookbook items globally into Codex.

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/.codex/config.toml` (table: `mcp_servers`) |
| Skills | `~/.codex/skills/` |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into `~/.codex/config.toml`:

```bash
# From the ai-cookbook root:
python3 install/codex/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/codex/merge-mcp.py chrome-devtools grafana
```

The script reads from `install/mcp-servers.json`, auto-fills variables from `install/.mcp-vars.json`, and merges into the existing `~/.codex/config.toml` while preserving other Codex settings and tables.

> For `grafana`, install the binary first: `brew install mcp-grafana`

---

## Install Skills

Install skill folders into `~/.codex/skills/` (with script path resolution):

```bash
# From the ai-cookbook root:
bash install/install-skills.sh codex
```

Or install individually:

```bash
bash install/install-skills.sh codex audit-sql
bash install/install-skills.sh codex git-workflow
```
