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
        "messages": [],          # ← empty — no history needed
        "user_input": f"""
Project idea: {state.get('user_input', '')}

Plan summary: {state.get('plan', '')[:500]}

Cost summary: {state.get('cost', '')[:500]}

Risks summary: {state.get('edges', '')[:500]}
"""                              # ← truncate each section to 500 chars
    }):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()

    return {
        "messages": [AIMessage(content=full_response)],
        "prd": full_response
    }