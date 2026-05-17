# agents/supervisor/supervisor.py
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_core.messages import AIMessage
from agents.supervisor_state import SupervisorState
from agents.supervisor.router import classify_intent
from agents.sub_agents.planner_agent import PlannerAgent
from agents.sub_agents.cost_agent import CostAgent
from agents.sub_agents.edge_case_agent import EdgeCaseAgent
from agents.sub_agents.doc_agent import DocAgent
from agents.sub_agents.chat_agent import ChatAgent
from agents.sub_agents.memory_agent import MemoryAgent
from memory.stm import checkpointer


def supervisor_node(state: SupervisorState) -> dict:
    """Classifies intent and routes to appropriate sub-agents."""
    intent = classify_intent(state.get("messages", []))
    return {"intent": intent}


def run_planner(state: SupervisorState) -> dict:
    """Runs PlannerAgent."""
    agent = PlannerAgent()
    result = agent._safe_run(state["idea"], state.get("context", ""))
    return {
        "planner_result": result,
        "plan": result["output"],
    }


def run_cost(state: SupervisorState) -> dict:
    """Runs CostAgent."""
    agent = CostAgent()
    result = agent._safe_run(state["idea"], state.get("context", ""))
    return {
        "cost_result": result,
        "cost": result["output"],
    }


def run_edge_case(state: SupervisorState) -> dict:
    """Runs EdgeCaseAgent."""
    agent = EdgeCaseAgent()
    result = agent._safe_run(state["idea"], state.get("context", ""))
    return {
        "edge_case_result": result,
        "edges": result["output"],
    }


def run_doc(state: SupervisorState) -> dict:
    """Runs DocAgent with whatever results arrived."""
    agent = DocAgent()
    # Build context from available results
    context_parts = []
    if state.get("planner_result") and state["planner_result"]["success"]:
        context_parts.append(f"PLAN:{state['planner_result']['output']}")
    if state.get("cost_result") and state["cost_result"]["success"]:
        context_parts.append(f"COST:{state['cost_result']['output']}")
    if state.get("edge_case_result") and state["edge_case_result"]["success"]:
        context_parts.append(f"EDGES:{state['edge_case_result']['output']}")

    context = "\n".join(context_parts)
    result = agent._safe_run(state["idea"], context)
    return {
        "doc_result": result,
        "prd": result["output"],
    }


def run_chat(state: SupervisorState) -> dict:
    """Runs ChatAgent."""
    agent = ChatAgent()
    result = agent._safe_run(state["idea"], state.get("context", ""))
    return {
        "chat_result": result,
        "messages": [AIMessage(content=result["output"])] if result["output"] else [],
    }


def route_from_supervisor(state: SupervisorState):
    """Routes based on intent."""
    intent = state.get("intent", "validate")

    if intent == "plan":
        return [
            Send("planner", state),
            Send("cost", state),
            Send("edge_case", state),
        ]
    elif intent == "validate":
        return "chat"
    elif intent == "new":
        return "memory"
    elif intent == "memories":
        return "memory"
    elif intent == "clearmemory":
        return "memory"
    elif intent == "quit":
        return "memory"

    return "chat"


def route_after_parallel(state: SupervisorState):
    """After parallel agents complete, route to doc."""
    return "doc"


def route_after_doc(state: SupervisorState):
    """After doc completes, end."""
    return END


def build_supervisor():
    """Builds the supervisor graph."""
    builder = StateGraph(SupervisorState)

    # Add nodes
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("planner", run_planner)
    builder.add_node("cost", run_cost)
    builder.add_node("edge_case", run_edge_case)
    builder.add_node("doc", run_doc)
    builder.add_node("chat", run_chat)
    builder.add_node(
        "memory",
        lambda s: {
            "memory_result": {
                "agent_name": "memory",
                "output": "",
                "success": True,
                "error": None,
            }
        },
    )

    # Entry point
    builder.set_entry_point("supervisor")

    # Supervisor routing
    builder.add_conditional_edges("supervisor", route_from_supervisor)

    # Parallel agents → doc
    for agent in ["planner", "cost", "edge_case"]:
        builder.add_edge(agent, "doc")

    # Doc → END
    builder.add_edge("doc", END)

    # Chat → END
    builder.add_edge("chat", END)

    # Memory → END
    builder.add_edge("memory", END)

    return builder.compile(checkpointer=checkpointer)


supervisor = build_supervisor()
