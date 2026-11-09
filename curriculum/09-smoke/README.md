---
templates:
  - explain
  - assign
  - gate
---

# Module 9 — 合约、安全与冒烟结业

**模板**：说明 → 作业 → 验收门

## 说明型

签字面要写清权限/失败策略；**单元绿 ≠ 冒烟**。结业必须有一条最短真路径冒烟。

## 作业型

1. `my-agent/CONTRACT.md` — 权限与失败策略（短）  
2. `my-agent/smoke.py`（或 `scripts/smoke.sh`）— 冒烟脚本，成功 exit 0  
审核后进入验收门。

## 验收门

`grade 9`：跑 `python smoke.py`（在 my-agent 下）须成功；CONTRACT 存在；log 有 assign pass。
