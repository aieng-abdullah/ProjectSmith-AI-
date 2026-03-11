"""
Creates a LangGraph chat graph with short-term memory. 
The graph node extracts facts from the latest user input, prepends them to the prompt, 
generates an AI response via the LLMService, appends the AIMessage to the conversation state,
and uses the memory checkpointer for automatic persistence

"""
from langgraph.graph import StateGraph, MessagesState, START, END
from llms.model import LLMService
from langchain_core.messages import HumanMessage, AIMessage

def create_chat_graph(llm_service: LLMService, memory):
    """Build LangGraph chat graph with structured memory."""
    
    def chat_node(state: MessagesState):

        last_message = state["messages"][-1]
        user_input = last_message.content

        memory.extract_facts(user_input)

        facts_text = " | ".join(
            f"{k}: {v}" for k, v in memory.facts.items()
        )

        prompt = f"{facts_text}\n{user_input}"

        response_text = "".join(
             chunk for chunk in llm_service.generate(prompt)
                )

        return {

         "messages": state["messages"] + [AIMessage(content=response_text)]
         }       

    builder = StateGraph(MessagesState)
    builder.add_node("chat", chat_node)
    builder.set_entry_point("chat")
    builder.add_edge("chat", END)

    return builder.compile(checkpointer=memory.checkpointer)