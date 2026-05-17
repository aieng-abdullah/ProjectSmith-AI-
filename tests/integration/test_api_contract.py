"""Integration test for API response contracts."""

from unittest.mock import patch, MagicMock
from agents.sub_agents.planner_agent import PlannerAgent
from agents.sub_agents.cost_agent import CostAgent
from agents.sub_agents.edge_case_agent import EdgeCaseAgent
from agents.sub_agents.doc_agent import DocAgent


def _fake_result(agent_name: str, output: str):
    return {
        "agent_name": agent_name,
        "output": output,
        "success": bool(output),
        "error": None,
    }


def test_plan_endpoint_returns_same_shape(monkeypatch):
    """Verify that /plan returns the same JSON structure as before."""
    from src.api.main import plan, PlanRequest

    monkeypatch.setattr(
        PlannerAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("planner", "plan-output"),
    )
    monkeypatch.setattr(
        CostAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("cost", "cost-output"),
    )
    monkeypatch.setattr(
        EdgeCaseAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("edge_case", "edges-output"),
    )
    monkeypatch.setattr(
        DocAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("doc", "prd-output"),
    )

    request = PlanRequest(user_id="test", thread_id="t1", message="plan it")
    response = plan(request)

    assert all(k in response for k in ["plan", "cost", "edges", "prd"])
    assert response["plan"] == "plan-output"
    assert response["cost"] == "cost-output"
    assert response["edges"] == "edges-output"
    assert response["prd"] == "prd-output"
