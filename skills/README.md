# Skills Authoring Guide

This repository stores installable skills under `skills/<skill-name>/`.

## Required Structure

Each skill must include:

```text
skills/<skill-name>/
└── SKILL.md
```

Optional folders:

- `scripts/` for deterministic helper commands
- `references/` for long docs loaded only when needed
- `assets/` for templates or static files

## SKILL.md Contract

Every `SKILL.md` must start with YAML frontmatter:

```yaml
---
name: <skill-name>
description: <what it does + when to use it>
---
```

Rules:

- `name` must match folder name exactly.
- Use lowercase letters, digits, and hyphens only.
- Put all trigger guidance in `description`.
- Keep body instructions execution-focused and concise.

## Writing Rules

- Prefer imperative workflow steps over long explanations.
- Add hard constraints for risky behavior (force-push, destructive DB ops, etc.).
- Prefer one reliable command path instead of many alternatives.
- Ask for confirmation before destructive actions.
- If a repository template exists (PR/issue/MR), treat it as source of truth.

## Script Usage Rules

- Invoke helper scripts with `scripts/<file>` paths.
- If a script is required by the skill, include that script in the skill folder.
- Keep scripts shellcheck-friendly and dependency-light.

## Update Checklist

When creating or changing a skill:

1. Ensure frontmatter is valid and folder/name match.
2. Verify any commands in the skill are executable in a normal shell.
3. If adding a new skill, update:
   - Root `README.md` skill list.
   - `install/INSTALL.md` skill list/table.
4. If the skill has scripts, run a basic smoke check.
