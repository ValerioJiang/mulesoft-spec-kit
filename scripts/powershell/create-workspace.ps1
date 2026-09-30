<#
.SYNOPSIS
Create or update a central Spec Kit workspace from this toolkit checkout (PowerShell twin of scripts/bash/create-workspace.sh).

.PARAMETER Target
Directory to create or update.

.PARAMETER Integration
Coding agent integration (default: claude).

.PARAMETER Script
Spec Kit helper-script variant: sh, ps or py (default: sh; use ps only if your agent runs in PowerShell and `python3` is on its PATH).

.PARAMETER WithSfWorkspace
Also install the optional sf-workspace add-on (extended Salesforce lifecycle; its prompts contain deploy/login/test commands).

.PARAMETER Update
Refresh the preset, extensions and workflow of an existing workspace.

.EXAMPLE
scripts\powershell\create-workspace.ps1 ..\my-workspace -Integration claude
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Target,
    [string]$Integration = "claude",
    [ValidateSet("sh", "ps", "py")][string]$Script = "sh",
    [switch]$WithSfWorkspace,
    [switch]$Update
)
$ErrorActionPreference = "Stop"

function Fail($message) { Write-Error "create-workspace: $message"; exit 1 }
function Run($exe, [string[]]$arguments) {
    & $exe @arguments
    if ($LASTEXITCODE -ne 0) { Fail "$exe $($arguments -join ' ') failed with exit code $LASTEXITCODE" }
}

$toolkit = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path.TrimEnd('\')
if (-not (Get-Command specify -ErrorAction SilentlyContinue)) { Fail "specify CLI not found on PATH" }

# Every refusal is decided before anything is created.
$targetPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Target).TrimEnd('\')
$ignoreCase = [System.StringComparison]::OrdinalIgnoreCase
if ($targetPath.Equals($toolkit, $ignoreCase) -or $targetPath.StartsWith("$toolkit\", $ignoreCase)) {
    Fail "refusing to create a workspace inside the toolkit checkout ($toolkit)"
}
$hasSpecify = Test-Path (Join-Path $targetPath ".specify")
if ($hasSpecify -and -not $Update) { Fail "$targetPath is already a Spec Kit project; re-run with -Update to refresh the toolkit components" }
if (-not $hasSpecify -and $Update) { Fail "$targetPath is not a Spec Kit project yet; run without -Update" }
New-Item -ItemType Directory -Force -Path $targetPath | Out-Null

$extensions = @("technical-solution", "mulesoft", "salesforce")
if ($WithSfWorkspace) { $extensions += "sf-workspace" }

Push-Location $targetPath
try {
    if (-not $Update) {
        $initArgs = @("init", "--here", "--force", "--non-interactive", "--ignore-agent-tools",
                      "--integration", $Integration, "--script", $Script,
                      "--preset", (Join-Path $toolkit "presets\central-workspace"))
        foreach ($ext in $extensions) { $initArgs += @("--extension", (Join-Path $toolkit "extensions\$ext")) }
        Run "specify" $initArgs
        Run "specify" @("workflow", "add", "--dev", (Join-Path $toolkit "workflows\technical-solution"))
    } else {
        if (Test-Path ".specify\presets\central-workspace") {
            Run "specify" @("preset", "update", "central-workspace", "--dev", (Join-Path $toolkit "presets\central-workspace"))
        } else {
            Run "specify" @("preset", "add", "--dev", (Join-Path $toolkit "presets\central-workspace"))
        }
        foreach ($ext in $extensions) {
            Run "specify" @("extension", "add", "--dev", (Join-Path $toolkit "extensions\$ext"), "--force")
        }
        & specify workflow remove technical-solution 2>$null | Out-Null
        Run "specify" @("workflow", "add", "--dev", (Join-Path $toolkit "workflows\technical-solution"))
    }

    # `specify extension add --dev` links every generated command to a cache under
    # .specify\extensions\<id>\.specify-dev\. A workspace is a shared repository, and Git checks
    # symlinks out as plain text files where they are unsupported (the Windows default), so turn
    # the links back into regular files. `specify init` writes regular files already.
    Get-ChildItem -LiteralPath $targetPath -Recurse -Force -File -Attributes ReparsePoint |
        Where-Object { $_.FullName -notlike "$targetPath\.git\*" -and (($_.Target -join '') -replace '/', '\') -like '*.specify-dev\*' } |
        ForEach-Object {
            $content = [System.IO.File]::ReadAllBytes($_.FullName)
            Remove-Item -LiteralPath $_.FullName -Force
            [System.IO.File]::WriteAllBytes($_.FullName, $content)
        }

    # Verify every component is present; specify init returns 0 even when a component failed.
    $missing = @()
    if (-not (Test-Path ".specify\presets\central-workspace\preset.yml")) { $missing += "preset central-workspace" }
    foreach ($ext in $extensions) {
        if (-not (Test-Path ".specify\extensions\$ext\extension.yml")) { $missing += "extension $ext" }
    }
    if (-not (Test-Path ".specify\workflows\technical-solution\workflow.yml")) { $missing += "workflow technical-solution" }
    if ($missing.Count -gt 0) { Fail ("workspace verification failed; missing: " + ($missing -join ", ")) }

    # Seed the root .gitignore (machine-local registry, Python bytecode, local agent settings,
    # the dev-install cache of the CLI).
    $lines = @("spec-kit-workspace.local.json", "__pycache__/", "*.pyc", ".claude/settings.local.json", ".specify-dev/")
    $existing = @()
    if (Test-Path ".gitignore") { $existing = Get-Content ".gitignore" }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    foreach ($line in $lines) {
        if ($existing -notcontains $line) {
            [System.IO.File]::AppendAllText((Join-Path $targetPath ".gitignore"), "$line`n", $utf8NoBom)
        }
    }
}
finally { Pop-Location }

Write-Host ""
Write-Host "Workspace ready at: $targetPath  (integration: $Integration, scripts: $Script, extensions: $($extensions -join ' '))"
Write-Host "Next: open your coding agent there and run /speckit-technical-solution-setup"
Write-Host "      (creates spec-kit-workspace.json, initiatives/ and .specify/profiles/ without overwriting anything)."
