# Module 1 — Tool-using Agent

**时长**：约 8 小时  
**目标**：实现一个最小 **ReAct / tool loop** CLI Agent（无第三方 LLM SDK 强制依赖：可用规则策略完成测验）。

## 场景

你要做一个命令行助手：用户输入自然语言意图，Agent **多步**调用工具完成任务。

内置工具（必须实现）：

| Tool | 作用 |
|------|------|
| `calc` | 计算简单算术表达式（只含数字与 + - * / ( )） |
| `now` | 返回 ISO 时间字符串（UTC） |
| `kb_get` | 按 key 读取本地知识库 `starter/kb.json` |

## 你要实现

编辑 `starter/agent.py`：

- `parse_goal(text) -> dict`（可选，便于测试）
- `run_agent(goal: str, max_steps: int = 6) -> dict`  
  返回：
  ```json
  {
    "ok": true,
    "steps": [{"thought": "...", "tool": "calc", "args": {"expr": "1+1"}, "observation": "2"}],
    "final": "..."
  }
  ```

**策略要求（测验用，不必接真模型）**：

实现 `decide(goal, history) -> {"tool","args"} | {"final": str}`：

1. 若 goal 匹配计算（含 `计算`/`calc`/`=?` 或纯算式），调用 `calc`
2. 若询问时间（`几点`/`time`/`now`），调用 `now`
3. 若询问知识库键（`kb:` 前缀或 `查知识` + key），调用 `kb_get`
4. 工具结果回来后，用 `final` 汇总结束
5. 未知意图：`final` 说明无法处理，`ok` 仍可为 true（steps 可空）

也要实现 `tools.py` 里的三个工具函数，供 Agent 调用。

## 验收

`agent-bridge grade 1` 会跑 `tests/test_agent.py`。

## 加分（不阻塞）

- 非法算式安全失败（不 `eval` 任意代码）
- steps 里留下可读 thought
