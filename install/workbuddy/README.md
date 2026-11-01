# Install for WorkBuddy

Instructions for installing ai-cookbook items globally into WorkBuddy.

## Config Locations

| Type | Path |
|------|------|
| Skills | `~/.workbuddy/skills/<skill-name>/` |
| MCP | `~/.workbuddy/mcp.json` (see [mcp_configuration](../../README.md#mcps)) |
| Memory | `~/.workbuddy/MEMORY.md` |

---

## Install Skills

Skills are copied into `~/.workbuddy/skills/`:

```bash
# From the ai-cookbook root:
bash install/install-skills.sh workbuddy
```

Or install individually:

```bash
bash install/install-skills.sh workbuddy spec-driven
bash install/install-skills.sh workbuddy git-workflow
```

The target directory is wiped and re-copied on every run, so re-installing is safe and always yields the repo's current content.

## Runtime Adaptation

WorkBuddy deviates from the upstream tool conventions that most skills are written against:

| Upstream | WorkBuddy |
|----------|-----------|
| `Task` tool | `Agent` tool |
| `subagent_type: "general_purpose_task"` | `subagent_type: "general-purpose"` |

`install/workbuddy/runtime-note.md` records this mapping. `install-skills.sh` inserts that note right after the YAML frontmatter of any SKILL.md that declares `subagent_type` — i.e. every skill that spawns sub-agents. Frontmatter itself is never touched, and skills that don't use sub-agents are left byte-identical to `skills/<name>/`.

## Verify

```bash
ls ~/.workbuddy/skills/
head -10 ~/.workbuddy/skills/spec-driven/SKILL.md   # should show the runtime note
```
