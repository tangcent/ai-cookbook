---
name: github-cli
description: Operate GitHub from terminal with `gh` for repositories, pull requests, issues, releases, actions, and API calls. Use for any GitHub task. For template-compliant PR or issue creation, load reference workflows under references/.
---

# GitHub CLI

## Execution Policy

For GitHub tasks, use `gh` as the primary interface.

Rules:

- Always run `gh` commands before falling back to raw APIs.
- Use `gh api` instead of `curl` for GitHub REST/GraphQL.
- Do not hardcode tokens in commands or scripts.
- Confirm destructive operations (merge/close/delete/release delete).

## Preflight

1. Verify CLI and auth:
   ```bash
   gh --version
   gh auth status
   ```
2. Resolve repository context:
   - In repo: use current remote context.
   - Outside repo: require `-R owner/repo`.
3. Prefer machine-readable output when summarizing:
   - `--json ... --jq ...`

## Conditional References

Load detailed flows only when needed:

- PR creation with template compliance:
  - read `references/create-pr.md`
- Issue creation with template compliance:
  - read `references/create-issue.md`

Keep this file focused on common `gh` operations and routing.

## High-Value Commands

```bash
# Repository
gh repo view
gh repo clone owner/repo
gh repo create my-repo --public --description "My new repo"
gh repo fork owner/repo
gh repo list owner --limit 20
gh browse

# Pull requests
gh pr list
gh pr list --state all
gh pr view 42
gh pr view 42 --json title,state,body,reviews
gh pr diff 42
gh pr checkout 42
gh pr review 42 --approve
gh pr merge 42 --squash
gh pr merge 42 --squash --delete-branch
gh pr close 42

# Issues
gh issue list
gh issue view 123
gh issue view 123 --json title,state,body,comments
gh issue close 123
gh issue reopen 123
gh issue comment 123 --body "I can reproduce this"

# Search
gh search code "functionName" --repo owner/repo
gh search issues "memory leak" --repo owner/repo
gh search prs "fix auth" --state merged --author username

# Releases
gh release list
gh release view v1.2.3
gh release create v1.2.3 --title "Release v1.2.3" --notes "Changelog..."
gh release create v1.2.3 --generate-notes
gh release upload v1.2.3 ./dist/app.zip
gh release delete v1.2.3 --yes

# Actions
gh workflow list
gh workflow view "CI"
gh workflow run "CI" --ref main
gh run list
gh run view 12345
gh run watch 12345
gh run view 12345 --log
gh run rerun 12345
gh run cancel 12345
```

## Common Workflows

### Review and merge a PR

1. Inspect:
   ```bash
   gh pr view <number> --json title,author,mergeStateStatus,url
   gh pr diff <number>
   ```
2. Approve/comment:
   ```bash
   gh pr review <number> --approve
   ```
3. Merge (confirm strategy with user if not specified):
   ```bash
   gh pr merge <number> --squash --delete-branch
   ```

### Investigate an issue

1. Read issue:
   ```bash
   gh issue view <number> --json title,body,labels,assignees,url
   ```
2. Search related PR/code:
   ```bash
   gh search prs "<keyword>" --repo owner/repo --state all
   gh search code "<keyword>" --repo owner/repo
   ```

### Monitor CI

```bash
gh run list --limit 10
gh run watch <run-id>
gh run view <run-id> --log-failed
```

## Troubleshooting

- `gh: command not found` -> install `gh`.
- `not logged in` -> `gh auth login`.
- Wrong repo context -> use `-R owner/repo`.
- Missing scopes -> `gh auth refresh -s <scope>`.
