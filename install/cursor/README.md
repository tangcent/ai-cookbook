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

The script reads from `install/mcp-servers.json`, auto-fills variables from `install/.mcp-vars.json`, and merges into the existing `~/.cursor/mcp.json` (preserving other keys).

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Copy skill folders into `~/.cursor/skills/`:

```bash
# From the ai-cookbook root:
mkdir -p ~/.cursor/skills
for skill in skills/*/SKILL.md; do
  dir="$(dirname "$skill")"
  name="$(basename "$dir")"
  rm -rf ~/.cursor/skills/"$name"
  cp -r "$dir" ~/.cursor/skills/"$name"
done
```

Or install individually:

```bash
cp -r skills/audit-sql ~/.cursor/skills/
cp -r skills/git-workflow ~/.cursor/skills/
```
