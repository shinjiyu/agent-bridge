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
