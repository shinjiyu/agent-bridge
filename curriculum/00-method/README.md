# Module 0 — 学法与结业壳

**时长**：约 1 小时  
**对应大纲**：M0 / 怎么学 = 三问 + 提问

## 怎么学这一课（交互）

**只在 Cursor Chat 里完成。** 可以打开本 README 阅读。

1. 对 Coach 说你的回答 / 决定（提问、三问、范围）。
2. 让 Coach **把结论写入** `starter/`（你不要离开对话去手改作业当主路径）。
3. 在 Chat 说「帮我评分」——由 Coach 跑 `agent-bridge grade`。

Coach 不得替你编造没有依据的「能 / 成本」；必须来自你在对话里说过的内容。


## 目标

1. 立下学习契约：三问（能 / 边界用证据个案 / 成本）；提纲不列「不能」目录。
2. 初始化结业仓库壳：`workspace/my-agent/`（后面课往这里长）。

## 在 Chat 里要完成的事

对 Coach 说明，并让其写入 `starter/answers.json`：

- `chat_only_ack`: true（你确认主界面是 Chat）
- `can`: ≥2 条，每条 `claim` + `evidence`（≥20 字）——关于「用 Chat 驱动学习 / Cursor Agent」你亲眼见过的能力
- `costs`: ≥3 条，kinds 须覆盖 `time`、`money`、`risk`
- `boundaries`（可选）: 0+ 条证据个案；**不要**为凑数编否定清单
- `graduation_ready`: true，且磁盘上存在 `../my-agent/README.md`（相对本模块目录，即 workspace/my-agent）

## 验收

`agent-bridge grade 0`（由 Chat 里的 Coach 执行）
