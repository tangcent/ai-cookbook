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

Git workflow automation with safer branch decisions, conventional commits, rebasing, syncing, and MR links.

- Create branches with inferred prefixes (`feature/`, `fix/`, `hotfix/`, `release/`, `chore/`)
- Safer commit flow with auto rebase onto default branch and controlled force-push
- Sync active branches and consolidate integration branches with confirmations
- Generate GitLab MR URLs from current remote automatically

> 💬 Tell your AI: "install git-workflow"
<!-- AI: Run install/INSTALL.md to install the git-workflow skill -->


### github-cli

Operate GitHub with the `gh` CLI for repositories, pull requests, issues, releases, CI runs, and API calls.

- Enforces `gh`-first execution for GitHub tasks
- Works with structured output (`--json` + `--jq`) for scripting and summaries
- Loads detailed PR/issue template workflows from `github-cli/references/*` only when needed

> 💬 Tell your AI: "install github-cli"
<!-- AI: Run install/INSTALL.md to install the github-cli skill -->


### gitlab-cli

Operate GitLab with the `glab` CLI for repositories, merge requests, issues, pipelines, releases, and API calls.

- Auto-detects self-hosted GitLab hostname from git remotes
- Enforces `glab`-first execution and `glab api` for raw API calls
- Loads detailed MR template workflow from `gitlab-cli/references/create-mr.md` only when needed

> 💬 Tell your AI: "install gitlab-cli"
<!-- AI: Run install/INSTALL.md to install the gitlab-cli skill -->

### create-skill

Create or update skills in this repository following local skill authoring standards.

- Scaffolds `skills/<name>/SKILL.md` with valid frontmatter
- Enforces naming/trigger-description conventions
- Requires skill catalog updates in `README.md` and `install/INSTALL.md`

> 💬 Tell your AI: "install create-skill"
<!-- AI: Run install/INSTALL.md to install the create-skill skill -->


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


### kafka-viewer

Inspect Kafka servers, topics, and messages via `kafka-view-cli` to verify data correctness after changes.

- List Kafka servers and topics
- Read and sample recent messages from any topic
- Verify payload correctness after deploys or code changes
- Filter output with `--jq` for targeted inspection


### xxljob-test

Test XxlJob handlers locally by triggering them via HTTP POST with a simple script.

- Launch your service locally, then trigger any `@XxlJob` handler with `xxljob-trigger`
- Script accepts `executorHandler` and optional `executorParams` — builds the full request body for you
- Verify results via HTTP response and application logs

> 💬 Tell your AI: "install xxljob-test"
<!-- AI: Run install/INSTALL.md to install the xxljob-test skill -->


### zadig-deploy

Deploy services, check deployment status, and inspect deployed branches in [Zadig](https://zadig-local.tec-develop.cn). Supports browser automation via Playwright or Chrome DevTools MCP.

- Deploy a service to test environments (`test-01`, `test-02`)
- Check deployment status and running images
- Identify which branch/commit is currently deployed


### learn-from-mistakes

Capture AI corrections and build a persistent knowledge base of lessons learned, logged to Obsidian.

- Detects when the user corrects the AI (phrases like "you should", "why not", "that's wrong", "use X instead")
- Reflects on what went wrong: root cause, correct approach, and a distilled one-line rule
- Logs each lesson to Obsidian with rich tags: scope (global/project), domain (api/kafka/redis/mysql/etc.), error type, AI tool
- One note per lesson with descriptive filenames: `AI-Lesson-<description>-YYYY-MM-DD`
- Cross-tool: compile lessons into steering files for Kiro, Cursor, Claude, Cline, Copilot, etc.

> 💬 Tell your AI: "install learn-from-mistakes"
<!-- AI: Run install/INSTALL.md to install the learn-from-mistakes skill -->


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
