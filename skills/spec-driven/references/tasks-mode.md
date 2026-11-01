# Tasks Mode

## Purpose

Break the design into small, ordered, actionable implementation tasks that can be executed one at a time. Each task should be independently verifiable. Tasks use checkbox format for progress tracking.

## What This Mode Does

1. Analyze the design document (from `design.md` or user input)
2. Read requirements (from `requirements.md` or sub-files) to ensure full coverage
3. Decompose into atomic implementation tasks
4. Group tasks into phases ordered by dependency (foundational work first)
5. Define clear completion criteria for each task
6. Identify which files are created or modified per task — record them in a machine-parseable `Files:` line (see Task Format)
7. Cross-reference tasks back to requirements
8. Coverage acceptance: verify every acceptance criterion in requirements is covered by at least one task — run `trace <spec>` once the task list is written and resolve any orphan references or uncovered criteria before returning; report the coverage numbers in the return summary
9. Produce a formal task list document (with sub-files for large specs)

## Inputs

This mode reads from:

- **Upstream artifacts:** `.spec/{spec_name}/requirements.md` and `.spec/{spec_name}/design.md` (and sub-files if large feature)
- **Project codebase:** File structure, test patterns, build/config files
- **User context:** Ordering preferences, scope decisions

> **Important — Preserve traceability.** Each task must cross-reference the requirement(s) it satisfies and the design decisions it implements. Execute mode dispatches task workers as stateless sub-agents — tasks must carry enough context (requirement references, file targets, acceptance criteria) to be executable without re-reading the full requirements/design docs.

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
5. **File-aware:** Each task declares every file it creates or modifies in an exhaustive `Files:` line. The orchestrator parses these lines to detect file overlaps between tasks and build the execution DAG — a file not listed is off-limits for that task.
6. **Traceable:** Each task references the requirement(s) it satisfies.
7. **Checkpointed:** Add checkpoint tasks between phases to verify everything works before moving on.
8. **Contract/test-before-implementation, by default:** Consult [best-practices.md](best-practices.md) when splitting a unit of work. For most feature tasks, split into a test sub-task before the implementation sub-task (TDD). For API/interface tasks, split into a contract/type-definition sub-task before the implementation sub-task. Only skip this split for trivial changes or explicit throwaway work — see best-practices.md → "When to Skip".

## Task Format

Use checkbox format with hierarchical numbering for sub-tasks:

```markdown
- [ ] 1. [Task title]
  - Files: `path/a.ts`, `path/b.ts`
  - [ ] 1.1 [Sub-task description]
    - [Detail or specific instruction]
    - _Requirements: [Module] [Requirement#.Criteria#]_
  - [ ] 1.2 [Sub-task description]
    - _Requirements: [Module] [Requirement#.Criteria#]_
```

Mark completed tasks with `[x]`:
```markdown
- [x] 1. [Completed task]
  - Files: `path/a.ts`
  - [x] 1.1 [Completed sub-task]
```

Optional tasks (nice-to-haves, not core coverage) use `*` suffix:
```markdown
  - [ ]* 1.3 Write property test for [feature]
```

Note: the primary test for a piece of behavior is NOT optional — per [best-practices.md](best-practices.md), it comes *before* the implementation sub-task it validates, and isn't marked `*`. Reserve `*` for supplementary tests (property tests, extra edge cases) beyond the core test-first pair.

Rules for the `Files:` line:

- One `Files:` line directly under every top-level task title.
- Comma-separated, backtick-quoted paths, exhaustive: every file the task creates or modifies must appear.
- The orchestrator parses `Files:` lines to detect overlaps between tasks and build the execution DAG (`dag <spec>`); a file not listed is treated as off-limits for that task.
- Tasks that touch no files (e.g. checkpoints, pure investigation) use `Files: (none)`.
- `check <spec>` fails on any top-level task missing this line, so a missing `Files:` line breaks parallel scheduling — treat it as a defect, not a style issue.

## Interaction Protocol

Task workers never talk to the user directly — the orchestrator (main session) owns all user interaction.

Gate confirmations owned by the orchestrator:

1. **Task list review** — "Here are [N] tasks in [P] phases. Anything missing or out of order?"
2. **Scope check** — "Should I include test tasks? Documentation tasks?"
3. **Priority adjustment** — "Want to defer any of these to a later phase?"

Worker rules:

- Any unresolved question about scope, ordering, or priorities goes into `open_questions` in the return summary; the orchestrator relays it to the user at the tasks gate.
- If the orchestrator's handoff already contains the user's answers (scope or ordering decisions confirmed at the gate), apply them without asking again.

## Output

### Small Feature

Save a single `tasks.md` to `.spec/<spec-name>/tasks.md`

### Large Feature

Save a master index + per-module sub-files:
- `.spec/<spec-name>/tasks.md` — master index with phase ordering and module links
- `.spec/<spec-name>/tasks-<module>.md` — detailed tasks per module

## Large Spec Parallelization

For large specs, task decomposition runs master-then-parallel:

1. **Master skeleton first:** One worker (or the orchestrator) writes `tasks.md` with only the global structure — phase ordering, module index, and scaffolding/cross-cutting tasks. Phase ordering must be fixed at this step; it is the contract every module worker follows.
2. **Gate:** The orchestrator shows the skeleton to the user for confirmation (phase order, module split, scope).
3. **Per-module workers in parallel:** One worker per module, all dispatched in the same message. Each worker writes only its own `tasks-<module>.md`, following the master phase order and cross-reference conventions, and returns per the return contract.
4. **Consistency pass:** The orchestrator runs `check <spec>`, `trace <spec>`, and `dag <spec>`, then reconciles global numbering, cross-references between module files, and file overlaps across modules; fix conflicts or re-dispatch the offending module.

During Execute, each task worker checks off checkboxes only in its own module file; the orchestrator mirrors overall progress via TodoWrite.

## Template: tasks.md (Small Feature)

```markdown
# Tasks: [Feature Name]

## Overview
[Total task count] tasks in [phase count] phases. Tasks are ordered by dependency.

## Tasks

### Phase 1: [Phase Name]

- [ ] 1. [Task title]
  - Files: `src/[module]/[file-a]`, `src/[module]/[file-b]`
  - [ ] 1.1 [Sub-task with specific instruction]
    - [Implementation detail]
    - _Requirements: [Requirement#.Criteria#]_
  - [ ] 1.2 [Sub-task]
    - _Requirements: [Requirement#.Criteria#]_

- [ ] 2. Checkpoint — Verify [what to verify]
  - Files: (none)
  - Ensure all tests pass; report questions via the return summary.

### Phase 2: [Phase Name]

- [ ] 3. [Task title]
  - Files: `src/[module]/[file-c]`, `tests/[module]/[file-c-test]`
  - [ ] 3.1 Write test for [feature]
    - _Requirements: [Requirement#.Criteria#]_
  - [ ] 3.2 Implement [feature] to satisfy 3.1
    - _Requirements: [Requirement#.Criteria#]_

- [ ] 4. [Task title]
  - Files: `src/[module]/[file-d]`
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
  - Files: `[shared/config paths]`
  - [ ] 1.1 [Sub-task]
  - [ ] 1.2 [Sub-task]

- [ ] 2. Checkpoint — Verify [scaffolding works]
  - Files: (none)
  - Ensure all tests pass; report questions via the return summary.

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
  - Files: `src/[module]/[file-a]`, `src/[module]/[file-b]`
  - [ ] 1.1 [Sub-task]
    - [Implementation detail]
    - _Requirements: [Module] [Requirement#.Criteria#]_
  - [ ] 1.2 [Sub-task]
    - _Requirements: [Module] [Requirement#.Criteria#]_

- [ ] 2. [Task title]
  - Files: `src/[module]/[file-c]`, `tests/[module]/[file-c-test]`
  - [ ] 2.1 Write test for [feature]
    - _Requirements: [Module] [Requirement#.Criteria#]_
  - [ ] 2.2 Implement [feature] to satisfy 2.1
    - _Requirements: [Module] [Requirement#.Criteria#]_

- [ ] 3. Checkpoint — Verify [module] tests pass
  - Files: (none)
  - Ensure all tests pass; report questions via the return summary.
```

## Next Step

→ Return to the orchestrator per the return contract (`files_written`, `key_decisions`, `open_questions`), including task count, phase count, and requirement coverage in the summary.

→ The orchestrator runs `check <spec>` and `trace <spec>` (both must exit 0) and spot-checks the task list, then asks at the gate: "Tasks look good? Ready to start executing, or want to adjust anything?"

→ On approval, proceed to **Execute Mode**

## See Also

[best-practices.md](best-practices.md) — task sequencing guidance by category (TDD, contract-first APIs, migrations, refactoring, etc.), used when deciding how to split and order tasks above.
