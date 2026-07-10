# Execute Mode

## Purpose

Implement tasks from `tasks.md` (or `plan.md`), checking off each task as it completes. This is where code gets written.

## Inputs

This mode reads from:

- **Upstream artifacts:** `.spec/{spec_name}/tasks.md` (or `plan.md`), `.spec/{spec_name}/design.md` (for design context)
- **Project codebase:** Files listed in each task, plus any existing dependencies
- **Reference:** [best-practices.md](best-practices.md) — sequencing guidance by task category (TDD, contract-first, migrations, etc.)

> **Important — Read upstream artifacts from disk.** Execute mode runs in its own sub-agent. Always read tasks.md and design.md from disk — do not rely on conversation memory. Each task already carries requirement cross-references and file targets; use those for context. Never write spec references into source code.

## What This Mode Does

1. Read the task list (from `tasks.md`, `tasks-<module>.md`, or `plan.md`)
2. Build a dependency graph (DAG) of all tasks to identify parallelization opportunities
3. Execute tasks — sequentially for dependent chains, in parallel for independent tasks
4. Verify each task meets its acceptance criteria
5. Check off completed tasks (`- [x]`)
6. Continue until all tasks are done or user pauses

## Task Dependency Graph (DAG)

Before writing any code, always analyze the full task list to build a dependency graph. This determines execution order and identifies tasks that can run in parallel via sub-agents.

### Building the DAG

For each task, determine what it depends on:

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
1. Build DAG from all unchecked tasks in tasks.md
2. Identify top-level (depth 0) independent tasks
3. Group by file-disjointness → groups of parallelizable tasks
4. For each group:
   a. Single task → execute in current session
   b. Multiple tasks → spawn sub-agents (one per task or small batch)
5. Wait for all agents in the group to complete
6. Reconcile: check diagnostics across all modified files, verify no conflicts
7. Rebuild DAG (some tasks may now be at depth 0), repeat from step 2
8. Continue until all tasks done or a checkpoint/blocker is hit
```

**Parallel execution is a tool, not a requirement.** If tasks are small or there's only one task at a depth, execute sequentially. Only parallelize when it provides clear value (large independent tasks, disjoint files).

## Execution Rules

0. **Follow test/contract-before-implementation ordering within a task.** If a task pair splits test-vs-implementation or contract-vs-implementation (per [best-practices.md](best-practices.md)), execute in that order: write and run the test/contract first, confirm it fails or is otherwise validated on its own, then implement. If tasks.md wasn't pre-split this way but the work clearly falls into a category best-practices.md covers (bug fix, API, migration, refactor, performance), apply the same ordering anyway even within a single unsplit task.
1. **Build DAG first.** Analyze all unchecked tasks for dependencies before executing any of them.
2. **Parallelize when valuable.** Independent tasks touching different files can run in parallel sub-agents. Don't force it for trivial tasks.
3. **One task at a time per agent.** Each task (or small sequential batch) gets its own context. No agent handles overlapping file sets.
4. **Check off tasks.** After completing a task, update `- [ ]` → `- [x]` in the task file. Update sub-tasks too.
5. **Verify before checking off.** Check that acceptance criteria are met. Run diagnostics on modified files.
6. **Pause on blockers.** If a task can't be completed (missing info, unexpected complexity, conflict), explain why and ask the user how to proceed.
7. **Respect the spec.** Follow the design decisions in `design.md`. Don't deviate without discussing with the user.
8. **Minimal code.** Write only what's needed to satisfy the task. No gold-plating.
9. **No spec references in source code.** Never write references to spec documents (`requirements.md`, `design.md`, `tasks.md`, `plan.md`, `.spec/`, etc.) into source code, code comments, or documentation strings. Spec artifacts are planning tools — they have no place in production code. Code should stand on its own with self-documenting names and normal comments.
10. **Cross-reference requirements.** When a task references requirements (e.g. `_Requirements: Auth 2.1_`), verify the implementation satisfies those specific acceptance criteria — but do not copy the requirement reference into the code.

## Sequential Execution Per Task

When executing tasks one at a time (single agent, single task):

```
1. Read task details (description, files, acceptance criteria, requirement references)
2. Read relevant existing code for context
3. Implement the changes
4. Run diagnostics on modified files
5. Verify acceptance criteria
6. Update task checkbox: - [ ] → - [x] (in tasks.md or tasks-<module>.md)
7. Brief summary to user: "Task [N] done: [what was done]"
8. Continue to next task or pause for user input
```

## Parallel Execution Via Sub-Agents

When independent tasks can run in parallel:

```
1. Identify the parallel group (same DAG depth, disjoint file sets)
2. Spawn one sub-agent per task (or per small batch of sequential tasks)
3. Each sub-agent:
   - Reads the task file and relevant design docs from disk (not from conversation)
   - Implements its assigned task(s)
   - Verifies acceptance criteria
   - Checks off its task(s) in tasks.md
4. Wait for all sub-agents to complete
5. Reconcile: run diagnostics across all modified files, verify no cross-task conflicts
6. Report consolidated summary to user
```

### Sub-Agent Prompt Template

```
Implement the following task(s). Read the task file, design docs, and existing code from disk as needed.

## Task(s) to Implement
{task_details — description, files, acceptance criteria}

## Spec Name
{spec_name} — read .spec/{spec_name}/tasks.md and .spec/{spec_name}/design.md from disk

## Rules
- Only modify files explicitly listed in these tasks
- Never reference spec documents (.spec/, requirements.md, design.md, etc.) in source code
- Verify acceptance criteria before marking tasks done
- Update checkbox status in tasks.md when each task completes
- Return a summary of what was changed and which tasks were completed
```

### When NOT to Parallelize

- Tasks are trivial (each <2 minutes of work) — overhead of spawning agents outweighs benefit
- Tasks share files even if logically different — file conflicts create merge issues
- A checkpoint must pass before moving to the next group of tasks
- User explicitly requested sequential execution

## Checkpoint Tasks

Checkpoint tasks (e.g. "Checkpoint — Verify all tests pass") are verification gates:

1. Run the relevant test suite or build command
2. If everything passes, check off the checkpoint
3. If failures occur, fix them before proceeding
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
- If implementation reveals a design flaw, pause
- Explain the issue and propose alternatives
- Update `design.md` if the design changes
- Adjust remaining tasks if needed

### Test Failures
- Fix the code, not the test (unless the test is wrong)
- If fixing requires changes beyond the current task scope, note it and discuss

### File Conflicts After Parallel Execution
- If two parallel agents modified the same file (shouldn't happen with disjoint groups, but...) — manually merge
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
