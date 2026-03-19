#!/usr/bin/env python3
"""Merge MCP servers into OpenCode's global config (~/.config/opencode/opencode.json).

OpenCode format differences:
  - Top-level key is "mcp" (not "mcpServers")
  - "command" is an array: [command, ...args]
  - "environment" instead of "env"
  - Adds "type": "local"

Usage: python3 install/opencode/merge-mcp.py [server_name ...]
  No args = merge all servers. Pass names to merge specific ones.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib import import_module
lib = import_module("merge-mcp-lib")

CONFIG_PATH = Path.home() / ".config" / "opencode" / "opencode.json"


def transform(servers):
    """Convert standard format to OpenCode format."""
    result = {}
    for name, cfg in servers.items():
        entry = {"type": "local"}
        # Merge command + args into a single array
        cmd = cfg.get("command", "")
        args = cfg.get("args", [])
        entry["command"] = [cmd] + args
        # Rename env -> environment
        env = cfg.get("env")
        if env:
            entry["environment"] = env
        result[name] = entry
    return result


def main():
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    servers = lib.load_raw_servers(names)
    oc_servers = transform(servers)

    existing = {}
    if CONFIG_PATH.exists():
        try:
            existing = json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            existing = {}

    if "mcp" not in existing:
        existing["mcp"] = {}

    existing["mcp"] = lib.merge_servers(existing["mcp"], oc_servers,
                                       install_owned_keys={"command", "environment", "type"})

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(existing, indent=2) + "\n")

    merged = list(oc_servers.keys())
    print(f"Merged {len(merged)} MCP server(s) into {CONFIG_PATH}")
    for name in merged:
        print(f"  ✓ {name}")


if __name__ == "__main__":
    main()
