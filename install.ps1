param(
    [string]$InstallDir = "$HOME\.codex\skills",
    [string]$SkillName = "obsidian-ai-vault-installer"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$standardSource = Join-Path $repoRoot "skills\$SkillName"
$legacySource = Join-Path $repoRoot "skill"
$source = if (Test-Path -LiteralPath $standardSource) { $standardSource } else { $legacySource }
$target = Join-Path $InstallDir $SkillName

if (!(Test-Path -LiteralPath $source)) {
    throw "Cannot find skill source folder: $source"
}

if (Test-Path -LiteralPath $target) {
    $backup = "$target.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Move-Item -LiteralPath $target -Destination $backup
    Write-Host "Existing skill backed up to: $backup"
}

New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Recurse -Force

Write-Host "Installed skill to: $target"
Write-Host "Use prompt in your Agent: build my knowledge base / 帮我搭建知识库"
