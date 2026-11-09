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
            "smoke_command 退出码非 0\n"
            + (proc.stdout or "")[-500]
            + (proc.stderr or "")[-500]
        )
    print("OK: Module 9 passed — graduation track complete")

if __name__ == "__main__":
    main()
