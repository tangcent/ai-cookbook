#!/bin/bash
# Detect active feature branches based on latest 10 commits in master

set -e

# Detect default branch (main or master)
default_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

# Get latest 10 commit hashes from default branch
recent_commits=$(git log "$default_branch" -10 --pretty=format:"%H")

# Get all feature branches (local and remote)
branches=$(git branch -a | grep -E 'feature/' | sed 's/remotes\/origin\///' | sed 's/^\*\? *//' | sort -u)

echo "Checking active feature branches..."
echo ""

active_branches=()

for branch in $branches; do
    # Clean branch name
    clean_branch=$(echo "$branch" | sed 's/remotes\/origin\///')
    
    # Get merge-base
    merge_base=$(git merge-base "$clean_branch" "$default_branch" 2>/dev/null || echo "")
    
    if [ -z "$merge_base" ]; then
        continue
    fi
    
    # Check if merge-base is in recent commits
    if echo "$recent_commits" | grep -q "$merge_base"; then
        # Check if branch has commits ahead of default branch
        ahead_count=$(git rev-list "$default_branch".."$clean_branch" --count 2>/dev/null || echo "0")
        
        if [ "$ahead_count" -gt 0 ]; then
            active_branches+=("$clean_branch")
            echo "✓ $clean_branch ($ahead_count commits ahead)"
        fi
    fi
done

echo ""
if [ ${#active_branches[@]} -eq 0 ]; then
    echo "No active feature branches found."
    exit 0
fi

echo "Active branches: ${active_branches[@]}"
