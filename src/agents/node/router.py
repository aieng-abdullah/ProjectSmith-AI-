from langgraph.graph import END
from agents.state import AgentState

PLAN_TRIGGERS = {"plan it", "plan this", "build it", "let's plan", "lets plan", "go", "start planning"}


def router_node(state: AgentState) -> str:
    user_input = state.get("user_input", "").strip().lower()

    # check if user wants to trigger planning
    if any(trigger in user_input for trigger in PLAN_TRIGGERS):
        state["ready_to_plan"] = True

    ready = state.get("ready_to_plan", False)

    if not ready:
        return "chat"

    # planning sequence
    if not state.get("plan"):
        return "planner"

    if not state.get("cost"):
        return "cost"

    if not state.get("edges"):
        return "edge_case"

    if not state.get("prd"):
        return "doc"

    return END