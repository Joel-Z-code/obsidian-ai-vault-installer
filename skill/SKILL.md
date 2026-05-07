---
name: obsidian-ai-vault-installer
description: One-time installer for creating a standard Obsidian AI knowledge base Vault with Agent-readable rules, numbered folders, JSONL indexes, inbox and Clippings intake, core workflows, MVP self-test, setup report, usage guide, manual configuration checklist, customization guide, and uninstall reminder. Use when the user asks to build, initialize, automate setup, or create from scratch an Obsidian/AI/Agent knowledge base, such as "帮我搭建知识库", "帮我搭建这个知识库", "帮我从零搭建 Obsidian AI 知识库", or "帮我自动化搭建知识库". Do not use for daily operations on an existing knowledge base, inbox processing, writing articles, reviewing notes, plugin configuration, OCR, sync setup, migration, or general optimization.
---

# Obsidian AI Vault Installer

## Overview

Create a clean, standard Obsidian AI knowledge base Vault from scratch. This is a one-time installer, not an ongoing knowledge-management operator.

The installer creates the folder map, Agent rules, directory README files, JSONL indexes, core workflows, personal-context templates, usage guides, MVP self-test report, and setup report.

## Trigger Check

Use this skill only when the user wants to build or initialize a knowledge base.

Proceed for requests like:

- `帮我搭建知识库`
- `帮我搭建这个知识库`
- `帮我从零搭建 Obsidian AI 知识库`
- `帮我自动化搭建知识库`
- `帮我初始化一个 Agent 可用的 Obsidian Vault`

Do not run the installer for:

- inbox processing
- article writing or editing
- note review
- plugin installation or browser-extension configuration
- OCR
- sync or backup setup
- migration of an old Vault
- general optimization of an existing knowledge base

If intent is unclear, state that this skill is for one-time Vault installation and only proceed when the request is about building or initializing.

## Default Behavior

When the user does not provide a path, create `AI知识库/` in the current working directory.

When the target directory already exists, do not overwrite or delete anything. Create a timestamped sibling directory such as `AI知识库-20260508-0150/`.

If the user explicitly asks to supplement an existing Vault, only add missing files. Never overwrite existing files unless the user explicitly asks for a specific file replacement.

## Installation Command

Run the bundled script:

```bash
python scripts/create_vault.py
```

Useful options:

```bash
python scripts/create_vault.py --base-dir .
python scripts/create_vault.py --vault-name "AI知识库"
python scripts/create_vault.py --target "E:/Obsidian/AI知识库"
python scripts/create_vault.py --supplement-existing --target "E:/Obsidian/ExistingVault"
```

After running, read the script output and report the created Vault path, validation result, and next actions.

## What The Script Creates

The generated Vault includes:

- root files: `AGENTS.md`, `CLAUDE.md`, `README.md`
- intake: `00 收件箱/`, `Clippings/`
- creation: `01 内容创作/`
- topics: `02 选题管理/`
- materials: `03 素材管理/`
- data: `04 内容数据/`
- tools: `05 工具箱/`
- planning: `06 计划/`
- workflows: `07 系统方法/`
- deliverables: `08 交付物/`
- images: `09 image/`
- personal context: `10 About me/`

It also initializes the JSONL indexes, core workflow files, manual configuration checklist, customization guide, MVP self-test report, and setup report.

## Safety Rules

- Write only inside the target Vault directory.
- Do not delete files.
- Do not overwrite existing files by default.
- Do not install Obsidian, browser extensions, plugins, OCR tools, sync tools, or system packages.
- Do not request administrator privileges.
- Do not read credential files or sensitive folders.
- Do not use network access.

## Completion Report

After installation, tell the user:

- where the Vault was created
- what was created
- whether MVP self-test passed
- what the knowledge base can do now
- how to start using it
- which manual steps remain
- how to customize it later
- that this skill is a one-time installer and can be uninstalled after confirmation

Keep the message direct and zero-prior-knowledge friendly.

## Manual Steps To Tell The User

The installer cannot do these actions:

- install Obsidian desktop
- open the generated Vault inside Obsidian
- install Obsidian Web Clipper in the browser
- grant browser extension permissions
- configure sync or backup
- install optional plugins like Dataview, QuickAdd, or Kanban
- fill the user's personal context

## Validation

Before finalizing, verify:

- the script completed successfully
- key directories exist
- key files exist
- all JSONL files parse
- `07 系统方法/MVP自测报告.md` exists
- `07 系统方法/安装完成报告.md` exists

If validation fails, report the failed step, created path, and files already created. Do not attempt destructive cleanup.
