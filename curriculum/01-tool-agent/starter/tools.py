"""Tool implementations for the Module 1 agent. Fill these in."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

KB_PATH = Path(__file__).with_name("kb.json")


def calc(expr: str) -> str:
    """Evaluate a simple arithmetic expression safely. Return the number as str."""
    raise NotImplementedError("implement calc")


def now() -> str:
    """Return current UTC time as ISO-8601 string."""
    raise NotImplementedError("implement now")


def kb_get(key: str) -> str:
    """Look up key in kb.json. Raise KeyError if missing."""
    raise NotImplementedError("implement kb_get")
