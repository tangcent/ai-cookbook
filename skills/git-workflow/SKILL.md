---
name: git-workflow
description: Manage day-to-day Git workflow with safe branch creation, conventional commits, rebasing, pushing, MR creation, active-branch sync, and integration-branch consolidation. Use when the user asks to create branches, commit, push, sync feature/fix branches, rebuild dev branches, or open merge requests.
---

# Git Workflow

## Core Rules

1. Always sync remotes first:
   ```bash
   git fetch --all --prune
   ```
2. Always detect default branch dynamically (fallback `main`, then `master`):
   ```bash
   default_branch="$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')"
   [ -z "$default_branch" ] && default_branch="$(git branch -r --list 'origin/main' | head -n1 | sed 's@^ *origin/@@')"
   [ -z "$default_branch" ] && default_branch=master
   ```
3. Ask for confirmation before destructive operations:
   - `git push --force-with-lease`
   - `git reset --hard`
   - deleting branches/tags
4. Never use plain `--force`; use `--force-with-lease`.
5. Prefer `origin/<default-branch>` as rebase target.

## Branch and Commit Conventions

- Branch prefixes:
  - `feature/<name>`
  - `fix/<name>`
  - `hotfix/<name>`
  - `release/<name>`
  - `chore/<name>`
- Commit prefixes:
  - `feat:`, `fix:`, `perf:`, `refactor:`, `docs:`, `test:`, `chore:`, `release:`

## Bundled Helpers

Use these scripts from this skill directory:

- `scripts/detect-active-branches.sh [--base <branch>] [--window <n>]`
- `scripts/generate-mr-url.sh [source-branch] [target-branch]`

`generate-mr-url.sh` supports generic GitLab remotes (not only `git.tec-do.com`).

## Workflow A: Create Branch

1. Ensure repo is up to date:
   ```bash
   git fetch --all --prune
   ```
2. Pick base branch:
   - default: `origin/<default-branch>`
   - use user-provided base if specified
3. Normalize branch name:
   - If no prefix, infer one from intent (`feature`, `fix`, `chore`, `release`, `hotfix`)
   - Convert spaces/underscores to `-`
4. Create and checkout:
   ```bash
   git checkout -b <prefix>/<slug> origin/<base-branch>
   ```
5. If user asks to publish branch, push:
   ```bash
   git push -u origin <branch>
   ```
6. Show MR URL:
   ```bash
   bash scripts/generate-mr-url.sh <branch> <default-branch>
   ```

## Workflow B: Commit, Push, and MR

### 1. Branch safety decision

1. Detect current branch:
   ```bash
   current_branch="$(git branch --show-current)"
   ```
2. If current branch is protected/integration (`main`, `master`, `develop`, `dev`, `staging`) or user requested new branch:
   - create a new branch from `origin/<default-branch>` and continue there.
3. If current branch is feature/fix style, verify it is not stale:
   ```bash
   git cherry "origin/$default_branch" HEAD
   ```
   - If all commits are already upstream (only `-` lines), treat as stale and create a fresh branch.

### 2. Rebase onto latest default branch

1. Stash if worktree is dirty:
   ```bash
   git stash push -u -m "git-workflow-auto-stash"
   ```
2. Rebase:
   ```bash
   git rebase "origin/$default_branch"
   ```
3. If conflicts occur, ask user to resolve and continue:
   ```bash
   git rebase --continue
   ```
4. Restore stash if created:
   ```bash
   git stash pop
   ```

### 3. Stage and commit

1. Review status:
   ```bash
   git status --short
   ```
2. If user did not ask for partial staging, stage all:
   ```bash
   git add -A
   ```
3. Propose conventional commit title based on diff intent.
4. Ask for confirmation/edits on commit message.
5. Commit:
   ```bash
   git commit -m "<type>: <summary>"
   ```

### 4. Push

1. If rebase happened, default to:
   ```bash
   git push --force-with-lease origin <current-branch>
   ```
   Ask for confirmation first.
2. Otherwise:
   ```bash
   git push -u origin <current-branch>
   ```
3. Always print MR URL:
   ```bash
   bash scripts/generate-mr-url.sh <current-branch> <default-branch>
   ```

### 5. Create MR when requested

If user explicitly requested MR creation:

1. Prefer `glab mr create` when authenticated.
2. Build title/body from commits:
   ```bash
   git log "origin/$default_branch"..HEAD --pretty=format:'- %s' --reverse
   ```
3. Create MR:
   ```bash
   glab mr create \
     --target-branch "$default_branch" \
     --source-branch "$(git branch --show-current)" \
     --title "<title>" \
     --description "<description>"
   ```
4. If `glab` is unavailable, return URL from `generate-mr-url.sh`.

## Workflow C: Sync Active Feature/Fix Branches

1. Save current branch:
   ```bash
   origin_branch="$(git branch --show-current)"
   ```
2. Detect candidates:
   ```bash
   bash scripts/detect-active-branches.sh --base "$default_branch"
   ```
3. Show candidate list and ask user which branches to sync.
4. For each selected branch:
   - `git checkout <branch>`
   - `git rebase "origin/$default_branch"`
   - Resolve conflicts with user if needed
   - confirm then `git push --force-with-lease origin <branch>`
   - print MR URL via helper script
5. Return to original branch.

## Workflow D: Consolidate Integration Branch

Use for requests like "rebuild dev from active features".

1. Ask for target integration branch (default `dev`).
2. Detect active branches using helper script.
3. Ask user to confirm branch list and base feature branch.
4. Rebase each feature branch on `origin/<default-branch>` first.
5. Checkout target branch and hard reset to base feature branch:
   ```bash
   git checkout <target-branch>
   git reset --hard <base-feature-branch>
   ```
   Ask confirmation before reset.
6. Merge remaining feature branches one by one:
   ```bash
   git merge --no-ff <feature-branch>
   ```
7. Ask before push, then push and provide MR URL.

## Autonomy Principle

Make reasonable defaults automatically (prefix selection, staging, commit type, target branch).
Ask only when:

- action is destructive
- user intent is ambiguous
- required information cannot be inferred
