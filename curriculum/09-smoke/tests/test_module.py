from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
LOG = ROOT / "starter" / "log.md"
AGENT = WS / "my-agent"

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)

def log_text() -> str:
    if not LOG.exists():
        fail("缺少 starter/log.md")
    return LOG.read_text(encoding="utf-8")

def need_in_log(*needles: str) -> None:
    """Each needle may be alt1|alt2."""
    text = log_text()
    low = text.lower()
    for n in needles:
        alts = [a.strip() for a in n.split("|")]
        if not any(a.lower() in low or a in text for a in alts):
            fail(f"log.md 缺少标记/内容: {n}")

def need_agent_file(rel: str, min_len: int = 20) -> Path:
    p = AGENT / rel
    if not p.exists():
        fail(f"缺少 my-agent/{rel}")
    if len(p.read_text(encoding="utf-8").strip()) < min_len:
        fail(f"my-agent/{rel} 过短（<{min_len}字）")
    return p


import subprocess

def main() -> None:
    need_in_log("assign|作业")
    need_agent_file("CONTRACT.md", 30)
    smoke = AGENT / "smoke.py"
    script = AGENT / "scripts" / "smoke.sh"
    if smoke.exists():
        cmd = [sys.executable, str(smoke)]
        cwd = str(AGENT)
    elif script.exists():
        cmd = ["bash", str(script)]
        cwd = str(AGENT)
    else:
        fail("缺少 my-agent/smoke.py 或 scripts/smoke.sh")
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        fail(f"冒烟执行失败: {e}")
    if proc.returncode != 0:
        out = (proc.stdout or "")[-400] + (proc.stderr or "")[-400]
        fail("冒烟未通过\n" + out)
    print("OK: Module 9 passed — graduation track complete")

if __name__ == "__main__":
    main()
