# planner.py
import logging
from langchain_core.messages import AIMessage
from agents.state import AgentState
from llms.model import LLMService
import time

logger = logging.getLogger(__name__)
_service = LLMService(prompt_type="planner")


def planner_node(state: AgentState) -> dict:
    full_response = ""
    callback = state.get("stream_callback")

    for chunk in _service.generate({
        **state,
        "messages": [],
        "user_input": state.get("user_input", "")
    }):
        print(chunk, end="", flush=True)
        full_response += chunk
        if callback:
            callback("planner", chunk)  # ← send chunk to UI

    print()
    return {
        "messages": [AIMessage(content=full_response)],
        "plan": full_response
    }