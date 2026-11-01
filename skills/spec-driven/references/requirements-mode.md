# Requirements Mode

## Purpose

Transform a vague idea or feature request into a clear, structured set of requirements that everyone agrees on before any code is written.

## What This Mode Does

1. Understand the user's goal and context
2. Identify gaps that need clarification — return them as `open_questions` (see Interaction Protocol); never ask the user directly
3. Survey the existing codebase for relevant code, patterns, and constraints
4. Identify functional and non-functional requirements
5. Define acceptance criteria using EARS-style language
6. Identify edge cases, constraints, and assumptions
7. Produce a formal requirements document (with sub-files for large specs)

## Inputs

This mode reads from:

- **User request:** The original goal, problem statement, or feature description
- **Project codebase:** Existing code, patterns, conventions, tech stack (explore via Glob/Grep/Read)

> **Important — Preserve original references.** Record any URLs, external documentation, referenced files, or key code locations consulted during analysis in the output artifact. Downstream modes (Design, Tasks, Execute) run in separate sub-agents and will NOT have access to the original conversation. The artifact must be self-sufficient for traceability.

## Information to Collect

### From the User

- **Goal:** What problem are we solving? What's the desired outcome?
- **Users/Actors:** Who will use this? What roles are involved?
- **Scope:** What's in scope and what's explicitly out of scope?
- **Constraints:** Timeline, tech stack, existing systems, performance needs?
- **Priority:** Must-have vs nice-to-have features?

### From the Codebase

- Existing related code, models, APIs, or modules
- Current tech stack, frameworks, and patterns in use
- Database schema or data models that are relevant
- Existing tests or documentation that provide context
- Naming conventions and project structure

## Clarifying Questions

Workers never ask the user directly — unresolved questions go into `open_questions` in the return summary, and the orchestrator asks them at the requirements gate. Prioritize the most impactful questions first.

- "What's the main problem this solves for the user?"
- "Are there existing features this interacts with?"
- "What happens when [edge case]?"
- "Is there a specific performance or scale requirement?"
- "Any security or compliance considerations?"
- "What does success look like? How will we know it's done?"

Limit to 3-5 questions per round. Don't overwhelm the user.

## Interaction Protocol

Requirements workers never talk to the user directly — the orchestrator (main session) owns all user interaction, and the requirements gate cannot be skipped.

Gate confirmations owned by the orchestrator:

1. The list of functional requirements — "Here's what I understand we're building. Anything missing or wrong?"
2. Priority classification — "I've marked these as must-have and these as nice-to-have. Agree?"
3. Out-of-scope items — "These are explicitly NOT part of this work. Correct?"
4. Key assumptions — "I'm assuming X and Y. Let me know if that's off."

Worker rules:

- If any of the above is still unresolved when the work finishes, record it in `open_questions` in the return summary; the orchestrator relays it to the user at the gate.
- If questions remain open but the document is still writable, write a best-effort version anyway: mark the affected parts as assumptions, list the questions in the document's `Open Questions` section, and repeat them in the return summary. Do not block on unanswered questions.
- If the orchestrator's handoff already contains the user's answers, apply them without asking again.

## Writing Style: EARS Pattern

Use the EARS (Easy Approach to Requirements Syntax) pattern for acceptance criteria:

- **Event-driven:** WHEN [trigger], THE [system] SHALL [behavior]
- **State-driven:** WHERE [condition], THE [system] SHALL [behavior]
- **Unwanted behavior:** IF [unwanted condition], THE [system] SHALL [response]
- **Optional:** WHERE [feature is enabled], THE [system] SHALL [behavior]
- **Complex:** WHEN [trigger] AND WHERE [condition], THE [system] SHALL [behavior]

Examples:
- "WHEN a user submits the login form, THE system SHALL validate credentials within 2 seconds"
- "WHERE the cache is expired, THE system SHALL fetch fresh data from the API"
- "IF the database connection fails, THE system SHALL retry 3 times with exponential backoff"

## Output

### Small Feature (≤5 requirements)

Save a single `requirements.md` to `.spec/<spec-name>/requirements.md`

### Large Feature (>5 requirements or multiple modules)

Save a master index + per-module sub-files:
- `.spec/<spec-name>/requirements.md` — master index with glossary and module table
- `.spec/<spec-name>/requirements-<module>.md` — detailed requirements per module

## Large Spec Parallelization

For large specs, requirements elaboration runs master-then-parallel:

1. **Master skeleton first:** One worker (or the orchestrator) writes `requirements.md` with only the global structure — introduction, glossary, module breakdown, cross-cutting concerns, and out-of-scope items. The glossary is the contract every module worker must use.
2. **Gate:** The orchestrator shows the skeleton to the user for confirmation (module split, scope, glossary).
3. **Per-module workers in parallel:** One worker per module, all dispatched in the same message. Each worker writes only its own `requirements-<module>.md`, using the master glossary and EARS conventions, and returns per the return contract.
4. **Consistency pass:** The orchestrator checks terminology against the master glossary, cross-module references, and duplicate or conflicting requirements, then runs `check <spec>` to confirm the module index links resolve and re-dispatches the offending module on conflicts.

## Template: requirements.md (Small Feature)

```markdown
# Requirements: [Feature Name]

## Introduction
[1-3 sentence summary of what we're building and why]

## Glossary
- **[Term 1]**: [Definition]
- **[Term 2]**: [Definition]

## Requirements

### Requirement 1: [Title]

**User Story:** As a [actor], I want [goal], so that [benefit].

#### Acceptance Criteria

1. WHEN [trigger], THE [system] SHALL [behavior]
2. THE [system] SHALL [behavior]
3. WHERE [condition], THE [system] SHALL [behavior]

### Requirement 2: [Title]

**User Story:** As a [actor], I want [goal], so that [benefit].

#### Acceptance Criteria

1. WHEN [trigger], THE [system] SHALL [behavior]
2. IF [unwanted condition], THE [system] SHALL [response]

[... more requirements ...]

## Non-Functional Requirements

### NFR-1: [Title]
**Category:** Performance | Security | Scalability | Accessibility | Reliability
**Requirement:** THE [system] SHALL [quality attribute with measurable metric]

## Constraints
- [Technical constraint 1]
- [Business constraint 2]

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Out of Scope
- [Item 1]
- [Item 2]

## Open Questions
- [Any unresolved questions that need answers before design]
```

## Template: requirements.md (Large Feature — Master Index)

```markdown
# Requirements Document

## Introduction
[Summary of the overall feature/project and its purpose]

## Glossary
- **[Term 1]**: [Definition — used across all sub-requirement files]
- **[Term 2]**: [Definition]

## Module Index

| # | Module | File | Description |
|---|--------|------|-------------|
| 1 | [Module A] | [requirements-module-a.md](requirements-module-a.md) | [Brief description] |
| 2 | [Module B] | [requirements-module-b.md](requirements-module-b.md) | [Brief description] |
| 3 | [Module C] | [requirements-module-c.md](requirements-module-c.md) | [Brief description] |

Each sub-requirement file follows the same EARS patterns and glossary terms defined in this document.

## Cross-Cutting Concerns
- [Concern that spans multiple modules]
- [Shared constraint or assumption]

## Out of Scope
- [Item 1]
- [Item 2]
```

## Template: requirements-<module>.md (Sub-file)

```markdown
# Requirements: [Module Name]

## Introduction
[What this module does and why it exists]

## Requirements

### Requirement 1: [Title]

**User Story:** As a [actor], I want [goal], so that [benefit].

#### Acceptance Criteria

1. WHEN [trigger], THE [system] SHALL [behavior]
2. THE [system] SHALL [behavior]

### Requirement 2: [Title]

**User Story:** As a [actor], I want [goal], so that [benefit].

#### Acceptance Criteria

1. WHEN [trigger], THE [system] SHALL [behavior]
2. IF [unwanted condition], THE [system] SHALL [response]
```

## Next Step

→ Return to the orchestrator per the return contract (`files_written`, `key_decisions`, `open_questions`), including the requirement count in the summary.

→ The orchestrator spot-checks the document, then asks at the gate: "Requirements look good? Ready to move to Design, or want to revise anything?"

→ On approval, proceed to **Design Mode**
