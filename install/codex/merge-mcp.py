#!/usr/bin/env python3
"""Merge MCP servers into Codex's global config (~/.codex/config.toml).

Codex format: MCP servers live under [mcp_servers.<name>] in ~/.codex/config.toml.

Usage: python3 install/codex/merge-mcp.py [server_name ...]
  No args = merge all servers. Pass names to merge specific ones.
"""

import json
import re
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from importlib import import_module
lib = import_module("merge-mcp-lib")

CONFIG_PATH = Path.home() / ".codex" / "config.toml"
BARE_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def transform(servers):
    """Codex uses command/args/env under mcp_servers without extra fields."""
    return dict(servers)


def format_key(key):
    """Render a TOML key segment, quoting only when required."""
    return key if BARE_KEY_RE.match(key) else json.dumps(key)


def format_value(value):
    """Render a TOML scalar or array value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(format_value(item) for item in value) + "]"
    raise TypeError(f"Unsupported TOML value type: {type(value).__name__}")


def dump_table_body(lines, path, table, emit_header):
    """Serialize a TOML table and its child tables."""
    scalar_items = []
    child_tables = []
    for key, value in table.items():
        if isinstance(value, dict):
            child_tables.append((key, value))
        else:
            scalar_items.append((key, value))

    if emit_header and path and (scalar_items or not child_tables):
        lines.append("[" + ".".join(format_key(part) for part in path) + "]")

    for key, value in scalar_items:
        lines.append(f"{format_key(key)} = {format_value(value)}")

    for key, value in child_tables:
        if lines and lines[-1] != "":
            lines.append("")
        dump_table_body(lines, path + [key], value, emit_header=True)


def dumps_toml(data):
    """Serialize a nested dict into TOML."""
    lines = []
    dump_table_body(lines, [], data, emit_header=False)
    return "\n".join(lines).rstrip() + "\n"


def main():
    names = sys.argv[1:] if len(sys.argv) > 1 else None
    servers = lib.load_raw_servers(names)
    codex_servers = transform(servers)

    existing = {}
    if CONFIG_PATH.exists():
        try:
            existing = tomllib.loads(CONFIG_PATH.read_text())
        except tomllib.TOMLDecodeError:
            existing = {}

    if "mcp_servers" not in existing or not isinstance(existing["mcp_servers"], dict):
        existing["mcp_servers"] = {}

    existing["mcp_servers"] = lib.merge_servers(existing["mcp_servers"], codex_servers)

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(dumps_toml(existing))

    merged = list(codex_servers.keys())
    print(f"Merged {len(merged)} MCP server(s) into {CONFIG_PATH}")
    for name in merged:
        print(f"  ✓ {name}")


if __name__ == "__main__":
    main()
