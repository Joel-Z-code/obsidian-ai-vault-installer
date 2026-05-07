param(
    [string]$Repo = "Joel-Z-code/obsidian-ai-vault-installer",
    [string]$Branch = "main",
    [string]$InstallDir = "$HOME\.codex\skills",
    [string]$SkillName = "obsidian-ai-vault-installer"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$tempRoot = Join-Path $env:TEMP "obsidian-ai-vault-installer-$(Get-Date -Format 'yyyyMMddHHmmss')"
$zip = Join-Path $tempRoot "repo.zip"
$extract = Join-Path $tempRoot "repo"

New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null

$url = "https://github.com/$Repo/archive/refs/heads/$Branch.zip"
Write-Host "Downloading: $url"
Invoke-WebRequest -Uri $url -OutFile $zip

Expand-Archive -LiteralPath $zip -DestinationPath $extract -Force
$repoDir = Get-ChildItem -LiteralPath $extract -Directory | Select-Object -First 1
if ($null -eq $repoDir) {
    throw "Cannot find extracted repository folder."
}

$standardSource = Join-Path $repoDir.FullName "skills\$SkillName"
$legacySource = Join-Path $repoDir.FullName "skill"
$source = if (Test-Path -LiteralPath $standardSource) { $standardSource } else { $legacySource }
$target = Join-Path $InstallDir $SkillName

if (!(Test-Path -LiteralPath $source)) {
    throw "Cannot find skill source folder in repository: $source"
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
