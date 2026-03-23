---
name: gitlab-cli
description: Operate GitLab from terminal with `glab` for repositories, merge requests, issues, pipelines, releases, and API calls. Use for any GitLab task. For template-compliant MR creation, load reference workflow under references/.
---

# GitLab CLI

## Execution Policy

For GitLab tasks, use `glab` as the primary interface.

Rules:

- Always try `glab` first.
- Use `glab api` instead of raw `curl` for GitLab API calls.
- Do not hardcode tokens in commands.
- Confirm destructive actions (merge/close/delete/cancel).

## Preflight

1. Verify CLI:
   ```bash
   glab --version
   ```
2. Detect GitLab hostname from remote:
   ```bash
   host="$(git remote get-url origin 2>/dev/null | sed -E 's#^https?://([^/]+)/.*#\1#; s#^[^@]+@([^:]+):.*#\1#')"
   ```
3. Verify auth for host:
   ```bash
   glab auth status --hostname "$host"
   ```
4. Resolve repository context:
   - inside repo: auto-detected
   - outside repo: use `-R group/project`

## Conditional Reference

For MR creation with `.gitlab/merge_request_templates/*`, read:

- `references/create-mr.md`

Keep this file focused on general `glab` operations and routing.

## High-Value Commands

```bash
# Repository
glab repo view
glab repo clone owner/repo
glab repo create my-repo --description "My new repo"
glab repo fork owner/repo
glab repo list --group my-group
glab browse

# Merge requests
glab mr list
glab mr list --state all
glab mr view 42
glab mr view 42 --output json
glab mr checkout 42
glab mr approve 42
glab mr merge 42 --squash
glab mr merge 42 --squash --remove-source-branch
glab mr close 42
glab mr reopen 42
glab mr note 42 --message "Looks good to me"

# Issues
glab issue list
glab issue view 123
glab issue view 123 --output json
glab issue close 123
glab issue reopen 123
glab issue note 123 --message "I can reproduce this"

# Pipelines
glab ci status
glab ci list
glab ci run
glab ci run --variables KEY=value
glab ci view <pipeline-id>
glab ci retry <pipeline-id>
glab ci cancel <pipeline-id>
glab ci trace <job-id>

# Releases
glab release list
glab release view v1.2.3
glab release create v1.2.3 --name "Release v1.2.3" --notes "Changelog..."
glab release create v1.2.3 --ref main
glab release upload v1.2.3 ./dist/app.zip
glab release delete v1.2.3
```

## Common Workflows

### Review and merge MR

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

### Investigate issue

1. View the issue details:
   ```bash
   glab issue view <number>
   ```
2. Check related MRs:
   ```bash
   glab mr list --search "<keyword>"
   ```

### Monitor pipeline

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

- `glab: command not found` -> install `glab`.
- `not logged in` -> `glab auth login --hostname <host>`.
- wrong repo context -> use `-R group/project`.
- insufficient permissions -> refresh PAT scopes (`api`, repository scopes).
