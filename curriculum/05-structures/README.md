# Module 5 — 常见 Agent 结构

**时长**：约 2 小时  
**对应大纲**：K3 / M5

## 怎么学这一课（交互）

**只在 Cursor Chat 里完成。** 可以打开本 README 阅读。

1. 对 Coach 说你的回答 / 决定（提问、三问、范围）。
2. 让 Coach **把结论写入** `starter/`（你不要离开对话去手改作业当主路径）。
3. 在 Chat 说「帮我评分」——由 Coach 跑 `agent-bridge grade`。

Coach 不得替你编造没有依据的「能 / 成本」；必须来自你在对话里说过的内容。


## 结构表（扫一遍）

Tool-calling 环 / ReAct / Plan-and-Execute / Reflexion / CodeAct / 多 Agent / 环境环。  
预定 Graph 不在此表。

## 写入 `starter/answers.json`

- `surveyed`: 数组，至少包含 5 个结构 id（见 starter 注释可选 id）
- `primary_structure`: 你结业主结构（须在 surveyed 内）
- `why_primary`: ≥40 字（机制 + 成本直觉）
- `combo_notes`: 字符串，可空

可选 id：`tool_calling` `react` `plan_execute` `reflexion` `codeact` `multi_agent` `environment`

## 验收

`grade 5`
