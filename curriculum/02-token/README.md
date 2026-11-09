# Module 2 — Token 与逐 token 模型

**时长**：约 2 小时  
**对应大纲**：K0 / M2

## 怎么学这一课（交互）

**只在 Cursor Chat 里完成。** 可以打开本 README 阅读。

1. 对 Coach 说你的回答 / 决定（提问、三问、范围）。
2. 让 Coach **把结论写入** `starter/`（你不要离开对话去手改作业当主路径）。
3. 在 Chat 说「帮我评分」——由 Coach 跑 `agent-bridge grade`。

Coach 不得替你编造没有依据的「能 / 成本」；必须来自你在对话里说过的内容。


## 要搞清的机制（课文要点）

1. **Token**：文本先切成 token 再进模型。
2. **各家分词器不同**：同一段话，不同厂商的 token 数可以差很多；窗口与账单不可跨厂硬套。
3. **自回归**：按前缀一个 token 一个 token 往外吐；对话 / 工具结果 / 检索都是改前缀再继续吐。

不讲层内结构（QKV/FFN）。

## 写入 `starter/answers.json`

- `token_in_own_words`: ≥40 字
- `tokenizer_vendor_diff`: ≥40 字（说明为何不可横比）
- `autoregressive_loop`: ≥40 字
- `cost_scales_with`: 非空字符串，须同时提到前缀或输入、以及产出或输出（可用中英文）

## 验收

`grade 2`
