# Chrome DevTools MCP

- GitHub: [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)

Chrome DevTools MCP connects your AI assistant to a Chrome browser, enabling page navigation, DOM interaction, screenshots, network inspection, console monitoring, performance tracing, and Lighthouse audits.

## Key Features

- Navigate pages, click elements, fill forms, and type text
- Take page snapshots (a11y tree) and screenshots
- Inspect network requests and console messages
- Run JavaScript in the browser context
- Performance tracing and Lighthouse audits
- Multi-page/tab management

## Common Tools

| Tool | Description |
|------|-------------|
| `new_page` | Open a new tab and load a URL |
| `navigate_page` | Navigate to URL, back, forward, or reload |
| `take_snapshot` | Get a text snapshot of the page (a11y tree) |
| `take_screenshot` | Capture a PNG screenshot |
| `click` | Click on an element by uid |
| `fill` | Type into an input or select an option |
| `type_text` | Type text via keyboard into a focused input |
| `evaluate_script` | Run JavaScript in the page |
| `list_pages` | List all open browser tabs |
| `wait_for` | Wait for text to appear on the page |
| `list_network_requests` | List network requests since last navigation |
| `list_console_messages` | List console messages |
| `lighthouse_audit` | Run accessibility, SEO, and best practices audit |
| `performance_start_trace` | Start a performance trace recording |

## Sample Config

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"],
      "autoApprove": [
        "new_page",
        "take_snapshot",
        "click",
        "navigate_page",
        "close_page",
        "wait_for",
        "take_screenshot",
        "list_pages",
        "evaluate_script",
        "type_text"
      ],
      "disabled": false
    }
  }
}
```

> Requires a Chrome/Chromium browser running with remote debugging enabled, or the MCP will launch one automatically.
