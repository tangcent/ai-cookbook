# ai-cookbook

A curated collection of AI skills, practical tips, and Markdown documentation — featuring recommended MCP (Model Context Protocol) configurations, examples, and best practices.

## Quick Start

1. Clone this repository

```bash
git clone https://github.com/tangcent/ai-cookbook.git
cd ai-cookbook
```

2. Tell your AI: "install ai-cookbook"
<!-- AI: Run install/INSTALL.md to install all skills and MCPs -->

## Install

Install MCPs, CLIs, and Skills into your AI coding tools (Kiro, Claude Code, Cline, OpenCode, Tare, Antigravity) with the interactive guide:

→ [install/INSTALL.md](install/INSTALL.md)

## Skills

### audit-sql

Perform a production-readiness SQL audit on MyBatis mapper XML files. Acts as a Senior Database Engineer reviewing SQL queries for index integrity, execution plan risks, concurrency/locking issues, resource pressure, and scalability concerns.

- Discover and analyze all MyBatis mapper XML and DDL schema files
- Audit each SQL statement against index usage, full table scan risks, locking hazards, and N+1 patterns
- Produce a structured report grouped by mapper file with severity ratings (CRITICAL / HIGH / MEDIUM / LOW)

> 💬 Tell your AI: "install audit-sql"
<!-- AI: Run install/INSTALL.md to install the audit-sql skill -->


### grafana-dashboard

Build and modify Grafana dashboards following established style conventions — stat panel thresholds, timeseries styling, PromQL patterns, and layout structure.

- Requires the Grafana MCP; prompts the user to enable it if unavailable
- Enforces consistent panel styling: `background_solid` stat cards, `smooth` line interpolation, `opacity` gradient fills, standard threshold colors
- Codifies PromQL conventions: `clamp_min` for safe division, `$__range` for stat totals, `histogram_quantile * 1000` for latency
- Provides dashboard templates for HTTP Performance, Business Metrics, Outbound API, Pipeline/Queue, and Validation/Quality dashboards

> 💬 Tell your AI: "install grafana-dashboard"
<!-- AI: Run install/INSTALL.md to install the grafana-dashboard skill -->


### git-workflow

Git workflow management with branch prefixes, conventional commits, and advanced synchronization operations.

- Create branches with `feature/`, `release/`, `fix/` prefixes
- Conventional commit messages (`feat:`, `fix:`, `amend:`, `chore:`, `release:`)
- Sync feature branches onto latest master, consolidate branches, and generate merge request URLs

> 💬 Tell your AI: "install git-workflow"
<!-- AI: Run install/INSTALL.md to install the git-workflow skill -->


### github-cli

Interact with GitHub via the `gh` CLI — manage repositories, issues, pull requests, releases, code search, and API calls.

- Create, review, and merge pull requests
- Create and manage issues with labels, assignees, and comments
- Search code, issues, PRs, and repositories
- Manage releases, GitHub Actions workflows, and raw API calls
- Structured output with `--json` and `--jq` for programmatic use

> 💬 Tell your AI: "install github-cli"
<!-- AI: Run install/INSTALL.md to install the github-cli skill -->


### gitlab-cli

Interact with GitLab via the `glab` CLI — manage repositories, issues, merge requests, pipelines, releases, code search, and API calls.

- Create, review, and merge merge requests
- Create and manage issues with labels, assignees, and comments
- View and manage CI/CD pipelines and jobs
- Manage releases, tags, and raw GitLab API calls
- Structured output with `--output json` and `--jq` for programmatic use

> 💬 Tell your AI: "install gitlab-cli"
<!-- AI: Run install/INSTALL.md to install the gitlab-cli skill -->


### mysql-cli

Query, modify, and inspect MySQL databases via `mysql-cli`, a smart wrapper with multi-instance support and automatic database routing.

- Supports multiple MySQL instances in a single config (`~/.mysql-instances.cnf`)
- Auto-routes queries to the correct instance/database by table name
- Caches database metadata (instances, databases, tables) for fast lookup
- Execute any SQL: SELECT, INSERT, UPDATE, DELETE, ALTER TABLE, CREATE INDEX, etc.
- Execute `.sql` files with automatic target resolution
- Output as table, CSV, JSON, or vertical format

> 💬 Tell your AI: "install mysql-cli"
<!-- AI: Run install/INSTALL.md to install the mysql-cli skill -->


### playwright-cli

Automates browser interactions for web testing, form filling, screenshots, and data extraction via the `playwright-cli` CLI.

- Navigate websites, click elements, fill forms, take screenshots and PDFs
- Session management for isolating browser profiles across projects
- Request mocking, tracing, video recording, and storage state management
- Test code generation from interactive browser sessions

> 💬 Tell your AI: "install playwright-cli"
<!-- AI: Run install/INSTALL.md to install the playwright-cli skill and CLI -->


### spec-driven

Spec-driven development workflow for requirements gathering, design, task breakdown, and execution.

- Two flows: Spec (Requirements → Design → Tasks → Execute) and Plan (Plan → Execute)
- EARS-style requirement language with checkbox-based task tracking
- Artifacts saved to `.spec/<spec-name>/` with automatic scaling for large features
- Resume support — detects existing specs and continues from the last incomplete task

> 💬 Tell your AI: "install spec-driven"
<!-- AI: Run install/INSTALL.md to install the spec-driven skill -->


### markitdown

Convert various file formats (PDF, DOCX, XLSX, PPTX, HTML, images, etc.) to Markdown via CLI.

- Convert local files and URLs to Markdown
- Support for PDF, Word, Excel, PowerPoint, HTML, images, EPUB, email files
- Pipe support for integration with other tools
- Batch processing capabilities

> 💬 Tell your AI: "install markitdown"
<!-- AI: Run install/INSTALL.md to install the markitdown skill and CLI -->


### obsidian

Work with Obsidian vaults — create and edit Obsidian Flavored Markdown, Bases, JSON Canvas, and interact with vaults via the Obsidian CLI.

- Obsidian Flavored Markdown: wikilinks, embeds, callouts, properties, tags, comments, highlights
- Bases (`.base` files): database-like views with filters, formulas, and multiple view types (table, cards, list, map)
- JSON Canvas (`.canvas` files): visual canvases with text/file/link/group nodes, edges, and layout guidelines
- Obsidian CLI: read, create, search, and manage notes, tasks, properties; plugin and theme development

> 💬 Tell your AI: "install obsidian"
<!-- AI: Run install/INSTALL.md to install the obsidian skill -->


## MCPs

| MCP | Description | Docs | Quick Install |
|-----|-------------|------|---------------|
| [Maven Indexer](https://github.com/tangcent/maven-indexer-mcp) | Search classes, artifacts, and resources in local Maven/Gradle caches | [maven-indexer.md](mcp/maven-indexer.md) | 💬 "install maven-indexer" |
| [Grafana](https://github.com/grafana/mcp-grafana) | Dashboard management, Prometheus/Loki querying, alerts, and incidents | [grafana.md](mcp/grafana.md) | 💬 "install grafana" |
| [Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Browser automation, DOM interaction, network inspection, and performance tracing | [chrome-devtools.md](mcp/chrome-devtools.md) | 💬 "install chrome-devtools" |

<!-- AI: For any "install <mcp-name>" command, run install/INSTALL.md to install the specified MCP -->

## CLIs

| CLI | Description | Docs | Quick Install |
|-----|-------------|------|---------------|
| [Playwright CLI](https://github.com/microsoft/playwright-cli) | Token-efficient browser automation CLI for coding agents | [playwright-cli.md](cli/playwright-cli.md) | 💬 "install playwright-cli" |
| [GitHub CLI](https://github.com/cli/cli) | Repository management, issues, PRs, releases, and GitHub API from the terminal | [gh.md](cli/gh.md) | 💬 "install gh" |
| [GitLab CLI](https://gitlab.com/gitlab-org/cli) | Repository management, issues, MRs, pipelines, releases, and GitLab API from the terminal | [glab.md](cli/glab.md) | 💬 "install glab" |
| [MarkItDown](https://github.com/microsoft/markitdown) | Convert PDF, Word, Excel, PowerPoint, HTML, images to Markdown | [markitdown.md](cli/markitdown.md) | 💬 "install markitdown" |

<!-- AI: For any "install <cli-name>" command, run install/INSTALL.md to install the specified CLI -->
