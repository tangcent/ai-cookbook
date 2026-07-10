# Tasks Mode

## Purpose

Break the design into small, ordered, actionable implementation tasks that can be executed one at a time. Each task should be independently verifiable. Tasks use checkbox format for progress tracking.

## What This Mode Does

1. Analyze the design document (from `design.md` or user input)
2. Read requirements (from `requirements.md` or sub-files) to ensure full coverage
3. Cross-check: verify every acceptance criterion in requirements has at least one task covering it
4. Decompose into atomic implementation tasks
5. Group tasks into phases ordered by dependency (foundational work first)
6. Define clear completion criteria for each task
7. Identify which files are created or modified per task
8. Cross-reference tasks back to requirements
9. Produce a formal task list document (with sub-files for large specs)

## Inputs

This mode reads from:

- **Upstream artifacts:** `.spec/{spec_name}/requirements.md` and `.spec/{spec_name}/design.md` (and sub-files if large feature)
- **Project codebase:** File structure, test patterns, build/config files
- **User context:** Ordering preferences, scope decisions

> **Important — Preserve traceability.** Each task must cross-reference the requirement(s) it satisfies and the design decisions it implements. Execute mode runs in separate sub-agents — tasks must carry enough context (requirement references, file targets, acceptance criteria) to be executable without re-reading the full requirements/design docs.

## Information to Collect

### From Requirements

- All functional requirements and their acceptance criteria — these are the source of truth for what each task must satisfy
- Non-functional requirements that impose constraints on implementation (performance, security, etc.)
- Priority classification (must-have vs nice-to-have) to determine task ordering and optional task markers
- Acceptance criteria to cross-reference in tasks (e.g. `_Requirements: Auth 2.1, 2.3_`)
- If requirements exist as sub-files (`requirements-<module>.md`), read each relevant module's requirements

### From Design

- Component breakdown and affected files
- Data model changes and API contracts
- Dependencies between components that determine task ordering
- Package/file structure that determines where new code goes
- Design decisions that constrain implementation choices

### From the Codebase

- Existing file structure to determine where new code goes
- Existing test patterns to know what test tasks look like
- Build/config files that may need updates

### From the User

- Any ordering preferences
- Whether tests should be included as separate tasks or inline
- Any tasks they want to skip or defer

## Task Decomposition Rules

1. **Atomic:** Each task should do one thing. "Add user model AND create API endpoint" is two tasks.
2. **Phased:** Tasks are grouped into dependency-ordered phases (scaffolding → foundation → core → integration → UI).
3. **Verifiable:** Each task has clear criteria to know when it's done.
4. **Scoped:** Each task should be completable in a single focused session (roughly 1-30 minutes of agent work).
5. **File-aware:** Each task lists the files it will create or modify.
6. **Traceable:** Each task references the requirement(s) it satisfies.
7. **Checkpointed:** Add checkpoint tasks between phases to verify everything works before moving on.
8. **Contract/test-before-implementation, by default:** Consult [best-practices.md](best-practices.md) when splitting a unit of work. For most feature tasks, split into a test sub-task before the implementation sub-task (TDD). For API/interface tasks, split into a contract/type-definition sub-task before the implementation sub-task. Only skip this split for trivial changes or explicit throwaway work — see best-practices.md → "When to Skip".

## Task Format

Use checkbox format with hierarchical numbering for sub-tasks:

```markdown
- [ ] 1. [Task title]
  - [ ] 1.1 [Sub-task description]
    - [Detail or specific instruction]
    - _Requirements: [Module] [Requirement#.Criteria#]_
  - [ ] 1.2 [Sub-task description]
    - _Requirements: [Module] [Requirement#.Criteria#]_
```

Mark completed tasks with `[x]`:
```markdown
- [x] 1. [Completed task]
  - [x] 1.1 [Completed sub-task]
```

Optional tasks (nice-to-haves, not core coverage) use `*` suffix:
```markdown
  - [ ]* 1.3 Write property test for [feature]
```

Note: the primary test for a piece of behavior is NOT optional — per [best-practices.md](best-practices.md), it comes *before* the implementation sub-task it validates, and isn't marked `*`. Reserve `*` for supplementary tests (property tests, extra edge cases) beyond the core test-first pair.

## What to Confirm with User

Before finalizing tasks:

1. **Task list review** — "Here are [N] tasks in [P] phases. Anything missing or out of order?"
2. **Scope check** — "Should I include test tasks? Documentation tasks?"
3. **Priority adjustment** — "Want to defer any of these to a later phase?"

## Output

### Small Feature

Save a single `tasks.md` to `.spec/<spec-name>/tasks.md`

### Large Feature

Save a master index + per-module sub-files:
- `.spec/<spec-name>/tasks.md` — master index with phase ordering and module links
- `.spec/<spec-name>/tasks-<module>.md` — detailed tasks per module

## Template: tasks.md (Small Feature)

```markdown
# Tasks: [Feature Name]

## Overview
[Total task count] tasks in [phase count] phases. Tasks are ordered by dependency.

## Tasks

### Phase 1: [Phase Name]

- [ ] 1. [Task title]
  - [ ] 1.1 [Sub-task with specific instruction]
    - [Implementation detail]
    - _Requirements: [Requirement#.Criteria#]_
  - [ ] 1.2 [Sub-task]
    - _Requirements: [Requirement#.Criteria#]_

- [ ] 2. Checkpoint — Verify [what to verify]
  - Ensure all tests pass, ask the user if questions arise.

### Phase 2: [Phase Name]

- [ ] 3. [Task title]
  - [ ] 3.1 Write test for [feature]
    - _Requirements: [Requirement#.Criteria#]_
  - [ ] 3.2 Implement [feature] to satisfy 3.1
    - _Requirements: [Requirement#.Criteria#]_

- [ ] 4. [Task title]
  - [ ] 4.1 [Sub-task]
    - _Requirements: [Requirement#.Criteria#]_

[... more tasks ...]

## Notes
- Tasks marked with `*` are optional and can be skipped for faster MVP
- Checkpoints ensure incremental validation
```

## Template: tasks.md (Large Feature — Master Index)

```markdown
# Implementation Plan: [Feature Name]

## Overview
Complete implementation of [feature]. Tasks are split per module, ordered by dependency: [phase ordering description].

## Execution Order

### Phase 0: Project Scaffolding
- [tasks.md — Task 1 below](#task-1)

### Phase 1: [Phase Name]
1. [tasks-module-a.md](tasks-module-a.md) — [Description]
2. [tasks-module-b.md](tasks-module-b.md) — [Description]

### Phase 2: [Phase Name]
3. [tasks-module-c.md](tasks-module-c.md) — [Description]
4. [tasks-module-d.md](tasks-module-d.md) — [Description]

[... more phases ...]

## Tasks

- [ ] 1. [Scaffolding / cross-cutting task]
  - [ ] 1.1 [Sub-task]
  - [ ] 1.2 [Sub-task]

- [ ] 2. Checkpoint — Verify [scaffolding works]
  - Ensure all tests pass, ask the user if questions arise.

## Notes
- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each module task file references specific requirements and design documents
- Checkpoints ensure incremental validation
```

## Template: tasks-<module>.md (Sub-file)

```markdown
# Tasks: [Module Name] — [Brief Description]

> References: [requirements-<module>.md](requirements-<module>.md) | [design-<module>.md](design-<module>.md)

## Tasks

- [ ] 1. [Task title]
  - [ ] 1.1 [Sub-task]
    - [Implementation detail]
    - _Requirements: [Module] [Requirement#.Criteria#]_
  - [ ] 1.2 [Sub-task]
    - _Requirements: [Module] [Requirement#.Criteria#]_

- [ ] 2. [Task title]
  - [ ] 2.1 Write test for [feature]
    - _Requirements: [Module] [Requirement#.Criteria#]_
  - [ ] 2.2 Implement [feature] to satisfy 2.1
    - _Requirements: [Module] [Requirement#.Criteria#]_

- [ ] 3. Checkpoint — Verify [module] tests pass
  - Ensure all tests pass, ask the user if questions arise.
```

## Next Step

→ Summarize the task list and ask: "Tasks look good? Ready to start executing, or want to adjust anything?"

→ Proceed to **Execute Mode**

## See Also

[best-practices.md](best-practices.md) — task sequencing guidance by category (TDD, contract-first APIs, migrations, refactoring, etc.), used when deciding how to split and order tasks above.
