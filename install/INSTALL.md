# ai-cookbook Install Guide

Interactive guide for installing CLIs, MCPs, and Skills from this cookbook into your AI coding tools.

> Install targets global paths (`~/`) so MCPs and skills are available across all projects.

## Step 0: Check Prerequisites

Make sure the required runtimes are installed:

```bash
bash install/check-prerequisites.sh
```

This checks for `node`/`npm`/`npx`, `python`, `uv`/`uvx`, `git`, `gh`, `mcp-grafana`, `mysql`, and macOS OpenSSL cert. If anything is missing, it will offer to install it for you (via Homebrew, Go, or pip).

## Step 1: Detect Available AI Tools

Run the detection script to see which AI tools are installed on your machine:

```bash
bash install/detect-ai-tools.sh
```

Supported tools:
| Tool | Type | Global Config |
|------|------|---------------|
| Cursor | IDE | `~/.cursor/mcp.json` (key: `mcpServers`) |
| Kiro | IDE | `~/.kiro/settings/mcp.json` |
| Claude Code | CLI | `~/.claude.json` (key: `mcpServers`) |
| Cline | VS Code Extension | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| OpenCode | CLI | `~/.config/opencode/opencode.json` (key: `mcp`) |
| Antigravity | IDE | `~/.gemini/antigravity/mcp_config.json` |
| Trae | IDE | `~/Library/Application Support/Trae/User/mcp.json` |
| Trae CN | IDE | `~/Library/Application Support/Trae CN/User/mcp.json` |

## Step 1.5: Collect Existing MCP Variables

Before installing MCPs, scan your existing AI tool configs to collect any variables (paths, tokens, URLs) that are already configured. These will be reused to auto-fill new installations so you don't have to re-enter them.

```bash
bash install/collect-mcp-vars.sh
```

This scans all detected tool configs and saves discovered values to `install/.mcp-vars.json`. Variables collected include:

| Variable | From MCP | Example |
|----------|----------|---------|
| `grafana_command` | grafana | `/usr/local/bin/mcp-grafana` |
| `grafana_url` | grafana | `http://grafana.example.com` |
| `grafana_username` | grafana | `admin@example.com` |
| `grafana_password` | grafana | `****` |
| `grafana_org_id` | grafana | `1` |

If a variable is already filled in one tool (e.g. Kiro has your Grafana URL), it will be auto-filled when installing the same MCP into another tool (e.g. Claude Code).

## Step 2: Choose What to Install

Ask yourself (or let the agent ask you):

> What would you like to install?

| Option | Description |
|--------|-------------|
| `all` | Install all CLIs + MCPs + Skills |
| `all cli` | Install all CLIs (playwright-cli, gh, glab, markitdown) |
| `all mcp` | Install all MCPs (chrome-devtools, grafana, maven-indexer) |
| `all skills` | Install all Skills (audit-sql, grafana-dashboard, git-workflow, github-cli, gitlab-cli, mysql-cli, playwright-cli, markitdown, spec-driven) |
| `<specific>` | Install a specific item by name (e.g. `grafana`, `git-workflow`, `playwright-cli`) |

## Step 3: Choose Target AI Tool(s)

> Which AI tool(s) should receive the installation?

| Option | Description |
|--------|-------------|
| `all` | Install into all detected AI tools |
| `<specific>` | Install into a specific tool (e.g. `kiro`, `claude`, `cline`) |

## Step 4: Run Installation

MCP definitions are maintained in a single file: `install/mcp-servers.json`. Each tool has a merge script that transforms and merges them into the tool's config format.

### Install a Single MCP

Pass the MCP name as an argument to the merge script for each target tool:

```bash
# Example: install only grafana into Kiro
python3 install/kiro/merge-mcp.py grafana
```

To install into all detected tools at once:

```bash
python3 install/cursor/merge-mcp.py <mcp-name>
python3 install/kiro/merge-mcp.py <mcp-name>
python3 install/claude/merge-mcp.py <mcp-name>
python3 install/cline/merge-mcp.py <mcp-name>
python3 install/opencode/merge-mcp.py <mcp-name>
python3 install/antigravity/merge-mcp.py <mcp-name>
python3 install/trae/merge-mcp.py <mcp-name>
python3 install/trae-cn/merge-mcp.py <mcp-name>
```

### Install a Single Skill

Copy the skill folder into the target tool's skill directory:

| AI Tool | Skill Directory |
|---------|----------------|
| Cursor | `~/.cursor/skills/` |
| Kiro | `~/.kiro/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cline | `~/.cline/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Antigravity | `~/.gemini/antigravity/skills/` |
| Trae | `~/.trae/skills/` |
| Trae CN | `~/.trae-cn/skills/` |

```bash
# Example: install only audit-sql into Kiro
mkdir -p ~/.kiro/skills
cp -r skills/audit-sql ~/.kiro/skills/
```

To install a skill into all detected tools at once:

```bash
SKILL=<skill-name>
for dir in ~/.cursor/skills ~/.kiro/skills ~/.claude/skills ~/.cline/skills ~/.config/opencode/skills ~/.gemini/antigravity/skills ~/.trae/skills ~/.trae-cn/skills; do
  [ -d "$(dirname "$dir")" ] && mkdir -p "$dir" && rm -rf "$dir/$SKILL" && cp -r "skills/$SKILL" "$dir/$SKILL"
done
```

### Install a Single CLI

| CLI | Install Command |
|-----|----------------|
| playwright-cli | `npm install -g @playwright/cli@latest` |
| gh | `brew install gh` |
| glab | `brew install glab` |
| markitdown | `pip install markitdown` or `uvx markitdown` |

### Install All (bulk)

To install all MCPs into all tools:

```bash
python3 install/cursor/merge-mcp.py
python3 install/kiro/merge-mcp.py
python3 install/claude/merge-mcp.py
python3 install/cline/merge-mcp.py
python3 install/opencode/merge-mcp.py
python3 install/antigravity/merge-mcp.py
python3 install/trae/merge-mcp.py
python3 install/trae-cn/merge-mcp.py
```

To install all skills into all tools, see each tool's README for the bulk copy loop.

### Tool-specific details

Each tool has its own README with full instructions for installing CLIs, MCPs, and Skills (including skill directory paths and copy commands). Refer to these for the complete per-tool setup:

| AI Tool | Merge Script | Full Instructions |
|---------|-------------|-------------------|
| Cursor | `python3 install/cursor/merge-mcp.py` | [install/cursor/README.md](cursor/README.md) |
| Kiro | `python3 install/kiro/merge-mcp.py` | [install/kiro/README.md](kiro/README.md) |
| Claude Code | `python3 install/claude/merge-mcp.py` | [install/claude/README.md](claude/README.md) |
| Cline | `python3 install/cline/merge-mcp.py` | [install/cline/README.md](cline/README.md) |
| OpenCode | `python3 install/opencode/merge-mcp.py` | [install/opencode/README.md](opencode/README.md) |
| Antigravity | `python3 install/antigravity/merge-mcp.py` | [install/antigravity/README.md](antigravity/README.md) |
| Trae | `python3 install/trae/merge-mcp.py` | [install/trae/README.md](trae/README.md) |
| Trae CN | `python3 install/trae-cn/merge-mcp.py` | [install/trae-cn/README.md](trae-cn/README.md) |

> **For AI agents:** When installing a single item, use the patterns above. For tool-specific details (skill directory paths, config formats), read that tool's README (e.g. `install/kiro/README.md`).

## Step 5: Fill Remaining Variables

After installation, some MCPs may still have placeholder values that need to be filled. The agent will:

1. List all MCP config files that contain unfilled placeholders
2. Show which variables still need values
3. Ask if you'd like to provide them now (the agent will fill them in for you)

### MCP Config File Locations (Global)

| AI Tool | Config File |
|---------|------------|
| Cursor | `~/.cursor/mcp.json` |
| Kiro | `~/.kiro/settings/mcp.json` |
| Claude Code | `~/.claude.json` |
| Cline | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| OpenCode | `~/.config/opencode/opencode.json` |
| Antigravity | `~/.gemini/antigravity/mcp_config.json` |
| Trae | `~/Library/Application Support/Trae/User/mcp.json` |
| Trae CN | `~/Library/Application Support/Trae CN/User/mcp.json` |

### Variables That May Need Filling

| MCP | Variable | Description |
|-----|----------|-------------|
| grafana | `command` | Path to `mcp-grafana` binary |
| grafana | `GRAFANA_URL` | Grafana instance URL |
| grafana | `GRAFANA_USERNAME` | Grafana login email |
| grafana | `GRAFANA_PASSWORD` | Grafana login password |
| grafana | `GRAFANA_ORG_ID` | Grafana organization ID |

> You can also manually edit the config files listed above at any time.

---

## Available Items

### CLIs
| Name | Description |
|------|-------------|
| playwright-cli | Token-efficient browser automation CLI for coding agents |
| gh | Repository management, issues, PRs, releases, and GitHub API from the terminal |
| glab | Repository management, issues, MRs, pipelines, releases, and GitLab API from the terminal |
| markitdown | Convert PDF, Word, Excel, PowerPoint, HTML, images to Markdown |

### MCPs
| Name | Description |
|------|-------------|
| chrome-devtools | Browser automation, DOM interaction, network inspection |
| grafana | Dashboard management, Prometheus/Loki querying, alerts |
| maven-indexer | Search classes/artifacts in local Maven/Gradle caches |

### Skills
| Name | Description |
|------|-------------|
| audit-sql | SQL audit on MyBatis mapper XML files |
| grafana-dashboard | Build Grafana dashboards with consistent style conventions |
| git-workflow | Branch prefixes, conventional commits, sync operations |
| github-cli | Interact with GitHub via the `gh` CLI |
| gitlab-cli | Interact with GitLab via the `glab` CLI |
| mysql-cli | Query, modify, and inspect MySQL with multi-instance auto-routing |
| playwright-cli | Browser automation for web testing, form filling, screenshots, and data extraction |
| markitdown | Convert various file formats to Markdown via CLI |
| spec-driven | Spec-driven development: requirements, design, tasks, and execution |
