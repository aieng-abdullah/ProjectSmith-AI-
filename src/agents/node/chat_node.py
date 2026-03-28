import logging
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from agents.state import AgentState
from memory.stm_manager import trim
from llms.model import LLMService

logger = logging.getLogger(__name__)

llm = LLMService(prompt_type="chat")


def chat_node(state: AgentState, config: RunnableConfig) -> dict:
    ltm_context = config.get("configurable", {}).get("ltm_context", "")

    full_response = ""
    for chunk in llm.generate({
        **state,
        "messages":    trim(state.get("messages", [])),
        "user_input":  state.get("user_input", ""),
        "ltm_context": ltm_context,
    }):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()

    return {
        "messages": [AIMessage(content=full_response)],
    }