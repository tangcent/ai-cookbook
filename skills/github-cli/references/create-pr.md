# Create PR (Template-Aware)

Use this flow when creating/updating a PR and template compliance matters.

## Workflow

### 1. Preflight

1. Ensure `gh` exists: `gh --version`
2. Ensure auth: `gh auth status`
3. Detect head branch: `git branch --show-current`

### 2. Determine base branch and base repository

Use this decision flow:

1. If user explicitly provides a base branch (or base repo), use it.
2. Detect repository metadata:
   ```bash
   gh repo view --json nameWithOwner,isFork,defaultBranchRef,parent
   ```
3. If `isFork=false` (official repo as `origin`):
   - default base repo: current repo
   - default base branch: `.defaultBranchRef.name` (typically `main`)
4. If `isFork=true` (fork as `origin`):
   - inspect remotes: `git remote -v`
   - if `upstream` remote exists, default base repo to upstream parent (`.parent.nameWithOwner`)
   - default base branch to upstream default branch (or `main` fallback)
   - if no upstream remote exists, still prefer parent repo from `gh repo view` and confirm with user
5. If the resolved base is not clearly default, ask user to confirm base branch/repo before creating the PR.

When creating PRs from a fork to upstream, pass explicit repo context:

```bash
gh pr create -R <upstream-owner>/<upstream-repo> --base <base-branch> --head <fork-owner>:<head-branch> ...
```

### 3. Read PR template

If `.github/pull_request_template.md` exists, preserve section order and markdown structure exactly.

If no template exists, use a concise body:

- Summary
- Testing
- Risks / rollback

### 4. Ensure branch is pushed

If upstream is missing:

```bash
git push -u origin <head-branch>
```

### 5. Draft body in temp file

```bash
pr_body_file="$(mktemp /tmp/gh-pr-body-XXXXXX).md"
```

Fill all sections. Use `N/A` or `None` when data is unavailable.

### 6. Preview and confirm

Show full body and temp file path, then ask for confirmation.

Skip confirmation only when user explicitly asks for non-interactive execution.

### 7. Create PR

```bash
gh pr create --base <base> --head <head> --title "<title>" --body-file "$pr_body_file"
```

Cleanup:

```bash
rm -f "$pr_body_file"
```

### 8. Report

Return PR URL and summarize title/base/head.

## Constraints

- Never skip template sections when template exists.
- Never create PR before preview/confirmation unless user waives preview.
- Never use raw `curl` for GitHub API when `gh` can do it.
