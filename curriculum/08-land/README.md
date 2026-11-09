# Module 8 — 主结构落地

**时长**：约 8 小时  
**对应大纲**：M8

## 怎么学这一课（交互）

**只在 Cursor Chat 里完成。** 可以打开本 README 阅读。

1. 对 Coach 说你的回答 / 决定（提问、三问、范围）。
2. 让 Coach **把结论写入** `starter/`（你不要离开对话去手改作业当主路径）。
3. 在 Chat 说「帮我评分」——由 Coach 跑 `agent-bridge grade`。

Coach 不得替你编造没有依据的「能 / 成本」；必须来自你在对话里说过的内容。


按 Module 5 选定的主结构，在 `my-agent/` 落地**至少一条真实任务路径**（通用 Agent，不是画死业务图交差）。

## 写入 `starter/answers.json`

- `primary_structure`: 与第 5 课一致的 id
- `task_path_description`: ≥60 字
- `entry_file`: my-agent 内入口相对路径
- `is_general_agent`: true

`entry_file` 必须存在。

## 验收

`grade 8`
