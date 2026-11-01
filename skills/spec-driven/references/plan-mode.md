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
4. Break down into ordered tasks with acceptance criteria — apply [best-practices.md](best-practices.md) when splitting tasks (test-first for most work, contract-first for APIs/interfaces)
5. Produce a single combined plan document

## Inputs

This mode reads from:

- **User request:** The goal, scope, and any constraints
- **Project codebase:** Relevant code, patterns, conventions, affected files

> **Important — Preserve original references.** Record URLs, external docs, and key files consulted in the plan. Execute mode dispatches task workers as stateless sub-agents — the plan must be self-sufficient with enough context (approach, acceptance criteria, file targets) that the executor doesn't need the original conversation.

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

## Interaction Protocol

Plan workers never talk to the user directly — the orchestrator (main session) owns all user interaction.

- Keep clarification to 2-3 questions max; unresolved ones go into `open_questions` in the return summary, and the orchestrator asks them at the plan gate.
- If the orchestrator's handoff already contains answers (goal, scope, preferences), apply them without asking again.

Gate confirmations owned by the orchestrator:

1. **Approach** — "Here's how I'd approach this: [brief summary]. Sound right?"
2. **Task list** — "Here are [N] tasks. Anything to add or remove?"

One round of confirmation is usually enough for Plan mode.

## Output

Save to `.spec/<spec-name>/plan.md`

`plan.md` uses the same task syntax as `tasks.md`, so the Spec Tools work on it: `status`, `done`, and `trace` behave identically. `dag` treats a plan as a serial chain (plans carry no `Files:` lines), which matches how Plan mode is meant to be executed. `check` only requires `Files:` lines in `tasks*.md`, so a plan is not penalized for omitting them.

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
  - [ ] 2.1 Write test for [feature]
  - [ ] 2.2 Implement [feature] to satisfy 2.1

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

→ Return to the orchestrator per the return contract (`files_written`, `key_decisions`, `open_questions`).

→ The orchestrator spot-checks the plan, then asks at the gate: "Plan looks good? Ready to start executing?"

→ On approval, proceed to **Execute Mode**
