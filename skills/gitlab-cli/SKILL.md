---
name: gitlab-cli
description: Interact with GitLab via the `glab` CLI — manage repositories, issues, merge requests, pipelines, releases, code search, and API calls. Use when the user asks to create MRs, check issues, manage pipelines, manage releases, or perform any GitLab operation.
---

# GitLab CLI Skill

## When to Activate

Activate this skill when the user asks to:

- Create, view, list, or merge merge requests (MRs)
- Create, view, list, or close issues
- Search for code, issues, MRs, or repositories
- Check repository info, branches, or commits
- Create or manage releases and tags
- View or manage CI/CD pipelines and jobs
- Make raw GitLab API calls
- Fork, clone, or create repositories
- Review or comment on merge requests

## Prerequisites

- `glab` must be installed and available in PATH.
- The user must be authenticated (`glab auth status` should show a logged-in account).
- If not authenticated, detect the GitLab hostname (see below) and guide the user to run `glab auth login --hostname <detected-host>`.

## Hard Rule

For GitLab tasks, **always use `glab` CLI**.

- Do **not** use a GitLab MCP server — it has been replaced by this CLI skill.
- Do **not** use `curl` with raw GitLab API URLs — use `glab api` instead (it handles auth automatically).
- Do **not** hardcode tokens or auth headers — `glab` manages authentication.

## Authentication

When this skill is activated, the workspace is likely a GitLab repository. Detect the GitLab hostname automatically from the git remote:

```bash
# Extract the GitLab hostname from the current repo's remote URL
# Handles both SSH (git@host:owner/repo.git) and HTTPS (https://host/owner/repo.git)
git remote get-url origin 2>/dev/null | sed -E 's#^https?://([^/]+)/.*#\1#; s#^[^@]+@([^:]+):.*#\1#'
```

Use the detected hostname for all auth commands below. If detection fails (not in a git repo), ask the user for their GitLab hostname.

```bash
# Check current auth status
glab auth status

# Interactive login (recommended) — replace <hostname> with detected value
glab auth login --hostname <hostname>

# Login with a personal access token
# Create at: https://<hostname>/-/profile/personal_access_tokens
# Scopes needed: api, read_user, read_repository, write_repository
glab auth login --hostname <hostname> --token <token>
```

If `glab auth status` shows no active account for the detected hostname, ask the user to authenticate before proceeding.

## Command Reference

### Repository Operations

```bash
# View current repository info
glab repo view

# View a specific repository
glab repo view owner/repo

# Clone a repository
glab repo clone owner/repo

# Create a new repository
glab repo create my-repo --description "My new repo"

# Fork a repository
glab repo fork owner/repo

# List repositories
glab repo list --group my-group

# Open repo in browser
glab browse
```

### Merge Requests

```bash
# Create a merge request (interactive)
glab mr create

# Create with all options specified
glab mr create --title "Add feature" --description "Description" --target-branch main --source-branch feature-branch

# Create as draft
glab mr create --title "Draft: feature" --draft

# List merge requests
glab mr list
glab mr list --state all
glab mr list --author @me
glab mr list --label bug --limit 20

# View a merge request
glab mr view 42
glab mr view 42 --output json

# Check out an MR locally
glab mr checkout 42

# Approve an MR
glab mr approve 42

# Revoke approval
glab mr revoke 42

# Merge an MR
glab mr merge 42 --squash
glab mr merge 42 --rebase
glab mr merge 42 --squash --remove-source-branch

# Close an MR
glab mr close 42

# Reopen an MR
glab mr reopen 42

# Add labels, assignees, reviewers
glab mr update 42 --label "enhancement" --assignee @me --reviewer teammate

# Add a note/comment
glab mr note 42 --message "Looks good to me"
```

### Issues

```bash
# Create an issue (interactive)
glab issue create

# Create with options
glab issue create --title "Bug: login fails" --description "Steps to reproduce..." --label bug --assignee @me

# List issues
glab issue list
glab issue list --label bug --state opened
glab issue list --assignee @me --limit 50

# View an issue
glab issue view 123
glab issue view 123 --output json

# Close an issue
glab issue close 123

# Reopen an issue
glab issue reopen 123

# Add a note/comment
glab issue note 123 --message "I can reproduce this"

# Edit an issue
glab issue update 123 --label "priority:high" --assignee teammate
```

### CI/CD Pipelines

```bash
# View pipeline status for current branch
glab ci view

# View pipeline status (compact)
glab ci status

# List pipelines
glab ci list

# Trigger a new pipeline
glab ci run

# Trigger with variables
glab ci run --variables KEY=value

# View a specific pipeline
glab ci view <pipeline-id>

# View pipeline jobs
glab ci view --output json

# Retry a failed pipeline
glab ci retry <pipeline-id>

# Cancel a running pipeline
glab ci cancel <pipeline-id>

# View job logs
glab ci trace <job-id>

# List pipeline jobs
glab ci job list
```

### Releases & Tags

```bash
# List releases
glab release list

# View a release
glab release view v1.2.3

# Create a release
glab release create v1.2.3 --name "Release v1.2.3" --notes "Changelog..."

# Create a release from a tag
glab release create v1.2.3 --ref main

# Upload assets to a release
glab release upload v1.2.3 ./dist/app.zip

# Delete a release
glab release delete v1.2.3
```

### Branches & Commits

```bash
# List branches (use git directly)
git branch -a

# View a commit via API
glab api projects/:id/repository/commits/<sha> --jq '.message'

# Compare branches via API
glab api projects/:id/repository/compare --field from=main --field to=feature-branch

# Browse commits in the browser
glab browse --commits
```

### Raw API Access

Use `glab api` for any GitLab REST API call. Authentication is handled automatically.

```bash
# REST API — GET
glab api projects/:id
glab api projects/:id/repository/commits --jq '.[0].id'

# REST API — POST
glab api projects/:id/issues --method POST --field title="New issue" --field description="Details"

# REST API — with pagination
glab api projects/:id/issues --paginate --jq '.[].title'

# Use :id as a shorthand for the current project's numeric ID
glab api projects/:id/merge_requests --jq '.[].title'
```

### Snippets (Gists equivalent)

```bash
# Create a snippet
glab snippet create --title "My snippet" --filename file.txt

# List snippets
glab snippet list

# View a snippet
glab snippet view <snippet-id>
```

## Output Formatting

`glab` supports structured output via `--output json` and `--jq` flags on most commands:

```bash
# Get MR data as JSON
glab mr view 42 --output json

# Use jq to extract specific fields
glab mr list --output json | jq '.[] | "\(.iid): \(.title)"'

# Get issue count
glab issue list --output json | jq 'length'
```

Prefer `--output json` + `jq` when results will be processed programmatically or presented in a structured way.

## Workflows

### Create an MR from Current Branch

1. Ensure changes are committed and pushed:
   ```bash
   git push origin HEAD
   ```
2. Create the MR:
   ```bash
   glab mr create --title "<title>" --description "<description>"
   ```
3. Confirm creation by viewing it:
   ```bash
   glab mr view --output json | jq '.web_url'
   ```

### Review and Merge an MR

1. Check out the MR locally:
   ```bash
   glab mr checkout <number>
   ```
2. Review the code, run tests.
3. Approve and merge:
   ```bash
   glab mr approve <number>
   glab mr merge <number> --squash --remove-source-branch
   ```

### Investigate an Issue

1. View the issue details:
   ```bash
   glab issue view <number>
   ```
2. Check related MRs:
   ```bash
   glab mr list --search "<keyword>"
   ```

### Monitor a CI Pipeline

1. View current pipeline status:
   ```bash
   glab ci view
   ```
2. Watch pipeline in real-time:
   ```bash
   glab ci view --live
   ```
3. If a job failed, view its logs:
   ```bash
   glab ci trace <job-id>
   ```
4. Retry if needed:
   ```bash
   glab ci retry <pipeline-id>
   ```

## Troubleshooting

- **"glab: command not found"** → Install via `brew install glab` (macOS), `sudo apt install glab` (Linux), or see [gitlab-org/cli installation](https://gitlab.com/gitlab-org/cli#installation).
- **"not logged in"** → Run `glab auth login` and follow the prompts.
- **"insufficient permissions"** → The token may lack required scopes. Create a new PAT with the needed scopes (api, read_user, read_repository, write_repository) at `https://<hostname>/-/profile/personal_access_tokens`.
- **"API rate limit exceeded"** → Wait for the reset window, or use a PAT with higher limits.
- **Wrong repository context** → `glab` auto-detects the repo from the current git remote. Use `-R owner/repo` to override: `glab mr list -R owner/repo`.
- **Self-hosted GitLab** → Detect the hostname from `git remote get-url origin`, then authenticate with `glab auth login --hostname <detected-host>`.
- **"could not determine base repo"** → You are not inside a git repository, or the remote is not a GitLab URL. Use `-R owner/repo` explicitly.
