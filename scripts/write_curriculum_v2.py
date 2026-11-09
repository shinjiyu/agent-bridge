#!/usr/bin/env python3
"""Generate chat-first curriculum modules aligned with OUTLINE.md."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "curriculum"

CHAT_BANNER = """## 怎么学这一课（交互）

**只在 Cursor Chat 里完成。** 可以打开本 README 阅读。

1. 对 Coach 说你的回答 / 决定（提问、三问、范围）。
2. 让 Coach **把结论写入** `starter/`（你不要离开对话去手改作业当主路径）。
3. 在 Chat 说「帮我评分」——由 Coach 跑 `agent-bridge grade`。

Coach 不得替你编造没有依据的「能 / 成本」；必须来自你在对话里说过的内容。
"""


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.lstrip("\n"), encoding="utf-8")
    print("wrote", rel)


def grade_sh() -> str:
    return """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 tests/test_module.py
"""


# --- shared test helpers embedded per module (keep self-contained) ---

HELPER = '''
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "starter"
MIN = 20

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)

def load(name: str = "answers.json") -> dict:
    path = STARTER / name
    if not path.exists():
        fail(f"缺少 starter/{name}（应在 Chat 里由 Coach 根据你的回答写入）")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{name} 不是合法 JSON: {e}")
    if not isinstance(data, dict):
        fail(f"{name} 必须是对象")
    return data

def need_str(data: dict, key: str, min_len: int = MIN) -> str:
    val = data.get(key)
    if not isinstance(val, str) or len(val.strip()) < min_len:
        fail(f"`{key}` 至少 {min_len} 字")
    return val.strip()

def need_list(data: dict, key: str, n: int) -> list:
    rows = data.get(key)
    if not isinstance(rows, list) or len(rows) < n:
        fail(f"`{key}` 至少 {n} 条")
    return rows
'''


def mod0() -> None:
    write(
        "00-method/README.md",
        f"""# Module 0 — 学法与结业壳

**时长**：约 1 小时  
**对应大纲**：M0 / 怎么学 = 三问 + 提问

{CHAT_BANNER}

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
""",
    )
    write(
        "00-method/starter/answers.json",
        """{
  "chat_only_ack": false,
  "can": [],
  "costs": [],
  "boundaries": [],
  "graduation_ready": false
}
""",
    )
    write(
        "00-method/rubric.md",
        "证据须来自对话中的真实尝试；Coach 不得代填虚构 can/cost。\n",
    )
    write(
        "00-method/hints.md",
        "先在 Chat 里做两次小实验再说能与成本。结业壳只需 my-agent/README.md 说明这是结业仓库。\n",
    )
    write(
        "00-method/tests/test_module.py",
        HELPER
        + '''
def main() -> None:
    data = load()
    if data.get("chat_only_ack") is not True:
        fail("chat_only_ack 必须为 true（确认只在 Chat 完成作业）")
    cans = need_list(data, "can", 2)
    for i, row in enumerate(cans, 1):
        if not isinstance(row, dict):
            fail(f"can[{i}] 必须是对象")
        need_str(row, "claim", 4)
        need_str(row, "evidence", 20)
    costs = need_list(data, "costs", 3)
    kinds = set()
    for i, row in enumerate(costs, 1):
        if not isinstance(row, dict):
            fail(f"costs[{i}] 必须是对象")
        kind = str(row.get("kind", "")).strip()
        if kind not in {"time", "money", "risk"}:
            fail(f"costs[{i}].kind 只能是 time/money/risk")
        kinds.add(kind)
        need_str(row, "claim", 4)
        need_str(row, "evidence", 20)
    missing = {"time", "money", "risk"} - kinds
    if missing:
        fail("成本须覆盖 time/money/risk，缺: " + ", ".join(sorted(missing)))
    bounds = data.get("boundaries", [])
    if bounds is None:
        bounds = []
    if not isinstance(bounds, list):
        fail("boundaries 必须是数组")
    for i, row in enumerate(bounds, 1):
        if not isinstance(row, dict):
            fail(f"boundaries[{i}] 必须是对象")
        need_str(row, "claim", 4)
        need_str(row, "evidence", 20)
    if data.get("graduation_ready") is not True:
        fail("graduation_ready 必须为 true")
    shell = ROOT.parent / "my-agent" / "README.md"
    if not shell.exists():
        fail("缺少 workspace/my-agent/README.md（结业壳）")
    if len(shell.read_text(encoding="utf-8").strip()) < 20:
        fail("my-agent/README.md 至少 20 字，说明这是结业 Agent 仓库")
    print("OK: Module 0 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("00-method/grade.sh", grade_sh())


def mod1() -> None:
    write(
        "01-ask/README.md",
        f"""# Module 1 — 提问练习

**时长**：约 1 小时  
**对应大纲**：M1

{CHAT_BANNER}

## 目标

面对「要做一套通用 Agent」这件事，先写出问题清单，再动手。

## 写入 `starter/answers.json`

- `questions`: ≥5 条字符串，每条 ≥15 字
- 至少 3 条明显指向 **能 / 成本 / 机制或范围**（含关键词即可：能、成本、token、工具、范围、冒烟、权限…）
- `not_implementation_checklist`: true（你确认这些问题不是「先实现哪几个函数」清单）

## 验收

Chat 说「帮我评分」→ `grade 1`
""",
    )
    write(
        "01-ask/starter/answers.json",
        """{
  "questions": [],
  "not_implementation_checklist": false
}
""",
    )
    write("01-ask/rubric.md", "问题应推进决策，而不是索要实现步骤清单。\n")
    write("01-ask/hints.md", "问窗口谁付钱、工具失败怎么办、结业做哪几面 Harness。\n")
    write(
        "01-ask/tests/test_module.py",
        HELPER
        + '''
KEYS = ("能", "成本", "token", "工具", "范围", "冒烟", "权限", "can", "cost", "scope", "tool")

def main() -> None:
    data = load()
    qs = need_list(data, "questions", 5)
    hit = 0
    for i, q in enumerate(qs, 1):
        if not isinstance(q, str) or len(q.strip()) < 15:
            fail(f"questions[{i}] 至少 15 字")
        if any(k.lower() in q.lower() for k in KEYS):
            hit += 1
    if hit < 3:
        fail("至少 3 条问题应触及能/成本/机制或范围（看关键词）")
    if data.get("not_implementation_checklist") is not True:
        fail("not_implementation_checklist 须为 true")
    print("OK: Module 1 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("01-ask/grade.sh", grade_sh())


def mod2() -> None:
    write(
        "02-token/README.md",
        f"""# Module 2 — Token 与逐 token 模型

**时长**：约 2 小时  
**对应大纲**：K0 / M2

{CHAT_BANNER}

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
""",
    )
    write(
        "02-token/starter/answers.json",
        """{
  "token_in_own_words": "",
  "tokenizer_vendor_diff": "",
  "autoregressive_loop": "",
  "cost_scales_with": ""
}
""",
    )
    write("02-token/rubric.md", "用自己的话；不要粘贴公式墙。\n")
    write("02-token/hints.md", "用同一段中文分别想象 OpenAI 与另一家的切法差异即可。\n")
    write(
        "02-token/tests/test_module.py",
        HELPER
        + '''
def main() -> None:
    data = load()
    for key in ("token_in_own_words", "tokenizer_vendor_diff", "autoregressive_loop"):
        need_str(data, key, 40)
    scale = need_str(data, "cost_scales_with", 10)
    low = scale.lower()
    has_in = any(x in scale for x in ("前缀", "输入", "input", "prefix", "上下文", "prompt"))
    has_out = any(x in low for x in ("产出", "输出", "output", "生成", "completion", "吐"))
    if not (has_in and has_out):
        fail("cost_scales_with 须同时提到输入/前缀侧与输出/产出侧")
    print("OK: Module 2 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("02-token/grade.sh", grade_sh())


def mod3() -> None:
    write(
        "03-tools/README.md",
        f"""# Module 3 — 工具入门

**时长**：约 2 小时  
**对应大纲**：K1 / M3

{CHAT_BANNER}

## 要点

工具调用：模型提出调用 → 结果**写回前缀** → 再继续逐 token 生成。

## 写入 `starter/answers.json`

- `tool_loop`: ≥40 字，说清回写前缀
- `example_tool_name`: 非空
- `example_observation_in_prefix`: ≥20 字（观察/结果如何进前缀）

## 验收

`grade 3`
""",
    )
    write(
        "03-tools/starter/answers.json",
        """{
  "tool_loop": "",
  "example_tool_name": "",
  "example_observation_in_prefix": ""
}
""",
    )
    write("03-tools/rubric.md", "重点是前缀滚动，不是某个 SDK 函数名。\n")
    write("03-tools/hints.md", "想象一次 weather 调用：JSON 结果粘进下一轮消息。\n")
    write(
        "03-tools/tests/test_module.py",
        HELPER
        + '''
def main() -> None:
    data = load()
    loop = need_str(data, "tool_loop", 40)
    if not any(x in loop for x in ("前缀", "prefix", "上下文", "context", "写回", "回写")):
        fail("tool_loop 须提到结果写回前缀/上下文")
    name = data.get("example_tool_name")
    if not isinstance(name, str) or not name.strip():
        fail("example_tool_name 不能为空")
    need_str(data, "example_observation_in_prefix", 20)
    print("OK: Module 3 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("03-tools/grade.sh", grade_sh())


def mod4() -> None:
    write(
        "04-agent-def/README.md",
        f"""# Module 4 — 通用 Agent、ReAct 与 Graph

**时长**：约 2 小时  
**对应大纲**：K2 / M4

{CHAT_BANNER}

## 要点

- 本课 **Agent = 通用 Agent**：任务开放，下一步主要由模型（常靠工具）决定。
- **ReAct** = 典型工具环（Reason → Act → Observe → …）。
- **预定 Graph / 工作流** = 编排，**不叫**本课的 Agent。

## 写入 `starter/answers.json`

- `general_agent_def`: ≥40 字
- `react_in_own_words`: ≥40 字
- `graph_is`: 必须是 `"orchestration"` 或中文等价说明里含「编排」或「工作流」
- `graduation_is_general_agent`: true

## 验收

`grade 4`
""",
    )
    write(
        "04-agent-def/starter/answers.json",
        """{
  "general_agent_def": "",
  "react_in_own_words": "",
  "graph_is": "",
  "graduation_is_general_agent": false
}
""",
    )
    write("04-agent-def/rubric.md", "能区分控制流在模型侧还是图画死。\n")
    write("04-agent-def/hints.md", "问：下一步谁决定——模型还是边？\n")
    write(
        "04-agent-def/tests/test_module.py",
        HELPER
        + '''
def main() -> None:
    data = load()
    need_str(data, "general_agent_def", 40)
    react = need_str(data, "react_in_own_words", 40)
    if not any(x in react.lower() for x in ("工具", "tool", "act", "观察", "observe", "reason")):
        fail("react_in_own_words 须体现工具环")
    g = need_str(data, "graph_is", 4)
    gl = g.lower()
    if not (
        gl == "orchestration"
        or "编排" in g
        or "工作流" in g
        or "workflow" in gl
    ):
        fail('graph_is 应表明是编排/工作流（或填 "orchestration"）')
    if data.get("graduation_is_general_agent") is not True:
        fail("graduation_is_general_agent 须为 true")
    print("OK: Module 4 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("04-agent-def/grade.sh", grade_sh())


def mod5() -> None:
    write(
        "05-structures/README.md",
        f"""# Module 5 — 常见 Agent 结构

**时长**：约 2 小时  
**对应大纲**：K3 / M5

{CHAT_BANNER}

## 结构表（扫一遍）

Tool-calling 环 / ReAct / Plan-and-Execute / Reflexion / CodeAct / 多 Agent / 环境环。  
预定 Graph 不在此表。

## 写入 `starter/answers.json`

- `surveyed`: 数组，至少包含 5 个结构 id（见 starter 注释可选 id）
- `primary_structure`: 你结业主结构（须在 surveyed 内）
- `why_primary`: ≥40 字（机制 + 成本直觉）
- `combo_notes`: 字符串，可空

可选 id：`tool_calling` `react` `plan_execute` `reflexion` `codeact` `multi_agent` `environment`

## 验收

`grade 5`
""",
    )
    write(
        "05-structures/starter/answers.json",
        """{
  "surveyed": [],
  "primary_structure": "",
  "why_primary": "",
  "combo_notes": ""
}
""",
    )
    write("05-structures/rubric.md", "主结构要能落地到 my-agent，别只选听过的名词。\n")
    write("05-structures/hints.md", "不确定就选 tool_calling 或 react，成本最好估。\n")
    write(
        "05-structures/tests/test_module.py",
        HELPER
        + '''
ALLOWED = {
    "tool_calling", "react", "plan_execute", "reflexion",
    "codeact", "multi_agent", "environment",
}

def main() -> None:
    data = load()
    surveyed = need_list(data, "surveyed", 5)
    for s in surveyed:
        if s not in ALLOWED:
            fail(f"未知结构 id: {s}")
    primary = str(data.get("primary_structure", "")).strip()
    if primary not in surveyed:
        fail("primary_structure 必须在 surveyed 内")
    need_str(data, "why_primary", 40)
    notes = data.get("combo_notes", "")
    if notes is not None and not isinstance(notes, str):
        fail("combo_notes 须为字符串")
    print("OK: Module 5 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("05-structures/grade.sh", grade_sh())


def mod6() -> None:
    write(
        "06-harness-map/README.md",
        f"""# Module 6 — Harness 地图与范围

**时长**：约 2 小时  
**对应大纲**：K4–K5 / M6  
**知识地图**：[agent-harness-articles](https://github.com/shinjiyu/agent-harness-articles)

{CHAT_BANNER}

## 写入 `starter/answers.json`

- `faces_in_scope`: ≥3 个（从 cost / context / orchestration / contracts / evaluation / security）
- `faces_out_of_scope`: 数组（可含 embodied）；每项须有一行理由写入 `out_reasons` map
- `capability_cost_sketch`: ≥60 字（结业系统能做什么 + 成本口径草稿）

## 验收

`grade 6`
""",
    )
    write(
        "06-harness-map/starter/answers.json",
        """{
  "faces_in_scope": [],
  "faces_out_of_scope": [],
  "out_reasons": {},
  "capability_cost_sketch": ""
}
""",
    )
    write("06-harness-map/rubric.md", "范围外写清故意不做，不算偷懒。\n")
    write("06-harness-map/hints.md", "主路径至少含 cost、context、orchestration 之一组。\n")
    write(
        "06-harness-map/tests/test_module.py",
        HELPER
        + '''
FACES = {"cost", "context", "orchestration", "contracts", "evaluation", "security", "embodied"}

def main() -> None:
    data = load()
    ins = need_list(data, "faces_in_scope", 3)
    for f in ins:
        if f not in FACES:
            fail(f"未知 face: {f}")
    outs = data.get("faces_out_of_scope", [])
    if not isinstance(outs, list):
        fail("faces_out_of_scope 须为数组")
    reasons = data.get("out_reasons", {})
    if not isinstance(reasons, dict):
        fail("out_reasons 须为对象")
    for f in outs:
        r = reasons.get(f)
        if not isinstance(r, str) or len(r.strip()) < 10:
            fail(f"out_reasons[{f}] 至少 10 字")
    need_str(data, "capability_cost_sketch", 60)
    print("OK: Module 6 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("06-harness-map/grade.sh", grade_sh())


def mod7() -> None:
    write(
        "07-cost-context/README.md",
        f"""# Module 7 — 成本与上下文进系统

**时长**：约 4 小时  
**对应大纲**：M7

{CHAT_BANNER}

把口径写进 `workspace/my-agent/`，不只停留在 answers。

## 写入

`starter/answers.json`：

- `cost_metric`: ≥20 字（如何计量 token/钱/延迟）
- `context_strategy`: ≥40 字
- `files_touched`: ≥1 个相对 `my-agent/` 的路径

并且这些文件在 `workspace/my-agent/` 下真实存在且非空。

## 验收

`grade 7`
""",
    )
    write(
        "07-cost-context/starter/answers.json",
        """{
  "cost_metric": "",
  "context_strategy": "",
  "files_touched": []
}
""",
    )
    write("07-cost-context/rubric.md", "牵动面应可控；改策略不该扫全库。\n")
    write("07-cost-context/hints.md", "先在 my-agent 加 COST.md 与 CONTEXT.md 两页也行。\n")
    write(
        "07-cost-context/tests/test_module.py",
        HELPER
        + '''
def main() -> None:
    data = load()
    need_str(data, "cost_metric", 20)
    need_str(data, "context_strategy", 40)
    files = need_list(data, "files_touched", 1)
    base = ROOT.parent / "my-agent"
    for rel in files:
        if not isinstance(rel, str) or not rel.strip():
            fail("files_touched 条目须为路径字符串")
        p = base / rel
        if not p.exists() or p.stat().st_size < 20:
            fail(f"my-agent/{rel} 不存在或过短")
    print("OK: Module 7 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("07-cost-context/grade.sh", grade_sh())


def mod8() -> None:
    write(
        "08-land/README.md",
        f"""# Module 8 — 主结构落地

**时长**：约 8 小时  
**对应大纲**：M8

{CHAT_BANNER}

按 Module 5 选定的主结构，在 `my-agent/` 落地**至少一条真实任务路径**（通用 Agent，不是画死业务图交差）。

## 写入 `starter/answers.json`

- `primary_structure`: 与第 5 课一致的 id
- `task_path_description`: ≥60 字
- `entry_file`: my-agent 内入口相对路径
- `is_general_agent`: true

`entry_file` 必须存在。

## 验收

`grade 8`
""",
    )
    write(
        "08-land/starter/answers.json",
        """{
  "primary_structure": "",
  "task_path_description": "",
  "entry_file": "",
  "is_general_agent": false
}
""",
    )
    write("08-land/rubric.md", "路径应可讲述：输入 → 工具/步骤 → 输出。\n")
    write("08-land/hints.md", "最小也可：一个 CLI 入口 + 一个 mock 工具循环。\n")
    write(
        "08-land/tests/test_module.py",
        HELPER
        + '''
ALLOWED = {
    "tool_calling", "react", "plan_execute", "reflexion",
    "codeact", "multi_agent", "environment",
}

def main() -> None:
    data = load()
    primary = str(data.get("primary_structure", "")).strip()
    if primary not in ALLOWED:
        fail("primary_structure 无效")
    need_str(data, "task_path_description", 60)
    entry = str(data.get("entry_file", "")).strip()
    if not entry:
        fail("entry_file 不能为空")
    p = ROOT.parent / "my-agent" / entry
    if not p.exists():
        fail(f"缺少 my-agent/{entry}")
    if data.get("is_general_agent") is not True:
        fail("is_general_agent 须为 true")
    print("OK: Module 8 passed")

if __name__ == "__main__":
    main()
''',
    )
    write("08-land/grade.sh", grade_sh())


def mod9() -> None:
    write(
        "09-smoke/README.md",
        f"""# Module 9 — 合约、安全与冒烟结业

**时长**：约 6 小时  
**对应大纲**：M9

{CHAT_BANNER}

## 写入 `starter/answers.json`

- `contract_summary`: ≥40 字（签字面：权限/失败策略等）
- `smoke_command`: 非空（在 my-agent 下可执行的冒烟命令，如 `python smoke.py`）
- `smoke_passed`: true（Coach 实际跑过并确认）

仓库中须有 `my-agent/smoke` 脚本或 `smoke.py` / `scripts/smoke.sh` 之一，且 `smoke_command` 能跑通（grader 会在 my-agent 下执行该命令，exit 0）。

## 验收

`grade 9` → 通过即毕业轨完成
""",
    )
    write(
        "09-smoke/starter/answers.json",
        """{
  "contract_summary": "",
  "smoke_command": "",
  "smoke_passed": false
}
""",
    )
    write("09-smoke/rubric.md", "冒烟须走真实入口，不是只跑单元测试。\n")
    write("09-smoke/hints.md", "最小冒烟：启动入口 + 打印 ok 并 exit 0，再逐步加真路径。\n")
    write(
        "09-smoke/tests/test_module.py",
        HELPER
        + '''
import subprocess, shlex

def main() -> None:
    data = load()
    need_str(data, "contract_summary", 40)
    cmd = str(data.get("smoke_command", "")).strip()
    if not cmd:
        fail("smoke_command 不能为空")
    if data.get("smoke_passed") is not True:
        fail("smoke_passed 须为 true（Coach 确认已跑通）")
    base = ROOT.parent / "my-agent"
    if not base.is_dir():
        fail("缺少 my-agent")
    try:
        proc = subprocess.run(
            cmd, shell=True, cwd=str(base),
            capture_output=True, text=True, timeout=120,
        )
    except Exception as e:
        fail(f"执行 smoke_command 失败: {e}")
    if proc.returncode != 0:
        fail(
            "smoke_command 退出码非 0\\n"
            + (proc.stdout or "")[-500]
            + (proc.stderr or "")[-500]
        )
    print("OK: Module 9 passed — graduation track complete")

if __name__ == "__main__":
    main()
''',
    )
    write("09-smoke/grade.sh", grade_sh())


def main() -> None:
    mod0()
    mod1()
    mod2()
    mod3()
    mod4()
    mod5()
    mod6()
    mod7()
    mod8()
    mod9()
    for sh in ROOT.glob("*/grade.sh"):
        sh.chmod(0o755)


if __name__ == "__main__":
    main()
