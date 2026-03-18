# Install for Claude Code

Instructions for installing ai-cookbook items globally into Claude Code.

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/.claude.json` (key: `mcpServers`) |
| Skills | `~/.claude/skills/` |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into `~/.claude.json`:

```bash
# From the ai-cookbook root:
python3 install/claude/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/claude/merge-mcp.py github grafana
```

The script reads from `install/mcp-servers.json`, auto-fills variables from `install/.mcp-vars.json`, and merges into the existing `~/.claude.json` (preserving other keys).

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Install skill folders into `~/.claude/skills/` (with script path resolution):

```bash
# From the ai-cookbook root:
bash install/install-skills.sh claude
```

Or install individually:

```bash
bash install/install-skills.sh claude audit-sql
bash install/install-skills.sh claude git-workflow
```
