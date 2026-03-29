import logging
from langchain_core.messages import AIMessage
from agents.state import AgentState
from llms.model import LLMService
import time
from agents.tools.web_search import search_pricing

logger = logging.getLogger(__name__)

llm = LLMService(prompt_type="cost")


def cost_node(state: AgentState) -> dict:
    time.sleep(5)
    pricing_data = search_pricing(state.get("user_input", ""))
    full_response = ""
    for chunk in llm.generate({
        **state,
        "messages": [],
        "user_input": f"""
Project idea: {state.get('user_input', '')}
Plan: {state.get('plan', '')[:500]}
Real pricing data from web: {pricing_data}
"""
    }):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()
    return {
        "messages": [AIMessage(content=full_response)],
        "cost": full_response
    }