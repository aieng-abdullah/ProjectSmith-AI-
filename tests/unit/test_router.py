from unittest.mock import Mock

from langchain_core.messages import HumanMessage

from agents.supervisor.router import classify_intent


def test_plan_trigger_never_calls_llm(monkeypatch):
    mock_generate = Mock()
    monkeypatch.setattr("agents.supervisor.router.llm.generate", mock_generate)

    intent = classify_intent([HumanMessage(content="plan it")])

    assert intent == "plan"
    mock_generate.assert_not_called()
