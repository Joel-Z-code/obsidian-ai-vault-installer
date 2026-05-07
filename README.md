# Obsidian AI Vault Installer

一条命令，把 Obsidian AI 知识库的基础框架搭起来。

这个项目提供一个一次性安装器 Skill。安装后，对 Agent 说 `帮我搭建知识库`，它会自动生成一套标准版 Obsidian AI 知识库：目录、规则、索引、工作流、收件箱、Clippings 入口和 MVP 自测报告都会一起创建好

## 快速安装

```powershell
npx skills add github:Joel-Z-code/obsidian-ai-vault-installer
```

安装完成后，重启或刷新你的 Agent 环境，然后发送：

```text
帮我搭建知识库
```

## 它解决什么问题

很多人想让 Claude Code、Codex 这类 Agent 帮自己做知识管理，但第一步就会卡住：

- 不知道 Obsidian Vault 应该怎么分目录。
- 不知道 `AGENTS.md`、`CLAUDE.md` 应该写什么。
- 不知道资料、文章、选题、复盘应该分别放哪里。
- 不知道怎么让 Agent 下次进来还能读懂上下文。

这个 Skill 解决的是“从零搭建地基”的问题。它不替你完成所有知识管理，但会先把一个可运行的工作台搭好。

## 使用路径

```text
安装 Skill
  ↓
发送：帮我搭建知识库
  ↓
生成标准版 Obsidian AI 知识库
  ↓
用 Obsidian 打开生成的 Vault
  ↓
把资料丢进 00 收件箱 或 Clippings
  ↓
让 Agent 处理收件箱、整理素材、反哺选题、写作和复盘
```

## 会生成什么

运行后会创建一套标准版 Vault，包含：

```text
AI知识库/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── 00 收件箱/
├── Clippings/
├── 01 内容创作/
├── 02 选题管理/
├── 03 素材管理/
├── 04 内容数据/
├── 05 工具箱/
├── 06 计划/
├── 07 系统方法/
├── 08 交付物/
├── 09 image/
└── 10 About me/
```

首版会生成：

| 内容 | 作用 |
| --- | --- |
| 56 个基础文件 | 创建可运行的知识库骨架 |
| 10 个 JSONL 索引 | 记录收件箱、选题、素材、文章、计划等状态 |
| 4 条核心工作流 | 知识管理、内容创作、周复盘、收件箱处理 |
| `AGENTS.md` / `CLAUDE.md` | 让 Agent 进入 Vault 后知道怎么工作 |
| `Clippings/` | 接收 Obsidian Web Clipper 等工具生成的剪藏 |
| MVP 自测报告 | 验证目录、规则和索引是否创建成功 |

## 能做什么

- 自动创建标准版 Obsidian AI 知识库。
- 自动写入 Agent 规则和目录说明。
- 自动初始化 JSONL 索引。
- 自动接入 `00 收件箱/` 和 `Clippings/`。
- 自动写入核心工作流。
- 自动生成使用教程、手动配置清单、定制化指南。
- 自动跑一轮 MVP 自测。

## 不做什么

- 不安装 Obsidian 桌面软件。
- 不安装浏览器扩展。
- 不配置 Obsidian Web Clipper。
- 不登录账号。
- 不配置云同步。
- 不做 OCR。
- 不迁移旧知识库。
- 不删除用户文件。

## 更新

重新运行安装命令即可更新 Skill：

```powershell
npx skills add github:Joel-Z-code/obsidian-ai-vault-installer
```

如果本地已经安装过旧版本，安装器会直接替换旧 Skill 文件。它只替换安装器 Skill，不会删除或修改已经生成的知识库。

## 备用安装

如果你的环境暂时不能使用 `skills add`，可以使用仓库自带安装器：

```powershell
npx github:Joel-Z-code/obsidian-ai-vault-installer
```

Windows PowerShell 也可以使用：

```powershell
powershell -ExecutionPolicy Bypass -Command "iwr https://raw.githubusercontent.com/Joel-Z-code/obsidian-ai-vault-installer/main/install-from-github.ps1 -OutFile $env:TEMP\install-obsidian-ai-vault-installer.ps1; & $env:TEMP\install-obsidian-ai-vault-installer.ps1"
```

## 本地测试

```powershell
python .\skills\obsidian-ai-vault-installer\scripts\create_vault.py --base-dir .\test-output --vault-name AI知识库-test
```

成功时会输出：

```json
{
  "status": "ok"
}
```

## 卸载

这个 Skill 是一次性安装器。知识库搭建完成后，日常使用不再依赖它。

确认不再需要后，可以删除：

```text
~/.codex/skills/obsidian-ai-vault-installer
```

删除 Skill 不会删除已经生成的知识库。

## 版本

当前版本：`v0.1.0`

首版目标：把教程里的 Obsidian AI 知识库主线流程封装成一个可安装、可运行、可自测的标准版 Skill。
