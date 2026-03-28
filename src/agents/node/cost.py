import logging
from langchain_core.messages import AIMessage
from agents.state import AgentState
from llms.model import LLMService
from memory.stm_manager import trim
import time

logger = logging.getLogger(__name__)


llm = LLMService(prompt_type="cost")

def cost_node(state: AgentState) -> dict:
    time.sleep(5)
    full_response = ""
    for chunk in llm.generate({
        **state,
        "messages": trim(state.get("messages", [])),
        "user_input": f"""
Project idea: {state.get('user_input', '')}
Plan: {state.get('plan', '')}
"""
    }):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()

    return {
        "messages": [AIMessage(content=full_response)],
        "cost": full_response
    }