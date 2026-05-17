from unittest.mock import Mock

from langchain_core.messages import HumanMessage

from agents.supervisor.supervisor import (  # noqa: E501
    supervisor,
    PlannerAgent,
    CostAgent,
    EdgeCaseAgent,
    DocAgent,
)


def _fake_result(agent_name: str, output: str):
    return {
        "agent_name": agent_name,
        "output": output,
        "success": bool(output),
        "error": None,
    }


def test_all_three_agents_produce_results(monkeypatch):
    monkeypatch.setattr(
        PlannerAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("planner", "plan"),
    )
    monkeypatch.setattr(
        CostAgent, "_safe_run", lambda self, idea, context: _fake_result("cost", "cost")
    )
    monkeypatch.setattr(
        EdgeCaseAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("edge_case", "edges"),
    )
    monkeypatch.setattr(
        DocAgent, "_safe_run", lambda self, idea, context: _fake_result("doc", "prd")
    )

    state = {
        "messages": [HumanMessage(content="plan it")],
        "idea": "build x",
        "context": "some context",
    }

    result = supervisor.invoke(state, config={"configurable": {"thread_id": "test"}})

    assert result["planner_result"]["success"] is True
    assert result["cost_result"]["success"] is True
    assert result["edge_case_result"]["success"] is True
    assert result["doc_result"]["success"] is True
    assert result["plan"] == "plan"
    assert result["cost"] == "cost"
    assert result["edges"] == "edges"
    assert result["prd"] == "prd"


def test_cost_failure_still_produces_prd(monkeypatch):
    monkeypatch.setattr(
        PlannerAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("planner", "plan"),
    )
    monkeypatch.setattr(
        EdgeCaseAgent,
        "_safe_run",
        lambda self, idea, context: _fake_result("edge_case", "edges"),
    )
    monkeypatch.setattr(
        CostAgent,
        "_safe_run",
        lambda self, idea, context: {
            "agent_name": "cost",
            "output": "",
            "success": False,
            "error": "boom",
        },
    )
    monkeypatch.setattr(
        DocAgent, "_safe_run", lambda self, idea, context: _fake_result("doc", "prd")
    )

    state = {
        "messages": [HumanMessage(content="plan it")],
        "idea": "build x",
        "context": "some context",
    }

    result = supervisor.invoke(state, config={"configurable": {"thread_id": "test"}})

    assert result["cost_result"]["success"] is False
    assert result["doc_result"]["success"] is True
    assert result["prd"] == "prd"
