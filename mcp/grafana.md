# Grafana MCP

- GitHub: [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana)

Grafana MCP connects your AI assistant to a Grafana instance, enabling dashboard management, Prometheus/Loki querying, alert rule management, incident handling, and more — all from within your editor.

## Key Features

- Search, view, and update Grafana dashboards
- Query Prometheus metrics and Loki logs
- Manage alert rules and contact points
- Create and manage incidents
- Render panel images and generate deeplinks
- Browse datasources, folders, and annotations

## Common Tools

| Tool | Description |
|------|-------------|
| `search_dashboards` | Search dashboards by query string |
| `get_dashboard_by_uid` | Get full dashboard JSON by UID |
| `get_dashboard_summary` | Get a compact dashboard overview |
| `list_datasources` | List all configured datasources |
| `query_prometheus` | Execute a PromQL query |
| `query_loki_logs` | Execute a LogQL query |
| `list_alert_rules` | List alert rules with state and labels |
| `update_dashboard` | Create or patch a dashboard |
| `get_panel_image` | Render a panel as PNG |
| `generate_deeplink` | Generate URLs for dashboards/panels/explore |

## Sample Config

```json
{
  "mcpServers": {
    "grafana": {
      "command": "/path/to/mcp-grafana",
      "args": [],
      "env": {
        "GRAFANA_URL": "http://your-grafana-instance.com",
        "GRAFANA_USERNAME": "[email]",
        "GRAFANA_PASSWORD": "[password]",
        "GRAFANA_ORG_ID": "1"
      },
      "autoApprove": [
        "search_dashboards",
        "get_dashboard_by_uid",
        "list_datasources",
        "get_dashboard_summary",
        "query_prometheus",
        "list_prometheus_metric_names",
        "list_prometheus_label_values",
        "generate_deeplink",
        "get_panel_image"
      ],
      "disabled": false
    }
  }
}
```

> Install the `mcp-grafana` binary from [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana) and update the `command` path accordingly.

## Installation

```bash
# Via Homebrew (recommended)
brew install mcp-grafana

# Or via Go
go install github.com/grafana/mcp-grafana@latest
```

After installing, find the binary path with `which mcp-grafana` and use it in the `command` field above.
