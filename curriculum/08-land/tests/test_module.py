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
