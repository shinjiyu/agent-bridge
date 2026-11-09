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


KEYS = ("能", "成本", "token", "工具", "范围", "冒烟", "权限", "can", "cost", "scope", "tool", "prefix", "前缀")

def main() -> None:
    text = log_text()
    lines = [ln.strip("- ").strip() for ln in text.splitlines() if ln.strip().startswith(("-", "*")) or ln.strip()[:1].isdigit()]
    # also accept "Q:" lines
    for ln in text.splitlines():
        s = ln.strip()
        if s.lower().startswith("q:") or s.startswith("问"):
            lines.append(s)
    # fallback: numbered questions in ask: block
    qs = []
    for ln in text.splitlines():
        s = ln.strip()
        if len(s) >= 15 and any(k in s for k in ("？", "?", "吗", "如何", "怎样", "多少", "什么")):
            qs.append(s)
    if len(qs) < 5:
        fail(f"log 中可识别的问题不足 5 条（当前 {len(qs)}）。Coach 请把学生原问写入 log。")
    hit = sum(1 for q in qs if any(k.lower() in q.lower() for k in KEYS))
    if hit < 3:
        fail("至少 3 条问题应触及能/成本/机制或范围")
    need_in_log("ask|追问")
    print("OK: Module 1 passed")

if __name__ == "__main__":
    main()
