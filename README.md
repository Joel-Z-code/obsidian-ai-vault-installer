# Obsidian AI Vault Installer

一键搭建标准版 Obsidian AI 知识库的 Skill。

安装后，对 Agent 说：

```text
帮我搭建知识库
```

它会自动创建一套标准版 Obsidian AI 知识库，包括目录结构、`AGENTS.md`、`CLAUDE.md`、JSONL 索引、核心工作流、收件箱、`Clippings`、使用教程、手动配置清单、定制化指南和 MVP 自测报告。

## 适合谁

- 想从零搭建 Obsidian AI 知识库的人。
- 不想手动照教程建目录、写规则、建索引的人。
- 想让 Agent 后续能稳定读取规则、整理资料、写作和复盘的人。

## 它能做什么

- 创建标准版 Vault。
- 创建 `00 收件箱` 到 `10 About me`。
- 接入 `Clippings` 作为 Web Clipper 输入入口。
- 写入根规则和目录说明。
- 初始化 JSONL 索引。
- 写入知识管理、内容创作、周复盘、收件箱处理工作流。
- 跑 MVP 自测。
- 输出安装完成报告和使用说明。

## 它不做什么

- 不安装 Obsidian。
- 不安装浏览器扩展。
- 不配置 Obsidian Web Clipper。
- 不登录账号。
- 不配置云同步。
- 不做 OCR。
- 不迁移旧知识库。
- 不删除用户文件。

## 一键安装（推荐）

使用 Skills CLI 安装：

```powershell
npx skills add github:Joel-Z-code/obsidian-ai-vault-installer
```

默认安装到：

```text
~/.codex/skills/obsidian-ai-vault-installer
```

安装完成后，重启或刷新你的 Agent 环境，然后发送：

```text
帮我搭建知识库
```

## 备用 npx 安装

如果你的环境还没有 `skills add`，可以直接运行仓库自带安装器：

```powershell
npx github:Joel-Z-code/obsidian-ai-vault-installer
```

## PowerShell 安装

在 Windows PowerShell 里运行：

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr https://raw.githubusercontent.com/Joel-Z-code/obsidian-ai-vault-installer/main/install-from-github.ps1 -OutFile $env:TEMP\install-obsidian-ai-vault-installer.ps1; & $env:TEMP\install-obsidian-ai-vault-installer.ps1"
```

PowerShell 脚本同样默认安装到：

```text
~/.codex/skills/obsidian-ai-vault-installer
```

安装完成后，重启或刷新你的 Agent 环境，然后发送：

```text
帮我搭建知识库
```

## 手动安装

1. 下载本仓库。
2. 把 `skill/` 文件夹复制到：

```text
~/.codex/skills/obsidian-ai-vault-installer
```

3. 重启或刷新 Agent 环境。
4. 发送：

```text
帮我搭建知识库
```

## 本地测试

在仓库根目录运行：

```powershell
python .\skills\obsidian-ai-vault-installer\scripts\create_vault.py --base-dir .\test-output --vault-name AI知识库-test
```

成功时会输出：

```json
{
  "status": "ok"
}
```

## 安全说明

- 安装器只写入目标 Vault 目录。
- 默认不覆盖已有文件。
- 同名目录存在时，会创建带时间戳的新目录。
- 不联网。
- 不删除文件。
- 不请求管理员权限。

## 卸载

这个 Skill 是一次性安装器。知识库搭建完成后，日常使用不再依赖它。

确认不再需要后，可以删除：

```text
~/.codex/skills/obsidian-ai-vault-installer
```

删除 Skill 不会删除已经生成的知识库。
