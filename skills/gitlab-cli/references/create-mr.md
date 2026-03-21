# Create MR (Template-Aware)

Use this flow when creating/updating an MR and template compliance matters.

## Workflow

### 1. Preflight

1. Ensure `glab` exists: `glab --version`
2. Detect hostname from `git remote get-url origin`
3. Ensure auth for hostname: `glab auth status --hostname <host>`
4. Detect head branch: `git branch --show-current`

### 2. Determine target branch and target project

Use this decision flow:

1. If user explicitly provides target branch/project, use it.
2. Read current project metadata:
   ```bash
   glab api projects/:id --output json
   ```
3. Default target branch:
   - `.default_branch` from project metadata
   - fallback to `origin/HEAD`
   - then fallback to `main`
4. Determine whether current repo is a fork:
   - if `.forked_from_project` exists, treat current repo as fork
   - inspect remotes: `git remote -v`
   - if `upstream` remote exists, prefer upstream project as target
   - otherwise prefer `.forked_from_project.path_with_namespace` and confirm with user
5. If base target is not clearly default, ask user to confirm target project/branch.

When creating an MR from fork branch to upstream target, use explicit repo/head:

```bash
glab mr create \
  -R <upstream-group>/<upstream-project> \
  --target-branch <target-branch> \
  --head <fork-group>/<fork-project> \
  --source-branch <head-branch> ...
```

For non-fork or same-project flow, create MR in current project context.

### 3. Read MR template (if present)

Check `.gitlab/merge_request_templates/*.md`:

- One template: use it
- Multiple templates: select by intent or ask user
- None: use concise body (Summary / Testing / Risks)

### 4. Ensure branch is pushed

Run only if upstream is missing:

```bash
git push -u origin <head-branch>
```

### 5. Draft description in temp file

```bash
mr_body_file="$(mktemp /tmp/glab-mr-body-XXXXXX).md"
```

Preserve template headings/structure. Fill unknown fields as `N/A` or `None`.

### 6. Preview and confirm

Show temp file path and final title/description.

Skip confirmation only when user explicitly asks for non-interactive execution.

### 7. Create MR

Use the fork-target command variant above when MR target project is upstream.
Use the command below for same-project MRs:

```bash
glab mr create \
  --target-branch <target-branch> \
  --source-branch <head-branch> \
  --title "<title>" \
  --description "$(cat "$mr_body_file")"
```

Cleanup:

```bash
rm -f "$mr_body_file"
```

### 8. Report

Return MR URL and summarize title/source/target.

## Constraints

- Never skip template sections when template exists.
- Never create MR before preview/confirmation unless user waives preview.
- Never use raw `curl` for GitLab API when `glab` can do it.
