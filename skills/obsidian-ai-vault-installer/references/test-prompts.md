# Test Prompts

| Prompt | Expected behavior |
| --- | --- |
| 帮我搭建知识库 | Trigger installer and create a standard Vault. |
| 帮我从零搭建一个 Obsidian AI 知识库 | Trigger installer and create a standard Vault. |
| 帮我处理收件箱 | Do not trigger installer; this is daily Vault operation. |
| 帮我写一篇文章 | Do not trigger installer; this is content creation. |
| 我已经有一个知识库了，帮我补齐 Agent 规则 | Boundary case; supplement only missing files after target path is clear, never overwrite. |
