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
