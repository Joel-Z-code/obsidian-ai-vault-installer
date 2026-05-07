param(
    [string]$InstallDir = "$HOME\.codex\skills",
    [string]$SkillName = "obsidian-ai-vault-installer"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $repoRoot "skills\$SkillName"
$target = Join-Path $InstallDir $SkillName

if (!(Test-Path -LiteralPath $source)) {
    throw "Cannot find skill source folder: $source"
}

if (Test-Path -LiteralPath $target) {
    Write-Host "Updating existing skill at: $target"
    Remove-Item -LiteralPath $target -Recurse -Force
}

New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $target -Recurse -Force

Write-Host "Installed skill to: $target"
Write-Host "Use prompt in your Agent: build my knowledge base / 帮我搭建知识库"
