from langgraph.graph import END
from agents.state import AgentState

PLAN_TRIGGERS = {
    "plan it", "plan this", "build it",
    "let's plan", "lets plan", "start planning"
}

MIN_MESSAGES = 4


def router_node(state: AgentState) -> str:
    user_input = state.get("user_input", "").strip().lower()
    messages   = state.get("messages", [])

    # check if already flagged as ready by the API (plan_state sets this to True)
    ready = state.get("ready_to_plan", False)

    # also check trigger phrase for CLI usage
    if not ready:
        is_trigger         = any(trigger in user_input for trigger in PLAN_TRIGGERS)
        has_enough_context = len(messages) >= MIN_MESSAGES
        if is_trigger and has_enough_context:
            ready = True
            state["ready_to_plan"] = True

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