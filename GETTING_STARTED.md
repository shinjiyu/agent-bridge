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

## 交互形式

**主界面是 Chat。** 可以打开文件阅读；不要离开对话去手写课程代码。  
下一课、三问、改结业仓库、评分，都在对话里完成（Coach 代跑 CLI、按你的意图改文件）。

## 学习循环

1. `agent-bridge init` — 复制课程到 `~/.agent-bridge/workspace`，解锁 Module 0，安装 Coach Skill（只需这一次可在终端做）  
2. 用 Cursor 打开该 workspace（或本仓库），**之后主要待在 Chat**  
3. 对 Coach 说「继续下一课」——由 Coach 跑 `next`、打开课文、在对话里带着学  
4. 你负责提问与三问取舍；需要改代码时让 Coach 在 Chat 里改，不要自己手写 `starter/` 当主路径  
5. 说「帮我评分」—— Coach 跑 `grade`；通过则解锁下一课  
6. 卡住时在 Chat 里要 hint，或继续提问  

（CLI 仍可用，但是退路；主路径是 Chat。）

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
