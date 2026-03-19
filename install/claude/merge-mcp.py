#!/usr/bin/env python3
"""Merge MCP servers into Claude Code's global config (~/.claude.json).

Claude format: mcpServers at top level of ~/.claude.json (which may have other keys).

Usage: python3 install/claude/merge-mcp.py [server_name ...]
  No args = merge all servers. Pass names to merge specific ones.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib import import_module
lib = import_module("merge-mcp-lib")

CONFIG_PATH = Path.home() / ".claude.json"


def transform(servers):
    """Claude uses standard format. Install disabled by default — enable per-project as needed."""
    result = {}
    for name, cfg in servers.items():
        entry = dict(cfg)
        entry["disabled"] = True
        result[name] = entry
    return result


def main():
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    servers = lib.load_raw_servers(names)
    claude_servers = transform(servers)

    # Load existing config (claude.json may have other top-level keys)
    existing = {}
    if CONFIG_PATH.exists():
        try:
            existing = json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            existing = {}

    if "mcpServers" not in existing:
        existing["mcpServers"] = {}

    existing_servers = existing["mcpServers"]
    existing["mcpServers"] = lib.deep_merge(existing_servers, claude_servers)
    # Preserve user-controlled fields (e.g. disabled) set via the Claude UI
    lib.preserve_user_fields(existing["mcpServers"], existing_servers)

    CONFIG_PATH.write_text(json.dumps(existing, indent=2) + "\n")

    merged = list(claude_servers.keys())
    print(f"Merged {len(merged)} MCP server(s) into {CONFIG_PATH}")
    for name in merged:
        print(f"  ✓ {name}")


if __name__ == "__main__":
    main()
