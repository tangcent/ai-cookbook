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


### git-workflow

Git workflow management with branch prefixes, conventional commits, and advanced synchronization operations.

- Create branches with `feature/`, `release/`, `fix/` prefixes
- Conventional commit messages (`feat:`, `fix:`, `amend:`, `chore:`, `release:`)
- Sync feature branches onto latest master, consolidate branches, and generate merge request URLs


### github-cli

Interact with GitHub via the `gh` CLI — manage repositories, issues, pull requests, releases, code search, and API calls.

- Create, review, and merge pull requests
- Create and manage issues with labels, assignees, and comments
- Search code, issues, PRs, and repositories
- Manage releases, GitHub Actions workflows, and raw API calls
- Structured output with `--json` and `--jq` for programmatic use


### mysql-cli

Query, modify, and inspect MySQL databases via `mysql-cli`, a smart wrapper with multi-instance support and automatic database routing.

- Supports multiple MySQL instances in a single config (`~/.mysql-instances.cnf`)
- Auto-routes queries to the correct instance/database by table name
- Caches database metadata (instances, databases, tables) for fast lookup
- Execute any SQL: SELECT, INSERT, UPDATE, DELETE, ALTER TABLE, CREATE INDEX, etc.
- Execute `.sql` files with automatic target resolution
- Output as table, CSV, JSON, or vertical format


### playwright-cli

Automates browser interactions for web testing, form filling, screenshots, and data extraction via the `playwright-cli` CLI.

- Navigate websites, click elements, fill forms, take screenshots and PDFs
- Session management for isolating browser profiles across projects
- Request mocking, tracing, video recording, and storage state management
- Test code generation from interactive browser sessions


### markitdown

Convert various file formats (PDF, DOCX, XLSX, PPTX, HTML, images, etc.) to Markdown via CLI.

- Convert local files and URLs to Markdown
- Support for PDF, Word, Excel, PowerPoint, HTML, images, EPUB, email files
- Pipe support for integration with other tools
- Batch processing capabilities


## MCPs

| MCP | Description | Docs |
|-----|-------------|------|
| [Maven Indexer](https://github.com/tangcent/maven-indexer-mcp) | Search classes, artifacts, and resources in local Maven/Gradle caches | [maven-indexer.md](mcp/maven-indexer.md) |
| [Grafana](https://github.com/grafana/mcp-grafana) | Dashboard management, Prometheus/Loki querying, alerts, and incidents | [grafana.md](mcp/grafana.md) |
| [Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Browser automation, DOM interaction, network inspection, and performance tracing | [chrome-devtools.md](mcp/chrome-devtools.md) |

## CLIs

| CLI | Description | Docs |
|-----|-------------|------|
| [Playwright CLI](https://github.com/microsoft/playwright-cli) | Token-efficient browser automation CLI for coding agents | [playwright-cli.md](cli/playwright-cli.md) |
| [GitHub CLI](https://github.com/cli/cli) | Repository management, issues, PRs, releases, and GitHub API from the terminal | [gh.md](cli/gh.md) |
| [MarkItDown](https://github.com/microsoft/markitdown) | Convert PDF, Word, Excel, PowerPoint, HTML, images to Markdown | [markitdown.md](cli/markitdown.md) |
