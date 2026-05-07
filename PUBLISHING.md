# Publishing Guide

## 1. Create a GitHub repository

在 GitHub 网页端创建一个新仓库：

```text
obsidian-ai-vault-installer
```

先不要勾选 README、LICENSE、.gitignore，因为本地目录已经包含这些文件。

## 2. Initialize local git

在本目录运行：

```powershell
git init
git add .
git commit -m "Initial release"
git branch -M main
git remote add origin https://github.com/Joel-Z-code/obsidian-ai-vault-installer.git
git push -u origin main
```

这里已经使用你的仓库地址：`https://github.com/Joel-Z-code/obsidian-ai-vault-installer`。

## 3. Test install command

推送完成后，打开仓库页面，确认 `install-from-github.ps1` 可以访问。

优先测试 Skills CLI 安装：

```powershell
npx skills add github:Joel-Z-code/obsidian-ai-vault-installer
```

也可以测试仓库自带 npx 安装器：

```powershell
npx github:Joel-Z-code/obsidian-ai-vault-installer
```

也可以测试 PowerShell 安装：

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr https://raw.githubusercontent.com/Joel-Z-code/obsidian-ai-vault-installer/main/install-from-github.ps1 -OutFile $env:TEMP\install-obsidian-ai-vault-installer.ps1; & $env:TEMP\install-obsidian-ai-vault-installer.ps1"
```

## 4. Release

确认安装命令可用后，在 GitHub 创建 Release：

```text
v0.1.0
```

说明：

```text
First public release of Obsidian AI Vault Installer.
```
