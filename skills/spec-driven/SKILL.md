---
name: spec-driven
description: "Spec-driven development workflow. ACTIVATE THIS SKILL broadly — whenever the user's message contains keywords like 'requirements', 'plan', 'spec', 'design', 'tasks', 'feature', 'build', 'implement', 'architecture', '需求', '计划', '设计', '任务', '功能', '实现', or any topic that may benefit from structured development. Err on the side of activating. After activation, the skill itself will analyze intent and decide the appropriate action."
---

# Spec-Driven Development Skill

## When to Activate

**Activate this skill broadly.** If the user's message touches on ANY of the following, activate first, analyze later:

- Contains keywords: "requirements", "plan", "spec", "design", "tasks", "feature", "build", "implement", "architecture", "verify", "compare", "migrate", "refactor", "review", "audit"
- Contains Chinese keywords: "需求", "计划", "设计", "任务", "功能", "实现", "重构", "迁移", "对比", "审查", "评审"
- Uses a keyword as a prefix/label (e.g. "requirements: ...", "design: ...", "plan: ...")
- Describes building, verifying, comparing, or analyzing a feature or system
- Involves work that could benefit from structured planning — even if the user didn't explicitly ask for it

**Principle: activate tolerantly, then analyze deeply.** It's better to activate and discover the skill isn't needed than to miss a case where it is.

## Post-Activation Intent Analysis

After this skill is activated, do NOT immediately jump into a mode. First, analyze the user's actual intent:

### Step 1: Classify the intent

Read the user's message carefully and classify it into one of these categories:

| Category | Signal | Action |
|---|---|---|
| **Explicit mode request** | Message starts with a mode keyword as prefix/label (e.g. "requirements: ...", "design: ...", "plan: ...") | Enter that mode directly. The content after the prefix is the subject. |
| **Clear structured-work intent** | User clearly wants to spec, plan, design, or build something step by step | Enter the appropriate mode per the Mode Detection table below. |
| **Ambiguous — could benefit from structure** | Message involves complex work (verify, compare, migrate, refactor) that might benefit from structured analysis, but the user didn't explicitly ask for it | **Ask the user.** Briefly explain what this skill offers and suggest a mode. E.g. "This sounds like it could benefit from a structured requirements analysis. Want me to enter Requirements mode to break this down systematically, or would you prefer I just tackle it directly?" |
| **Not a fit** | After analysis, the task is simple/direct and doesn't need structured workflow | Proceed without entering any mode. Just do the task normally. |

### Step 2: Act on classification

- For **explicit** and **clear** intents → enter the mode, no need to ask.
- For **ambiguous** intents → ask the user to confirm before entering a mode. Keep the question short and actionable. Suggest the mode you think fits best.
- For **not a fit** → just do the work. Don't force structure where it's not needed.

### Examples

| User says | Classification | Action |
|---|---|---|
| "requirements: verify easy-api implements all features from easy-yapi" | Explicit mode request | Enter Requirements mode, subject = feature parity verification |
| "let's spec out the auth module" | Clear structured-work intent | Enter Requirements mode |
| "compare the API endpoints between v1 and v2" | Ambiguous | Ask: "Want me to do a structured requirements analysis of the differences, or just do a quick comparison?" |
| "fix the typo in README" | Not a fit | Just fix it, no structured flow needed |

## Core Concepts

This skill provides two structured flows for turning ideas into working code, plus a review capability that spans both:

1. **Spec Flow:** Requirements → Design → Tasks → Execute
2. **Plan Flow:** Plan → Execute
3. **Review Mode:** an audit pass over existing artifacts — usable at any point, especially when resuming a spec in a session that didn't create it

Both flows lean on [best-practices.md](references/best-practices.md) when breaking work into tasks and executing it — e.g. test-first for most coding tasks, contract-first for APIs and interfaces.

Users can enter at any step. If they say "design X", start from Design. If they say "plan X", use the Plan flow. If they say "build X" without context, start from Requirements. If they say "review X" or are resuming a spec cold (see "Resuming Work" below), use Review Mode first.

## Mode Detection

Detect the appropriate starting mode from the user's prompt:

| User Intent | Starting Mode | Flow |
|---|---|---|
| "requirements", "requirements: ...", "spec", "what do we need", "需求" | Requirements | Spec |
| "design", "design: ...", "architecture", "how should we build", "设计" | Design | Spec |
| "tasks", "tasks: ...", "break down", "what are the steps", "任务" | Tasks | Spec |
| "plan", "plan: ...", "roadmap", "outline the work", "计划" | Plan | Plan |
| "execute", "implement", "build", "let's do it", "实现" | Execute | (either) |
| "build X from scratch", "create X" (vague) | Requirements | Spec |
| "review", "review: ...", "audit the spec", "does this still hold up", "审查", "评审" | Review | (either) |

This table applies only after intent has been classified as "explicit" or "clear" in the Post-Activation Intent Analysis step above.

## Output Location

All spec artifacts are saved to `.spec/<spec-name>/` directory in the project root:

```
.spec/<spec-name>/
├── requirements.md                    # Master requirements (with module index for large specs)
├── requirements-<module>.md           # Per-module requirements (large specs only)
├── design.md                          # Master design (with module index for large specs)
├── design-<module>.md                 # Per-module design (large specs only)
├── tasks.md                           # Master task list (with phase ordering and module index)
├── tasks-<module>.md                  # Per-module tasks (large specs only)
└── plan.md                            # Combined plan (Plan flow only)
```

Use a kebab-case name derived from the feature description (e.g. `user-authentication`, `payment-integration`).

### Scaling Strategy

- **Small features** (≤5 requirements): Keep everything in single files (`requirements.md`, `design.md`, `tasks.md`)
- **Large features** (>5 requirements or multiple modules): Split into master index + per-module sub-files
  - Master files serve as index documents linking to sub-files
  - Sub-files follow the naming pattern: `<type>-<module>.md` (e.g. `requirements-auth.md`, `design-auth.md`, `tasks-auth.md`)
  - Sub-files use relative links to reference each other (e.g. `[requirements-auth.md](requirements-auth.md)`)

## Agent-Based Execution

Each mode runs in a **sub-agent** spawned via the `Task` tool (`subagent_type: "general_purpose_task"`). The sub-agent reads input files from disk, writes output artifacts, and returns a summary. The main session stays lean — it only holds the spec name, current phase, and transition summaries.

### Why Sub-Agents

- **Context isolation:** Each mode's work (code exploration, design discussion, implementation) stays in the sub-agent's context and is released when done.
- **Clean boundaries:** Each mode's reference file already defines its inputs (what to read) and outputs (what to write). The sub-agent follows those instructions exactly.
- **Main session stays small:** ~500-1000 tokens regardless of how many modes have run.

### How to Spawn a Mode Agent

For each mode, spawn a sub-agent with this structure:

```
Task tool:
  subagent_type: "general_purpose_task"
  description: "[Requirements/Design/Tasks/Plan/Execute] mode for {spec_name}"

  query:
    Run the [mode name] from the spec-driven skill.

    ## Spec
    - spec_name: {spec_name}
    - Project root: {workspace_root}

    ## Instructions
    1. Read the full mode instructions from:
       {absolute_path_to_reference_file}
       (e.g. .../references/requirements-mode.md)
    2. Read any existing upstream artifacts from .spec/{spec_name}/
    3. Follow the mode instructions to produce output artifact(s)
    4. Return a summary with:
       - What was produced (files written)
       - Key decisions made
       - Open questions (if any)
       - Suggested next mode

    ## User Input
    {user_original_request_or_context}
```

### Spec Flow

**Step 1 — Requirements Agent**
Reference: [requirements-mode.md](references/requirements-mode.md)
Inputs: user request, project codebase
Outputs: `.spec/{spec_name}/requirements.md` (+ sub-files)

**Step 2 — Design Agent**
Reference: [design-mode.md](references/design-mode.md)
Inputs: `.spec/{spec_name}/requirements.md` + codebase
Outputs: `.spec/{spec_name}/design.md` (+ sub-files)

**Step 3 — Tasks Agent**
Reference: [tasks-mode.md](references/tasks-mode.md)
Inputs: `.spec/{spec_name}/requirements.md`, `.spec/{spec_name}/design.md`
Outputs: `.spec/{spec_name}/tasks.md` (+ sub-files)

**Step 4 — Execute**
Reference: [execute-mode.md](references/execute-mode.md)
Inputs: `.spec/{spec_name}/tasks.md`, `.spec/{spec_name}/design.md`
Outputs: code changes + checkbox updates in tasks.md

### Plan Flow

**Step 1 — Plan Agent**
Reference: [plan-mode.md](references/plan-mode.md)
Inputs: user request, project codebase
Outputs: `.spec/{spec_name}/plan.md`

**Step 2 — Execute**
Reference: [execute-mode.md](references/execute-mode.md)
Inputs: `.spec/{spec_name}/plan.md`
Outputs: code changes + checkbox updates in plan.md

### Review Mode (Cross-Cutting)

**Reference:** [review-mode.md](references/review-mode.md)
Inputs: all existing `.spec/{spec_name}/` artifacts, current codebase
Outputs: a review report (findings + recommendations), not persisted unless the user asks for it

Review Mode doesn't belong to a fixed position in either flow — it can run before Design, before Tasks, before Execute, or on its own as a health check. Its most important use case is auditing a spec that was created in a *different session*, where the current thread has no memory of the decisions behind it (see "Resuming Work" below).

### Best Practices (Cross-Cutting)

**Reference:** [best-practices.md](references/best-practices.md)
Consulted by: Tasks Mode and Plan Mode (when splitting work into tasks), Execute Mode (when deciding what to build first within a task)

Covers task-sequencing defaults by category: TDD for general coding tasks, contract-first for APIs/interfaces, regression-test-first for bug fixes, migration-first for schema changes, characterization-tests for refactors, and benchmark-first for performance work. Not a mode with its own artifact — it's a lens the other modes apply.

### Orchestrator Responsibilities (Main Session)

The main session acts as orchestrator:

1. **Intent analysis** — classify intent, pick flow and starting mode
2. **Spawn sub-agent** — construct the spawn prompt (spec name, reference file path, user input)
3. **Handle clarifications** — if a sub-agent returns questions, present them to the user and re-spawn with answers
4. **Review summary** — check the sub-agent's returned summary for completeness
5. **User confirmation** — before moving to the next mode, ask: "Ready to move to [next mode]?"
6. **Navigation** — users can jump back to any mode to revise, or skip modes

### Navigation Between Modes

- After a sub-agent completes, the orchestrator presents the summary and asks: "Ready to move to [next mode]?"
- Users can jump back to any previous mode to revise (e.g. "let's update the requirements") — re-spawn that mode's agent
- Users can skip modes (e.g. "skip design, go straight to tasks")
- If executing without prior artifacts, ask: "I don't see a spec for this. Want to start from requirements, or should I create a quick plan?"

### Transition Summary Format

After each sub-agent completes, the orchestrator produces:

```
--- Mode Complete: [Requirements/Design/Tasks/Plan] ---
Spec: <spec-name>
Key decisions: <2-5 bullet points>
Artifacts written: <files>
Open questions: <any, or "none">
Next mode: <suggested>
---
```

## Resuming Work

When the user returns to continue work on an existing spec, first determine whether this is a **same-session continuation** or a **cold start** (new thread/session with no memory of the spec's creation — e.g. a fresh conversation, or an earlier session's summary was compacted away). This distinction matters because a cold-start session cannot rely on decisions it never actually saw — it can only trust what's written to disk.

### Same-Session Continuation

If this conversation created or already reviewed the artifacts:

1. Check `.spec/` for existing artifacts
2. Read the latest artifacts to understand current state
3. If `tasks.md` exists, check task statuses (checkbox `[x]` vs `[ ]`) and resume from the first incomplete task
4. Inform the user: "Found existing spec for [name]. [N] of [M] tasks completed. Continuing from task [next]."

### Cold Start (New Thread, Existing Spec)

If `.spec/<name>/` already has artifacts but nothing in the current conversation shows them being created or discussed:

1. **Don't resume blindly.** Checkbox state and prior "confirmations" from another session aren't verifiable from here — treat them as claims to be checked, not facts.
2. Offer Review Mode before resuming: "This spec looks like it was built in an earlier session. Want me to review it for consistency before continuing, or just resume from the task list as-is?"
3. If the user wants to just resume — proceed as in Same-Session Continuation, but flag it: "Resuming without review — task checkboxes are being trusted as-is."
4. If the user wants a review (or doesn't respond with a strong preference) — run **Review Mode** ([review-mode.md](references/review-mode.md)) first:
   - Load all artifacts fully from disk
   - Check traceability (requirements ↔ design ↔ tasks)
   - Check currency (do referenced files/APIs/models still exist and match?)
   - Spot-check completed tasks against actual code, not just the checkbox
   - Report findings and recommended fixes
5. Only after review (or explicit user opt-out) proceed to Execute Mode or whichever mode the user needs next.

## Hard Rules

- Always save artifacts to `.spec/<spec-name>/` — never lose work
- Always ask for user confirmation before moving to the next mode
- Never skip user confirmation on requirements or design decisions
- Keep artifacts updated — when executing, update task checkboxes in `tasks.md`
- Reference existing code and project structure when generating design and tasks
- Each task in `tasks.md` must be small enough to implement in a single focused session
- Use EARS-style requirement language (WHEN/WHERE/THE system SHALL) for formal requirements
- Use checkbox format (`- [ ]` / `- [x]`) for task tracking — this enables progress scanning
- Cross-reference between documents: tasks reference requirements, design references requirements
- Each mode runs in its own sub-agent — spawn via the Task tool, not inline
- Sub-agents read from disk and write to disk; the main session only keeps spec name and transition summaries
- Never trust prior "confirmations" or checkbox state on a spec this session didn't create — verify against disk and code before resuming or building on it (see Resuming Work → Cold Start)
- Review Mode reports and recommends only — it never edits artifacts or code directly; fixes go through the relevant mode
- Default to test-first for coding tasks and contract-first for API/interface tasks (see [best-practices.md](references/best-practices.md)) — skip only for trivial or explicitly throwaway work, and say so when skipping
