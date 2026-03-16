#!/usr/bin/env bash
# Check prerequisites required by ai-cookbook MCPs and CLIs.
# Reports missing tools and offers to install them.

set -euo pipefail

missing=()

echo "Checking prerequisites..."
echo ""

# --- Node.js / npm / npx ---
if command -v node &>/dev/null; then
  echo "✅ node $(node --version)"
else
  echo "❌ node: not found"
  missing+=("node")
fi

if command -v npm &>/dev/null; then
  echo "✅ npm $(npm --version)"
else
  echo "❌ npm: not found"
  missing+=("npm")
fi

if command -v npx &>/dev/null; then
  echo "✅ npx $(npx --version)"
else
  echo "❌ npx: not found"
  missing+=("npx")
fi

# --- Python ---
if command -v python3 &>/dev/null; then
  echo "✅ python3 $(python3 --version 2>&1 | awk '{print $2}')"
elif command -v python &>/dev/null; then
  echo "✅ python $(python --version 2>&1 | awk '{print $2}')"
else
  echo "❌ python: not found"
  missing+=("python")
fi

# --- uv / uvx ---
if command -v uv &>/dev/null; then
  echo "✅ uv $(uv --version 2>&1 | awk '{print $2}')"
else
  echo "❌ uv: not found"
  missing+=("uv")
fi

if command -v uvx &>/dev/null; then
  echo "✅ uvx (available)"
else
  echo "❌ uvx: not found (installed with uv)"
  missing+=("uvx")
fi

# --- Git (nice to have) ---
if command -v git &>/dev/null; then
  echo "✅ git $(git --version | awk '{print $3}')"
else
  echo "❌ git: not found"
  missing+=("git")
fi

# --- gh (for GitHub CLI) ---
if command -v gh &>/dev/null; then
  echo "✅ gh ($(which gh))"
  if ! gh auth status &>/dev/null; then
    echo "   ⚠️  gh is not authenticated. Please run 'gh auth login'."
  fi
else
  echo "❌ gh: not found"
  missing+=("gh")
fi

# --- glab (for GitLab CLI) ---
if command -v glab &>/dev/null; then
  echo "✅ glab ($(which glab))"
  if ! glab auth status &>/dev/null; then
    echo "   ⚠️  glab is not authenticated. Please run 'glab auth login'."
  fi
else
  echo "❌ glab: not found"
  missing+=("glab")
fi

# --- mcp-grafana (for Grafana MCP) ---
if command -v mcp-grafana &>/dev/null; then
  echo "✅ mcp-grafana ($(which mcp-grafana))"
else
  echo "❌ mcp-grafana: not found"
  missing+=("mcp-grafana")
fi

# --- macOS: OpenSSL cert for markitdown CLI (HTTPS URL fetching) ---
if [[ "$(uname)" == "Darwin" ]]; then
  if [ -f /opt/homebrew/etc/openssl@3/cert.pem ]; then
    echo "✅ openssl@3 cert (/opt/homebrew/etc/openssl@3/cert.pem)"
  else
    echo "⚠️  openssl@3 cert: not found (optional, for markitdown CLI HTTPS URL fetching on macOS)"
    missing+=("openssl@3")
  fi
fi

# --- mysql client (for mysql-cli skill) ---
if command -v mysql &>/dev/null; then
  echo "✅ mysql $(mysql --version 2>&1 | head -1)"
else
  echo "❌ mysql: not found (needed by mysql-cli skill)"
  missing+=("mysql")
fi

# --- markitdown (for markitdown skill) ---
if command -v markitdown &>/dev/null; then
  echo "✅ markitdown ($(which markitdown))"
else
  echo "❌ markitdown: not found (needed by markitdown skill)"
  missing+=("markitdown")
fi

echo ""

# --- Summary ---
if [ ${#missing[@]} -eq 0 ]; then
  echo "All prerequisites are installed. You're good to go."
  exit 0
fi

echo "Missing: ${missing[*]}"
echo ""
echo "These are needed by:"
echo "  node/npm/npx        → chrome-devtools MCP, maven-indexer MCP, playwright-cli"
echo "  git                 → git-workflow skill"
echo "  gh                  → github-cli skill"
echo "  glab                → gitlab-cli skill"
echo "  mcp-grafana         → Grafana MCP"
echo "  openssl@3           → markitdown CLI (macOS SSL cert for HTTPS URLs)"
echo "  mysql               → mysql-cli skill"
echo "  markitdown          → markitdown skill"
echo ""

# --- Helper function to install Python package via all available pip tools ---
pip_install_all() {
  local package="$1"
  local installed=false
  
  if command -v pipx &>/dev/null; then
    echo "Installing via pipx (recommended for CLI tools)..."
    pipx install "$package" && installed=true
  fi
  if command -v pip3 &>/dev/null; then
    echo "Installing via pip3 (Python $(pip3 --version | grep -oP 'python \K[0-9]+'))..."
    pip3 install "$package" && installed=true
  fi
  if command -v pip &>/dev/null; then
    echo "Installing via pip..."
    pip install "$package" && installed=true
  fi
  
  if [[ "$installed" == true ]]; then
    return 0
  else
    return 1
  fi
}

# --- Interactive install offers ---
# Only offer if running in an interactive terminal
if [ ! -t 0 ]; then
  echo "Run this script in an interactive terminal to get install prompts."
  exit 1
fi

# Track what we've already asked about to avoid duplicate prompts
asked_node=false
asked_uv=false

for tool in "${missing[@]}"; do
  case "$tool" in
    node|npm|npx)
      if [ "$asked_node" = false ]; then
        asked_node=true
        read -rp "Install Node.js (via Homebrew)? [y/N] " ans
        if [[ "$ans" =~ ^[Yy]$ ]]; then
          if command -v brew &>/dev/null; then
            brew install node
          else
            echo "Homebrew not found. Install Node.js from https://nodejs.org/"
          fi
        fi
      fi
      ;;
    python)
      read -rp "Install Python 3 (via Homebrew)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if command -v brew &>/dev/null; then
          brew install python
        else
          echo "Homebrew not found. Install Python from https://www.python.org/"
        fi
      fi
      ;;
    uv|uvx)
      if [ "$asked_uv" = false ]; then
        asked_uv=true
        read -rp "Install uv (includes uvx)? [y/N] " ans
        if [[ "$ans" =~ ^[Yy]$ ]]; then
          if command -v brew &>/dev/null; then
            brew install uv
          elif command -v pip3 &>/dev/null; then
            pip3 install uv
          elif command -v pip &>/dev/null; then
            pip install uv
          else
            echo "No package manager found. Install uv from https://docs.astral.sh/uv/getting-started/installation/"
          fi
        fi
      fi
      ;;
    git)
      read -rp "Install git (via Homebrew)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if command -v brew &>/dev/null; then
          brew install git
        else
          echo "Homebrew not found. Install git from https://git-scm.com/"
        fi
      fi
      ;;
    gh)
      read -rp "Install GitHub CLI (gh) (via Homebrew)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if command -v brew &>/dev/null; then
          brew install gh
          echo ""
          if ! gh auth status &>/dev/null; then
            echo "⚠️  GitHub CLI is not authenticated."
            echo "   Please run 'gh auth login' to authenticate."
          fi
        else
          echo "Homebrew not found. Install from https://cli.github.com/manual/installation"
        fi
      fi
      ;;
    glab)
      read -rp "Install GitLab CLI (glab) (via Homebrew)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if command -v brew &>/dev/null; then
          brew install glab
          echo ""
          if ! glab auth status &>/dev/null; then
            echo "⚠️  GitLab CLI is not authenticated."
            echo "   Please run 'glab auth login' to authenticate."
          fi
        else
          echo "Homebrew not found. Install from https://gitlab.com/gitlab-org/cli#installation"
        fi
      fi
      ;;
    mcp-grafana)
      read -rp "Install mcp-grafana (via Homebrew)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if command -v brew &>/dev/null; then
          brew install mcp-grafana
        elif command -v go &>/dev/null; then
          echo "Installing via go install..."
          go install github.com/grafana/mcp-grafana@latest
        else
          echo "Install from https://github.com/grafana/mcp-grafana/releases"
        fi
      fi
      ;;
    openssl@3)
      read -rp "Install openssl@3 (via Homebrew, for markitdown CLI SSL)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if command -v brew &>/dev/null; then
          brew install openssl@3
        else
          echo "Homebrew not found. Install from https://brew.sh/ first, then: brew install openssl@3"
        fi
      fi
      ;;
    mysql)
      read -rp "Install mysql client (via Homebrew)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if command -v brew &>/dev/null; then
          brew install mysql-client
          echo "You may need to add mysql-client to your PATH:"
          echo "  echo 'export PATH=\"/opt/homebrew/opt/mysql-client/bin:\$PATH\"' >> ~/.zshrc"
        else
          echo "Homebrew not found. Install from https://dev.mysql.com/downloads/shell/"
        fi
      fi
      ;;
    markitdown)
      read -rp "Install markitdown (via pipx/pip)? [y/N] " ans
      if [[ "$ans" =~ ^[Yy]$ ]]; then
        if pip_install_all 'markitdown[all]'; then
          echo "CLI installed to: $(which markitdown 2>/dev/null || echo 'run: hash -r && which markitdown')"
        else
          echo "pip/pipx not found. Install from https://pypi.org/project/markitdown/"
        fi
      fi
      ;;
  esac
done

echo ""
echo "Done. Re-run this script to verify."
