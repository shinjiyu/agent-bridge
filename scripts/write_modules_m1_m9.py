#!/usr/bin/env python3
"""Rewrite curriculum modules 1–9 onto coach templates + light gates."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "curriculum"

GRADE_SH = """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 tests/test_module.py
"""

LOG_STUB = """# Session log

（Coach 按模板追加；禁止问卷 JSON。）
"""


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.lstrip("\n"), encoding="utf-8")
    print("wrote", rel)


def grade_helpers() -> str:
    return '''
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
LOG = ROOT / "starter" / "log.md"
AGENT = WS / "my-agent"

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)

def log_text() -> str:
    if not LOG.exists():
        fail("缺少 starter/log.md")
    return LOG.read_text(encoding="utf-8")

def need_in_log(*needles: str) -> None:
    """Each needle may be alt1|alt2."""
    text = log_text()
    low = text.lower()
    for n in needles:
        alts = [a.strip() for a in n.split("|")]
        if not any(a.lower() in low or a in text for a in alts):
            fail(f"log.md 缺少标记/内容: {n}")

def need_agent_file(rel: str, min_len: int = 20) -> Path:
    p = AGENT / rel
    if not p.exists():
        fail(f"缺少 my-agent/{rel}")
    if len(p.read_text(encoding="utf-8").strip()) < min_len:
        fail(f"my-agent/{rel} 过短（<{min_len}字）")
    return p
'''


def mod(n: str, slug: str, readme: str, test_body: str, hints: str, rubric: str) -> None:
    base = f"{n}-{slug}"
    write(f"{base}/README.md", readme)
    write(f"{base}/starter/log.md", LOG_STUB)
    write(f"{base}/hints.md", hints + "\n")
    write(f"{base}/rubric.md", rubric + "\n")
    write(f"{base}/tests/test_module.py", grade_helpers() + "\n" + test_body)
    write(f"{base}/grade.sh", GRADE_SH)
    # drop legacy answers.json if present
    ans = ROOT / base / "starter" / "answers.json"
    if ans.exists():
        ans.unlink()
        print("removed", ans.relative_to(ROOT))


def main() -> None:
    # M1
    mod(
        "01",
        "ask",
        """---
templates:
  - explain
  - ask
  - gate
---

# Module 1 — 提问练习

**模板**：说明 → 追问 → 验收门

## 说明型

好问题推进 **能 / 成本 / 机制或范围**，不是「先实现哪个函数」清单。

## 追问型

面对即将做的通用 Agent 结业物，在 Chat 里提出至少 **5** 个问题。Coach 记入 `starter/log.md`（逐条原话即可）。

## 验收门

`grade 1`：log 里有 ≥5 条问题，且至少 3 条触及能/成本/token/工具/范围/冒烟/权限等。
""",
        '''
KEYS = ("能", "成本", "token", "工具", "范围", "冒烟", "权限", "can", "cost", "scope", "tool", "prefix", "前缀")

def main() -> None:
    text = log_text()
    lines = [ln.strip("- ").strip() for ln in text.splitlines() if ln.strip().startswith(("-", "*")) or ln.strip()[:1].isdigit()]
    # also accept "Q:" lines
    for ln in text.splitlines():
        s = ln.strip()
        if s.lower().startswith("q:") or s.startswith("问"):
            lines.append(s)
    # fallback: numbered questions in ask: block
    qs = []
    for ln in text.splitlines():
        s = ln.strip()
        if len(s) >= 15 and any(k in s for k in ("？", "?", "吗", "如何", "怎样", "多少", "什么")):
            qs.append(s)
    if len(qs) < 5:
        fail(f"log 中可识别的问题不足 5 条（当前 {len(qs)}）。Coach 请把学生原问写入 log。")
    hit = sum(1 for q in qs if any(k.lower() in q.lower() for k in KEYS))
    if hit < 3:
        fail("至少 3 条问题应触及能/成本/机制或范围")
    need_in_log("ask|追问")
    print("OK: Module 1 passed")

if __name__ == "__main__":
    main()
''',
        "问题写成原话；不必分类字段。",
        "审的是问题质量，不是数量刷屏。",
    )

    # M2
    mod(
        "02",
        "token",
        """---
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
""",
        '''
def main() -> None:
    need_in_log("explain|说明", "ask|追问")
    text = log_text()
    if "token" not in text.lower() and "令牌" not in text:
        fail("log 须谈到 token")
    if "分词" not in text and "tokenizer" not in text.lower() and "各家" not in text:
        fail("log 须谈到各家分词器差异")
    if not any(x in text for x in ("逐 token", "下一个 token", "前缀", "自回归", "autoregressive")):
        fail("log 须谈到逐 token / 前缀滚动")
    print("OK: Module 2 passed")

if __name__ == "__main__":
    main()
''',
        "用自己的话，三五行够。",
        "不考公式。",
    )

    # M3
    mod(
        "03",
        "tools",
        """---
templates:
  - explain
  - experiment
  - ask
  - gate
---

# Module 3 — 工具入门

**模板**：说明 → 实验 → 追问 → 验收门  
**对应**：K1

## 说明型

工具：模型提出调用 → **结果写回前缀** → 再逐 token 生成。

## 实验型

当场走一次「假工具」或真工具：看观察如何进下一轮上下文。一两句现象即可。

## 追问型

工具结果若不写回前缀，模型还能不能基于结果继续？成本多在哪？

## 验收门

`grade 3`：log 有 experiment + 提到写回前缀/上下文。
""",
        '''
def main() -> None:
    need_in_log("experiment|实验", "ask|追问")
    text = log_text()
    if not any(x in text for x in ("前缀", "prefix", "上下文", "写回", "回写", "观察")):
        fail("log 须体现工具结果回到前缀/上下文")
    print("OK: Module 3 passed")

if __name__ == "__main__":
    main()
''',
        "一次实验够。",
        "盯前缀，不盯 SDK 名。",
    )

    # M4
    mod(
        "04",
        "agent-def",
        """---
templates:
  - explain
  - ask
  - choose
  - gate
---

# Module 4 — 通用 Agent / ReAct vs Graph

**模板**：说明 → 追问 → 抉择 → 验收门  
**对应**：K2

## 说明型

- **通用 Agent**：任务开放，下一步主要由模型（常靠工具）决定。  
- **ReAct**：Reason → Act → Observe 的工具环。  
- **预定 Graph**：控制流在图上 → 本课叫编排/工作流，不叫 Agent。

## 追问型

「下一步谁决定——模型还是边？」用自己的话说清差别。

## 抉择型

结业物确认：主形态是 **通用 Agent**（不是画死业务图）。一句理由。

## 验收门

`grade 4`：log 含 explain/ask/choose；choose 声明 general agent；提到 ReAct 或工具环与 Graph/编排差别。
""",
        '''
def main() -> None:
    need_in_log("explain|说明", "ask|追问", "choose|抉择")
    text = log_text()
    if "general" not in text.lower() and "通用" not in text:
        fail("choose 须声明通用 Agent")
    if "react" not in text.lower() and "工具环" not in text and "Reason" not in text:
        fail("log 须提到 ReAct 或工具环")
    if not any(x in text for x in ("Graph", "graph", "编排", "工作流", "workflow")):
        fail("log 须对照 Graph/编排")
    print("OK: Module 4 passed")

if __name__ == "__main__":
    main()
''',
        "一句话分清控制流在谁手里。",
        "结业必须是通用 Agent。",
    )

    # M5
    mod(
        "05",
        "structures",
        """---
templates:
  - explain
  - choose
  - gate
---

# Module 5 — 常见 Agent 结构

**模板**：说明 → 抉择 → 验收门  
**对应**：K3

## 说明型（结构表，扫一眼）

`tool_calling` / `react` / `plan_execute` / `reflexion` / `codeact` / `multi_agent` / `environment`  
（预定 Graph 不在表内。）

## 抉择型

选结业 **主结构**（上表之一）+ 一句成本理由。写入 `my-agent/SCOPE.md` 与 log。

## 验收门

`grade 5`：SCOPE.md 含 `primary_structure: <id>`；log 有 choose。
""",
        '''
ALLOWED = {
    "tool_calling", "react", "plan_execute", "reflexion",
    "codeact", "multi_agent", "environment",
}

def main() -> None:
    need_in_log("explain|说明", "choose|抉择")
    scope = need_agent_file("SCOPE.md", 15)
    text = scope.read_text(encoding="utf-8")
    found = None
    for a in ALLOWED:
        if a in text:
            found = a
            break
    if not found:
        fail("SCOPE.md 须含 primary_structure 之一: " + ", ".join(sorted(ALLOWED)))
    print(f"OK: Module 5 passed (primary={found})")

if __name__ == "__main__":
    main()
''',
        "不确定就选 tool_calling 或 react。",
        "主结构要能在后面落地。",
    )

    # M6
    mod(
        "06",
        "harness-map",
        """---
templates:
  - explain
  - choose
  - ask
  - gate
---

# Module 6 — Harness 地图与范围

**模板**：说明 → 抉择 → 追问 → 验收门  
**知识**：[agent-harness-articles](https://github.com/shinjiyu/agent-harness-articles)

## 说明型

Harness 面：cost / context / orchestration / contracts / evaluation / security（embodied 选修）。

## 抉择型

选 ≥3 个 **做** 的面；其余标故意不做（各一句理由）。写入 `my-agent/SCOPE.md`（追加）。

## 追问型

用几句话草绘：结业系统能做什么 + 成本怎么看。

## 验收门

`grade 6`：SCOPE 含 in_scope；log 有 choose + ask。
""",
        '''
FACES = {"cost", "context", "orchestration", "contracts", "evaluation", "security", "embodied"}

def main() -> None:
    need_in_log("choose|抉择", "ask|追问")
    scope = need_agent_file("SCOPE.md", 20)
    text = scope.read_text(encoding="utf-8").lower()
    hit = [f for f in FACES if f in text]
    if len(hit) < 3:
        fail("SCOPE.md 至少点名 3 个 harness 面")
    print("OK: Module 6 passed")

if __name__ == "__main__":
    main()
''',
        "范围外写清故意不做。",
        "对接 harness-articles 即可，不通读论文。",
    )

    # M7
    mod(
        "07",
        "cost-context",
        """---
templates:
  - explain
  - assign
  - gate
---

# Module 7 — 成本与上下文进系统

**模板**：说明 → 作业 → 验收门

## 说明型

把「怎么计量成本」「上下文策略是什么」写进自己的系统，不要停在口头。

## 作业型

在 `my-agent/` 落下至少：

- `COST.md` — 计量口径  
- `CONTEXT.md` — 上下文/记忆策略  

Chat 里让 Coach 按你的决定写；你说「审核」。

## 验收门

`grade 7`：两文件存在且非空；log 有 assign: pass。
""",
        '''
def main() -> None:
    need_in_log("assign|作业")
    need_agent_file("COST.md", 40)
    need_agent_file("CONTEXT.md", 40)
    text = log_text()
    if "pass" not in text.lower() and "通过" not in text:
        fail("log 须有 assign 审核通过痕迹（pass/通过）")
    print("OK: Module 7 passed")

if __name__ == "__main__":
    main()
''',
        "两页短文档即可。",
        "策略可换且牵动面可控。",
    )

    # M8
    mod(
        "08",
        "land",
        """---
templates:
  - ask
  - assign
  - gate
---

# Module 8 — 主结构落地

**模板**：追问 → 作业 → 验收门

## 追问型

按 SCOPE 里的主结构，说清 **一条真实任务路径**（输入 → 步骤/工具 → 输出）。

## 作业型

在 `my-agent/` 落地可运行入口（如 `main.py` 或 `agent.py`），体现通用 Agent（工具环即可，允许 mock 工具）。审核通过。

## 验收门

`grade 8`：入口文件存在；log 含任务路径与 assign pass；声明 general agent。
""",
        '''
def main() -> None:
    need_in_log("ask|追问", "assign|作业")
    text = log_text()
    if "general" not in text.lower() and "通用" not in text:
        fail("log 须声明通用 Agent")
    # find an entry file
    candidates = ["main.py", "agent.py", "run.py", "src/main.py"]
    found = None
    for c in candidates:
        p = AGENT / c
        if p.exists() and p.stat().st_size >= 20:
            found = c
            break
    if not found:
        # any .py at top level
        pys = list(AGENT.glob("*.py"))
        pys = [p for p in pys if p.stat().st_size >= 20]
        if not pys:
            fail("my-agent 下缺少可运行入口 .py")
        found = pys[0].name
    if "pass" not in text.lower() and "通过" not in text:
        fail("log 须有 assign 审核通过")
    print(f"OK: Module 8 passed (entry≈{found})")

if __name__ == "__main__":
    main()
''',
        "mock 工具也行，路径要讲得清。",
        "不要交一张画死的业务 Graph 当结业。",
    )

    # M9
    mod(
        "09",
        "smoke",
        """---
templates:
  - explain
  - assign
  - gate
---

# Module 9 — 合约、安全与冒烟结业

**模板**：说明 → 作业 → 验收门

## 说明型

签字面要写清权限/失败策略；**单元绿 ≠ 冒烟**。结业必须有一条最短真路径冒烟。

## 作业型

1. `my-agent/CONTRACT.md` — 权限与失败策略（短）  
2. `my-agent/smoke.py`（或 `scripts/smoke.sh`）— 冒烟脚本，成功 exit 0  
审核后进入验收门。

## 验收门

`grade 9`：跑 `python smoke.py`（在 my-agent 下）须成功；CONTRACT 存在；log 有 assign pass。
""",
        '''
import subprocess

def main() -> None:
    need_in_log("assign|作业")
    need_agent_file("CONTRACT.md", 30)
    smoke = AGENT / "smoke.py"
    script = AGENT / "scripts" / "smoke.sh"
    if smoke.exists():
        cmd = [sys.executable, str(smoke)]
        cwd = str(AGENT)
    elif script.exists():
        cmd = ["bash", str(script)]
        cwd = str(AGENT)
    else:
        fail("缺少 my-agent/smoke.py 或 scripts/smoke.sh")
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail(f"冒烟执行失败: {e}")
    if proc.returncode != 0:
        out = (proc.stdout or "")[-400] + (proc.stderr or "")[-400]
        fail("冒烟未通过\\n" + out)
    print("OK: Module 9 passed — graduation track complete")

if __name__ == "__main__":
    main()
''',
        "冒烟先跑通入口，再加真路径。",
        "过门 = 毕业轨完成。",
    )

    for sh in ROOT.glob("*/grade.sh"):
        sh.chmod(0o755)
    print("done")


if __name__ == "__main__":
    main()
