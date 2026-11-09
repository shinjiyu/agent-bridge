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
