#!/usr/bin/env python3
"""Module 0 — light gate: shell + short chat log."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
LOG = ROOT / "starter" / "log.md"
SHELL = WS / "my-agent" / "README.md"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def main() -> None:
    if not SHELL.exists():
        fail("缺少 my-agent/README.md（作业型产物）")
    if len(SHELL.read_text(encoding="utf-8").strip()) < 20:
        fail("my-agent/README.md 至少 20 字")
    if not LOG.exists():
        fail("缺少 starter/log.md（Coach 应留下实验/追问痕迹）")
    text = LOG.read_text(encoding="utf-8")
    low = text.lower()
    if "experiment" not in low and "实验" not in text:
        fail("log.md 须有实验留痕（含 experiment 或「实验」）")
    if "ask" not in low and "追问" not in text and "能" not in text:
        fail("log.md 须有追问/三问留痕")
    print("OK: Module 0 passed")


if __name__ == "__main__":
    main()
