"""Minimal MCP-like JSON-RPC server over stdio. Implement handle_message."""
from __future__ import annotations

import json
import sys
from typing import Any


def handle_message(msg: dict[str, Any]) -> dict[str, Any]:
    """Handle one JSON-RPC request object and return a response object."""
    raise NotImplementedError("implement handle_message")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        req = json.loads(line)
        resp = handle_message(req)
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
