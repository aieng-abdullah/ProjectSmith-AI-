import agents.node.chat_node as chat_node
import agents.node.cost as cost_node
import agents.node.doc_node as doc_node
import agents.node.edge_case as edge_case_node
import agents.node.planner as planner_node
import agents.sub_agents.memory_agent as memory_agent_module

from agents.sub_agents.chat_agent import ChatAgent
from agents.sub_agents.cost_agent import CostAgent
from agents.sub_agents.doc_agent import DocAgent
from agents.sub_agents.edge_case_agent import EdgeCaseAgent
from agents.sub_agents.memory_agent import MemoryAgent
from agents.sub_agents.planner_agent import PlannerAgent


def test_sub_agents_run_standalone(monkeypatch):
    monkeypatch.setattr(
        planner_node._service, "generate", lambda *args, **kwargs: iter(["plan-output"])
    )
    monkeypatch.setattr(cost_node.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        cost_node.llm, "generate", lambda *args, **kwargs: iter(["cost-output"])
    )
    monkeypatch.setattr(
        "agents.tools.web_search.search_pricing", lambda query: "pricing-data"
    )
    monkeypatch.setattr(edge_case_node.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        edge_case_node.llm, "generate", lambda *args, **kwargs: iter(["edges-output"])
    )
    monkeypatch.setattr(doc_node.time, "sleep", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        doc_node.llm, "generate", lambda *args, **kwargs: iter(["prd-output"])
    )
    monkeypatch.setattr(
        chat_node.llm, "generate", lambda *args, **kwargs: iter(["chat-output"])
    )
    monkeypatch.setattr(
        memory_agent_module, "summarize_and_save", lambda user_id, thread_id: None
    )

    planner_result = PlannerAgent().run("idea", "context")
    cost_result = CostAgent().run("idea", "plan text")
    edge_result = EdgeCaseAgent().run("idea", "plan text")
    doc_result = DocAgent().run(
        "idea", "PLAN: plan text\nCOST: cost text\nEDGES: edges text"
    )
    chat_result = ChatAgent().run("idea", "ltm-context")
    memory_result = MemoryAgent().run("idea", "USER_ID:test\nTHREAD_ID:thread123")

    assert planner_result["success"] is True
    assert planner_result["agent_name"] == "planner"
    assert cost_result["success"] is True
    assert edge_result["success"] is True
    assert doc_result["success"] is True
    assert chat_result["success"] is True
    assert chat_result["output"] == "chat-output"
    assert memory_result["success"] is True
    assert "thread123" in memory_result["output"]
