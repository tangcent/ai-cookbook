#!/usr/bin/env bash
# install.sh — One-command installer for ai-cookbook skills.
#
# Downloads the repository archive, then delegates to install/install-skills.sh
# so script path rewriting and tool runtime notes stay in sync with a local install.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/tangcent/ai-cookbook/main/install/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/tangcent/ai-cookbook/main/install/install.sh | bash -s -- kiro
#   curl -fsSL https://raw.githubusercontent.com/tangcent/ai-cookbook/main/install/install.sh | bash -s -- workbuddy review-pr
#   curl -fsSL https://raw.githubusercontent.com/tangcent/ai-cookbook/main/install/install.sh | bash -s -- all
#
# Arguments:
#   [tool]       Target tool name or "all"; omit to select detected tools interactively.
#   [skill ...]  Skill names to install; omit to install every skill.
#
# Environment:
#   AI_COOKBOOK_ARCHIVE_URL  Override the archive URL (useful for mirrors or testing).

set -euo pipefail

ARCHIVE_URL="${AI_COOKBOOK_ARCHIVE_URL:-https://github.com/tangcent/ai-cookbook/archive/refs/heads/main.tar.gz}"
ALL_TOOLS="cursor kiro claude codex cline opencode antigravity trae trae-cn workbuddy"

TOOL_ARG="${1:-}"
shift || true

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Downloading ai-cookbook from $ARCHIVE_URL"
if ! curl -fsSL "$ARCHIVE_URL" -o "$TMP_DIR/archive.tar.gz"; then
  echo "Failed to download the ai-cookbook archive." >&2
  exit 1
fi

if ! tar -xzf "$TMP_DIR/archive.tar.gz" -C "$TMP_DIR" --strip-components=1; then
  echo "Failed to extract the ai-cookbook archive." >&2
  exit 1
fi

INSTALL_SKILLS="$TMP_DIR/install/install-skills.sh"
DETECT_TOOLS="$TMP_DIR/install/detect-ai-tools.sh"
if [ ! -f "$INSTALL_SKILLS" ]; then
  echo "Archive does not contain install/install-skills.sh." >&2
  exit 1
fi

is_supported_tool() {
  for supported in $ALL_TOOLS; do
    [ "$1" = "$supported" ] && return 0
  done
  return 1
}

detect_installed_tools() {
  local detected="" result=""
  if [ -f "$DETECT_TOOLS" ]; then
    detected="$(bash "$DETECT_TOOLS" 2>/dev/null | awk -F': ' '$2 == "available" { print $1 }' | tr '\n' ' ' || true)"
  fi
  for tool in $ALL_TOOLS; do
    case " $detected " in
      *" $tool "*) result="$result $tool" ;;
    esac
  done
  echo "${result# }"
}

if [ -n "$TOOL_ARG" ]; then
  TOOLS="$TOOL_ARG"
else
  DETECTED="$(detect_installed_tools)"
  echo "Detected AI tools: ${DETECTED:-none}"
  # With `curl | bash`, stdin carries the script itself. Read from the terminal
  # instead so the selection prompt still works in a pipe.
  if { [ -t 0 ] || [ -t 1 ]; } && [ -r /dev/tty ]; then
    printf "Install into which tools? (comma-separated, 'all' for every tool) [%s]: " "${DETECTED:-all}"
    read -r answer < /dev/tty || true
    answer="$(echo "${answer:-}" | tr -d ' ')"
    TOOLS="${answer:-${DETECTED:-all}}"
  else
    echo "Non-interactive shell; installing into detected tools."
    TOOLS="${DETECTED:-all}"
  fi
fi

TOOLS="$(echo "$TOOLS" | tr ',' ' ')"
for tool in $TOOLS; do
  if [ "$tool" = "all" ]; then
    TOOLS="$ALL_TOOLS"
    break
  fi
  if ! is_supported_tool "$tool"; then
    echo "Unknown tool: $tool" >&2
    echo "Available: $ALL_TOOLS" >&2
    exit 1
  fi
done

for tool in $TOOLS; do
  echo ""
  echo "Installing into $tool..."
  bash "$INSTALL_SKILLS" "$tool" "$@"
done
