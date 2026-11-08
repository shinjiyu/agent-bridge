from __future__ import annotations

import json
import sys
from pathlib import Path

STARTER = Path(__file__).resolve().parents[1] / "starter"
sys.path.insert(0, str(STARTER))

from server import handle_message  # noqa: E402


def test_list_tools():
    resp = handle_message({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
    assert resp["id"] == 1
    tools = resp["result"]["tools"]
    names = {t["name"] for t in tools}
    assert names >= {"echo", "add"}
    for t in tools:
        assert "description" in t
        assert "inputSchema" in t


def test_echo():
    resp = handle_message(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "echo", "arguments": {"text": "hi"}},
        }
    )
    text = resp["result"]["content"][0]["text"]
    assert text == "hi"


def test_add():
    resp = handle_message(
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "add", "arguments": {"a": 2, "b": 5}},
        }
    )
    assert resp["result"]["content"][0]["text"] in ("7", "7.0")


def test_unknown_method():
    resp = handle_message({"jsonrpc": "2.0", "id": 4, "method": "nope", "params": {}})
    assert "error" in resp
    assert resp["error"]["code"] == -32601


def test_unknown_tool():
    resp = handle_message(
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "missing", "arguments": {}},
        }
    )
    assert "error" in resp
    assert "unknown tool" in resp["error"]["message"].lower()
