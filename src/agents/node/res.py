import logging
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from agents.state import AgentState
from memory.stm_manager import trim
from llms.model import LLMService

logger = logging.getLogger(__name__)

_services = {
    "bp":       LLMService(prompt_type="bp"),
    "engineer": LLMService(prompt_type="engineer"),
    "psycho":   LLMService(prompt_type="psycho"),
}


def llm_node(state: AgentState, config: RunnableConfig) -> dict:
    persona = state.get("persona", "bp")
    service = _services.get(persona)

    if not service:
        err = f"[Error: unknown persona '{persona}']"
        return {"messages": [AIMessage(content=err)]}

    # read ltm_context from config — bypasses checkpointer overwrite
    ltm_context = config.get("configurable", {}).get("ltm_context", "")

    trimmed_state = {
        **state,
        "messages":    trim(state.get("messages", [])),
        "ltm_context": ltm_context,
    }

    full_response = ""
    for chunk in service.generate(trimmed_state):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()

    return {
        "messages": [AIMessage(content=full_response)],
    }