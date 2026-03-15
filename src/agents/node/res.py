from langchain_core.messages import HumanMessage, AIMessage
from agents.state import AgentState
from llms.model import LLMService


_services = {
    "bp":       LLMService(prompt_type="bp"),
    "engineer": LLMService(prompt_type="engineer"),  # must match get_prompt exactly
    "psycho":   LLMService(prompt_type="psycho"),
}


def llm_node(state: AgentState) -> dict:
    persona = state.get("persona", "bp")
    service = _services.get(persona)

    if not service:
        err = f"[Error: unknown persona '{persona}']"
        return {
            "messages": [AIMessage(content=err)],
            "current_response": err
        }

    full_response = ""

    # stream chunks
    for chunk in service.generate(state):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()

    return {
        "messages": [
            HumanMessage(content=state["user_input"]),
            AIMessage(content=full_response)
        ]
    }