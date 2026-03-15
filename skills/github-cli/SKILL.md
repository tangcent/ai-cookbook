---
name: github-cli
description: Interact with GitHub via the `gh` CLI — manage repositories, issues, pull requests, releases, code search, and API calls. Use when the user asks to create PRs, check issues, search code, manage releases, or perform any GitHub operation.
---

# GitHub CLI Skill

## When to Activate

Activate this skill when the user asks to:

- Create, view, list, or merge pull requests
- Create, view, list, or close issues
- Search for code, issues, PRs, or repositories
- Check repository info, branches, or commits
- Create or manage releases and tags
- View or manage GitHub Actions workflows and runs
- Make raw GitHub API calls
- Fork, clone, or create repositories
- Review or comment on pull requests

## Prerequisites

- `gh` must be installed and available in PATH.
- The user must be authenticated (`gh auth status` should show a logged-in account).
- If not authenticated, guide the user to run `gh auth login`.

## Hard Rule

For GitHub tasks, **always use `gh` CLI**.

- Do **not** use the GitHub MCP server — it has been replaced by this CLI skill.
- Do **not** use `curl` with raw GitHub API URLs — use `gh api` instead (it handles auth automatically).
- Do **not** hardcode tokens or auth headers — `gh` manages authentication.

## Authentication

```bash
# Check current auth status
gh auth status

# Interactive login (recommended)
gh auth login

# Login with a personal access token
echo "<token>" | gh auth login --with-token

# Switch between accounts
gh auth switch
```

If `gh auth status` shows no active account, ask the user to authenticate before proceeding.

## Command Reference

### Repository Operations

```bash
# View current repository info
gh repo view

# View a specific repository
gh repo view owner/repo

# Clone a repository
gh repo clone owner/repo

# Create a new repository
gh repo create my-repo --public --description "My new repo"

# Fork a repository
gh repo fork owner/repo

# List repositories
gh repo list owner --limit 20

# Open repo in browser
gh browse
```

### Pull Requests

```bash
# Create a pull request (interactive)
gh pr create

# Create with all options specified
gh pr create --title "Add feature" --body "Description" --base main --head feature-branch

# Create as draft
gh pr create --title "WIP: feature" --draft

# List pull requests
gh pr list
gh pr list --state all
gh pr list --author @me
gh pr list --label bug --limit 20

# View a pull request
gh pr view 42
gh pr view 42 --json title,state,body,reviews

# View PR diff
gh pr diff 42

# Check out a PR locally
gh pr checkout 42

# Review a PR
gh pr review 42 --approve
gh pr review 42 --request-changes --body "Please fix the typo"
gh pr review 42 --comment --body "Looks good overall"

# Merge a PR
gh pr merge 42 --squash
gh pr merge 42 --merge
gh pr merge 42 --rebase
gh pr merge 42 --squash --delete-branch

# Close a PR
gh pr close 42

# Add labels, assignees, reviewers
gh pr edit 42 --add-label "enhancement" --add-assignee @me --add-reviewer teammate
```

### Issues

```bash
# Create an issue (interactive)
gh issue create

# Create with options
gh issue create --title "Bug: login fails" --body "Steps to reproduce..." --label bug --assignee @me

# List issues
gh issue list
gh issue list --label bug --state open
gh issue list --assignee @me --limit 50

# View an issue
gh issue view 123
gh issue view 123 --json title,state,body,comments

# Close an issue
gh issue close 123

# Reopen an issue
gh issue reopen 123

# Add a comment
gh issue comment 123 --body "I can reproduce this"

# Edit an issue
gh issue edit 123 --add-label "priority:high" --add-assignee teammate

# Pin/unpin an issue
gh issue pin 123
gh issue unpin 123

# Transfer an issue to another repo
gh issue transfer 123 owner/other-repo
```

### Search

```bash
# Search code
gh search code "functionName" --repo owner/repo
gh search code "import React" --language javascript --limit 20

# Search issues
gh search issues "memory leak" --repo owner/repo
gh search issues "bug" --state open --label "priority:high"

# Search PRs
gh search prs "fix auth" --state merged --author username

# Search repositories
gh search repos "machine learning" --language python --sort stars

# Search commits
gh search commits "fix typo" --repo owner/repo
```

### Releases & Tags

```bash
# List releases
gh release list

# View a release
gh release view v1.2.3

# Create a release
gh release create v1.2.3 --title "Release v1.2.3" --notes "Changelog..."
gh release create v1.2.3 --generate-notes

# Create a draft release
gh release create v1.2.3 --draft --title "Release v1.2.3"

# Upload assets to a release
gh release upload v1.2.3 ./dist/app.zip

# Delete a release
gh release delete v1.2.3 --yes
```

### GitHub Actions (Workflows & Runs)

```bash
# List workflows
gh workflow list

# View a workflow
gh workflow view "CI"

# Run a workflow
gh workflow run "CI" --ref main

# List workflow runs
gh run list
gh run list --workflow "CI" --limit 10

# View a specific run
gh run view 12345

# Watch a run in progress
gh run watch 12345

# View run logs
gh run view 12345 --log

# Re-run a failed run
gh run rerun 12345

# Cancel a run
gh run cancel 12345
```

### Branches & Commits

```bash
# List branches (use git directly — gh doesn't have a branch list command)
git branch -a

# View a commit
gh api repos/{owner}/{repo}/commits/<sha> --jq '.commit.message'

# Compare branches
gh api repos/{owner}/{repo}/compare/main...feature-branch --jq '.commits[].commit.message'

# Browse commits in the browser
gh browse --commit <sha>
```

### Raw API Access

Use `gh api` for any GitHub REST or GraphQL API call. Authentication is handled automatically.

```bash
# REST API — GET
gh api repos/owner/repo
gh api repos/owner/repo/commits --jq '.[0].sha'

# REST API — POST
gh api repos/owner/repo/issues --method POST --field title="New issue" --field body="Details"

# REST API — with pagination
gh api repos/owner/repo/issues --paginate --jq '.[].title'

# GraphQL
gh api graphql -f query='
  query {
    repository(owner: "owner", name: "repo") {
      issues(first: 5, states: OPEN) {
        nodes { title url }
      }
    }
  }
'
```

### Gists

```bash
# Create a gist
gh gist create file.txt --public --desc "My gist"

# List gists
gh gist list

# View a gist
gh gist view <gist-id>

# Edit a gist
gh gist edit <gist-id>
```

## Output Formatting

`gh` supports structured output via `--json` and `--jq` flags on most commands:

```bash
# Get PR data as JSON
gh pr view 42 --json title,state,author,url

# Use jq to extract specific fields
gh pr list --json number,title --jq '.[] | "\(.number): \(.title)"'

# Get issue count
gh issue list --state open --json number --jq 'length'
```

Prefer `--json` + `--jq` when results will be processed programmatically or presented in a structured way.

## Workflows

### Create a PR from Current Branch

1. Ensure changes are committed and pushed:
   ```bash
   git push origin HEAD
   ```
2. Create the PR:
   ```bash
   gh pr create --title "<title>" --body "<description>"
   ```
3. Confirm creation by viewing it:
   ```bash
   gh pr view --json url --jq '.url'
   ```

### Review and Merge a PR

1. Check out the PR locally:
   ```bash
   gh pr checkout <number>
   ```
2. Review the code, run tests.
3. Approve and merge:
   ```bash
   gh pr review <number> --approve
   gh pr merge <number> --squash --delete-branch
   ```

### Investigate an Issue

1. View the issue details:
   ```bash
   gh issue view <number>
   ```
2. Search related code:
   ```bash
   gh search code "<keyword>" --repo owner/repo
   ```
3. Check related PRs:
   ```bash
   gh search prs "<keyword>" --repo owner/repo --state all
   ```

### Monitor a CI Run

1. List recent runs:
   ```bash
   gh run list --limit 5
   ```
2. Watch a run in real-time:
   ```bash
   gh run watch <run-id>
   ```
3. If failed, view logs:
   ```bash
   gh run view <run-id> --log-failed
   ```
4. Re-run if needed:
   ```bash
   gh run rerun <run-id>
   ```

## Troubleshooting

- **"gh: command not found"** → Install via `brew install gh` (macOS), `sudo apt install gh` (Linux), or see [cli/cli installation](https://github.com/cli/cli#installation).
- **"not logged in"** → Run `gh auth login` and follow the prompts.
- **"insufficient permissions"** → The token may lack required scopes. Run `gh auth refresh -s <scope>` to add scopes (e.g. `-s admin:org`).
- **"API rate limit exceeded"** → Wait for the reset window, or authenticate with a PAT that has higher limits.
- **Wrong repository context** → `gh` auto-detects the repo from the current git remote. Use `-R owner/repo` to override: `gh pr list -R owner/repo`.
- **"could not determine base repo"** → You are not inside a git repository, or the remote is not a GitHub URL. Use `-R owner/repo` explicitly.
