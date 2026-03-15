#!/bin/bash

# Get current branch if no argument provided
BRANCH=${1:-$(git rev-parse --abbrev-ref HEAD)}

# Get remote URL
REMOTE_URL=$(git remote get-url origin)

# Parse remote URL to extract host and project path
if [[ $REMOTE_URL =~ ^git@([^:]+):(.+)\.git$ ]]; then
    # SSH format: git@git.example.com:group/project.git
    HOST="${BASH_REMATCH[1]}"
    PROJECT="${BASH_REMATCH[2]}"
elif [[ $REMOTE_URL =~ ^https?://([^/]+)/(.+)\.git$ ]]; then
    # HTTPS format: https://git.example.com/group/project.git
    HOST="${BASH_REMATCH[1]}"
    PROJECT="${BASH_REMATCH[2]}"
else
    echo "Error: Unable to parse remote URL: $REMOTE_URL" >&2
    exit 1
fi

# URL encode the branch name
ENCODED_BRANCH=$(printf %s "$BRANCH" | jq -sRr @uri)

# Generate and output the merge request URL
echo "https://${HOST}/${PROJECT}/merge_requests/new?merge_request%5Bsource_branch%5D=${ENCODED_BRANCH}"
