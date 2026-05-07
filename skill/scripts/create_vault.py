#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a standard Obsidian AI knowledge base Vault.

This installer is intentionally conservative:
- it writes only inside the target Vault directory
- it never deletes files
- it never overwrites existing files unless supplement mode writes only missing files
- it uses no network access
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


TZ = timezone(timedelta(hours=8))
VERSION = "0.1.0"


ROOT_FILES: dict[str, str] = {}
README_FILES: dict[str, str] = {}
WORKFLOW_FILES: dict[str, str] = {}
TEMPLATE_FILES: dict[str, str] = {}
JSONL_FILES: dict[str, list[dict[str, str]]] = {}


def now_iso() -> str:
    return datetime.now(TZ).replace(microsecond=0).isoformat()


def timestamp() -> str:
    return datetime.now(TZ).strftime("%Y%m%d-%H%M")


def normalize_path(path: str) -> Path:
    return Path(path).expanduser().resolve()


def unique_target(base_dir: Path, vault_name: str) -> Path:
    target = (base_dir / vault_name).resolve()
    if not target.exists():
        return target
    return (base_dir / f"{vault_name}-{timestamp()}").resolve()


def write_text_once(path: Path, content: str, created: list[str], skipped: list[str]) -> None:
    if path.exists():
        skipped.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    created.append(str(path))


def write_jsonl_once(path: Path, rows: list[dict[str, str]], created: list[str], skipped: list[str]) -> None:
    if path.exists():
        skipped.append(str(path))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    data = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    path.write_text(data, encoding="utf-8", newline="\n")
    created.append(str(path))


def ensure_dirs(root: Path) -> list[str]:
    dirs = [
        "00 收件箱",
        "Clippings",
        "01 内容创作/01 AI生产力专栏",
        "01 内容创作/02 独立文章",
        "02 选题管理",
        "03 素材管理/教材",
        "03 素材管理/网页剪藏",
        "03 素材管理/书摘",
        "03 素材管理/播客摘要",
        "03 素材管理/聊天记录",
        "04 内容数据",
        "05 工具箱/Templates",
        "05 工具箱/Skills",
        "06 计划/01 年度计划",
        "06 计划/02 周计划",
        "06 计划/03 商业计划",
        "06 计划/04 每日记录",
        "06 计划/05 周复盘",
        "07 系统方法/测试样本",
        "08 交付物",
        "09 image",
        "10 About me",
    ]
    made: list[str] = []
    for rel in dirs:
        path = root / rel
        path.mkdir(parents=True, exist_ok=True)
        made.append(str(path))
    return made


def init_templates() -> None:
    ROOT_FILES.update(
        {
            "AGENTS.md": """# AGENTS.md

这个 Vault 是个人 AI 知识库和 Agent 工作台。目标是用稳定的上下文文件、目录边界和索引记录，取代每次临时解释背景。

核心理念：上下文优先于提示词。Agent 先读规则，再读目录说明，再读索引，最后才执行具体任务。

## 输出习惯

- 默认使用简体中文。
- 默认读者是零前置知识：不要假设用户知道术语、背景、工具、目录结构或操作步骤。
- 先给直接结论，再解释必要概念，再给可执行步骤。
- 第一次出现专业词时，用括号补一句白话解释。
- 涉及命令、脚本、路径时，给完整可执行版本。
- 不使用邀请式结尾，例如“如需我可以”“如果你愿意”。

## 根规则

- 进入 Vault 后先读本文件。
- 进入任何长期目录前，先读该目录的 `README.md`。
- 创建新文件前，先根据任务路由表判断应该写入哪个目录。
- 操作 JSONL 文件时只允许追加新行，不覆盖、不整体重写，除非用户明确要求维护索引。
- 写文章、改稿、做选题前，必须先读 `10 About me/写作风格.md`、`10 About me/内容定位.md`、`10 About me/审稿标准.md`。
- 输出可长期保存的内容后，更新对应目录的索引 JSONL。
- 引用资料时标明来源文件路径。

## 模块地图

| 目录 | 职责 |
| --- | --- |
| `00 收件箱/` | 手动投放的临时想法、未分类材料、快速捕获内容 |
| `Clippings/` | Obsidian Web Clipper 等工具自动生成的剪藏入口，只作为输入流，不作为长期分类目录 |
| `01 内容创作/` | 专栏文章、独立文章、草稿、改稿 |
| `02 选题管理/` | 选题池、热点筛选、待写列表 |
| `03 素材管理/` | 教材、网页剪藏、书摘、播客摘要、聊天记录、金句 |
| `04 内容数据/` | 发布数据、平台表现、增长复盘数据 |
| `05 工具箱/` | Skills、模板、脚本、插件说明 |
| `06 计划/` | 年度计划、周计划、每日记录、周复盘 |
| `07 系统方法/` | 工作流、规则迭代、系统设计方法 |
| `08 交付物/` | 正式交付内容、项目输出、客户资料 |
| `09 image/` | 配图、封面、截图、导出图片 |
| `10 About me/` | 个人背景、写作风格、内容定位、审稿标准 |

## 任务路由表

| 用户任务 | 先读 | 写入 |
| --- | --- | --- |
| 记录一个想法 | `00 收件箱/README.md` | `00 收件箱/` |
| 处理收件箱 | `00 收件箱/README.md`、`Clippings/README.md`、`07 系统方法/工作流-收件箱处理.md` | `00 收件箱/inbox_index.jsonl`，并按类型写入目标目录 |
| 写文章或改文章 | `10 About me/` 下的风格文件 | `01 内容创作/` |
| 管理选题 | `02 选题管理/README.md` | `02 选题管理/topics_index.jsonl` |
| 整理资料 | `03 素材管理/README.md` | `03 素材管理/` |
| 复盘一周 | `06 计划/README.md`、`daily_log.jsonl` | `06 计划/05 周复盘/` |
| 沉淀方法 | `07 系统方法/README.md` | `07 系统方法/` |
| 建 Skill 或模板 | `05 工具箱/README.md` | `05 工具箱/` |

## JSONL 记录格式

每行是一个完整 JSON 对象。推荐字段：

```json
{"time":"2026-01-01T09:00:00+08:00","task":"任务名称","source":"来源路径","output":"产物路径","status":"done","next_action":""}
```
""",
            "CLAUDE.md": """# CLAUDE.md

这是给 Claude Code 兼容使用的入口文件。

主规则文件是 `AGENTS.md`。进入本 Vault 后，先读取 `AGENTS.md`，再按其中的模块地图、任务路由表和 JSONL 规则执行。

最重要的五条规则：

1. 所有输出默认保持零前置知识，先解释背景和术语，再给步骤。
2. 进入目录先读 `README.md`。
3. JSONL 只追加，不覆盖。
4. 写作类任务先读 `10 About me/` 下的个人上下文文件。
5. 处理收件箱时同时扫描 `00 收件箱/` 和 `Clippings/`；用户不负责命名、分类、解释和搬运，Agent 必须先读内容和元数据，再自动判断类型、标题和去向。
""",
            "README.md": """# AI知识库

这是一个标准版 Obsidian AI 知识库 Vault。

Vault 是 Obsidian 的本地知识库文件夹。这里的 Markdown 文件既可以给人阅读，也可以给 Agent 读取、搜索和更新。

## 第一次怎么用

1. 用 Obsidian 打开这个文件夹。
2. 把网页、文章、聊天记录、PDF 文本、OCR 文本、灵感和复盘丢进 `00 收件箱/`。
3. 如果使用 Obsidian Web Clipper，它可能会自动写入 `Clippings/`，这是正常入口。
4. 对 Agent 说：`处理收件箱`。
5. 补写 `10 About me/` 下的个人上下文，让 Agent 更懂你的目标、风格和判断标准。

## 当前能做什么

- 承接未整理资料。
- 把资料消化成摘要、概念卡、方法卡、操作清单。
- 从素材反哺选题。
- 支持文章大纲、草稿和审稿。
- 支持每日记录、周计划和周复盘。
- 用 JSONL 记录任务状态和索引。

## 核心文件

- `AGENTS.md`：Agent 总规则。
- `CLAUDE.md`：Claude Code 兼容入口。
- 各目录 `README.md`：说明该目录放什么、不放什么。
- `*.jsonl`：任务、素材、文章、计划等索引记录。

## 后续定制

先补 `10 About me/`，再根据真实使用情况修改 `07 系统方法/定制化指南.md` 中列出的规则。
""",
        }
    )

    readmes = {
        "00 收件箱/README.md": """# 00 收件箱

这里是所有未整理信息的主入口。用户只需要把资料丢进来，不需要命名、分类、解释或搬运。

如果工具不能直接写入这里，而是自动写入 `Clippings/`，也属于正常输入。Agent 处理收件箱时会一起扫描这些外部采集入口。

适合放：网页剪藏、文章、聊天记录、PDF 文本、OCR 文本、临时链接、灵感、复盘片段。

视频不直接放这里。视频内容需要先转成文本。

处理规则：先读正文，再读元数据，最后参考文件名；自动判断类型、生成标题、决定去向。判断不清时标记 `needs_review`。
""",
        "Clippings/README.md": """# Clippings

这里是 Obsidian Web Clipper 等工具自动生成的剪藏入口。

它不是长期资料目录，也不是用户需要手动维护的分类目录。工具把网页剪藏写到这里是正常现象。

Agent 处理收件箱时，必须把本目录和 `00 收件箱/` 一起扫描。
""",
        "01 内容创作/README.md": """# 01 内容创作

这里放文章大纲、正文草稿、改稿记录和审稿记录。

写作前先读 `10 About me/写作风格.md`、`10 About me/内容定位.md`、`10 About me/审稿标准.md`。
""",
        "01 内容创作/01 AI生产力专栏/README.md": "# 01 AI生产力专栏\n\n这里放同一主题长期专栏内容。\n",
        "01 内容创作/02 独立文章/README.md": "# 02 独立文章\n\n这里放单篇独立文章的大纲、草稿和审稿记录。\n",
        "02 选题管理/README.md": """# 02 选题管理

这里放选题池、待写列表和选题判断记录。

选题索引使用 `topics_index.jsonl`，只追加，不覆盖。
""",
        "03 素材管理/README.md": """# 03 素材管理

这里放已经有保存价值的长期素材，包括教材、网页剪藏、书摘、播客摘要、聊天记录和金句。

原始信息不要直接当知识使用。优先消化成摘要、概念卡、方法卡或操作清单。
""",
        "03 素材管理/教材/README.md": "# 教材\n\n这里放教程、课程、方法论材料及其消化卡片。\n",
        "03 素材管理/网页剪藏/README.md": "# 网页剪藏\n\n这里放从网页保存并消化后的长期素材。\n",
        "03 素材管理/书摘/README.md": "# 书摘\n\n这里放书籍摘录和消化记录。\n",
        "03 素材管理/播客摘要/README.md": "# 播客摘要\n\n这里放播客转写、摘要和可复用观点。\n",
        "03 素材管理/聊天记录/README.md": "# 聊天记录\n\n这里放已经筛选并值得保留的聊天记录消化结果。\n",
        "04 内容数据/README.md": "# 04 内容数据\n\n这里放发布数据、平台表现和增长复盘数据。\n",
        "05 工具箱/README.md": "# 05 工具箱\n\n这里放可复用工具、模板、脚本、插件说明和 Skills。\n",
        "05 工具箱/Templates/README.md": "# Templates\n\n这里放可复用 Markdown 模板。\n",
        "05 工具箱/Skills/README.md": "# Skills\n\n这里放 Agent Skill 说明和本地技能包。\n",
        "06 计划/README.md": "# 06 计划\n\n这里放年度计划、周计划、商业计划、每日记录和周复盘。\n",
        "06 计划/01 年度计划/README.md": "# 年度计划\n\n这里放年度目标和长期规划。\n",
        "06 计划/02 周计划/README.md": "# 周计划\n\n这里放每周计划。\n",
        "06 计划/03 商业计划/README.md": "# 商业计划\n\n这里放商业目标、项目计划和商业假设。\n",
        "06 计划/04 每日记录/README.md": "# 每日记录\n\n这里放每日行动、观察和复盘记录。结构化记录写入 `daily_log.jsonl`。\n",
        "06 计划/05 周复盘/README.md": "# 周复盘\n\n这里放周复盘报告和下周计划输入。\n",
        "07 系统方法/README.md": "# 07 系统方法\n\n这里放工作流、规则迭代、系统设计方法、安装报告和自测报告。\n",
        "07 系统方法/测试样本/README.md": "# 测试样本\n\n这里放安装器自测使用的隔离样本，不作为正式资料入口。\n",
        "08 交付物/README.md": "# 08 交付物\n\n这里放正式交付内容、项目输出和客户资料。\n",
        "09 image/README.md": "# 09 image\n\n这里放配图、封面、截图和导出图片。\n",
        "10 About me/README.md": "# 10 About me\n\n这里放个人背景、写作风格、内容定位、审稿标准和沟通偏好。先补这里，Agent 后续输出才会更贴近你。\n",
    }
    README_FILES.update(readmes)

    WORKFLOW_FILES.update(
        {
            "07 系统方法/工作流-知识管理闭环.md": """# 工作流：知识管理闭环

## 一句话结论

知识管理闭环就是把原始信息先消化成摘要、金句、方法和标签，再放入可检索素材库，最后反哺选题。

## 流程

信息来源 → 消化 → 分类存档 → 选题反哺

## Agent 执行规则

1. 先读 `AGENTS.md`。
2. 再读 `03 素材管理/README.md`。
3. 判断资料类型。
4. 不直接堆原文，先拆成概念卡、方法卡或操作清单。
5. 完成后追加 `03 素材管理/materials_index.jsonl`。
6. 如果能形成选题，再追加 `02 选题管理/topics_index.jsonl`。
""",
            "07 系统方法/工作流-内容创作闭环.md": """# 工作流：内容创作闭环

## 一句话结论

内容创作闭环就是把选题、素材、起草、审稿、发布、归档绑定到固定目录和索引。

## 流程

选题 → 素材 → 起草 → 审稿 → 发布 → 归档

## Agent 执行规则

1. 先读 `AGENTS.md` 和 `01 内容创作/README.md`。
2. 读取 `10 About me/写作风格.md`、`内容定位.md`、`审稿标准.md`。
3. 查 `02 选题管理/topics_index.jsonl` 和 `03 素材管理/materials_index.jsonl`。
4. 先输出大纲，再写正文。
5. 完成后追加 `01 内容创作/articles_index.jsonl`。
""",
            "07 系统方法/工作流-周复盘闭环.md": """# 工作流：周复盘闭环

## 一句话结论

周复盘闭环就是让系统读取每日记录、对比周计划、追踪目标，并产出下周计划。

## 流程

每日日志追加 → 周计划对比 → 目标追踪 → 下周规划

## Agent 执行规则

1. 先读 `AGENTS.md` 和 `06 计划/README.md`。
2. 读取本周 `daily_log.jsonl`。
3. 读取对应周计划。
4. 读取 `goals_tracker.jsonl`。
5. 输出周复盘到 `06 计划/05 周复盘/`。
""",
            "07 系统方法/工作流-收件箱处理.md": """# 工作流：收件箱处理

## 一句话结论

收件箱处理就是允许用户先把资料乱放进入口目录，再由 Agent 定期识别、消化、归档、建索引和反哺选题。

入口目录包括：

- `00 收件箱/`：用户手动投放入口。
- `Clippings/`：Obsidian Web Clipper 等剪藏工具自动生成的入口。

## 核心原则

- 用户只负责把资料塞进来，不负责命名、分类、解释和搬运。
- 判断资料时，优先读内容，其次看元数据，最后才参考文件名。
- 文件名可以是默认名、随机名、网页标题、下载名或工具生成名。
- 原始资料优先保留，消化结果另存为 Markdown。
- JSONL 只追加，不覆盖。

## 处理流程

1. 扫描 `00 收件箱/` 和 `Clippings/`。
2. 判断资料类型：网页剪藏、聊天记录、PDF 文本、OCR 文本、灵感、复盘片段。
3. 选择主动作：归档、消化、反哺选题、记录日志、暂存待清洗。
4. 生成必要的 Markdown 消化产物。
5. 追加 `00 收件箱/inbox_index.jsonl`。
6. 必要时追加素材索引、选题索引或每日记录。

判断不清时标记 `needs_review`，不要求用户先补文件名。
""",
            "07 系统方法/零前置知识输出规范.md": """# 零前置知识输出规范

## 一句话结论

默认把读者当作第一次接触这个系统的人，先讲结论，再补必要背景，再给可执行步骤。

## 规则

- 不假设用户知道术语。
- 第一次出现专业词时，用括号补一句白话解释。
- 先给直接结论。
- 再解释为什么。
- 最后给步骤或文件路径。
- 避免邀请式结尾。
""",
            "07 系统方法/手动配置清单.md": """# 手动配置清单

## 一句话结论

安装器已经创建本地知识库文件结构，但外部软件、浏览器扩展、账号授权和同步配置需要用户手动完成。

## 需要用户手动做

1. 安装 Obsidian 桌面软件。
2. 用 Obsidian 打开这个 Vault 文件夹。
3. 安装浏览器扩展 Obsidian Web Clipper。
4. 授权浏览器扩展访问需要剪藏的网站。
5. 确认 Web Clipper 输出目录，可以接受默认 `Clippings/`。
6. 选择同步和备份方案，例如 Obsidian Sync、iCloud、OneDrive、Git 或其他方案。
7. 按需要安装 Dataview、QuickAdd、Kanban 等可选插件。
8. 补写 `10 About me/` 下的个人上下文。

## 安装器不能做什么

安装器不安装软件、不登录账号、不授权浏览器、不配置云同步、不做 OCR、不发布文章。
""",
            "07 系统方法/定制化指南.md": """# 定制化指南

## 一句话结论

标准版知识库只是地基。后续最重要的定制，是把你的真实背景、目标、风格和工作流写进上下文。

## 最先定制哪里

1. `10 About me/我的介绍.md`
2. `10 About me/写作风格.md`
3. `10 About me/内容定位.md`
4. `10 About me/审稿标准.md`
5. `10 About me/沟通偏好.md`

## 怎么让 Agent 帮你定制

直接告诉 Agent：

```text
请根据我的真实情况，帮我补全 10 About me 下的个人上下文。
```

或者：

```text
我想把这个知识库改成适合做公众号/小红书/研究/项目管理的版本，请先理解我的需求，再给出修改方案。
```

## 后续可以定制什么

- 目录结构。
- 写作流程。
- 素材消化格式。
- 复盘模板。
- 选题判断标准。
- 插件配置。
- 新的专用 Skill。
""",
        }
    )

    TEMPLATE_FILES.update(
        {
            "10 About me/我的介绍.md": "# 我的介绍\n\n在这里写你的身份、正在做的项目、长期目标、关注领域和不想处理的事情。\n",
            "10 About me/写作风格.md": "# 写作风格\n\n在这里写你喜欢和不喜欢的表达方式、标题偏好、文章结构、案例要求和语气边界。\n",
            "10 About me/内容定位.md": "# 内容定位\n\n在这里写你主要写什么、不写什么、目标读者是谁、内容服务什么目标。\n",
            "10 About me/审稿标准.md": "# 审稿标准\n\n在这里写发布前必须检查什么、哪些表达一票否决、是否需要案例/来源/行动步骤。\n",
            "10 About me/沟通偏好.md": "# 沟通偏好\n\n在这里写你希望 Agent 怎么汇报、什么时候先确认、什么时候直接执行。\n",
            "10 About me/个人上下文填写指南.md": """# 个人上下文填写指南

## 一句话结论

先补 `10 About me/`，Agent 才能减少泛泛而谈，输出更贴近你的真实需求。

## 最小填写顺序

1. 你是谁。
2. 你现在最重要的目标。
3. 你写给谁看。
4. 你喜欢什么表达风格。
5. 你最讨厌 Agent 输出什么。
""",
            "05 工具箱/Templates/素材消化模板.md": "# 标题\n\n## 一句话结论\n\n## 来源\n\n## 摘要\n\n## 可复用观点\n\n## 可关联选题\n\n## 下一步\n",
            "05 工具箱/Templates/周复盘模板.md": "# 周复盘\n\n## 本周完成\n\n## 没完成\n\n## 关键收获\n\n## 问题与原因\n\n## 下周计划\n",
            "05 工具箱/Templates/零前置知识文章模板.md": "# 标题\n\n## 直接结论\n\n## 背景解释\n\n## 核心论点\n\n## 例子\n\n## 可执行步骤\n\n## 总结\n",
        }
    )


def init_jsonl(vault_name: str) -> None:
    t = now_iso()
    JSONL_FILES.update(
        {
            "00 收件箱/inbox_index.jsonl": [
                {"time": t, "task": "初始化收件箱索引", "source": "installer", "output": "00 收件箱/inbox_index.jsonl", "status": "done", "next_action": "把未整理资料放入 00 收件箱 或 Clippings"}
            ],
            "01 内容创作/articles_index.jsonl": [
                {"time": t, "task": "初始化文章索引", "source": "installer", "output": "01 内容创作/articles_index.jsonl", "status": "done", "next_action": ""}
            ],
            "02 选题管理/topics_index.jsonl": [
                {"time": t, "task": "初始化选题索引", "source": "installer", "output": "02 选题管理/topics_index.jsonl", "status": "done", "next_action": ""}
            ],
            "03 素材管理/materials_index.jsonl": [
                {"time": t, "task": "初始化素材索引", "source": "installer", "output": "03 素材管理/materials_index.jsonl", "status": "done", "next_action": ""}
            ],
            "04 内容数据/content_data_index.jsonl": [
                {"time": t, "task": "初始化内容数据索引", "source": "installer", "output": "04 内容数据/content_data_index.jsonl", "status": "done", "next_action": ""}
            ],
            "05 工具箱/skills_index.jsonl": [
                {"time": t, "task": "初始化工具箱索引", "source": "installer", "output": "05 工具箱/skills_index.jsonl", "status": "done", "next_action": ""}
            ],
            "06 计划/goals_tracker.jsonl": [
                {"time": t, "task": "初始化目标追踪索引", "source": "installer", "output": "06 计划/goals_tracker.jsonl", "status": "done", "next_action": ""}
            ],
            "06 计划/04 每日记录/daily_log.jsonl": [
                {"time": t, "task": "初始化每日记录", "source": "installer", "output": "06 计划/04 每日记录/daily_log.jsonl", "status": "done", "next_action": ""}
            ],
            "07 系统方法/workflow_index.jsonl": [
                {"time": t, "task": "初始化系统方法索引", "source": "installer", "output": "07 系统方法/workflow_index.jsonl", "status": "done", "next_action": "后续新增规则和工作流时追加记录"},
                {"time": t, "task": "安装标准版 Obsidian AI 知识库", "source": "obsidian-ai-vault-installer", "output": vault_name, "status": "done", "next_action": "补写个人上下文并开始处理收件箱"},
            ],
            "08 交付物/deliverables_index.jsonl": [
                {"time": t, "task": "初始化交付物索引", "source": "installer", "output": "08 交付物/deliverables_index.jsonl", "status": "done", "next_action": ""}
            ],
        }
    )


def validate_jsonl(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.jsonl"):
        for i, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{path}:{i}: {exc}")
    return errors


def validate_vault(root: Path) -> tuple[bool, list[str]]:
    required = [
        "AGENTS.md",
        "CLAUDE.md",
        "README.md",
        "00 收件箱/README.md",
        "Clippings/README.md",
        "01 内容创作/README.md",
        "02 选题管理/README.md",
        "03 素材管理/README.md",
        "04 内容数据/README.md",
        "05 工具箱/README.md",
        "06 计划/README.md",
        "07 系统方法/README.md",
        "08 交付物/README.md",
        "09 image/README.md",
        "10 About me/README.md",
        "07 系统方法/工作流-知识管理闭环.md",
        "07 系统方法/工作流-内容创作闭环.md",
        "07 系统方法/工作流-周复盘闭环.md",
        "07 系统方法/工作流-收件箱处理.md",
        "07 系统方法/零前置知识输出规范.md",
        "07 系统方法/手动配置清单.md",
        "07 系统方法/定制化指南.md",
        "10 About me/个人上下文填写指南.md",
    ]
    missing = [rel for rel in required if not (root / rel).exists()]
    jsonl_errors = validate_jsonl(root)
    errors = [f"missing: {rel}" for rel in missing] + jsonl_errors
    return not errors, errors


def write_reports(root: Path, created: list[str], skipped: list[str], validation_ok: bool, validation_errors: list[str]) -> None:
    t = now_iso()
    status = "通过" if validation_ok else "未通过"
    report = f"""# 安装完成报告

## 一句话结论

标准版 Obsidian AI 知识库已经创建完成，MVP 自测结果：{status}。

## 基本信息

- 创建时间：{t}
- 安装器版本：{VERSION}
- Vault 路径：`{root}`
- 新建文件数：{len(created)}
- 跳过已有文件数：{len(skipped)}

## 已完成

- 创建编号目录结构。
- 创建 `Clippings/` 外部剪藏入口。
- 写入 `AGENTS.md` 和 `CLAUDE.md`。
- 写入目录 `README.md`。
- 初始化 JSONL 索引。
- 写入知识管理、内容创作、周复盘、收件箱处理四条核心工作流。
- 写入零前置知识输出规范。
- 写入手动配置清单和定制化指南。
- 写入个人上下文模板。

## 当前能做什么

- 承接未整理资料。
- 消化网页、文章、聊天记录、PDF 文本、OCR 文本和灵感。
- 反哺选题。
- 支持文章创作流程。
- 支持每日记录和周复盘。
- 让 Agent 通过规则文件理解这个知识库。

## 下一步

1. 用 Obsidian 打开这个 Vault。
2. 补写 `10 About me/` 下的个人上下文。
3. 把资料放入 `00 收件箱/` 或 `Clippings/`。
4. 对 Agent 说：`处理收件箱`。

## 卸载提醒

创建这个 Vault 的 Skill 是一次性安装器。知识库搭建完成后，日常使用不再依赖安装器 Skill。确认不再需要后，可以按所在 Agent 环境的 Skill 删除方式卸载它。删除 Skill 不会删除这个 Vault。
"""
    self_test = f"""# MVP 自测报告

## 一句话结论

自测结果：{status}。

## 检查项

- 关键目录存在。
- 关键文件存在。
- JSONL 文件可以解析。
- `00 收件箱/` 和 `Clippings/` 已接入。
- 核心工作流文件存在。
- 个人上下文模板存在。

## 错误

{chr(10).join(f"- {e}" for e in validation_errors) if validation_errors else "无。"}

## 说明

本次自测只验证标准版骨架是否可运行，不安装外部软件、不配置浏览器扩展、不做 OCR、不配置同步。
"""
    (root / "07 系统方法/安装完成报告.md").write_text(report, encoding="utf-8", newline="\n")
    (root / "07 系统方法/MVP自测报告.md").write_text(self_test, encoding="utf-8", newline="\n")


def create_vault(args: argparse.Namespace) -> int:
    init_templates()
    base_dir = normalize_path(args.base_dir)
    if args.target:
        target = normalize_path(args.target)
        if target.exists() and not args.supplement_existing:
            target = (target.parent / f"{target.name}-{timestamp()}").resolve()
    else:
        target = unique_target(base_dir, args.vault_name)

    target.mkdir(parents=True, exist_ok=True)
    init_jsonl(target.name)
    ensure_dirs(target)

    created: list[str] = []
    skipped: list[str] = []

    for rel, content in ROOT_FILES.items():
        write_text_once(target / rel, content, created, skipped)
    for rel, content in README_FILES.items():
        write_text_once(target / rel, content, created, skipped)
    for rel, content in WORKFLOW_FILES.items():
        write_text_once(target / rel, content, created, skipped)
    for rel, content in TEMPLATE_FILES.items():
        write_text_once(target / rel, content, created, skipped)
    for rel, rows in JSONL_FILES.items():
        write_jsonl_once(target / rel, rows, created, skipped)

    validation_ok, validation_errors = validate_vault(target)
    write_reports(target, created, skipped, validation_ok, validation_errors)
    validation_ok, validation_errors = validate_vault(target)

    result = {
        "status": "ok" if validation_ok else "failed",
        "vault_path": str(target),
        "version": VERSION,
        "created_files": len(created),
        "skipped_existing_files": len(skipped),
        "validation_errors": validation_errors,
        "setup_report": str(target / "07 系统方法/安装完成报告.md"),
        "self_test_report": str(target / "07 系统方法/MVP自测报告.md"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if validation_ok else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a standard Obsidian AI knowledge base Vault.")
    parser.add_argument("--base-dir", default=".", help="Base directory used when --target is not provided.")
    parser.add_argument("--vault-name", default="AI知识库", help="Vault directory name.")
    parser.add_argument("--target", default="", help="Exact target Vault path.")
    parser.add_argument("--supplement-existing", action="store_true", help="Add only missing files to an existing Vault.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return create_vault(args)


if __name__ == "__main__":
    raise SystemExit(main())
