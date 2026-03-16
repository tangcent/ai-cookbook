# Execute Mode

## Purpose

Implement tasks one by one from `tasks.md` (or `plan.md`), checking off each task as it completes. This is where code gets written.

## What This Mode Does

1. Read the task list (from `tasks.md`, `tasks-<module>.md`, or `plan.md`)
2. Identify the next unchecked task (`- [ ]`)
3. Implement the task by writing/modifying code
4. Verify the task meets its acceptance criteria
5. Check off the task (`- [x]`)
6. Move to the next task or pause for user input

## Execution Rules

1. **One task at a time.** Complete and verify each task before starting the next.
2. **Check off tasks.** After completing a task, update `- [ ]` → `- [x]` in the task file. Update sub-tasks too.
3. **Verify before checking off.** Check that acceptance criteria are met. Run diagnostics on modified files.
4. **Pause on blockers.** If a task can't be completed (missing info, unexpected complexity, conflict), explain why and ask the user how to proceed.
5. **Respect the spec.** Follow the design decisions in `design.md`. Don't deviate without discussing with the user.
6. **Minimal code.** Write only what's needed to satisfy the task. No gold-plating.
7. **Cross-reference.** When a task references requirements (e.g. `_Requirements: Auth 2.1_`), verify the implementation satisfies those specific acceptance criteria.

## Execution Workflow Per Task

```
1. Read task details (description, files, acceptance criteria, requirement references)
2. Read relevant existing code for context
3. Implement the changes
4. Run diagnostics on modified files
5. Verify acceptance criteria
6. Update task checkbox: - [ ] → - [x] (in tasks.md or tasks-<module>.md)
7. Brief summary to user: "Task [N] done: [what was done]"
8. Ask: "Continue to Task [N+1]?" or auto-continue if user said "execute all"
```

## Checkpoint Tasks

Checkpoint tasks (e.g. "Checkpoint — Verify all tests pass") are verification gates:

1. Run the relevant test suite or build command
2. If everything passes, check off the checkpoint
3. If failures occur, fix them before proceeding
4. Ask the user if any questions arise during the checkpoint

## What to Confirm with User

- **Before starting:** "I'll start with Task [N]: [title]. Ready?"
- **On completion:** "Task [N] done. [Brief summary]. Moving to Task [N+1]?"
- **On blocker:** "Task [N] is blocked because [reason]. How should I proceed?"
- **On deviation:** "The design says [X] but I think [Y] would be better because [reason]. Want to update the design?"
- **Batch mode:** If user says "execute all" or "implement everything", proceed through all tasks with minimal interruption, only pausing on blockers and checkpoints.

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

## Output

No new document is produced. Execute mode modifies:

- **Code files** — as specified in each task
- **tasks.md / tasks-<module>.md / plan.md** — checkbox updates
- **design.md** — only if design changes are agreed upon

## Completion

When all tasks are checked off:

1. Summarize what was built: "All [N] tasks complete. [Feature name] is implemented."
2. Suggest next steps if applicable: "You might want to run the full test suite, or review the changes before committing."
