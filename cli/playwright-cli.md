# Playwright CLI

- GitHub: [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli)

Playwright CLI provides a token-efficient command-line interface for browser automation, designed for coding agents. Unlike MCP-based approaches that load large tool schemas and accessibility trees into context, Playwright CLI uses concise, purpose-built commands — making it ideal for high-throughput agents balancing browser automation with large codebases.

## Key Features

- Token-efficient browser automation (no page data forced into LLM context)
- Headless by default, with `--headed` mode for visual debugging
- Session management for isolating browser profiles across projects
- Skills system for agent integration (Claude Code, GitHub Copilot, etc.)
- Visual dashboard (`playwright-cli show`) for monitoring agent browser sessions

## Common Commands

| Command | Description |
|---------|-------------|
| `playwright-cli open <url>` | Open a URL in the browser |
| `playwright-cli click <selector>` | Click an element |
| `playwright-cli type <text>` | Type text into a focused element |
| `playwright-cli press <key>` | Press a key (e.g. Enter, Tab) |
| `playwright-cli screenshot` | Take a screenshot |
| `playwright-cli snapshot` | Get an accessibility snapshot of the page |
| `playwright-cli list` | List all active sessions |
| `playwright-cli show` | Open the visual monitoring dashboard |
| `playwright-cli close-all` | Close all browser sessions |
| `playwright-cli install --skills` | Install skills for agent integration |

## Installation

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

## Usage with Coding Agents

Install skills for automatic agent integration:

```bash
playwright-cli install --skills
```

Or point your agent at the CLI directly:

```
Test the "add todo" flow on https://demo.playwright.dev/todomvc using playwright-cli.
Check playwright-cli --help for available commands.
```

## Session Management

```bash
# Default session
playwright-cli open https://example.com

# Named session
playwright-cli -s=my-project open https://example.com --persistent

# Use with coding agents via env var
PLAYWRIGHT_CLI_SESSION=todo-app claude .

# Manage sessions
playwright-cli list          # list all sessions
playwright-cli close-all     # close all browsers
playwright-cli kill-all      # forcefully kill all browser processes
```
