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
