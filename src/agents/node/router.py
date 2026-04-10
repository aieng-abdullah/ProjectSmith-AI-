from langgraph.graph import END
from agents.state import AgentState

PLAN_TRIGGERS = {
    "plan it", "plan this", "build it",
    "let's plan", "lets plan", "start planning"
}

MIN_MESSAGES = 4  # at least 2 user + 2 advisor exchanges before planning


def router_node(state: AgentState) -> str:
    user_input = state.get("user_input", "").strip().lower()
    messages   = state.get("messages", [])

    # only trigger planning if exact trigger phrase AND enough conversation
    is_trigger      = any(trigger == user_input for trigger in PLAN_TRIGGERS)
    has_enough_context = len(messages) >= MIN_MESSAGES

    if is_trigger and has_enough_context:
        state["ready_to_plan"] = True

    ready = state.get("ready_to_plan", False)

    if not ready:
        return "chat"

    if not state.get("plan"):
        return "planner"

    if not state.get("cost"):
        return "cost"

    if not state.get("edges"):
        return "edge_case"

    if not state.get("prd"):
        return "doc"

    return END