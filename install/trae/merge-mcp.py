#!/usr/bin/env python3
"""Merge MCP servers into Trae's global config (~/Library/Application Support/Trae/User/mcp.json).

Trae format: mcpServers at top level of mcp.json (which may have other keys).

Usage: python3 install/trae/merge-mcp.py [server_name ...]
  No args = merge all servers. Pass names to merge specific ones.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib import import_module
lib = import_module("merge-mcp-lib")

CONFIG_PATH = Path.home() / "Library" / "Application Support" / "Trae" / "User" / "mcp.json"


def transform(servers):
    """Trae uses standard format, no extra fields needed."""
    return dict(servers)


def main():
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    servers = lib.load_raw_servers(names)
    trae_servers = transform(servers)

    # Load existing config (mcp.json may have other top-level keys)
    existing = {}
    if CONFIG_PATH.exists():
        try:
            existing = json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            existing = {}

    if "mcpServers" not in existing:
        existing["mcpServers"] = {}

    existing["mcpServers"] = lib.merge_servers(existing["mcpServers"], trae_servers)

    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(existing, indent=2) + "\n")

        merged = list(trae_servers.keys())
        print(f"Merged {len(merged)} MCP server(s) into {CONFIG_PATH}")
        for name in merged:
            print(f"  ✓ {name}")
    except PermissionError:
        print(f"\n❌ Permission denied: Cannot write to {CONFIG_PATH}")
        print("\nPlease run the script manually from your terminal:")
        print(f"\n  cd {Path(__file__).parent.parent.parent}")
        print(f"  python3 install/trae/merge-mcp.py {' '.join(names) if names else ''}")
        print("\nThis will allow the script to write to the Trae configuration file.")
        sys.exit(1)


if __name__ == "__main__":
    main()
