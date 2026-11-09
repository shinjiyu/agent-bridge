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
