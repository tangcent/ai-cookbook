---
name: git-workflow
description: Git workflow management with branch prefixes, conventional commits, and advanced synchronization operations. Use when user asks to create branches, make commits, sync features, consolidate branches, or rebuild integration branches.
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

Steps:
1. Run git status to see staged/unstaged changes
2. If no files are staged, ask what files to add or stage all changes
3. Ask the user for the commit type and message if not provided
4. Format the commit message as: `<prefix>: <description>`
5. Create the commit
6. Ask if user wants to push to remote
7. If yes, push the current branch: `git push origin <current-branch>`
8. After successful push, output merge request URL: `bash scripts/generate-mr-url.sh`
9. Confirm the commit (and push) to the user

If the user provides a message without a prefix, ask which prefix to use.

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
