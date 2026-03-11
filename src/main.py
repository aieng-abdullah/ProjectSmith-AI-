from llms.model import LLMService
from memory.short_memory import ShortTermMemory
from memory.graph_factory import create_chat_graph
from langchain_core.messages import HumanMessage

def main():

    persona = input("Choose persona (bp / psycho / eninner): ")

    llm = LLMService(prompt_type=persona)

    memory = ShortTermMemory()
    memory.set_thread("session1")

    chat_graph = create_chat_graph(llm, memory)

    print("\n=== Chatbot Started ===\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in {"exit", "quit"}:
            break

        result = chat_graph.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            memory.config
        )

        ai_message = result["messages"][-1]

        print("AI:", ai_message.content)





main()