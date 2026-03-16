# GitLab CLI

- GitLab: [gitlab-org/cli](https://gitlab.com/gitlab-org/cli)

GitLab CLI (`glab`) brings GitLab to the terminal — manage repositories, issues, merge requests, pipelines, releases, and more without leaving your workflow. It replaces the need for a GitLab MCP server by providing direct, scriptable access to the GitLab API.

## Key Features

- Create and manage repositories, branches, and forks
- Open, review, and merge merge requests
- Create and manage issues with labels and assignees
- View and manage CI/CD pipelines and jobs
- Browse and manage releases and tags
- Authenticate via `glab auth login` (OAuth or PAT)
- Supports self-hosted GitLab instances

## Common Commands

| Command | Description |
|---------|-------------|
| `glab repo clone <repo>` | Clone a repository |
| `glab repo view <repo>` | View repository details |
| `glab mr create` | Create a new merge request |
| `glab mr list` | List merge requests |
| `glab mr view <number>` | View merge request details |
| `glab mr merge <number>` | Merge a merge request |
| `glab issue create` | Create a new issue |
| `glab issue list` | List issues |
| `glab issue view <number>` | View issue details |
| `glab release create <tag>` | Create a new release |
| `glab release list` | List releases |
| `glab ci view` | View pipeline status |
| `glab ci list` | List pipelines |
| `glab api <endpoint>` | Make authenticated API requests |
| `glab browse` | Open the repository in the browser |

## Installation

```bash
# Via Homebrew (recommended)
brew install glab

# Or via Go
go install gitlab.com/gitlab-org/cli/cmd/glab@main

# Or via pip
pip install glab
```

## Authentication

```bash
# Interactive login (recommended)
glab auth login

# Login to a self-hosted instance
glab auth login --hostname gitlab.example.com

# Login with a personal access token
glab auth login --hostname gitlab.example.com --token <token>

# Check auth status
glab auth status
```

## Usage Examples

```bash
# Clone a repo and create a feature branch
glab repo clone owner/repo
cd repo
git checkout -b feature/my-feature

# Create a merge request
glab mr create --title "Add feature" --description "Description of changes"

# Review and merge
glab mr approve 42
glab mr merge 42 --squash --remove-source-branch

# Create an issue
glab issue create --title "Bug report" --label bug --assignee @me

# View CI/CD pipeline status
glab ci view

# Make a raw API call
glab api projects/:id/repository/commits --jq '.[0].id'
```
