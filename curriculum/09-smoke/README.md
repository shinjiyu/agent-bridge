# Module 9 — 合约、安全与冒烟结业

**时长**：约 6 小时  
**对应大纲**：M9

## 怎么学这一课（交互）

**只在 Cursor Chat 里完成。** 可以打开本 README 阅读。

1. 对 Coach 说你的回答 / 决定（提问、三问、范围）。
2. 让 Coach **把结论写入** `starter/`（你不要离开对话去手改作业当主路径）。
3. 在 Chat 说「帮我评分」——由 Coach 跑 `agent-bridge grade`。

Coach 不得替你编造没有依据的「能 / 成本」；必须来自你在对话里说过的内容。


## 写入 `starter/answers.json`

- `contract_summary`: ≥40 字（签字面：权限/失败策略等）
- `smoke_command`: 非空（在 my-agent 下可执行的冒烟命令，如 `python smoke.py`）
- `smoke_passed`: true（Coach 实际跑过并确认）

仓库中须有 `my-agent/smoke` 脚本或 `smoke.py` / `scripts/smoke.sh` 之一，且 `smoke_command` 能跑通（grader 会在 my-agent 下执行该命令，exit 0）。

## 验收

`grade 9` → 通过即毕业轨完成
