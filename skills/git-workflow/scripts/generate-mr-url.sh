#!/usr/bin/env bash

set -euo pipefail

remote="origin"
source_branch="${1:-$(git rev-parse --abbrev-ref HEAD)}"
target_branch="${2:-}"

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "Error: not inside a git repository" >&2
  exit 1
}

remote_url="$(git remote get-url "$remote" 2>/dev/null || true)"
if [[ -z "$remote_url" ]]; then
  echo "Error: remote '$remote' not found" >&2
  exit 1
fi

host=""
project=""

if [[ "$remote_url" =~ ^git@([^:]+):(.+)$ ]]; then
  host="${BASH_REMATCH[1]}"
  project="${BASH_REMATCH[2]}"
elif [[ "$remote_url" =~ ^https?://([^/]+)/(.+)$ ]]; then
  host="${BASH_REMATCH[1]}"
  project="${BASH_REMATCH[2]}"
else
  echo "Error: unsupported remote URL format: $remote_url" >&2
  exit 1
fi

project="${project%.git}"

if [[ -z "$target_branch" ]]; then
  target_branch="$(git symbolic-ref "refs/remotes/${remote}/HEAD" 2>/dev/null | sed "s@^refs/remotes/${remote}/@@")"
fi
if [[ -z "$target_branch" ]] && git show-ref --verify --quiet "refs/remotes/${remote}/main"; then
  target_branch="main"
fi
if [[ -z "$target_branch" ]]; then
  target_branch="master"
fi

urlencode() {
  python3 -c 'import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$1"
}

encoded_source="$(urlencode "$source_branch")"
encoded_target="$(urlencode "$target_branch")"

echo "https://${host}/${project}/-/merge_requests/new?merge_request%5Bsource_branch%5D=${encoded_source}&merge_request%5Btarget_branch%5D=${encoded_target}"
