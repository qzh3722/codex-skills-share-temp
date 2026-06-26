param(
  [string]$CodexDir = $(if ($env:CODEX_SKILLS_DIR) { $env:CODEX_SKILLS_DIR } elseif ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex\skills" }),
  [string]$ClaudeDir = $(if ($env:CLAUDE_SKILLS_DIR) { $env:CLAUDE_SKILLS_DIR } else { Join-Path $HOME ".claude\skills" }),
  [switch]$SkipClaude
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsRoot = Join-Path $Root "skills"

if (-not (Test-Path -LiteralPath $SkillsRoot)) {
  throw "Missing skills directory: $SkillsRoot"
}

function Copy-SkillsTo {
  param([string]$TargetDir)
  New-Item -ItemType Directory -Force -Path $TargetDir | Out-Null
  Get-ChildItem -LiteralPath $SkillsRoot -Directory | ForEach-Object {
    $dest = Join-Path $TargetDir $_.Name
    if (Test-Path -LiteralPath $dest) {
      Remove-Item -LiteralPath $dest -Recurse -Force
    }
    Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
    Write-Host "Installed $($_.Name) -> $dest"
  }
}

Copy-SkillsTo -TargetDir $CodexDir

if (-not $SkipClaude) {
  Copy-SkillsTo -TargetDir $ClaudeDir
}

Write-Host "Done."
