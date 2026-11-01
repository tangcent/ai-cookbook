# Execute Mode

## Purpose

Implement tasks from `tasks.md` (or `plan.md`), checking off each task as it completes. This is where code gets written.

## Inputs

This mode reads from:

- **Upstream artifacts:** `.spec/{spec_name}/tasks.md` (or `plan.md`), `.spec/{spec_name}/design.md` (for design context)
- **Project codebase:** Files listed in each task, plus any existing dependencies
- **Reference:** [best-practices.md](best-practices.md) — sequencing guidance by task category (TDD, contract-first, migrations, etc.)

> **Important — Read upstream artifacts from disk.** Execute mode is orchestrated by the main session, and task workers run as sub-agents. Both read tasks.md and design.md from disk — never rely on conversation memory. Each task already carries requirement cross-references and file targets; use those for context. Never write spec references into source code.

## Orchestration Model

Execute mode is orchestrated directly by the main session — unlike the other modes, there is no top-level Execute agent. This file is the orchestrator's playbook.

- **Orchestrator (main session):** runs `dag` for the dependency graph, groups parallelizable tasks, dispatches task workers, reconciles after each group, owns checkbox updates (via `done`), runs checkpoint gates, and handles all user interaction
- **Task workers (sub-agents):** implement assigned tasks only. Dispatched via the Agent tool with `subagent_type: "general-purpose"`. They read spec context from disk, touch only listed files, self-verify acceptance criteria, and return a structured summary. Workers never talk to the user and never spawn further sub-agents

## What This Mode Does

1. Read the task list (from `tasks.md`, `tasks-<module>.md`, or `plan.md`) — `status <spec>` gives the current progress and the next incomplete task
2. Get the dependency graph (DAG) and suggested rounds from `dag <spec>`
3. Dispatch task workers — sequentially for dependent chains, in parallel groups for independent tasks
4. Reconcile after each task/group — verify acceptance criteria, run diagnostics
5. Check off completed tasks with `done <spec> <id>` — for a single `tasks.md`, only the orchestrator writes checkboxes
6. Continue until all tasks are done or user pauses

## Task Dependency Graph (DAG)

Before any code is written, the orchestrator needs a dependency graph over the remaining tasks. `dag <spec>` computes it deterministically — file intersections, phase barriers, checkpoint gates, and per-module phase order from the master `Execution Order` table. Run it rather than re-deriving the graph by hand; use `--json` when you need the raw edges.

### Building the DAG

`dag` encodes these dependency rules:

- **File conflicts:** Two tasks that modify the same file are dependent — order matters.
- **Logical dependencies:** Task B needs Task A's output (e.g. "Create User model" must finish before "Add User API").
- **Phase boundaries:** Tasks in later phases depend on earlier phases completing (checkpoints gate progress).

A task is **independent** at a given depth when all its dependencies are already satisfied.

### Identifying Parallelizable Groups

Tasks at the same DAG depth can be parallelized when they touch **disjoint sets of files** (no shared write targets). Parallel execution happens in groups:

```
DAG Example:
  Task 1 (models/user.py)
  Task 2 (services/auth.py)          ← same depth, different files → PARALLEL
      │                │
  Task 3 (api/auth.py, services/auth.py)  ← depends on Task 2
      │
  Task 4 (tests/test_auth.py)             ← depends on Task 3
```

Execution order: Group 1 (Task 1 + Task 2 in parallel) → Task 3 → Task 4.

### Executing the DAG

```
1. Run `dag <spec>` — it lists every unchecked task grouped into rounds and parallel batches
2. For each round:
   a. Single task in the batch → dispatch one task worker (or do it inline if trivial)
   b. Multiple tasks in the batch → dispatch all workers in the same message (one Agent call per task) for true parallelism
3. Wait for all workers in the round to complete
4. Reconcile: check diagnostics across all modified files, verify no conflicts, cross-check worker summaries against acceptance criteria
5. Flip verified tasks with `done <spec> <id>` (single tasks.md: the orchestrator writes them; large spec: `done <module>:<id>`)
6. Re-run `dag <spec>` (completed tasks drop out automatically) and repeat from step 2
7. Continue until all tasks done or a checkpoint/blocker is hit
```

Rounds and batches are a scheduling *suggestion*: `dag` groups by file-disjointness within a round, and it falls back to conservative serial ordering when a task is missing its `Files:` line (or when the spec is a `plan.md`, which has no `Files:` lines at all). Override the grouping when you know better — for example, split a large batch into smaller waves.

If `dag` prints a `BLOCKED` round and exits 1, the task list contains a dependency cycle or an unsatisfiable chain — fix the tasks before dispatching anything.

**Parallel execution is a tool, not a requirement.** If tasks are small or there's only one task at a depth, execute sequentially. Only parallelize when it provides clear value (large independent tasks, disjoint files).

## Execution Rules

0. **Follow test/contract-before-implementation ordering within a task.** If a task pair splits test-vs-implementation or contract-vs-implementation (per [best-practices.md](best-practices.md)), execute in that order: write and run the test/contract first, confirm it fails or is otherwise validated on its own, then implement. If tasks.md wasn't pre-split this way but the work clearly falls into a category best-practices.md covers (bug fix, API, migration, refactor, performance), apply the same ordering anyway even within a single unsplit task.
1. **Get the DAG first.** Run `dag <spec>` before executing any task; don't derive dependencies from memory.
2. **Parallelize when valuable.** Independent tasks touching different files can run in parallel sub-agents. Don't force it for trivial tasks.
3. **One task at a time per worker.** Each task (or small sequential batch) gets its own context. No worker handles overlapping file sets.
4. **Check off tasks with `done`.** After a task is verified, run `done <spec> <id>` (it flips the task and its sub-tasks). For a single `tasks.md`, only the orchestrator writes checkboxes; in large specs each worker checks off only in its own `tasks-<module>.md` via `done <module>:<id>`. Never hand-edit `- [ ]` markers.
5. **Verify before checking off.** Check that acceptance criteria are met. Run diagnostics on modified files.
6. **Pause on blockers.** If a task can't be completed (missing info, unexpected complexity, conflict), the worker returns a `blocked` flag with the reason. The orchestrator continues independent branches and escalates the blocked task to the user.
7. **Respect the spec.** Follow the design decisions in `design.md`. Don't deviate without discussing with the user.
8. **Minimal code.** Write only what's needed to satisfy the task. No gold-plating.
9. **No spec references in source code.** Never write references to spec documents (`requirements.md`, `design.md`, `tasks.md`, `plan.md`, `.spec/`, etc.) into source code, code comments, or documentation strings. Spec artifacts are planning tools — they have no place in production code. Code should stand on its own with self-documenting names and normal comments.
10. **Cross-reference requirements.** When a task references requirements (e.g. `_Requirements: Auth 2.1_`), verify the implementation satisfies those specific acceptance criteria — but do not copy the requirement reference into the code.
11. **Workers stay in their lane.** A task worker only modifies files listed in its assigned tasks, never talks to the user, and never spawns further sub-agents.

## Worker Execution Per Task

What each task worker does for its assigned task(s):

```
1. Read task details (description, files, acceptance criteria, requirement references) from the task file on disk
2. Read relevant existing code for context
3. Implement the changes — only files listed in the task
4. Run diagnostics on modified files
5. Verify acceptance criteria
6. Large specs only: check off the task in its own tasks-<module>.md with `done <module>:<id>` (never the shared master)
7. Return summary: files changed, verification results, issues (blocked / design_conflict flags where applicable)
```

The orchestrator then verifies the report, flips the checkbox with `done <spec> <id>` (single tasks.md), and informs the user: "Task [N] done: [what was done]".

## Parallel Execution Via Task Workers

When independent tasks can run in parallel:

```
1. Identify the parallel group (same DAG depth, disjoint file sets)
2. Dispatch one worker per task (or per small batch of sequential tasks) — all Agent calls in the same message
3. Each worker:
   - Reads the task file and relevant design docs from disk (not from conversation)
   - Implements its assigned task(s), touching only listed files
   - Verifies acceptance criteria
   - Large specs only: checks off its task(s) in its own tasks-<module>.md with `done <module>:<id>` (never the shared master)
4. Wait for all workers to complete
5. Reconcile: run diagnostics across all modified files, verify no cross-task conflicts
6. Orchestrator flips checkboxes with `done` (single tasks.md) and reports consolidated summary to user
```

### Task Worker Prompt Template

```
Agent tool:
  subagent_type: "general-purpose"
  description: "Task [N] for {spec_name}"

  prompt:
    Implement the following task(s) from the spec-driven skill.

    ## Task(s) to Implement
    {task_details — description, files, acceptance criteria}

    ## Spec
    - spec_name: {spec_name}
    - Workspace root: {workspace_root}
    - Read .spec/{spec_name}/tasks.md and .spec/{spec_name}/design.md from disk

    ## Handoff (confirmed context — do not re-ask)
    {confirmed decisions / resolved Q&A relevant to this task}

    ## Worker Contract
    - Only modify files explicitly listed in these tasks
    - Read all spec context from disk, not from assumptions
    - Verify acceptance criteria before reporting done
    - Never reference spec documents (.spec/, requirements.md, design.md, etc.) in source code
    - Checkbox updates: {single tasks.md: do NOT edit tasks.md — report completion only |
      large spec: run `done <spec> <module>:<id>` on your own tasks-<module>.md}
    - Never interact with the user; never spawn further sub-agents

    ## Return Contract
    Return: files_changed, tasks_completed, verification_results (diagnostics/tests run),
    issues — each flagged as `blocked` (can't proceed, why) or
    `design_conflict` (design.md is wrong/insufficient, why) where applicable
```

### When NOT to Parallelize

- Tasks are trivial (each <2 minutes of work) — overhead of spawning agents outweighs benefit
- Tasks share files even if logically different — file conflicts create merge issues
- A checkpoint must pass before moving to the next group of tasks
- User explicitly requested sequential execution

## Checkpoint Tasks

Checkpoint tasks (e.g. "Checkpoint — Verify all tests pass") are verification gates run by the orchestrator between groups:

1. Run the relevant test suite or build command (inline, or delegated to a single worker)
2. If everything passes, check off the checkpoint with `done <spec> <id>`
3. If failures occur, dispatch a fix worker with the failure details before proceeding
4. Ask the user if any questions arise during the checkpoint

## What to Confirm with User

- **Before starting:** "I built a DAG from the tasks. [N] tasks in [M] parallelizable groups. Start with group 1: [task titles]?"
- **On completion:** "Task [N] done. [Brief summary]. Moving to Task [N+1]?"
- **On parallel group completion:** "Group [G] done: [summary of all tasks in group]. Moving to group [G+1]?"
- **On blocker:** "Task [N] is blocked because [reason]. How should I proceed?"
- **On deviation:** "The design says [X] but I think [Y] would be better because [reason]. Want to update the design?"
- **Batch mode:** If user says "execute all" or "implement everything", proceed through all tasks/groups with minimal interruption, only pausing on blockers and checkpoints.

## Handling Issues During Execution

### Acceptance Criteria Not Met
- Re-examine the implementation
- Fix issues before checking off
- If criteria are unrealistic, discuss with user and update the task file

### Unexpected Complexity
- If a task is much larger than expected, propose splitting it
- Add new sub-tasks to the task file
- Get user confirmation before proceeding

### Design Conflicts
- If a worker returns a `design_conflict` flag (or the orchestrator spots one), pause execution
- Present the conflict and options to the user; the user decides
- Re-dispatch Design mode targeted at the affected section to update `design.md`
- Update the affected tasks (Tasks mode, targeted) before resuming execution

### Test Failures
- Fix the code, not the test (unless the test is wrong)
- If fixing requires changes beyond the current task scope, note it and discuss

### Blocked Workers
- A worker returns `blocked` with a reason → the orchestrator continues independent DAG branches
- Escalate to the user with context; once resolved, re-dispatch the task statelessly with the answer in the handoff block

### File Conflicts After Parallel Execution
- If two parallel workers modified the same file (shouldn't happen with disjoint groups, but...) — manually merge
- Run diagnostics on all modified files
- If conflicts are unresolvable, report to user

## Output

No new document is produced. Execute mode modifies:

- **Code files** — as specified in each task
- **tasks.md / tasks-<module>.md / plan.md** — checkbox updates
- **design.md** — only if design changes are agreed upon

## Completion

When all tasks are checked off:

1. Summarize what was built: "All [N] tasks complete. [Feature name] is implemented."
2. Suggest next steps if applicable: "You might want to run the full test suite, or review the changes before committing."
