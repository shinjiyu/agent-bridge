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


FACES = {"cost", "context", "orchestration", "contracts", "evaluation", "security", "embodied"}

def main() -> None:
    need_in_log("choose|抉择", "ask|追问")
    scope = need_agent_file("SCOPE.md", 20)
    text = scope.read_text(encoding="utf-8").lower()
    hit = [f for f in FACES if f in text]
    if len(hit) < 3:
        fail("SCOPE.md 至少点名 3 个 harness 面")
    print("OK: Module 6 passed")

if __name__ == "__main__":
    main()
