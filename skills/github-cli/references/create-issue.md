# Create Issue (Template-Aware)

Use this flow when creating an issue and repository issue templates matter.

## Workflow

### 1. Preflight

1. Ensure `gh` exists: `gh --version`
2. Ensure auth: `gh auth status`
3. Ensure repo context is known (current repo or `-R owner/repo`)

### 2. Pick template type

Classify user intent:

- Bug report
- Feature request
- Question/discussion
- Other

If ambiguous, ask user which template type to use.

### 3. Read repository template

Read selected file under `.github/ISSUE_TEMPLATE/`.

Treat template as source of truth for:

- Required fields
- Title prefix
- Labels
- Option constraints

### 4. Build issue body

```bash
issue_body_file="$(mktemp /tmp/gh-issue-body-XXXXXX).md"
```

Fill required sections. Use `N/A` where template allows.

### 5. Preview and confirm

Show final title/body and temp file path, then ask for confirmation.

Skip confirmation only when user explicitly asks for non-interactive execution.

### 6. Create issue

Base command:

```bash
gh issue create --title "<title>" --body-file "$issue_body_file"
```

If template defines labels, append one `--label` per template label.

Cleanup:

```bash
rm -f "$issue_body_file"
```

### 7. Report

Return issue URL and summarize template/labels.

## Constraints

- Never hardcode template labels/prefixes when template exists.
- Never skip required template fields.
- Never create issue before preview/confirmation unless user waives preview.
