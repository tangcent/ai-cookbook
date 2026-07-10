# Best Practices by Task Type

## Purpose

Guidance for how to sequence work for common categories of coding tasks. This is not a standalone mode — it's consulted by **Tasks Mode** (when deciding how to split tasks) and **Execute Mode** (when deciding execution order within a task).

## General Principle: Define "Correct" Before Building It

Across almost every category below, the same pattern repeats: establish a concrete, checkable definition of done — a test, a contract, a schema, a benchmark — *before* writing the internals that must satisfy it. This gives fast feedback when something breaks, and freedom to change internals later without breaking consumers.

See "When to Skip" at the end — this is a default, not a mandate.

## 1. General Coding Tasks → Test-Driven Development (TDD)

For most feature work, default to red-green-refactor:

1. Write a failing test expressing the desired behavior for the smallest slice of the task
2. Write the minimum code to make it pass
3. Refactor with the test as a safety net
4. Repeat for the next slice

**In Tasks Mode:** split "write test for X" and "implement X" as adjacent sub-tasks, test sub-task first. Don't mark the test sub-task optional (`*`) — it's part of the definition of done, not a nice-to-have. Only skip it if the project genuinely has no test infrastructure and setting one up is out of scope.

```markdown
- [ ] 3. [Feature X]
  - [ ] 3.1 Write test for [behavior]
    - _Requirements: [Req#.Criteria#]_
  - [ ] 3.2 Implement [behavior] to satisfy 3.1
    - _Requirements: [Req#.Criteria#]_
```

**In Execute Mode:** write and run the test first, confirm it fails for the expected reason, then implement, then confirm it passes.

## 2. API-Related Tasks → Contract-First

For anything exposing an API (REST/GraphQL/RPC, or an internal interface consumed by other modules):

1. Define the contract first — request/response shapes, status/error codes, types, OpenAPI/GraphQL schema, or function signatures
2. Get user confirmation on the contract during **Design Mode**, before Tasks Mode breaks it into implementation work — the contract is usually the highest-leverage decision: cheap to change now, expensive once consumers depend on it
3. Only after the contract is settled, decompose implementation: types/schema → handler/business logic → persistence → contract test

The "API / Interface Design" section in `design.md` IS the contract for these tasks — treat it as the primary deliverable, not boilerplate filled in after the fact.

```markdown
- [ ] 2. [Endpoint/Interface Name]
  - [ ] 2.1 Define request/response types per design.md contract
  - [ ] 2.2 Implement handler logic
  - [ ] 2.3 Write contract test verifying request/response shape and error cases
    - _Requirements: [Req#.Criteria#]_
```

If in-repo consumers of the API exist (a frontend calling this backend, another service), consider a task to stub/mock the contract early so dependent work can proceed in parallel, even before the real implementation lands.

## 3. Other Common Cases

### Bug Fixes → Regression Test First
Write a test that reproduces the bug — it should fail against current code — before touching the fix. Fix until it passes. This proves the bug existed, proves the fix works, and stops it from silently coming back.

```markdown
- [ ] 1. Fix [bug]
  - [ ] 1.1 Write failing test reproducing [bug]
  - [ ] 1.2 Fix [root cause]
  - [ ] 1.3 Verify the regression test and full suite pass
```

### Refactoring → Characterization Tests Before Changing Anything
If solid tests already cover the code being refactored, rely on them. If not, write characterization tests first that pin down current behavior (even if that behavior isn't ideal — the goal is a safety net, not a spec). Never refactor and change behavior in the same task; that defeats the safety net.

### Database / Schema Changes → Migration-First, Reversible
Write the migration (up and down) before the code that depends on the new schema. Add a task to verify the migration is reversible (down restores prior state cleanly) before building on top of it.

### Public Interfaces / Shared Libraries → Interface-First
When other modules or packages will depend on this code, define and confirm the public signature/types/exports before writing internals — same rationale as API contracts, just for in-process boundaries instead of network ones. Internals can change freely later; the signature is the expensive-to-change part.

### Performance-Sensitive Work → Benchmark-First
Before optimizing, write a benchmark or measurement capturing the current baseline. Optimize, then re-run the same benchmark to prove the improvement. Without a baseline, "faster" is unverifiable.

## When to Skip Test/Contract-First

Don't force this ceremony where it adds no signal:

- Throwaway scripts, one-off migrations run once and discarded, exploratory spikes explicitly framed as such
- Trivial changes (typos, config value changes, comment updates)
- The user explicitly asks to move fast and accepts the tradeoff

When skipping, say so rather than silently omitting it: "This is a trivial config change, skipping a dedicated test task — let me know if you'd like one anyway."

## Where This Is Consulted

- **Tasks Mode** — when splitting a unit of work into test/contract vs. implementation sub-tasks, and deciding ordering between them
- **Execute Mode** — when deciding what to write first within a task pair (test before implementation, contract before implementation)

This file has no "next mode" of its own — it's a lens applied while running those two modes.
