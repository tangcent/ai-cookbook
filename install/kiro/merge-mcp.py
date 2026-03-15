#!/usr/bin/env python3
"""Merge MCP servers into Kiro's global config (~/.kiro/settings/mcp.json).

Kiro format: standard mcpServers with autoApprove and disabled fields.

Usage: python3 install/kiro/merge-mcp.py [server_name ...]
  No args = merge all servers. Pass names to merge specific ones.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib import import_module
lib = import_module("merge-mcp-lib")

CONFIG_PATH = Path.home() / ".kiro" / "settings" / "mcp.json"

# Kiro-specific: autoApprove lists per server
AUTO_APPROVE = {
    "chrome-devtools": [
        "new_page", "take_snapshot", "click", "navigate_page",
        "close_page", "wait_for", "take_screenshot", "list_pages",
        "evaluate_script", "type_text"
    ],
    "github": [
        "get_me", "get_file_contents", "list_branches",
        "get_commit", "get_release_by_tag"
    ],
    "grafana": [
        "search_dashboards", "get_dashboard_by_uid", "list_datasources",
        "get_dashboard_summary", "query_prometheus",
        "list_prometheus_metric_names", "list_prometheus_label_values",
        "generate_deeplink", "get_panel_image"
    ],
    "markitdown": ["convert_to_markdown"],
    "maven-indexer": [
        "search_classes", "get_class_details",
        "search_artifacts", "refresh_index"
    ],
}


def transform(servers):
    """Add Kiro-specific fields: autoApprove, disabled."""
    result = {}
    for name, cfg in servers.items():
        entry = dict(cfg)
        if name in AUTO_APPROVE:
            entry["autoApprove"] = AUTO_APPROVE[name]
        entry["disabled"] = False
        result[name] = entry
    return result


def main():
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    servers = lib.load_raw_servers(names)
    kiro_servers = transform(servers)

    # Load existing config
    existing = {}
    if CONFIG_PATH.exists():
        try:
            existing = json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            existing = {}

    if "mcpServers" not in existing:
        existing["mcpServers"] = {}

    # Merge: new servers override existing ones by name
    existing["mcpServers"] = lib.deep_merge(existing["mcpServers"], kiro_servers)

    # Write back
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(existing, indent=2) + "\n")

    merged = list(kiro_servers.keys())
    print(f"Merged {len(merged)} MCP server(s) into {CONFIG_PATH}")
    for name in merged:
        print(f"  ✓ {name}")


if __name__ == "__main__":
    main()
