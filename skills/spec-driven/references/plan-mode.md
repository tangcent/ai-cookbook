# Plan Mode

## Purpose

A lightweight alternative to the full Spec flow. Combines requirements gathering and task breakdown into a single pass — ideal for smaller features, well-understood work, or when the user wants to move fast.

## When to Use Plan Mode

- The feature is relatively small or well-scoped
- The user says "plan" rather than "spec" or "requirements"
- The user wants a quick breakdown without formal design docs
- The technical approach is straightforward and doesn't need a separate design phase

## What This Mode Does

1. Understand the user's goal (brief requirements gathering)
2. Survey the codebase for relevant context
3. Propose an approach with inline design notes
4. Break down into ordered tasks with acceptance criteria
5. Produce a single combined plan document

## Information to Collect

### From the User

- **Goal:** What are we building? (1-2 sentences is fine)
- **Scope:** Any boundaries or constraints?
- **Preferences:** Any specific approach or tech choices?

Keep it conversational. Plan mode is meant to be fast — 2-3 questions max.

### From the Codebase

- Relevant existing code, patterns, and conventions
- Files that will be affected
- Dependencies and integration points

## What to Confirm with User

Before finalizing the plan:

1. **Approach** — "Here's how I'd approach this: [brief summary]. Sound right?"
2. **Task list** — "Here are [N] tasks. Anything to add or remove?"

One round of confirmation is usually enough for Plan mode.

## Output

Save to `.spec/<spec-name>/plan.md`

## Template: plan.md

```markdown
# Plan: [Feature Name]

## Goal
[1-2 sentence summary of what we're building and why]

## Approach
[Brief technical approach — what components are involved, key decisions, any notable patterns.
Include inline design notes where relevant rather than a separate design doc.]

## Scope
**In scope:**
- [Item 1]
- [Item 2]

**Out of scope:**
- [Item 1]

## Tasks

- [ ] 1. [Task title]
  - [ ] 1.1 [Sub-task with specific instruction]
    - [Implementation detail]
  - [ ] 1.2 [Sub-task]

- [ ] 2. [Task title]
  - [ ] 2.1 [Sub-task]
  - [ ]* 2.2 Write test for [feature]

- [ ] 3. Checkpoint — Verify [what to verify]

[... more tasks ...]

## Notes
[Any assumptions, risks, or things to watch out for during execution]
```

## Differences from Spec Flow

| Aspect | Plan Mode | Spec Flow |
|--------|-----------|-----------|
| Documents produced | 1 (`plan.md`) | Up to 3+ (`requirements.md`, `design.md`, `tasks.md` + sub-files) |
| Requirements depth | Brief goal + scope | Full EARS-style FR/NFR with acceptance criteria |
| Design depth | Inline approach notes | Separate design doc with data models, APIs, architecture diagrams |
| Task format | Same checkbox format | Same checkbox format, but with requirement cross-references |
| Best for | Small-medium features, clear scope | Complex features, team alignment, unfamiliar domains |
| Speed | Fast (1 confirmation round) | Thorough (confirmation per phase) |

## Next Step

→ Summarize the plan and ask: "Plan looks good? Ready to start executing?"

→ Proceed to **Execute Mode**
