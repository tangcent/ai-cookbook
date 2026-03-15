# Install for Trae CN

Instructions for installing ai-cookbook items globally into Trae CN.

## Config Locations

| Type | Path |
|------|------|
| MCP | `~/Library/Application Support/Trae CN/User/mcp.json` (key: `mcpServers`) |
| Skills | `~/.trae-cn/skills/` |

---

## Install CLIs

### playwright-cli

```bash
npm install -g @playwright/cli@latest
```

---

## Install MCPs

Merge all MCP servers into `~/Library/Application Support/Trae CN/User/mcp.json`:

```bash
# From the ai-cookbook root:
python3 install/trae-cn/merge-mcp.py
```

Or merge specific servers:

```bash
python3 install/trae-cn/merge-mcp.py github grafana
```

The script reads from `install/mcp-servers.json`, auto-fills variables from `install/.mcp-vars.json`, and merges into the existing `~/Library/Application Support/Trae CN/User/mcp.json` (preserving other keys).

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Copy skill folders into `~/.trae-cn/skills/`:

```bash
# From the ai-cookbook root:
mkdir -p ~/.trae-cn/skills
for skill in skills/*/SKILL.md; do
  dir="$(dirname "$skill")"
  name="$(basename "$dir")"
  rm -rf ~/.trae-cn/skills/"$name"
  cp -r "$dir" ~/.trae-cn/skills/"$name"
done
```

Or install individually:

```bash
cp -r skills/audit-sql ~/.trae-cn/skills/
cp -r skills/git-workflow ~/.trae-cn/skills/
```
