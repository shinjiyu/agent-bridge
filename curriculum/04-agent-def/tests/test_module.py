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


def main() -> None:
    need_in_log("explain|说明", "ask|追问", "choose|抉择")
    text = log_text()
    if "general" not in text.lower() and "通用" not in text:
        fail("choose 须声明通用 Agent")
    if "react" not in text.lower() and "工具环" not in text and "Reason" not in text:
        fail("log 须提到 ReAct 或工具环")
    if not any(x in text for x in ("Graph", "graph", "编排", "工作流", "workflow")):
        fail("log 须对照 Graph/编排")
    print("OK: Module 4 passed")

if __name__ == "__main__":
    main()
