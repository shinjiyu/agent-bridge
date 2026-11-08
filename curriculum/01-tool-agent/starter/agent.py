"""Minimal tool-loop agent. Implement decide + run_agent."""
from __future__ import annotations

from typing import Any

from tools import calc, kb_get, now


def decide(goal: str, history: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Return either:
      {"tool": "calc"|"now"|"kb_get", "args": {...}, "thought": "..."}
    or:
      {"final": "...", "thought": "..."}
    """
    raise NotImplementedError("implement decide")


def run_agent(goal: str, max_steps: int = 6) -> dict[str, Any]:
    """
    Run the tool loop. Return:
      {"ok": bool, "steps": [...], "final": str}
    """
    raise NotImplementedError("implement run_agent")


if __name__ == "__main__":
    import sys

    g = " ".join(sys.argv[1:]) or "计算 1+2*3"
    print(run_agent(g))
