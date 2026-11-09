# Module 3 — 工具入门

**时长**：约 2 小时  
**对应大纲**：K1 / M3

## 怎么学这一课（交互）

**只在 Cursor Chat 里完成。** 可以打开本 README 阅读。

1. 对 Coach 说你的回答 / 决定（提问、三问、范围）。
2. 让 Coach **把结论写入** `starter/`（你不要离开对话去手改作业当主路径）。
3. 在 Chat 说「帮我评分」——由 Coach 跑 `agent-bridge grade`。

Coach 不得替你编造没有依据的「能 / 成本」；必须来自你在对话里说过的内容。


## 要点

工具调用：模型提出调用 → 结果**写回前缀** → 再继续逐 token 生成。

## 写入 `starter/answers.json`

- `tool_loop`: ≥40 字，说清回写前缀
- `example_tool_name`: 非空
- `example_observation_in_prefix`: ≥20 字（观察/结果如何进前缀）

## 验收

`grade 3`
