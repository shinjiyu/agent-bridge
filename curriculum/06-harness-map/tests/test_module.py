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
