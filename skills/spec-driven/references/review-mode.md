# Review Mode

## Purpose

Audit existing spec artifacts for completeness, internal consistency, and alignment with the current codebase. This mode exists specifically for the **cold-start case**: a new thread/session that has no memory of how the spec was built, and needs to verify the spec is trustworthy before continuing execution or making further decisions based on it.

Review Mode is read-oriented and does not write code. It produces a report and recommends (or triggers) targeted fixes via the other modes.

## When This Mode Triggers

- **Explicit:** "review the spec", "review-mode: ...", "audit the plan", "check the spec for X", "does this spec still make sense", "revisit the design/tasks"
- **Implicit (new-thread heuristic):** the user asks to "continue", "pick this up", or discusses a feature that already has `.spec/<name>/` artifacts, but nothing in the current conversation history shows those artifacts being created or discussed. Treat this as a signal that you're in a fresh thread relative to that spec. Offer review as an option before just resuming: "This spec looks like it was built in an earlier session — want me to review it for consistency before continuing, or just resume from the task list?"

Review Mode is orthogonal to the Spec/Plan flows — it can be invoked at any point, on any subset of existing artifacts, and doesn't require re-running Requirements → Design → Tasks in order.

## Core Principle: Assume Nothing From Memory

Because a new thread has zero memory of prior decisions, treat every review as if you've never seen this spec before — even if earlier turns in *this* conversation touched it. Never reason from a summary or from what "seems likely" — reload the actual files.

## What This Mode Does

1. **Discover** — scan `.spec/` for existing spec directories. If the target spec isn't obvious from the user's message, list what was found and ask which one.
2. **Load fully from disk** — read `requirements.md`, `design.md`, `tasks.md`/`plan.md` and all sub-files in full. Do not infer content from filenames, headers alone, or partial reads.
3. **Inventory** — note which artifacts exist, which are missing entirely, and which are partially filled (e.g. `design.md` still has unresolved items in "Open Questions", or a module in the index has no sub-file yet).
4. **Cross-check traceability**:
   - Every task cites a requirement/design reference — flag orphan tasks (cite nothing, or cite something that doesn't exist)
   - Every requirement has corresponding design coverage — flag requirements with no design section addressing them
   - Every design decision is compatible with the requirements — flag contradictions (e.g. design proposes something requirements marked "Out of Scope")
5. **Check currency against the codebase** — for each file, API, model, or convention referenced in `design.md`/`tasks.md`, verify it still exists and still matches the description. Code may have moved on since the spec was written (refactors, renames, deleted modules).
6. **Check execution progress** — read checkbox state in `tasks.md`. For tasks marked `[x]`, spot-check the actual code to confirm the implementation matches what the task described — don't trust the checkbox alone.
7. **Surface findings** — group into: Gaps, Inconsistencies, Stale References, Progress Mismatches.
8. **Recommend next action** — don't just report. Propose the smallest fix path for each finding (re-spawn Requirements/Design/Tasks mode scoped to the specific issue, not a full regeneration).

## Inputs

- `.spec/<spec-name>/` — all artifacts and sub-files (requirements, design, tasks/plan)
- Current project codebase — to verify currency of referenced files/APIs/models
- Git log since the spec files' last modification (optional) — a quick way to spot what may have drifted

## What NOT to Do

- Don't rewrite artifacts during review — Review Mode reports and recommends; fixes happen via a follow-up call to the relevant mode.
- Don't skip loading a file because "it was probably fine" — every artifact gets read in full.
- Don't assume task checkboxes are accurate without spot-checking the code for at least the most recently checked-off tasks.

## Output: Review Report

Review Mode produces a report. It is **not saved to disk by default** — only persist it (as `.spec/<spec-name>/review.md`) if the user asks for a record.

```markdown
## Spec Review: <spec-name>

### Artifacts Found
- [x] requirements.md (+2 sub-files)
- [x] design.md
- [ ] tasks.md — MISSING

### Traceability
- Requirement 3 ("...") has no corresponding design section — GAP
- Task 7 references Requirement 9, which does not exist — ORPHAN

### Currency
- design.md references `services/PaymentGateway.ts`, removed in a later refactor — STALE
- All other referenced files still exist and match their descriptions

### Progress (tasks.md)
- 6 of 10 tasks checked off
- Task 4 marked done, but the code shows only partial implementation — MISMATCH

### Recommendation
1. Regenerate the design section covering Requirement 3
2. Fix Task 7's requirement reference, or add the missing requirement
3. Update design.md's file reference for the removed PaymentGateway
4. Re-verify Task 4's implementation and correct its checkbox status
```

## What to Confirm with User

- "Found [N] issues. Want me to fix them now, or did you just want a status report?"
- If fixing: "I'll re-run [Requirements/Design/Tasks] mode scoped to [specific issue]. OK?"
- If a progress mismatch is found: "Task [N] looks incomplete — want me to finish it, or just correct the checkbox?"
- If the spec is clean: "Everything checks out — [N] tasks done, traceability is intact, no stale references. Want to continue execution?"

## Next Step

- If issues were found and the user wants fixes → re-spawn the specific mode agent(s) needed (Requirements, Design, or Tasks), scoped to just the flagged issue — not a full re-do of that mode
- If everything checks out → hand off to **Execute Mode** to continue from the next incomplete task
- If the user only wanted a health check → just report; make no changes
