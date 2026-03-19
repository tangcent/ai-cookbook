"""
Shared library for MCP merge scripts.
Reads mcp-servers.json, substitutes variables from .mcp-vars.json,
and provides tool-specific transform + merge functions.
"""

import json
import os
import re
import sys
from pathlib import Path

INSTALL_DIR = Path(__file__).parent
RAW_MCP_FILE = INSTALL_DIR / "mcp-servers.json"
VARS_FILE = INSTALL_DIR / ".mcp-vars.json"

# Variable pattern: ${var_name:-default_value} or ${var_name}
VAR_PATTERN = re.compile(r"\$\{(\w+)(?::-(.*?))?\}")


def load_vars():
    """Load collected variables from .mcp-vars.json."""
    if VARS_FILE.exists():
        try:
            data = json.loads(VARS_FILE.read_text())
            return data.get("variables", {})
        except (json.JSONDecodeError, KeyError):
            pass
    return {}


def substitute(value, variables):
    """Replace ${var:-default} patterns in a string value."""
    if not isinstance(value, str):
        return value

    def replacer(m):
        var_name = m.group(1)
        default = m.group(2) if m.group(2) is not None else ""
        return variables.get(var_name, default)

    return VAR_PATTERN.sub(replacer, value)


def substitute_deep(obj, variables):
    """Recursively substitute variables in a JSON-like structure."""
    if isinstance(obj, str):
        return substitute(obj, variables)
    if isinstance(obj, list):
        return [substitute_deep(v, variables) for v in obj]
    if isinstance(obj, dict):
        return {k: substitute_deep(v, variables) for k, v in obj.items()}
    return obj


def load_raw_servers(names=None):
    """Load and variable-substitute the raw MCP server definitions.
    If names is provided, only include those servers.
    """
    raw = json.loads(RAW_MCP_FILE.read_text())
    variables = load_vars()
    servers = substitute_deep(raw, variables)

    # Remove empty env dicts and empty SSL_CERT_FILE
    for name, cfg in servers.items():
        env = cfg.get("env", {})
        # Remove empty string values from env
        cfg["env"] = {k: v for k, v in env.items() if v}
        if not cfg["env"]:
            del cfg["env"]

    if names:
        servers = {k: v for k, v in servers.items() if k in names}

    return servers


def deep_merge(base, override):
    """Deep merge override into base dict. Override wins on conflicts."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def merge_servers(existing_servers, new_servers, install_owned_keys=None):
    """Merge new server definitions into existing ones, preserving user settings.

    For new servers (not in existing config): use the full definition as-is.
    For existing servers: only update install-owned keys (command, args, env by default)
    and preserve everything else the user may have configured.
    """
    if install_owned_keys is None:
        install_owned_keys = {"command", "args", "env"}
    result = dict(existing_servers)
    for name, new_cfg in new_servers.items():
        if name not in result:
            # New server — use full definition including defaults
            result[name] = new_cfg
        else:
            # Existing server — only update install-owned keys
            for key in install_owned_keys:
                if key in new_cfg:
                    result[name][key] = new_cfg[key]
    return result
