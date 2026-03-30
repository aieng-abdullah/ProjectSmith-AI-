import logging
from langchain_core.messages import AIMessage
from agents.state import AgentState
from llms.model import LLMService
import time

logger = logging.getLogger(__name__)

llm = LLMService(prompt_type="doc")


def doc_node(state: AgentState) -> dict:
    time.sleep(5)
    full_response = ""

    for chunk in llm.generate({
        **state,
        "messages": [],
        "user_input": f"""
Project idea: {state.get('user_input', '')}
Plan: {state.get('plan', '')[:500]}
Cost advice: {state.get('cost', '')[:500]}
Risks and edge cases: {state.get('edges', '')[:500]}
"""
    }):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()

    return {
        "messages": [AIMessage(content=full_response)],
        "prd": full_response
    }