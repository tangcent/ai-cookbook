---
name: create-skill
description: Create or update a skill in this repository under skills/<skill-name>. Use when the user asks to add a new skill, improve an existing skill, scaffold skill structure, or align a skill with repository standards.
---

# Create Skill

Create or update skills in this repository following `skills/README.md`.

## Workflow

### 1. Gather intent

Collect or infer:

- Skill name (`lowercase-hyphen` format)
- Trigger description (what it does and when to use it)
- Whether it needs `scripts/`, `references/`, or `assets/`
- Whether this is a new skill or an update to an existing one

If the user provides partial info, proceed with reasonable defaults and ask only if blocked.

### 2. Read local standards

Read `skills/README.md` before creating or modifying the skill.

### 3. Create or update skill files

For a new skill, create:

```text
skills/<skill-name>/SKILL.md
```

Use this template:

```markdown
---
name: <skill-name>
description: <what it does + when to use it>
---

# <Skill Title>

## Workflow

1. ...
```

If helper logic is deterministic, add scripts under `skills/<skill-name>/scripts/`.

### 4. Integrate into repository docs

When adding a new skill, update:

- `README.md` skill catalog

### 5. Validate

Run quick checks:

- Frontmatter exists and name matches folder.
- Referenced scripts exist.
- Any bundled script has executable permission if intended to run directly.

### 6. Summarize

Report:

- Files created/updated
- Validation outcomes
- Any follow-up needed

## Constraints

- Never create skills outside `skills/<skill-name>/`.
- Never skip repository doc updates when adding new skills.
- Keep instructions concise and execution-focused.
