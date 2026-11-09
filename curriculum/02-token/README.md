---
templates:
  - explain
  - ask
  - gate
---

# Module 2 — Token 与逐 token 模型

**模板**：说明 → 追问 → 验收门  
**对应**：K0

## 说明型（短）

1. 文本先切成 **token** 再进模型。  
2. **各家分词器不同**，同一任务 token 数/费用不可跨厂硬套。  
3. 模型 **一个 token 一个 token** 往外吐；对话/工具/检索都是改前缀再继续吐。  
成本随前缀与产出的 token 数涨。

## 追问型

用自己的话回答三问（Coach 写入 log）：token 是什么；为何不能跨厂比 token；生成如何滚动。

## 验收门

`grade 2`：log 含上述三点痕迹（标记 `token` / `tokenizer`|分词 / `autoregressive`|逐 token|前缀）。
