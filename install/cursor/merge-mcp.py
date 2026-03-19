#!/usr/bin/env python3
"""Merge MCP servers into Cursor's global config (~/.cursor/mcp.json).

Cursor format: mcpServers at top level of ~/.cursor/mcp.json.

Usage: python3 install/cursor/merge-mcp.py [server_name ...]
  No args = merge all servers. Pass names to merge specific ones.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib import import_module
lib = import_module("merge-mcp-lib")

CONFIG_PATH = Path.home() / ".cursor" / "mcp.json"


def transform(servers):
    """Cursor uses standard format, no extra fields needed."""
    return dict(servers)


def main():
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    servers = lib.load_raw_servers(names)
    cursor_servers = transform(servers)

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    existing = {}
    if CONFIG_PATH.exists():
        try:
            existing = json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            existing = {}

    if "mcpServers" not in existing:
        existing["mcpServers"] = {}

    existing["mcpServers"] = lib.merge_servers(existing["mcpServers"], cursor_servers)

    CONFIG_PATH.write_text(json.dumps(existing, indent=2) + "\n")

    merged = list(cursor_servers.keys())
    print(f"Merged {len(merged)} MCP server(s) into {CONFIG_PATH}")
    for name in merged:
        print(f"  ✓ {name}")


if __name__ == "__main__":
    main()
