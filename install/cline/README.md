# Install for Cline

Instructions for installing ai-cookbook items globally into Cline (VS Code extension).

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| Skills | `~/.cline/skills/<skill-name>/SKILL.md` |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into the Cline config:

```bash
# From the ai-cookbook root:
python3 install/cline/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/cline/merge-mcp.py github grafana
```

The script reads from `install/mcp-servers.json`, adds Cline-specific fields (`disabled`), auto-fills variables from `install/.mcp-vars.json`, and merges into the existing config.

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Install skill folders into `~/.cline/skills/` (with script path resolution):

```bash
# From the ai-cookbook root:
bash install/install-skills.sh cline
```

Or install individually:

```bash
bash install/install-skills.sh cline audit-sql
bash install/install-skills.sh cline git-workflow
```
