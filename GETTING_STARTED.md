# Getting Started — Agent Bridge

面向：有编程经验、想转到 **AI Agent 工程师** 的个人学员。

## 交互形式

**主界面是 Chat。** 可以打开文件阅读；不要离开对话去手写课程代码。  
Coach 按模板推进：说明 / 追问 / 实验 / 抉择 / 作业 / 验收门（见 `packages/coach-skill/templates/`）。  
你负责读、答、选、说「审核」「验收」；Coach 改仓库并跑 grade。

## 依赖

- Node.js **≥ 22**（进度库用内置 `node:sqlite`）
- pnpm 9（`corepack prepare pnpm@9.15.0 --activate`）
- Python 3（模块 `grade.sh` 用标准库即可；无需 pytest）

## 安装（只需一次，可在终端）

```bash
git clone https://github.com/shinjiyu/agent-bridge
cd agent-bridge
pnpm install
pnpm -r run build
```

建议把 CLI 放到 PATH，或使用：

```bash
alias agent-bridge='pnpm --dir /path/to/agent-bridge cli'
```

然后：

```bash
agent-bridge init          # 课程 → ~/.agent-bridge/workspace，装 Coach Skill
agent-bridge install-skill # 拉取最新 Coach 时再跑
```

## 学习循环（Chat）

1. 用 Cursor 打开 `~/.agent-bridge/workspace`（或本仓库）
2. 对 Coach 说「继续下一课」
3. 在对话里回答三问 / 做取舍；让 Coach 写入当前模块 `starter/answers.json`（以及 `my-agent/`）
4. 说「帮我评分」→ 通过则解锁下一课
5. 卡住就继续提问或说「要 hint」

大纲见 [OUTLINE.md](./OUTLINE.md)。模块 0–9 已按大纲铺开；结业物在 workspace 的 `my-agent/`。

## 模块一览

| Id | 内容 |
|----|------|
| 0 | 学法与结业壳 |
| 1 | 提问练习 |
| 2 | Token / 逐 token |
| 3 | 工具入门 |
| 4 | 通用 Agent / ReAct vs Graph |
| 5 | 常见结构 |
| 6 | Harness 地图与范围 |
| 7 | 成本与上下文进系统 |
| 8 | 主结构落地 |
| 9 | 合约、安全、冒烟结业 |
