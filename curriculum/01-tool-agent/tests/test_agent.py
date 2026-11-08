from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

STARTER = Path(__file__).resolve().parents[1] / "starter"
sys.path.insert(0, str(STARTER))

import agent  # noqa: E402
import tools  # noqa: E402


def test_calc_basic():
    assert tools.calc("1+2*3") == "7" or float(tools.calc("1+2*3")) == 7.0


def test_calc_rejects_names():
    with pytest.raises(Exception):
        tools.calc("__import__('os').system('echo hacked')")


def test_now_iso():
    s = tools.now()
    assert "T" in s
    assert s.endswith("Z") or "+" in s or s.endswith("00:00")


def test_kb_get():
    assert "Paris" in tools.kb_get("capitals.france")


def test_agent_calc_goal():
    out = agent.run_agent("请计算 (2+3)*4")
    assert out["ok"] is True
    assert any(s.get("tool") == "calc" for s in out["steps"])
    assert "20" in str(out["final"])


def test_agent_now_goal():
    out = agent.run_agent("现在 UTC 几点 / what time is now")
    assert any(s.get("tool") == "now" for s in out["steps"])
    assert out["final"]


def test_agent_kb_goal():
    out = agent.run_agent("查知识 capitals.france")
    assert any(s.get("tool") == "kb_get" for s in out["steps"])
    assert "Paris" in str(out["final"])
