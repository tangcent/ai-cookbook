#!/usr/bin/env python3
"""Merge MCP servers into Cline's global config.

Cline format: mcpServers with disabled field.
Config: ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json

Usage: python3 install/cline/merge-mcp.py [server_name ...]
  No args = merge all servers. Pass names to merge specific ones.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib import import_module
lib = import_module("merge-mcp-lib")

CONFIG_PATH = (
    Path.home()
    / "Library/Application Support/Code/User/globalStorage"
    / "saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
)


def transform(servers):
    """Add Cline-specific field: disabled."""
    result = {}
    for name, cfg in servers.items():
        entry = dict(cfg)
        entry["disabled"] = True
        result[name] = entry
    return result


def main():
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    servers = lib.load_raw_servers(names)
    cline_servers = transform(servers)

    existing = {}
    if CONFIG_PATH.exists():
        try:
            existing = json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            existing = {}

    if "mcpServers" not in existing:
        existing["mcpServers"] = {}

    existing_servers = existing["mcpServers"]
    existing["mcpServers"] = lib.merge_servers(existing_servers, cline_servers)

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(existing, indent=2) + "\n")

    merged = list(cline_servers.keys())
    print(f"Merged {len(merged)} MCP server(s) into {CONFIG_PATH}")
    for name in merged:
        print(f"  ✓ {name}")


if __name__ == "__main__":
    main()
