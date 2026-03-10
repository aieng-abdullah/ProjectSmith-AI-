""".
This graph wraps your LLMService and adds short-term memory using
LangGraph's in-memory checkpointer. It is designed to be reusable
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import InMemorySaver
from llms.model import LLMService
from langchain_core.messages import HumanMessage, AIMessage


def create_chat_graph(llm_service: LLMService):
    """
    Create a LangGraph chatbot graph node with short-term memory.

    """

    def chat_node(state: MessagesState):
        """
        Node that generates AI response using LLMService.

        """
        # Append latest human message
        last_input = state["messages"][-1] if state["messages"] else {"role": "user", "content": ""}
        if isinstance(last_input, dict):
            user_input = last_input.get("content", "")
        else:
            user_input = last_input.content

        # Generate response using LLMService
        response_text = "".join(chunk for chunk in llm_service.generate(user_input))

        # Update state
        new_messages = state["messages"] + [HumanMessage(content=user_input), AIMessage(content=response_text)]
        return {"messages": new_messages}

    # Build the graph
    builder = StateGraph(MessagesState)
    builder.add_node("chat", chat_node)
    builder.set_entry_point("chat")
    builder.add_edge("chat", END)

    # Add short-term memory checkpoint
    checkpointer = InMemorySaver()
    graph = builder.compile(checkpointer=checkpointer)

    return graph