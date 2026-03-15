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

The script reads from `install/mcp-servers.json`, auto-fills variables from `install/.mcp-vars.json`, and merges into the existing config.

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Copy skill folders into `~/.gemini/antigravity/skills/`:

```bash
# From the ai-cookbook root:
mkdir -p ~/.gemini/antigravity/skills
for skill in skills/*/SKILL.md; do
  dir="$(dirname "$skill")"
  name="$(basename "$dir")"
  rm -rf ~/.gemini/antigravity/skills/"$name"
  cp -r "$dir" ~/.gemini/antigravity/skills/"$name"
done
```

Or install individually:

```bash
cp -r skills/audit-sql ~/.gemini/antigravity/skills/
cp -r skills/git-workflow ~/.gemini/antigravity/skills/
```
