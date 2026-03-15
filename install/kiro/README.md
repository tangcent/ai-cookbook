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

The script reads from `install/mcp-servers.json`, adds Kiro-specific fields (`autoApprove`, `disabled`), auto-fills variables from `install/.mcp-vars.json`, and merges into the existing config.

> For `github` and `grafana`, install the binaries first: `brew install github-mcp-server mcp-grafana`

---

## Install Skills

Copy skill folders into `~/.kiro/skills/`:

```bash
# From the ai-cookbook root:
mkdir -p ~/.kiro/skills
for skill in skills/*/SKILL.md; do
  dir="$(dirname "$skill")"
  name="$(basename "$dir")"
  rm -rf ~/.kiro/skills/"$name"
  cp -r "$dir" ~/.kiro/skills/"$name"
done
```

Or install individually:

```bash
cp -r skills/audit-sql ~/.kiro/skills/
cp -r skills/git-workflow ~/.kiro/skills/
```
