#!/usr/bin/env bash
# install-skills.sh — Install skills into AI tool skill directories.
#
# After copying, rewrites `scripts/` references in SKILL.md to absolute paths
# so the AI agent can invoke them from any working directory.
#
# Usage:
#   bash install/install-skills.sh [tool] [skill ...]
#
# Examples:
#   bash install/install-skills.sh kiro                  # all skills into Kiro
#   bash install/install-skills.sh all                   # all skills into all tools
#   bash install/install-skills.sh kiro mysql-cli        # one skill into Kiro
#   bash install/install-skills.sh all zadig-deploy      # one skill into all tools

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"

# ── Tool → skill directory mapping ──────────────────────────────────
ALL_TOOLS="cursor kiro claude cline opencode antigravity trae trae-cn"

tool_dir() {
  case "$1" in
    cursor)       echo "$HOME/.cursor/skills" ;;
    kiro)         echo "$HOME/.kiro/skills" ;;
    claude)       echo "$HOME/.claude/skills" ;;
    cline)        echo "$HOME/.cline/skills" ;;
    opencode)     echo "$HOME/.config/opencode/skills" ;;
    antigravity)  echo "$HOME/.gemini/antigravity/skills" ;;
    trae)         echo "$HOME/.trae/skills" ;;
    trae-cn)      echo "$HOME/.trae-cn/skills" ;;
    *) return 1 ;;
  esac
}

# ── Parse arguments ─────────────────────────────────────────────────
TOOL="${1:-all}"
shift || true

# ── Resolve target tools ────────────────────────────────────────────
if [ "$TOOL" = "all" ]; then
  TARGET_TOOLS="$ALL_TOOLS"
else
  if ! tool_dir "$TOOL" >/dev/null 2>&1; then
    echo "Unknown tool: $TOOL"
    echo "Available: $ALL_TOOLS"
    exit 1
  fi
  TARGET_TOOLS="$TOOL"
fi

# ── Resolve target skills ───────────────────────────────────────────
SKILL_NAMES="$*"
if [ -z "$SKILL_NAMES" ]; then
  SKILL_NAMES=""
  for skill_md in "$SKILLS_SRC"/*/SKILL.md; do
    [ -f "$skill_md" ] || continue
    name="$(basename "$(dirname "$skill_md")")"
    SKILL_NAMES="$SKILL_NAMES $name"
  done
fi

# ── Rewrite scripts/ paths to absolute in a SKILL.md ────────────────
rewrite_script_paths() {
  local skill_md="$1"
  local skill_dir
  skill_dir="$(dirname "$skill_md")"
  local scripts_dir="$skill_dir/scripts"

  # Only rewrite if the skill actually has a scripts/ directory
  [ -d "$scripts_dir" ] || return 0

  local abs_scripts
  abs_scripts="$(cd "$scripts_dir" && pwd)"

  # Replace `scripts/` with the absolute path
  if [ "$(uname)" = "Darwin" ]; then
    sed -i '' "s|scripts/|${abs_scripts}/|g" "$skill_md"
  else
    sed -i "s|scripts/|${abs_scripts}/|g" "$skill_md"
  fi
}

# ── Install ─────────────────────────────────────────────────────────
installed=0
for tool in $TARGET_TOOLS; do
  dest_base="$(tool_dir "$tool")"

  for skill in $SKILL_NAMES; do
    src="$SKILLS_SRC/$skill"
    if [ ! -f "$src/SKILL.md" ]; then
      echo "  [skip] $skill — no SKILL.md found"
      continue
    fi

    dest="$dest_base/$skill"
    mkdir -p "$dest_base"
    rm -rf "$dest"
    cp -r "$src" "$dest"

    # Rewrite scripts/ to absolute paths
    rewrite_script_paths "$dest/SKILL.md"

    echo "  [ok]   $skill → $dest"
    installed=$((installed + 1))
  done
done

echo ""
echo "Installed $installed skill(s)."
