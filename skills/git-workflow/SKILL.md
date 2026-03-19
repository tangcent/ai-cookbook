---
name: git-workflow
description: Git workflow management with branch prefixes, conventional commits, and advanced synchronization operations. Use when user asks to create branches, make commits, sync features, consolidate branches, or rebuild integration branches. AI autonomously decides commit prefix, staging, and whether to commit on current branch or create a new one from master/main.
---

# Git Workflow Management

You are a Git workflow assistant that helps with branch management, conventional commits, and feature synchronization.

## Branch Naming Conventions

- Feature branches: `feature/<branch-name>`
- Release branches: `release/<version-or-name>`
- Fix branches: `fix/<issue-or-description>`

## Commit Message Prefixes

- `feat:` A new feature
- `fix:` A bug fix
- `amend:` Amending or modifying existing functionality
- `chore:` Maintenance tasks, dependencies, configuration
- `release:` Release-related changes
- `doc:` Documentation changes (README, comments, API docs, guides)
- `perf:` Performance improvements (optimization, caching, reducing overhead)

## Available Commands

### Helper Script Location (Portable)

This skill includes helper scripts in the `scripts/` subdirectory.

- `scripts/detect-active-branches.sh`
- `scripts/generate-mr-url.sh`

Invoke them with relative paths (no fixed home directory paths), e.g.:

- `bash scripts/detect-active-branches.sh`
- `bash scripts/generate-mr-url.sh [branch-name]`

### detect-active-branches
Run the built-in script to identify active feature branches.

Usage: `bash scripts/detect-active-branches.sh`

The script identifies branches that:
- Have their merge-base within the latest 10 commits of master
- Have commits ahead of master (unmerged work)

### generate-mr-url
Generate a merge request URL for a branch.

Usage: `bash scripts/generate-mr-url.sh [branch-name]`

If no branch name is provided, uses the current branch. Outputs a URL like:
`https://git.example.com/group/project/merge_requests/new?merge_request%5Bsource_branch%5D=feature%2Fbranch-name`

### branch (alias: fb)
Create a new branch with the appropriate prefix.

Steps:
1. Ask the user for the branch type (feature/release/fix) and name if not provided
2. Validate the branch name follows the convention
3. Create the branch from the current HEAD or specified base branch
4. Checkout the new branch
5. Confirm creation to the user

If the user provides a branch name without a prefix, automatically add the appropriate prefix.

### commit (alias: gc)
Create a commit with conventional commit message prefix.

#### Step 0: Always Fetch Latest

Before any branch or commit decision, ALWAYS run:
```
git fetch origin
```
This ensures all remote tracking info is up to date.

#### Step 1: Detect Default Branch

Detect the default branch (`master` or `main`):
```
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
```
Fallback to `master` if detection fails. Use this as `<default-branch>` in all subsequent steps.

#### Step 2: Smart Branch Decision

Decide whether to commit on the current branch or create a new branch:

1. Run `git branch --show-current` to get the current branch name.
2. **Create a new branch from `<default-branch>`** if:
   - Current branch is `master`, `main`, `dev`, `develop`, or `staging`
   - The user explicitly asks for a new branch
   - Steps:
     - `git checkout -b <new-branch> origin/<default-branch>`
     - Infer the branch name and type from the changes/context (e.g., documentation changes → `doc/...`, bug fix → `fix/...`)
3. **Commit on current branch** if:
   - Current branch is already a feature/fix/release branch (has a prefix like `feature/`, `fix/`, `release/`)
   - The changes are clearly related to the current branch's purpose

The AI should make this decision autonomously without asking the user, unless the situation is genuinely ambiguous (e.g., unrelated changes on a feature branch).

#### Step 3: Rebase Current Branch onto Latest Default Branch

Before committing, check if the current branch needs rebasing:

1. Check if the branch has diverged or is behind the default branch:
   ```
   git rev-list --left-right --count origin/<default-branch>..HEAD
   ```
   The output is `<behind>\t<ahead>`. If `<behind>` > 0, the branch is behind.
2. Check if the branch contains merge commits (indicating previous merges from default branch):
   ```
   git log --merges --oneline origin/<default-branch>..HEAD
   ```
   If any merge commits are found, the branch has merged content from the default branch.
3. **Rebase if** the branch is behind the default branch OR has merge commits:
   - Stash any uncommitted changes first: `git stash`
   - Rebase: `git rebase origin/<default-branch>`
   - If conflicts occur:
     - List the conflicted files
     - Ask the user to resolve conflicts manually
     - Continue rebase: `git rebase --continue`
   - Restore stashed changes: `git stash pop` (if stashed earlier)
4. **Skip rebase if** the branch is up to date with the default branch and has no merge commits.

This keeps the branch history clean with linear commits on top of the latest default branch.

#### Step 4: Stage and Commit

1. Run `git status` to see staged/unstaged changes
2. If no files are staged, stage all changes (`git add -A`) — do NOT ask the user unless there is a clear reason to stage selectively (e.g., mix of unrelated changes)
3. Auto-detect the commit prefix from the changed files and context:
   - Only documentation files changed → `doc:`
   - Performance-related changes (caching, optimization) → `perf:`
   - New feature code → `feat:`
   - Bug fix → `fix:`
   - Config, deps, tooling → `chore:`
   - Modifying existing behavior → `amend:`
   - Release-related → `release:`
4. Generate a concise commit message: `<prefix>: <description>`
5. Show the proposed commit message and ask user to confirm or adjust
6. Create the commit

#### Step 5: Push

1. Ask if user wants to push to remote
2. If yes, and the branch was rebased in Step 3, use force push: `git push --force-with-lease origin <current-branch>`
3. If yes, and no rebase occurred, use normal push: `git push origin <current-branch>`
4. After successful push, output merge request URL: `bash scripts/generate-mr-url.sh`
5. Confirm the commit (and push) to the user

**Autonomy principle:** The AI should make reasonable decisions (staging, prefix, branch, rebase) on its own and only ask the user when the choice is genuinely unclear. Do not ask for things that can be inferred from context.

### sync-features (alias: sync)
Synchronize all active feature branches with latest master.

Steps:
1. Fetch latest changes from remote: `git fetch origin`
2. Update local master: `git checkout master && git pull origin master`
3. Identify active feature branches:
   - Run the built-in script: `bash scripts/detect-active-branches.sh`
   - Or manually: Get the latest 10 commits on master, check each feature branch's merge-base and ahead commits
   - Show the list of active branches to user and ask for confirmation
4. For each confirmed active feature branch:
   - Checkout the feature branch and fetch: `git checkout <branch> && git fetch origin <branch>`
   - Rebase onto master: `git rebase master`
   - If conflicts occur:
     - List the conflicted files
     - Ask the user to resolve conflicts manually
     - Wait for user confirmation that conflicts are resolved
     - Continue rebase: `git rebase --continue`
   - Force push to remote (after confirming with user): `git push --force-with-lease origin <branch-name>`
   - Output merge request URL: `bash scripts/generate-mr-url.sh <branch-name>`
5. Return to the original branch
6. Provide a summary of all synchronized branches

**IMPORTANT:** Always confirm before force-pushing each branch.

### consolidate-branch (alias: consolidate, rebuild)
Reset a target branch to a feature branch and merge all other active features. Also triggered by "rebuild [branch]".

Steps:
1. Ask user for target branch name (default: 'dev' if not specified)
2. Fetch latest changes from remote: `git fetch origin`
3. Update local master: `git checkout master && git pull origin master`
4. Identify active feature branches:
   - Run the built-in script: `bash scripts/detect-active-branches.sh`
   - Or manually: Get the latest 10 commits on master, check each feature branch's merge-base and ahead commits
5. If no active feature branches exist, inform the user and exit
6. Show the list of active feature branches to user and ask for confirmation to proceed
7. **Rebase each active feature branch onto latest master first:**
   - For each active feature branch:
     - Checkout the branch and fetch: `git checkout <branch> && git fetch origin <branch>`
     - Rebase onto master: `git rebase master`
     - If conflicts occur, ask user to resolve and continue
     - Force push to remote (after confirming): `git push --force-with-lease origin <branch>`
     - Output merge request URL: `bash scripts/generate-mr-url.sh <branch>`
8. Ask the user which feature branch to use as the base (or use the first one)
9. Check if target branch exists, create it if it doesn't
10. Checkout target branch and fetch: `git checkout <target-branch> && git fetch origin <target-branch>`
11. **CONFIRM with user:** This will reset <target-branch> to the selected feature branch
12. Hard reset target branch to the base feature branch: `git reset --hard <base-feature>`
13. For each other feature branch (excluding the base):
    - Merge the feature branch into target branch: `git merge --no-ff <feature-branch>`
    - If conflicts occur:
      - List the conflicted files
      - Ask the user to resolve conflicts manually
      - Wait for user confirmation
      - Complete the merge: `git merge --continue`
14. Ask if user wants to push target branch to remote
15. If pushed, output merge request URL: `bash scripts/generate-mr-url.sh <target-branch>`
16. Provide summary of consolidated branches

**IMPORTANT:** This is a destructive operation. Always confirm before resetting the target branch.

### sync-and-consolidate (alias: full-sync)
Perform both feature branch synchronization and branch consolidation.

This combines two operations:
1. Feature Branch Synchronization - Rebase all feature branches on latest master
2. Branch Consolidation - Consolidate all feature branches into a target branch

Steps:
1. Ask user for target branch name (default: 'dev' if not specified)
2. Ask user to confirm both operations
3. Execute Feature Branch Synchronization (sync-features workflow)
4. Execute Branch Consolidation (consolidate-branch workflow)
5. Provide final summary of all operations

This is useful for preparing an integration environment with all features integrated and up-to-date with master.

## Settings

- Default base branch: `master`
- Always require confirmation for destructive operations (force push, hard reset)
- Feature branch prefix: `feature/`
- Release branch prefix: `release/`
- Fix branch prefix: `fix/`
