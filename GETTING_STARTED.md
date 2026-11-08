# Getting Started — Agent Bridge

面向：有编程经验、想转到 **AI Agent 工程师** 的个人学员。

## 依赖

- Node.js **≥ 22**（进度库用内置 `node:sqlite`）
- pnpm 9（`corepack prepare pnpm@9.15.0 --activate`）
- Python 3.10+ 与 `pytest`（`python3 -m pip install pytest`）

## 安装 CLI（开发态）

```bash
cd /path/to/agent-bridge
pnpm install
pnpm -r run build
pnpm --filter @agent-bridge/cli exec node dist/bin.js init
```

或开发时不 build：

```bash
pnpm --filter @agent-bridge/cli exec node --import tsx src/bin.ts init
```

建议在 shell 里加别名：

```bash
alias agent-bridge='pnpm --filter @agent-bridge/cli --dir /path/to/agent-bridge exec node --import tsx src/bin.ts'
```

## 学习循环

1. `agent-bridge init` — 复制课程到 `~/.agent-bridge/workspace`，解锁 Module 0，安装 Coach Skill  
2. 用 Cursor 打开该 workspace（或本仓库）  
3. 对 Coach 说「继续下一课」，或运行 `agent-bridge next`  
4. 在当前模块 `starter/` 里实现  
5. `agent-bridge grade` — 通过则解锁下一课  
6. 卡住时：`agent-bridge hint` 或问 Coach（遵守反剧透）

## Coach Skill

`init` / `install-skill` 会把 [`packages/coach-skill`](./packages/coach-skill/SKILL.md) 拷到：

- `~/.agent-bridge/skills/agent-bridge-coach`
- `~/.cursor/skills/agent-bridge-coach`（若可写）

在 Cursor 对话里提及 Agent Bridge / 下一课即可触发。

## 模块一览

| Id | 内容 | MVP |
|----|------|-----|
| 0 | 学法：能 / 不能 / 成本 | 完整 |
| 1 | Tool-using Agent | 完整 |
| 2 | MCP Server | 完整 |
| 3–6 | RAG / Eval / Guardrails / Capstone | 骨架 |
