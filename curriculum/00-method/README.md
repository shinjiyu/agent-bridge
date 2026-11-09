---
templates:
  - explain
  - experiment
  - ask
  - assign
  - gate
---

# Module 0 — 学法与结业壳

**时长**：约 20–40 分钟  
**模板序列**：说明 → 实验 → 追问 → 作业 → 验收门

Coach 按序列推进；细节见 `packages/coach-skill/templates/`。

## 说明型（读这个就够）

学法只有两条：

1. **三问**：能做什么、成本多少；碰到具体主张再用证据问边界（不列「不能」清单）。
2. **提问**：用问题推进；先别啃实现。

结业物后面会在 `my-agent/` 里长成一套通用 Agent。这一课先立约定、建空壳。

## 实验型

当场对 Cursor 做 **一次** 小事（改个文件或跑条命令），用一两句话说清现象。

## 追问型

基于刚才的现象，Coach 只追两问：能稳住什么？成本你先想到哪一类？

## 作业型

在 workspace 建 `my-agent/README.md`（说明这是结业 Agent 仓库即可）。Chat 里让 Coach 写；你说「审核」。

## 验收门

`agent-bridge grade 0`：存在 `my-agent/README.md`（≥20 字）且 `00-method/starter/log.md` 含实验与追问留痕。
