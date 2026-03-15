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

Copy skill folders into `~/.claude/skills/`:

```bash
# From the ai-cookbook root:
mkdir -p ~/.claude/skills
for skill in skills/*/SKILL.md; do
  dir="$(dirname "$skill")"
  name="$(basename "$dir")"
  rm -rf ~/.claude/skills/"$name"
  cp -r "$dir" ~/.claude/skills/"$name"
done
```

Or install individually:

```bash
cp -r skills/audit-sql ~/.claude/skills/
cp -r skills/git-workflow ~/.claude/skills/
```
