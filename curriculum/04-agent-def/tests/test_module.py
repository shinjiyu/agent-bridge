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
