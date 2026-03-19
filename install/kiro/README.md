# Install for Kiro

Instructions for installing ai-cookbook items globally into Kiro.

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/.kiro/settings/mcp.json` |
| Skills | `~/.kiro/skills/<skill-name>/` |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into `~/.kiro/settings/mcp.json`:

```bash
# From the ai-cookbook root:
python3 install/kiro/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/kiro/merge-mcp.py github grafana
```

The script reads from `install/mcp-servers.json`, adds Kiro-specific fields (`autoApprove`, `disabled`), auto-fills variables from `install/.mcp-vars.json`, and merges into the existing config. MCPs are installed with `disabled: true` by default — enable them via the Kiro UI when you need them for a project. Re-running the script is safe; user-controlled settings like `disabled` are never overwritten.

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Install skill folders into `~/.kiro/skills/` (with script path resolution):

```bash
# From the ai-cookbook root:
bash install/install-skills.sh kiro
```

Or install individually:

```bash
bash install/install-skills.sh kiro audit-sql
bash install/install-skills.sh kiro git-workflow
```
