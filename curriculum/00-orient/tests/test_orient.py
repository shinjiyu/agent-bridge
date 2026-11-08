#!/usr/bin/env python3
"""Grade Module 0 — learning method: can / cannot / cost."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = ROOT / "starter" / "capability-card.json"
MIN = 20


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def need_text(item: dict, key: str, where: str) -> str:
    val = item.get(key)
    if not isinstance(val, str) or len(val.strip()) < MIN:
        fail(f"{where} 的 `{key}` 至少 {MIN} 字，且必须是你自己的尝试记录")
    return val.strip()


def main() -> None:
    if not CARD.exists():
        fail("缺少 starter/capability-card.json")
    try:
        data = json.loads(CARD.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"capability-card.json 不是合法 JSON: {e}")

    if str(data.get("subject", "")).strip() != "Cursor Agent":
        fail('subject 必须是 "Cursor Agent"（这一课只摸你正在用的助手）')

    for field, n in (("can", 2), ("cannot", 2)):
        rows = data.get(field)
        if not isinstance(rows, list) or len(rows) < n:
            fail(f"`{field}` 至少 {n} 条")
        for i, row in enumerate(rows, 1):
            if not isinstance(row, dict):
                fail(f"`{field}` 第 {i} 条必须是对象")
            need_text(row, "claim", f"{field}[{i}]")
            need_text(row, "evidence", f"{field}[{i}]")

    costs = data.get("costs")
    if not isinstance(costs, list) or len(costs) < 3:
        fail("`costs` 至少 3 条")
    kinds = set()
    for i, row in enumerate(costs, 1):
        if not isinstance(row, dict):
            fail(f"costs[{i}] 必须是对象")
        kind = str(row.get("kind", "")).strip()
        if kind not in {"time", "money", "risk"}:
            fail(f"costs[{i}].kind 只能是 time、money、risk")
        kinds.add(kind)
        need_text(row, "claim", f"costs[{i}]")
        need_text(row, "evidence", f"costs[{i}]")
    missing = {"time", "money", "risk"} - kinds
    if missing:
        fail("成本必须同时覆盖 time、money、risk，缺：" + ", ".join(sorted(missing)))

    print("OK: Module 0 passed")


if __name__ == "__main__":
    main()
