# GitHub CLI

- GitHub: [cli/cli](https://github.com/cli/cli)

GitHub CLI (`gh`) brings GitHub to the terminal — manage repositories, issues, pull requests, releases, gists, and more without leaving your workflow. It replaces the need for a GitHub MCP server by providing direct, scriptable access to the GitHub API.

## Key Features

- Create and manage repositories, branches, and forks
- Open, review, and merge pull requests
- Create and manage issues with labels and assignees
- Browse and manage releases and tags
- Authenticate via `gh auth login` (OAuth or PAT)
- Extensible with custom aliases and extensions

## Common Commands

| Command | Description |
|---------|-------------|
| `gh repo clone <repo>` | Clone a repository |
| `gh repo view <repo>` | View repository details |
| `gh pr create` | Create a new pull request |
| `gh pr list` | List pull requests |
| `gh pr view <number>` | View pull request details |
| `gh pr merge <number>` | Merge a pull request |
| `gh issue create` | Create a new issue |
| `gh issue list` | List issues |
| `gh issue view <number>` | View issue details |
| `gh release create <tag>` | Create a new release |
| `gh release list` | List releases |
| `gh api <endpoint>` | Make authenticated API requests |
| `gh browse` | Open the repository in the browser |
| `gh search repos <query>` | Search for repositories |
| `gh search issues <query>` | Search for issues |

## Installation

```bash
# Via Homebrew (recommended)
brew install gh

# Or via Conda
conda install gh --channel conda-forge

# Or via Spack
spack install gh
```

## Authentication

```bash
# Interactive login (recommended)
gh auth login

# Login with a personal access token
gh auth login --with-token < token.txt

# Check auth status
gh auth status
```

## Usage Examples

```bash
# Clone a repo and create a feature branch
gh repo clone owner/repo
cd repo
git checkout -b feature/my-feature

# Create a pull request
gh pr create --title "Add feature" --body "Description of changes"

# Review and merge
gh pr review 42 --approve
gh pr merge 42 --squash

# Create an issue
gh issue create --title "Bug report" --label bug --assignee @me

# Make a raw API call
gh api repos/owner/repo/commits --jq '.[0].sha'

# Search for code
gh search code "function_name" --repo owner/repo
```

## Extensions

GitHub CLI supports community-built extensions:

```bash
# Browse available extensions
gh extension browse

# Install an extension
gh extension install owner/extension-name

# List installed extensions
gh extension list
```
