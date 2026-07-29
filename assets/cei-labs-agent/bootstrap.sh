#!/usr/bin/env bash
#
# CEI Labs Agent — one-command bootstrap for macOS and Linux.
#
# What this does, in order:
#   1. Sanity-checks the environment and free disk space.
#   2. Installs Ollama (the local model runtime) if it is missing.
#   3. Installs uv (a fast, self-contained Python package/tool manager) if missing.
#   4. Installs the `ctf-agent` command from the CEI Labs Agent repository.
#   5. Launches the agent, which opens in your web browser.
#
# It is intentionally defensive: it never assumes a tool exists, prints friendly
# guidance on failure, and refuses to proceed if the machine is short on disk.
#
# Usage (CEI Labs CTF -- "AI Copilot Setup" track):
#   Download this exact file from the challenge page and run it directly:
#     sh bootstrap.sh
#
# You can re-run this script any time; it is safe to run repeatedly.

# Fail fast on errors and unset variables. `pipefail` is NOT POSIX: some /bin/sh
# implementations (e.g. older dash, the default on many Linux distros) reject
# `set -o pipefail` with an "Illegal option" error, which would abort the whole
# installer on the documented `curl … | sh` path. So enable it only when the
# running shell actually supports it, keeping this script safe under any sh.
set -eu
if ( set -o pipefail ) 2>/dev/null; then
  set -o pipefail
fi

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# TEMPORARY PIN (CEI Labs CTF distribution copy only -- not the upstream
# repo's own bootstrap.sh): pinned to stoptalkingishh's fork/branch because
# it carries ctf-agent-verify, which this CTF's "AI Copilot Setup" track
# depends on, and that isn't merged into Judgernaut777/CEI-Labs-Agent's
# default branch yet (see https://github.com/Judgernaut777/CEI-Labs-Agent/pull/2).
# Once that PR merges, switch this back to:
#   REPO_URL="git+https://github.com/Judgernaut777/CEI-Labs-Agent"
REPO_URL="git+https://github.com/stoptalkingishh/CEI-Labs-Agent@feature/ctf-verify-tool"
# Minimum free disk space we insist on before installing models + tooling (GB).
MIN_FREE_GB=6

# ---------------------------------------------------------------------------
# Pretty output helpers (fall back to plain text if the terminal is dumb).
# ---------------------------------------------------------------------------
if [ -t 1 ] && command -v tput >/dev/null 2>&1 && [ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]; then
  BOLD="$(tput bold)"; DIM="$(tput dim)"; RED="$(tput setaf 1)"
  GREEN="$(tput setaf 2)"; YELLOW="$(tput setaf 3)"; BLUE="$(tput setaf 4)"; RESET="$(tput sgr0)"
else
  BOLD=""; DIM=""; RED=""; GREEN=""; YELLOW=""; BLUE=""; RESET=""
fi

info()  { printf '%s\n' "${BLUE}${BOLD}==>${RESET} $*"; }
ok()    { printf '%s\n' "${GREEN}${BOLD} ✓ ${RESET} $*"; }
warn()  { printf '%s\n' "${YELLOW}${BOLD} ! ${RESET} $*" >&2; }
err()   { printf '%s\n' "${RED}${BOLD} ✗ ${RESET} $*" >&2; }
die()   { err "$*"; exit 1; }

have()  { command -v "$1" >/dev/null 2>&1; }

# Prepend a directory to PATH for the remainder of this script's run, so a
# freshly-installed tool becomes usable immediately without a shell restart.
prepend_path() {
  case ":${PATH}:" in
    *":$1:"*) : ;;                 # already present, do nothing
    *) export PATH="$1:${PATH}" ;;
  esac
}

# ---------------------------------------------------------------------------
# 0. Greeting + platform detection
# ---------------------------------------------------------------------------
printf '\n'
info "CEI Labs Agent — setup starting"
printf '%s\n' "${DIM}    A friendly, local AI teammate for beginner CTFs (Bandit, Krypton, Natas).${RESET}"
printf '\n'

OS="$(uname -s 2>/dev/null || echo unknown)"
case "${OS}" in
  Darwin) PLATFORM="macos" ;;
  Linux)  PLATFORM="linux" ;;
  *) die "Unsupported operating system: '${OS}'. This installer supports macOS and Linux. On Windows, use bootstrap.ps1 instead." ;;
esac
ok "Detected platform: ${PLATFORM}"

# ---------------------------------------------------------------------------
# 1. Disk-space preflight
# ---------------------------------------------------------------------------
# We measure free space on $HOME because that is where uv tools, the Python
# environment, and (by default) Ollama models are written.
check_disk_space() {
  local target="${HOME:-/}"
  local free_gb=""

  # `df -Pk` is POSIX and prints available blocks in 1K units in column 4.
  if have df; then
    local avail_k
    avail_k="$(df -Pk "${target}" 2>/dev/null | awk 'NR==2 {print $4}')" || avail_k=""
    if [ -n "${avail_k}" ]; then
      # Convert KiB -> GB (integer division; conservative rounding down).
      free_gb=$(( avail_k / 1024 / 1024 ))
    fi
  fi

  if [ -z "${free_gb}" ]; then
    warn "Could not determine free disk space; continuing anyway."
    return 0
  fi

  info "Free disk space on ${target}: ~${free_gb} GB"
  if [ "${free_gb}" -lt "${MIN_FREE_GB}" ]; then
    err "Only ~${free_gb} GB free, but at least ${MIN_FREE_GB} GB is recommended."
    err "Local AI models are large. Free up some space and re-run this installer."
    die "Aborting to avoid a half-finished install."
  fi
  ok "Disk space looks sufficient."
}
check_disk_space

# ---------------------------------------------------------------------------
# 2. Install Ollama (local model runtime) if missing
# ---------------------------------------------------------------------------
install_ollama() {
  if have ollama; then
    ok "Ollama is already installed ($(ollama --version 2>/dev/null | head -n1 || echo 'version unknown'))."
    return 0
  fi

  info "Installing Ollama (this powers the local AI models)…"
  if [ "${PLATFORM}" = "macos" ] && have brew; then
    # Prefer Homebrew on macOS when available — cleaner uninstall path.
    if brew install ollama; then
      ok "Ollama installed via Homebrew."
      return 0
    fi
    warn "Homebrew install failed; falling back to the official script."
  fi

  if ! have curl; then
    die "curl is required to install Ollama but was not found. Install curl and re-run."
  fi

  # The official one-line installer. Piping to sh is Ollama's documented method.
  if curl -fsSL https://ollama.com/install.sh | sh; then
    ok "Ollama installed."
  else
    err "The Ollama installer did not complete successfully."
    err "You can install it manually from https://ollama.com/download and then re-run this script."
    die "Cannot continue without Ollama."
  fi
}
install_ollama

# Make sure a freshly-installed ollama is on PATH for the rest of this run.
prepend_path "/usr/local/bin"
prepend_path "/opt/homebrew/bin"

# ---------------------------------------------------------------------------
# 3. Install uv (Python tool manager) if missing
# ---------------------------------------------------------------------------
install_uv() {
  if have uv; then
    ok "uv is already installed ($(uv --version 2>/dev/null || echo 'version unknown'))."
    return 0
  fi

  info "Installing uv (a fast, self-contained Python installer)…"
  if ! have curl; then
    die "curl is required to install uv but was not found. Install curl and re-run."
  fi

  if curl -LsSf https://astral.sh/uv/install.sh | sh; then
    ok "uv installed."
  else
    die "The uv installer failed. See https://docs.astral.sh/uv/ for manual instructions."
  fi

  # uv installs to ~/.local/bin (or ~/.cargo/bin on older versions). Add both so
  # the `uv` command is usable immediately, before any shell restart.
  prepend_path "${HOME}/.local/bin"
  prepend_path "${HOME}/.cargo/bin"

  # Some uv versions ship an env file that also fixes PATH; source it if present.
  if [ -f "${HOME}/.local/bin/env" ]; then
    # shellcheck disable=SC1091
    . "${HOME}/.local/bin/env" || true
  fi

  have uv || die "uv was installed but is not on PATH. Open a new terminal and re-run this script."
}
install_uv

# ---------------------------------------------------------------------------
# 4. Install the CEI Labs Agent CLI (`ctf-agent`) from the repository
# ---------------------------------------------------------------------------
install_agent() {
  info "Installing the CEI Labs Agent (ctf-agent)…"
  # `uv tool install` creates an isolated environment and exposes the entry point.
  # `--force` makes re-runs upgrade a previous install instead of erroring.
  if uv tool install --force "${REPO_URL}"; then
    ok "ctf-agent installed."
  else
    die "Installing ctf-agent failed. Check your network connection and re-run."
  fi

  # Ensure uv's tool-bin directory is on PATH (it is ~/.local/bin by default).
  uv tool update-shell >/dev/null 2>&1 || true
  prepend_path "${HOME}/.local/bin"
}
install_agent

# ---------------------------------------------------------------------------
# 5. Launch
# ---------------------------------------------------------------------------
printf '\n'
ok "Setup complete!"
printf '%s\n' "${DIM}    From now on you can start the agent any time by running:${RESET} ${BOLD}ctf-agent${RESET}"
printf '\n'

if have ctf-agent; then
  info "Launching CEI Labs Agent — it will open in your web browser…"
  # `exec` hands the terminal over to the agent so Ctrl-C stops it cleanly.
  exec ctf-agent
else
  warn "ctf-agent is installed but not yet on this shell's PATH."
  warn "Open a NEW terminal window and run:  ctf-agent"
  exit 0
fi
