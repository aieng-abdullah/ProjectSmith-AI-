from langchain_core.messages import AIMessage
from agents.state import AgentState
from agents.state import AgentState
from langchain_core.runnables import RunnableConfig
from agents.state import AgentState
from llms.model import LLMService
import time

from memory.stm_manager import trim


#define tha llm promt
llm = LLMService(prompt_type="planner")




def planner_node(state: AgentState) -> dict:
    time.sleep(5)
    full_response = ""
    for chunk in llm.generate({
        **state,
        "messages": trim(state.get("messages", [])),  # ← add trim
        "user_input": state.get("user_input", "")
    }):
        print(chunk, end="", flush=True)
        full_response += chunk

    print()
    return {
        "messages": [AIMessage(content=full_response)],
        "plan": full_response
    }
