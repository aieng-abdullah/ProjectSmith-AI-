import logging
import uuid
from langchain_core.messages import HumanMessage
from agents.graph import graph

logging.basicConfig(level=logging.WARNING)

VALID_PERSONAS = ["bp", "engineer", "psycho"]


def pick_persona() -> str:
    print("\nPersonas: bp | engineer | psycho")
    while True:
        choice = input("Pick persona: ").strip().lower()
        if choice in VALID_PERSONAS:
            return choice
        print(f"Choose from: {VALID_PERSONAS}")


def run():
    persona  = pick_persona()
    user_id  = input("Username: ").strip() or "default_user"

    # new session by default
    thread_id = str(uuid.uuid4())
    config    = {"configurable": {"thread_id": thread_id}}

    print(f"\n[{persona}] Session: {thread_id}")
    print("Commands: 'new' | 'resume <id>' | 'quit'\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nBye.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Bye.")
            break

        # fresh session — new thread_id = fresh memory
        if user_input.lower() == "new":
            thread_id = str(uuid.uuid4())
            config    = {"configurable": {"thread_id": thread_id}}
            print(f"[New session: {thread_id}]\n")
            continue

        # resume old session — paste a previous thread_id
        if user_input.lower().startswith("resume "):
            thread_id = user_input.split(" ", 1)[1].strip()
            config    = {"configurable": {"thread_id": thread_id}}
            print(f"[Resumed: {thread_id}]\n")
            continue

        print("Assistant: ", end="", flush=True)

        try:
            graph.invoke(
                {
                    "user_input":        user_input,
                    "persona":           persona,
                    "retrieved_context": "",
                    "user_id":           user_id,
                    "ltm_context":       "",
                    "messages":          [HumanMessage(content=user_input)],
                    "plan":              [],
                    "route":             "",
                },
                config=config,
            )
        except Exception as e:
            print(f"\n[Error: {e}]")

        print()


if __name__ == "__main__":
    run()