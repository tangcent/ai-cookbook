#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: detect-active-branches.sh [--base <branch>] [--window <commits>] [--remote <name>]

Detect active feature/fix-style branches:
- branch name matches (feature|fix|hotfix|release|chore)/
- branch is ahead of origin/<base>
- merge-base with origin/<base> appears within latest <window> commits on base
EOF
}

base_branch=""
window=10
remote="origin"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base)
      base_branch="${2:-}"
      shift 2
      ;;
    --window)
      window="${2:-}"
      shift 2
      ;;
    --remote)
      remote="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "Error: not inside a git repository" >&2
  exit 1
}

if [[ -z "$base_branch" ]]; then
  base_branch="$(git symbolic-ref "refs/remotes/${remote}/HEAD" 2>/dev/null | sed "s@^refs/remotes/${remote}/@@")"
fi
if [[ -z "$base_branch" ]] && git show-ref --verify --quiet "refs/remotes/${remote}/main"; then
  base_branch="main"
fi
if [[ -z "$base_branch" ]]; then
  base_branch="master"
fi

if ! git show-ref --verify --quiet "refs/remotes/${remote}/${base_branch}"; then
  echo "Error: ${remote}/${base_branch} not found. Run 'git fetch ${remote}' first." >&2
  exit 1
fi

recent_commits="$(git rev-list --max-count "$window" "${remote}/${base_branch}")"

# Collect local and remote branch names, normalize remote refs.
branch_list="$(
  {
    git for-each-ref --format='%(refname:short)' refs/heads
    git for-each-ref --format='%(refname:short)' "refs/remotes/${remote}"
  } | sed "s@^${remote}/@@" | sed 's@^HEAD$@@' | sort -u
)"

echo "Checking active branches against ${remote}/${base_branch} (window=${window})..."
echo

found=0

while IFS= read -r branch; do
  [[ -z "$branch" ]] && continue
  [[ "$branch" == "$base_branch" ]] && continue
  [[ "$branch" =~ ^(feature|fix|hotfix|release|chore)/ ]] || continue

  if git show-ref --verify --quiet "refs/heads/${branch}"; then
    ref="${branch}"
  elif git show-ref --verify --quiet "refs/remotes/${remote}/${branch}"; then
    ref="${remote}/${branch}"
  else
    continue
  fi

  merge_base="$(git merge-base "$ref" "${remote}/${base_branch}" 2>/dev/null || true)"
  [[ -z "$merge_base" ]] && continue

  if ! grep -q "^${merge_base}$" <<<"$recent_commits"; then
    continue
  fi

  ahead_count="$(git rev-list --count "${remote}/${base_branch}..${ref}" 2>/dev/null || echo 0)"
  if [[ "$ahead_count" -gt 0 ]]; then
    printf '✓ %s (%s commits ahead)\n' "$branch" "$ahead_count"
    found=1
  fi
done <<<"$branch_list"

echo
if [[ "$found" -eq 0 ]]; then
  echo "No active feature/fix-style branches found."
fi
