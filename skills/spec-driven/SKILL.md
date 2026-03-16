---
name: spec-driven
description: "Spec-driven development workflow. ACTIVATE THIS SKILL broadly — whenever the user's message contains keywords like 'requirements', 'plan', 'spec', 'design', 'tasks', 'feature', 'build', 'implement', 'architecture', '需求', '计划', '设计', '任务', '功能', '实现', or any topic that may benefit from structured development. Err on the side of activating. After activation, the skill itself will analyze intent and decide the appropriate action."
---

# Spec-Driven Development Skill

## When to Activate

**Activate this skill broadly.** If the user's message touches on ANY of the following, activate first, analyze later:

- Contains keywords: "requirements", "plan", "spec", "design", "tasks", "feature", "build", "implement", "architecture", "verify", "compare", "migrate", "refactor"
- Contains Chinese keywords: "需求", "计划", "设计", "任务", "功能", "实现", "重构", "迁移", "对比"
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

This skill provides two structured flows for turning ideas into working code:

1. **Spec Flow:** Requirements → Design → Tasks → Execute
2. **Plan Flow:** Plan → Execute

Users can enter at any step. If they say "design X", start from Design. If they say "plan X", use the Plan flow. If they say "build X" without context, start from Requirements.

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

## Flow 1: Spec Flow

### Step 1 — Requirements

Reference: [requirements-mode.md](references/requirements-mode.md)

Gather and formalize what needs to be built. Output: `requirements.md` (+ sub-files for large specs)

### Step 2 — Design

Reference: [design-mode.md](references/design-mode.md)

Define how it will be built technically. Output: `design.md` (+ sub-files for large specs)

### Step 3 — Tasks

Reference: [tasks-mode.md](references/tasks-mode.md)

Break the design into actionable implementation tasks. Output: `tasks.md` (+ sub-files for large specs)

### Step 4 — Execute

Reference: [execute-mode.md](references/execute-mode.md)

Implement tasks one by one, updating status as you go.

## Flow 2: Plan Flow

### Step 1 — Plan

Reference: [plan-mode.md](references/plan-mode.md)

Create a combined requirements + task breakdown in one pass. Output: `plan.md`

### Step 2 — Execute

Reference: [execute-mode.md](references/execute-mode.md)

Implement tasks from the plan one by one.

## Navigation Between Modes

- After completing any mode, summarize the output and ask: "Ready to move to [next mode]? Or would you like to revise?"
- Users can jump back to any previous mode to revise (e.g. "let's update the requirements")
- Users can skip modes (e.g. "skip design, go straight to tasks")
- If executing without prior artifacts, ask: "I don't see a spec for this. Want to start from requirements, or should I create a quick plan?"

### Context Compaction at Mode Transitions

When transitioning from one mode to the next, perform a context compaction to keep the conversation lean:

1. **Save everything to disk first.** All artifacts from the current mode must be written to `.spec/<spec-name>/` before transitioning. The files on disk are the source of truth, not the conversation history.

2. **Produce a transition summary.** At the end of each mode, output a compact summary block like:

   ```
   --- Mode Complete: [Requirements/Design/Tasks/Plan] ---
   Spec: <spec-name>
   Key decisions: <2-5 bullet points of the most important decisions made>
   Artifacts written: <list of files written/updated>
   Open questions: <any unresolved items, or "none">
   Next mode: <suggested next mode>
   ---
   ```

3. **When entering the next mode, read from disk — not from conversation memory.** Start the new mode by reading the relevant artifact files from `.spec/<spec-name>/`. Do not rely on what was discussed earlier in the conversation. This ensures the AI works from the canonical, complete artifacts rather than a potentially truncated or lossy conversation context.

4. **Drop intermediate details.** The conversation may have included back-and-forth discussion, rejected alternatives, and exploratory analysis during the previous mode. These do NOT need to be carried forward. Only the final artifacts and the transition summary matter.

This approach works universally across all AI tools — it doesn't depend on any native "compact" or "summarize" feature. By anchoring each mode to files on disk and keeping only a short transition summary in conversation, the context stays focused regardless of how long the overall spec process runs.

## Resuming Work

When the user returns to continue work on an existing spec:

1. Check `.spec/` for existing artifacts
2. Read the latest artifacts to understand current state
3. If `tasks.md` exists, check task statuses (checkbox `[x]` vs `[ ]`) and resume from the first incomplete task
4. Inform the user: "Found existing spec for [name]. [N] of [M] tasks completed. Continuing from task [next]."

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
- At every mode transition, perform context compaction: write artifacts to disk, output a transition summary, and start the next mode by reading from disk — not from conversation memory
