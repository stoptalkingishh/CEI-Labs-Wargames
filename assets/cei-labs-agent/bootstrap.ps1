<#
.SYNOPSIS
    CEI Labs Agent — one-command bootstrap for Windows (PowerShell).

.DESCRIPTION
    What this does, in order:
      1. Sanity-checks the environment and free disk space.
      2. Installs Ollama (the local model runtime) per-user and silently if missing,
         with a guided manual fallback if the silent install is not possible.
      3. Installs uv (a fast, self-contained Python package/tool manager) if missing.
      4. Installs the `ctf-agent` command from the CEI Labs Agent repository.
      5. Launches the agent, which opens in your web browser.

    It is intentionally defensive: it never assumes a tool exists, prints friendly
    guidance on failure, and refuses to proceed if the machine is short on disk.

.EXAMPLE
    CEI Labs CTF -- "AI Copilot Setup" track: download this exact file from
    the challenge page, then in PowerShell:
      powershell -ExecutionPolicy Bypass -File .\bootstrap.ps1

.NOTES
    Re-running this script is safe; it upgrades existing installs in place.
#>

# Stop on the first unhandled error so we never leave a half-finished install.
$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# TEMPORARY PIN (CEI Labs CTF distribution copy only -- not the upstream
# repo's own bootstrap.ps1): pinned to stoptalkingishh's fork/branch because
# it carries ctf-agent-verify, which this CTF's "AI Copilot Setup" track
# depends on, and that isn't merged into Judgernaut777/CEI-Labs-Agent's
# default branch yet (see https://github.com/Judgernaut777/CEI-Labs-Agent/pull/2).
# Once that PR merges, switch this back to:
#   $RepoUrl = 'git+https://github.com/Judgernaut777/CEI-Labs-Agent'
$RepoUrl   = 'git+https://github.com/stoptalkingishh/CEI-Labs-Agent@feature/ctf-verify-tool'
$MinFreeGB = 6                                   # Minimum recommended free disk (GB).
$OllamaUrl = 'https://ollama.com/download/OllamaSetup.exe'

# ---------------------------------------------------------------------------
# Pretty output helpers
# ---------------------------------------------------------------------------
function Write-Info  { param([string]$Msg) Write-Host "==> $Msg" -ForegroundColor Cyan }
function Write-Ok    { param([string]$Msg) Write-Host " OK  $Msg" -ForegroundColor Green }
function Write-Warn2 { param([string]$Msg) Write-Host " !   $Msg" -ForegroundColor Yellow }
function Write-Err2  { param([string]$Msg) Write-Host " X   $Msg" -ForegroundColor Red }
function Die         { param([string]$Msg) Write-Err2 $Msg; exit 1 }

function Test-Command {
    # Returns $true if the named command is resolvable on PATH.
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Update-SessionPath {
    # Rebuild this process's PATH from the persisted Machine + User values so a
    # freshly-installed tool becomes usable without opening a new terminal.
    $machine = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user    = [System.Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = (@($machine, $user) | Where-Object { $_ }) -join ';'
}

function Add-SessionPath {
    # Prepend a directory to this process's PATH if it is not already present.
    param([string]$Dir)
    if (-not $Dir) { return }
    if (($env:Path -split ';') -notcontains $Dir) {
        $env:Path = "$Dir;$env:Path"
    }
}

# ---------------------------------------------------------------------------
# 0. Greeting + prerequisite checks
# ---------------------------------------------------------------------------
Write-Host ''
Write-Info 'CEI Labs Agent — setup starting'
Write-Host '    A friendly, local AI teammate for beginner CTFs (Bandit, Krypton, Natas).' -ForegroundColor DarkGray
Write-Host ''

# TLS 1.2 is required for downloads on older Windows PowerShell (5.x).
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch { }

if (-not (Test-Command 'powershell') -and -not (Test-Command 'pwsh')) {
    Die 'PowerShell was not detected. This should not happen — please report it.'
}

# ---------------------------------------------------------------------------
# 1. Disk-space preflight
# ---------------------------------------------------------------------------
function Test-DiskSpace {
    # Measure free space on the system drive (where user installs + models land).
    $drive = $env:SystemDrive
    if (-not $drive) { $drive = 'C:' }
    try {
        $letter = $drive.TrimEnd(':')
        $psDrive = Get-PSDrive -Name $letter -ErrorAction Stop
        $freeGB = [math]::Floor($psDrive.Free / 1GB)
    } catch {
        Write-Warn2 'Could not determine free disk space; continuing anyway.'
        return
    }

    Write-Info "Free disk space on ${drive}: ~$freeGB GB"
    if ($freeGB -lt $MinFreeGB) {
        Write-Err2 "Only ~$freeGB GB free, but at least $MinFreeGB GB is recommended."
        Write-Err2 'Local AI models are large. Free up some space and re-run this installer.'
        Die 'Aborting to avoid a half-finished install.'
    }
    Write-Ok 'Disk space looks sufficient.'
}
Test-DiskSpace

# ---------------------------------------------------------------------------
# 2. Install Ollama (local model runtime) if missing
# ---------------------------------------------------------------------------
function Install-Ollama {
    if (Test-Command 'ollama') {
        Write-Ok 'Ollama is already installed.'
        return
    }

    Write-Info 'Installing Ollama (this powers the local AI models)…'

    # Prefer winget when available — cleanest per-user, silent path.
    if (Test-Command 'winget') {
        try {
            winget install --id Ollama.Ollama --accept-package-agreements --accept-source-agreements --silent --scope user
            if ($LASTEXITCODE -eq 0) {
                Write-Ok 'Ollama installed via winget.'
                Update-SessionPath
                Add-SessionPath (Join-Path $env:LOCALAPPDATA 'Programs\Ollama')
                return
            }
            Write-Warn2 'winget install did not complete; falling back to the direct installer.'
        } catch {
            Write-Warn2 "winget install failed ($($_.Exception.Message)); falling back to the direct installer."
        }
    }

    # Direct download of the official per-user installer, run silently.
    $tmp = Join-Path $env:TEMP 'OllamaSetup.exe'
    try {
        Write-Info "Downloading Ollama installer from $OllamaUrl …"
        Invoke-WebRequest -Uri $OllamaUrl -OutFile $tmp -UseBasicParsing
    } catch {
        Write-Err2 "Could not download the Ollama installer: $($_.Exception.Message)"
        Show-OllamaManualFallback
        Die 'Cannot continue without Ollama.'
    }

    try {
        # /VERYSILENT + /SUPPRESSMSGBOXES is the Inno Setup unattended flag set the
        # Ollama installer honours. It installs per-user, no admin prompt required.
        Write-Info 'Running the Ollama installer silently…'
        $proc = Start-Process -FilePath $tmp `
            -ArgumentList '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART' `
            -Wait -PassThru
        if ($proc.ExitCode -ne 0) {
            throw "installer exited with code $($proc.ExitCode)"
        }
        Write-Ok 'Ollama installed.'
    } catch {
        Write-Warn2 "Silent install failed: $($_.Exception.Message)"
        Write-Info 'Launching the installer interactively so you can click through it…'
        try {
            Start-Process -FilePath $tmp -Wait
        } catch {
            Show-OllamaManualFallback
            Die 'Cannot continue without Ollama.'
        }
    } finally {
        Remove-Item $tmp -ErrorAction SilentlyContinue
    }

    Update-SessionPath
    Add-SessionPath (Join-Path $env:LOCALAPPDATA 'Programs\Ollama')

    if (-not (Test-Command 'ollama')) {
        Write-Warn2 'Ollama was installed but is not yet on this shell''s PATH.'
        Write-Warn2 'That is fine — the agent talks to Ollama over the network, not the CLI.'
    }
}

function Show-OllamaManualFallback {
    Write-Host ''
    Write-Warn2 'Automatic Ollama installation was not possible on this machine.'
    Write-Host  '    Please install it manually (no admin rights needed):' -ForegroundColor DarkGray
    Write-Host  '      1. Open https://ollama.com/download in your browser.' -ForegroundColor DarkGray
    Write-Host  '      2. Download and run OllamaSetup.exe.' -ForegroundColor DarkGray
    Write-Host  '      3. Re-run this bootstrap script.' -ForegroundColor DarkGray
    Write-Host ''
}
Install-Ollama

# ---------------------------------------------------------------------------
# 3. Install uv (Python tool manager) if missing
# ---------------------------------------------------------------------------
function Install-Uv {
    if (Test-Command 'uv') {
        Write-Ok 'uv is already installed.'
        return
    }

    Write-Info 'Installing uv (a fast, self-contained Python installer)…'
    try {
        # Official Astral installer; installs per-user to ~\.local\bin.
        powershell -ExecutionPolicy ByPass -NoProfile -Command `
            "irm https://astral.sh/uv/install.ps1 | iex"
    } catch {
        Die "The uv installer failed: $($_.Exception.Message). See https://docs.astral.sh/uv/ for manual steps."
    }

    Update-SessionPath
    Add-SessionPath (Join-Path $env:USERPROFILE '.local\bin')

    if (-not (Test-Command 'uv')) {
        Die 'uv was installed but is not on PATH. Open a new PowerShell window and re-run this script.'
    }
    Write-Ok 'uv installed.'
}
Install-Uv

# ---------------------------------------------------------------------------
# 4. Install the CEI Labs Agent CLI (`ctf-agent`) from the repository
# ---------------------------------------------------------------------------
function Install-Agent {
    Write-Info 'Installing the CEI Labs Agent (ctf-agent)…'
    try {
        # --force upgrades a previous install instead of erroring on re-run.
        uv tool install --force $RepoUrl
        if ($LASTEXITCODE -ne 0) { throw "uv tool install exited with code $LASTEXITCODE" }
    } catch {
        Die "Installing ctf-agent failed: $($_.Exception.Message). Check your network and re-run."
    }

    # Ensure uv's tool-bin directory is registered on PATH for future terminals.
    try { uv tool update-shell | Out-Null } catch { }
    Update-SessionPath
    Add-SessionPath (Join-Path $env:USERPROFILE '.local\bin')
    Write-Ok 'ctf-agent installed.'
}
Install-Agent

# ---------------------------------------------------------------------------
# 5. Launch
# ---------------------------------------------------------------------------
Write-Host ''
Write-Ok 'Setup complete!'
Write-Host '    From now on you can start the agent any time by running:  ctf-agent' -ForegroundColor DarkGray
Write-Host ''

if (Test-Command 'ctf-agent') {
    Write-Info 'Launching CEI Labs Agent — it will open in your web browser…'
    ctf-agent
} else {
    Write-Warn2 'ctf-agent is installed but not yet on this shell''s PATH.'
    Write-Warn2 'Open a NEW PowerShell window and run:  ctf-agent'
    exit 0
}
