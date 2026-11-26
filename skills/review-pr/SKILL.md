---
name: review-pr
description: Reviews GitHub pull requests end-to-end - lands the code in a local worktree, judges whether the problem is real and the fix stays in scope, verifies by running builds and tests, reports graded findings, then either squash-merges or asks whether to autofix-and-merge vs. leave a message for the author. For multiple PRs, fans out one subagent per PR concurrently and aggregates the reports. Invoke when the user asks to review PRs, check a pull request, or decide whether to merge.
---

# Review PR

## Principle

Judge the change before the code. A PR that fixes a non-existent problem, or rewrites unrelated modules, is a bad PR however clean the diff looks. Every conclusion must be backed by files on disk and commands actually run — not by remote file blobs alone.

Phases 1-4 answer the four judgment questions (intent, reality, solution, scope), Phase 5 reviews details, Phase 7 reports. Phases 0 and 6 are non-negotiable: land the code locally, and verify by running it. Phase 8 is the disposition decision: prefer squash merge, and when findings exist, ask the user whether to autofix-and-merge or leave the author a message.

When the user asks to review **multiple PRs**, do not review them one by one in the main thread. Use Multi-PR Mode below: the main agent only prepares and aggregates, while one subagent per PR does the full Phase 0-7 review concurrently. Phase 8 always stays with the main agent.

---

## Multi-PR Mode — fan out one subagent per PR

Trigger: the user names two or more PRs, asks to review "these PRs", or asks for a batch review. A single PR continues with the normal Phase 0-8 flow.

### Step 1 — Prepare (main agent)

1. Resolve every PR number and its `baseRefName` with `gh pr view <N> --json number,title,body,baseRefName,headRefName,files`. Bases may differ; do not assume one base.
2. Fetch **all** heads in one shot before fanning out, so subagents never contend on the same remote ref:
   ```bash
   git fetch origin refs/pull/<A>/head:refs/pr/<A> refs/pull/<B>/head:refs/pr/<B>
   ```
3. Detect stacked PRs now: compare `headRefName`/`baseRefName` and the `--name-only` diffs. Record which PRs stack on which, so a subagent can be told to exclude another PR's files from its scope (see Phase 0's `comm -13` trick).
4. Assign each PR a **unique** worktree path, e.g. `<repo-root>/.worktrees/review-pr-<N>`. Two subagents must never share a worktree or a ref.

### Step 2 — Launch all subagents concurrently (main agent)

Spawn one subagent per PR **in the same message** (one tool call each) so they run in parallel. Use `general-purpose` (full tool access) and give each a unique `name` like `review-pr-<N>` so it can be messaged. The prompt must be self-contained — a subagent cannot see this conversation. Include:

- repo absolute path, PR number, its base branch, the pre-fetched `refs/pr/<N>`, and its assigned worktree path;
- the stacking context (which PRs it stacks on / which stack on it) and the files that belong to those PRs;
- an instruction to read this skill file (`<skill-path>/SKILL.md`) and run **Phases 0-7 in full**, including real build/test commands from Phase 6 — no "LGTM" without a run;
- a **hard stop at Phase 7**: no merge, no push, no `gh pr review`, no edit to any branch — those are external actions reserved for the main agent in Phase 8;
- the exact report shape from Phase 7 (Verdict / Problem / Solution and scope matrix / Findings / Verification / Open questions), returned as its final message.

### Step 3 — Aggregate (main agent)

Collect every subagent's report. Build a roll-up table with one row per PR:

| PR | Verdict | Blocking | Non-blocking | Verification |
|----|---------|----------|--------------|--------------|
| #N | ... | ... | ... | commands + pass/fail |

- If a subagent fails, times out, or returns an opinion without verification commands, **re-run it for that PR** or report that PR as unverified — never fill the gap with a guess.
- Each PR keeps its own full Phase 7 report below the roll-up; do not merge findings across PRs.

### Step 4 — Disposition (main agent, Phase 8)

Phase 8 is a single user decision covering all PRs, not one decision per subagent:

- Group by verdict: clean PRs → confirm squash merges; PRs with Blocking/Non-blocking findings → ask autofix-vs-message **per PR**, using the Phase 8 option table.
- Apply the chosen path for each PR yourself. Subagents never merge, push, or comment.
- Remove every worktree you created when done.

### Concurrency hygiene

- Unique worktree path and ref per PR — no exceptions.
- If two PRs touch the same module, their verification runs may race on build caches or ports; if a failure looks environmental, re-run that PR alone before calling it a real finding.
- Keep the fan-out bounded; for a very large batch, split into waves rather than spawning an unbounded number of subagents.

---

## Phase 0 — Land the PR locally

Never review by fetching remote files one by one. Read the real tree so surrounding code, sibling modules and tests are available.

```bash
git fetch origin refs/pull/<N>/head:refs/pr/<N>
git worktree add <local-path> refs/pr/<N>
gh pr view <N> --json title,body,baseRefName,headRefName,files
git log --oneline <base>..refs/pr/<N>
git diff --name-status <base>...refs/pr/<N>
```

Determine the base branch from `gh pr view` (`baseRefName`); do not assume `main`.

For stacked PRs, confirm how they sit on top of each other. Compare `--name-only` outputs to isolate this PR's own increment, and use the log to confirm linear stacking:

```bash
git diff --name-only <base>...refs/pr/<A> | sort > /tmp/pr-a.txt
git diff --name-only <base>...refs/pr/<B> | sort > /tmp/pr-b.txt
comm -13 /tmp/pr-a.txt /tmp/pr-b.txt   # files introduced by B only
```

Do not attribute another PR's files to this one.

---

## Phase 1 — What problem does the PR claim to solve?

- Restate it in one sentence, from the title, body, linked issues, commit messages and changed tests.
- Write down the acceptance criteria the author implies.
- If the description and the diff disagree, flag it as blocking until clarified.

## Phase 2 — Is the problem real, and worth solving?

Evidence, not intuition:

1. Reproduce on the base branch before looking at the fix — a failing command, test, or output.
2. Search the repo: is the capability already implemented elsewhere?
3. Check the linked issue state, existing tests and docs — is this by design, already solved, or cosmetic?
4. Decide: `real` / `not reproducible` / `by design` / `already solved` / `cosmetic`.

If the answer is anything but `real`, say so and stop. Do not review the details of a change that should not exist.

## Phase 3 — Is the solution reasonable?

- Is it the smallest change that fixes the problem? Does it reuse existing capabilities instead of adding new layers?
- Respect the target repository's own contracts. Read `AGENTS.md`, `CONTRIBUTING.md` and architecture docs if present; follow their branch, commit, layering and testing rules. Do not impose rules from this skill over the repository's stated conventions.
- Does the change fit the project's module/package boundaries, without new cross-layer dependencies or cycles?
- Name one simpler alternative. If the PR chose a heavier one, ask why.

## Phase 4 — Does the change exceed the stated problem?

Build a file-level change matrix and classify **every** changed file:

| Path | Status | Lines | In scope? | Note |
|------|--------|-------|-----------|------|
| `path/to/file` | M | +12/-3 | in scope | ... |

- Labels: `in scope` / `supporting` (tests, docs, CI) / `unrelated`.
- Watch for whole-file reformatting, drive-by refactors, dependency bumps, symbol renames, generated files, and unexplained golden/fixture churn.
- Out-of-scope changes are not automatically wrong, but call them out explicitly and ask for a split when they obscure the fix.

Scope is a correctness property: a well-written but out-of-scope PR still needs an explicit scope finding.

---

## Phase 5 — Review the details

Each finding must carry `file:line`, why it matters, and a concrete suggested change.

- Correctness: edge cases, nil/empty values, error paths, concurrency, platform differences.
- Regression: existing callers, output stability, snapshots/golden files.
- Tests: is the new behavior covered? Do tests assert behavior rather than implementation? Would they fail on the base branch?
- Docs: README, contribution guides and changelog consistent with the new behavior.
- Conventions: branch name, commit messages and the PR title follow the repository's stated rules; no merge commits inside the PR branch; no stray build output or temporary files. All artifacts that enter the repository — code, comments, commit messages, PR title and body — are written in the language the repository requires (commonly English).

---

## Phase 6 — Verify by running

1. Discover the real commands from the repository's CI config (`/.github/workflows/*`, Makefile, package scripts, etc.) and contribution docs. Replicate at least the affected modules.
2. Run the test suite and static checks. Examples by ecosystem:

   ```bash
   # Go
   go test ./... && go vet ./...
   # Node
   npm test && npm run lint
   # Python
   pytest && ruff check .
   # JVM
   ./gradlew test   # or: mvn test
   ```

3. If a golden/snapshot file changed, confirm the output change is intended and the refresh was deliberate, not a silent baseline rewrite.
4. Report the exact commands and their results. A review without a run is an opinion, not a review.

---

## Phase 7 — Report

Conclusion first, then numbered reasons.

```markdown
## Verdict: Approve / Request changes / Comment
<one sentence>

### Problem
Is it real? Worth solving? What is the evidence?

### Solution and scope
Approach assessment + file-level change matrix.

### Findings
| Level | Location | Issue | Suggested change |
|-------|----------|-------|------------------|
| Blocking | `path:line` | ... | ... |

### Verification
Commands run and pass/fail.

### Open questions
```

Rules:

- Three levels only: **Blocking** (must fix before merge), **Non-blocking** (should fix), **Nit** (optional).
- Never bury a blocking issue among nits. Never say "LGTM" without stating what was verified.

---

## Phase 8 — Decide the disposition (ask the user)

Merging and commenting are external, visible actions. Do not take them without an explicit user decision at this point.

### Default: prefer squash merge

The merge strategy is **squash by default** (`gh pr merge <N> --squash`) so the PR becomes one clean commit on the base branch. Before squashing, confirm:

- The **PR title** follows the repository's commit-message convention, because it becomes the commit subject on the base branch. Fix it with `gh pr edit <N> --title "..."` if needed.
- The PR is one logical change — a squashed commit cannot be split later. If it bundles unrelated work, ask the author to split instead of squashing.
- Required CI checks have passed.

### When there are no findings (Verdict: Approve)

Report the verdict, state the verification, then ask the user to confirm the squash merge. Do not merge unprompted.

### When there are Blocking or Non-blocking findings — ask the user to choose

Present the findings, then ask the user to pick one of two paths. Do not assume either:

| Option | What it means | When to use |
|--------|---------------|-------------|
| **A. Autofix → merge** | You fix the findings on the PR branch, re-verify, then squash-merge | Author is a teammate / you can write to the head branch; findings are small and unambiguous |
| **B. Leave a message for the author** | You post a review with the graded findings and request changes; you do not merge | External contributor, findings need the author's judgment, or you lack write access to the head branch |

If Nit-only findings exist and no Blocking/Non-blocking, mention them, offer to post them as comments, and otherwise proceed on the Approve path.

#### Path A — Autofix → merge

1. Proceed only after the user explicitly chooses autofix.
2. Confirm you can push to the head branch (forks may be read-only); if not, fall back to Path B and explain why.
3. Fix **only** the reported findings, in the PR's worktree. Do not expand scope or add unrelated refactors.
4. If the head branch has drifted from the base, rebase onto `origin/<base>`; never merge the base into the PR branch. Force-push only with `--force-with-lease` and after confirmation.
5. Commit with a message following the repository convention, push to the head branch.
6. Re-run Phase 6 verification on the amended branch. If anything fails, stop and report — do not merge.
7. Confirm the PR title still fits the squash commit subject, then squash-merge with the user's go-ahead.
8. Report exactly what you changed, what you ran, and the resulting merge commit.

#### Path B — Leave a message for the author

1. Proceed only after the user explicitly chooses to leave a message.
2. Do not edit or push to the PR branch, and do not merge.
3. Post a review with conclusion first, then numbered findings — each with `file:line`, why it matters, and a concrete suggested change. Use `--request-changes` for Blocking findings, otherwise `--comment`:

   ```bash
   gh pr review <N> --request-changes --body "<findings>"
   gh pr review <N> --comment --body "<findings>"
   ```

4. Write the body in the language the repository requires; keep it actionable and non-adversarial.
5. Tell the user what was posted and that the PR is left for the author to update.

---

## Notes

- Remove the temporary worktree when done if you created it: `git worktree remove <local-path>`.
- Never merge on a red CI, with unresolved Blocking findings, or without the user's go-ahead.
- When in doubt about scope or intent, ask rather than fix — an unnecessary autofix is itself an out-of-scope change.
