---
templates:
  - ask
  - assign
  - gate
---

# Module 8 — 主结构落地

**模板**：追问 → 作业 → 验收门

## 追问型

按 SCOPE 里的主结构，说清 **一条真实任务路径**（输入 → 步骤/工具 → 输出）。

## 作业型

在 `my-agent/` 落地可运行入口（如 `main.py` 或 `agent.py`），体现通用 Agent（工具环即可，允许 mock 工具）。审核通过。

## 验收门

`grade 8`：入口文件存在；log 含任务路径与 assign pass；声明 general agent。
