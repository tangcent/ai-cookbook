#!/usr/bin/env bash
# install-skills.sh — Install skills into AI tool skill directories.
#
# After copying, rewrites `scripts/` references in SKILL.md to absolute paths
# so the AI agent can invoke them from any working directory, and inserts the
# target tool's runtime note (install/<tool>/runtime-note.md) into any SKILL.md
# that relies on sub-agent conventions the tool spells differently.
#
# Usage:
#   bash install/install-skills.sh [tool] [skill ...]
#
# Examples:
#   bash install/install-skills.sh kiro                  # all skills into Kiro
#   bash install/install-skills.sh codex                 # all skills into Codex
#   bash install/install-skills.sh workbuddy             # all skills into WorkBuddy
#   bash install/install-skills.sh all                   # all skills into all tools
#   bash install/install-skills.sh kiro mysql-cli        # one skill into Kiro
#   bash install/install-skills.sh workbuddy spec-driven # one skill into WorkBuddy

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"

# ── Tool → skill directory mapping ────────────────────────────────────
ALL_TOOLS="cursor kiro claude codex cline opencode antigravity trae trae-cn workbuddy"

tool_dir() {
  case "$1" in
    cursor)       echo "$HOME/.cursor/skills" ;;
    kiro)         echo "$HOME/.kiro/skills" ;;
    claude)       echo "$HOME/.claude/skills" ;;
    codex)        echo "$HOME/.codex/skills" ;;
    cline)        echo "$HOME/.cline/skills" ;;
    opencode)     echo "$HOME/.config/opencode/skills" ;;
    antigravity)  echo "$HOME/.gemini/antigravity/skills" ;;
    trae)         echo "$HOME/.trae/skills" ;;
    trae-cn)      echo "$HOME/.trae-cn/skills" ;;
    workbuddy)    echo "$HOME/.workbuddy/skills" ;;
    *) return 1 ;;
  esac
}

# ── Parse arguments ───────────────────────────────────────────────────
TOOL="${1:-all}"
shift || true

# ── Resolve target tools ──────────────────────────────────────────────
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

# ── Resolve target skills ─────────────────────────────────────────────
SKILL_NAMES="$*"
if [ -z "$SKILL_NAMES" ]; then
  SKILL_NAMES=""
  for skill_md in "$SKILLS_SRC"/*/SKILL.md; do
    [ -f "$skill_md" ] || continue
    name="$(basename "$(dirname "$skill_md")")"
    SKILL_NAMES="$SKILL_NAMES $name"
  done
fi

# ── Rewrite scripts/ paths to absolute in a SKILL.md ──────────────────
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

# ── Insert tool-specific runtime note ─────────────────────────────────
# A tool can ship install/<tool>/runtime-note.md describing how its runtime
# deviates from the upstream conventions (e.g. WorkBuddy names the sub-agent
# tool `Agent`, not `Task`). The note is inserted right after the YAML
# frontmatter — prepending it would break frontmatter parsing. Only SKILL.md
# files that spawn sub-agents (they declare `subagent_type`) get the note.
apply_runtime_note() {
  local skill_md="$1"
  local tool="$2"
  local note="$SCRIPT_DIR/$tool/runtime-note.md"

  [ -f "$note" ] || return 0
  grep -q 'subagent_type' "$skill_md" || return 0

  # Last line of the frontmatter block (tolerates CRLF)
  local fm_end
  fm_end="$(awk 'NR>1 { line=$0; sub(/\r$/, "", line); if (line=="---") { print NR; exit } }' "$skill_md")"
  [ -n "$fm_end" ] || return 0

  local tmp
  tmp="$(mktemp)"
  {
    head -n "$fm_end" "$skill_md"
    printf '\n'
    cat "$note"
    tail -n "+$((fm_end + 1))" "$skill_md"
  } > "$tmp"
  mv "$tmp" "$skill_md"
}

# ── Install ───────────────────────────────────────────────────────────
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

    # Insert the tool's runtime note when the runtime deviates
    apply_runtime_note "$dest/SKILL.md" "$tool"

    echo "  [ok]   $skill → $dest"
    installed=$((installed + 1))
  done
done

echo ""
echo "Installed $installed skill(s)."
