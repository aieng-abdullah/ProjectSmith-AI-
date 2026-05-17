import pytest

from agents.sub_agents.base import BaseSubAgent


class CrashingAgent(BaseSubAgent):
    name = "crasher"

    def run(self, idea: str, context: str):
        raise RuntimeError("boom")


def test_safe_run_never_raises():
    agent = CrashingAgent()
    result = agent._safe_run("idea", "context")
    assert result["success"] is False
    assert result["agent_name"] == "crasher"
    assert result["error"] is not None
