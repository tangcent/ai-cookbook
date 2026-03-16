# Design Mode

## Purpose

Define the technical architecture and approach for implementing the requirements. Bridge the gap between "what" (requirements) and "how" (implementation tasks).

## What This Mode Does

1. Read and analyze requirements (from `requirements.md` or user input)
2. Survey the existing codebase for relevant patterns, models, APIs, and conventions
3. Propose a technical approach with component breakdown
4. Define data models, API contracts, and key interfaces
5. Identify design decisions with trade-offs
6. Identify technical risks and mitigation strategies
7. Produce a formal design document (with sub-files for large specs)

## Information to Collect

### From Requirements

- All functional requirements and their acceptance criteria
- Non-functional requirements (performance, security, etc.)
- Constraints, assumptions, and glossary terms

### From the Codebase

- **Project structure:** Frameworks, patterns (MVC, layered, hexagonal, etc.)
- **Existing models:** Database entities, DTOs, domain objects related to this feature
- **Existing APIs:** Endpoints, services, or interfaces this feature will extend or interact with
- **Conventions:** Naming patterns, error handling approach, logging patterns, test patterns
- **Dependencies:** Libraries and tools already in use that are relevant
- **Package structure:** Where new code should live based on existing organization

### From the User

- Preferences on approach if multiple options exist
- Any architectural decisions already made
- Integration points with external systems

## Design Principles to Apply

When producing the design, consider and document these where relevant:

1. **Consistency with existing codebase** — follow established patterns, don't introduce new paradigms without reason
2. **Separation of concerns** — clear boundaries between components
3. **Testability** — all core logic should be testable via injectable interfaces or pure functions
4. **Extensibility** — use interfaces and SPI patterns where future extension is likely
5. **Error handling** — define how errors propagate and are reported

## Design Decisions to Present

For each significant decision, present options with trade-offs:

```
**Decision: [What needs to be decided]**
- Option A: [approach] — Pros: [x, y] / Cons: [a, b]
- Option B: [approach] — Pros: [x, y] / Cons: [a, b]
- Recommendation: [which and why]
```

Don't present trivial decisions. Focus on choices that affect architecture, performance, or maintainability.

## What to Confirm with User

Before finalizing design:

1. **Overall approach** — "Here's the high-level architecture. Does this direction make sense?"
2. **Key design decisions** — Present options for non-obvious choices and get user's pick
3. **Data model changes** — "These are the schema/model changes needed. Any concerns?"
4. **API contracts** — "Here are the proposed interfaces. Anything to adjust?"
5. **Risk items** — "These are the technical risks I see. Anything else you're worried about?"

## Output

### Small Feature

Save a single `design.md` to `.spec/<spec-name>/design.md`

### Large Feature

Save a master index + per-module sub-files:
- `.spec/<spec-name>/design.md` — master index with architecture overview and module table
- `.spec/<spec-name>/design-<module>.md` — detailed design per module

## Template: design.md (Small Feature)

```markdown
# Design: [Feature Name]

## Overview
[Brief summary of the technical approach]

## Design Principles
[List key principles guiding this design — e.g. "Kotlin-idiomatic", "coroutines-first", "SPI extensibility"]

## Architecture

### Component Diagram
[Describe or use mermaid/ascii diagram showing components and their interactions]

### Affected Components
- **[Component 1]:** [What changes and why]
- **[Component 2]:** [What changes and why]
- **New: [Component 3]:** [What it does and why it's needed]

### Package / File Structure
```
path/to/feature/
├── models/          # Data models
├── services/        # Business logic
├── api/             # API layer
└── utils/           # Helpers
```

## Data Model

### New Models
```
[Model definition — class, interface, schema, or table DDL as appropriate for the project's language]
```

### Model Changes
- **[Existing Model]:** Add field `x` (type, purpose)

## API / Interface Design

### [Endpoint or Interface Name]
- **Method:** GET/POST/PUT/DELETE (for REST) or method signature (for internal interfaces)
- **Path:** `/api/v1/...`
- **Request:** [body/params description]
- **Response:** [response shape]
- **Error Cases:** [error scenarios and codes]

## Key Design Decisions

### Decision 1: [Title]
**Context:** [Why this decision matters]
**Options Considered:**
- Option A: [description] — [trade-offs]
- Option B: [description] — [trade-offs]
**Decision:** [Which option and rationale]

## Dependencies
- [Library/service 1]: [why needed, version if relevant]

## Security Considerations
- [Security item 1]

## Performance Considerations
- [Performance item 1]

## Technical Risks
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to mitigate] |

## File Changes Summary
| File | Action | Description |
|------|--------|-------------|
| `path/to/file.ts` | Create | [What it contains] |
| `path/to/existing.ts` | Modify | [What changes] |
```

## Template: design.md (Large Feature — Master Index)

```markdown
# Design Document — [Feature Name]

## Overview
[Summary of the overall technical approach]

### Design Principles
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

### Package Structure
```
[Overall package/directory structure for the feature]
```

## Architecture

### High-Level Architecture Diagram
[Mermaid diagram or ASCII art showing major components and data flow]

## Module Index

| # | Module | File | Description |
|---|--------|------|-------------|
| 1 | [Module A] | [design-module-a.md](design-module-a.md) | [Brief description] |
| 2 | [Module B] | [design-module-b.md](design-module-b.md) | [Brief description] |

## Cross-Cutting Design Decisions

### Decision 1: [Title]
**Context:** [Why this decision matters across modules]
**Decision:** [What was decided and why]
```

## Template: design-<module>.md (Sub-file)

```markdown
# Design: [Module Name]

> References: [requirements-<module>.md](requirements-<module>.md)

## Overview
[What this module does technically]

## Components
[Detailed component design for this module]

## Data Model
[Models specific to this module]

## Interfaces
[APIs and interfaces for this module]

## Design Decisions
[Module-specific decisions]
```

## Next Step

→ Summarize the design and ask: "Design looks solid? Ready to break this into tasks, or want to revise anything?"

→ Proceed to **Tasks Mode**
