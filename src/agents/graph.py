"""
This code builds a LangGraph flow where the state goes from START to a router node (for retrieval) to an LLM node and then to END.
The graph is compiled with a checkpointer to save conversation state.
heckpointer is included when compiling the graph so the conversation state can be saved in memory.

"""

from langgraph.graph import StateGraph, START, END
from agents.state import AgentState
from agents.node.res import llm_node
from memory.stm import checkpointer


def build_graph():
    builder = StateGraph(AgentState)

    
    builder.add_node("llm", llm_node)

    builder.add_edge(START, "llm")
    builder.add_edge("llm", END)

    return builder.compile(checkpointer=checkpointer)


graph = build_graph()  