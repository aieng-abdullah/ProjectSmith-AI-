"""
A cli base program for testing/run tha project without ui
"""
import logging
import uuid
from langchain_core.messages import HumanMessage
from agents.graph import graph
from memory.ltm_manager import (
    summarize_and_save,
    extract_and_save_facts,
    load_memories,
)
from memory.ltm import init_ltm, delete_memories, list_memories

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
    # init LTM table on startup — safe to call every time
    init_ltm()

    persona = pick_persona()
    user_id = input("Username: ").strip() or "default_user"

    # load LTM on session start — injected into system prompt
    ltm_context = load_memories(user_id, persona)
    if ltm_context:
        print("\n[Memory loaded from past sessions]\n")

    thread_id = str(uuid.uuid4())
    config    = config = {"configurable": {"thread_id": thread_id, "ltm_context": ltm_context}}

    print(f"\n[{persona}] Session: {thread_id}")
    print("Commands: 'new' | 'resume <id>' | 'memories' | 'clearmemory' | 'quit'\n")

    # track messages this session for LTM
    session_messages = []
    message_count    = 0

    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\n")
            break

        if not user_input:
            continue

        # save LTM on quit
        if user_input.lower() in ("quit", "exit"):
            if session_messages:
                print("[Saving memory...]")
                summarize_and_save(session_messages, user_id, persona)
            print("Bye.")
            break

        # save LTM before new session, reload after
        if user_input.lower() == "new":
            if session_messages:
                print("[Saving memory...]")
                summarize_and_save(session_messages, user_id, persona)

            session_messages = []
            message_count  = 0
            thread_id  = str(uuid.uuid4())
            ltm_context  = load_memories(user_id, persona)
            config  = {"configurable": {"thread_id": thread_id, "ltm_context": ltm_context}}  # updated
            print(f"[New session: {thread_id}]\n")
            continue


        if user_input.lower().startswith("resume "):
            thread_id = user_input.split(" ", 1)[1].strip()
            config    = {"configurable": {"thread_id": thread_id}}
            print(f"[Resumed: {thread_id}]\n")
            continue

        # show what LTM knows about this user
        if user_input.lower() == "memories":
            mems = list_memories(user_id)
            if not mems:
                print("[No memories found]\n")
            else:
                print(f"\n[Memories for {user_id}]:")
                for m in mems:
                    print(f"  [{m['created_at']}] {m['type']}: {m['content'][:100]}...")
                print()
            continue

        # wipe all LTM for this user
        if user_input.lower() == "clearmemory":
            confirm = input("Wipe all memories? (yes/no): ").strip().lower()
            if confirm == "yes":
                delete_memories(user_id)
                ltm_context = ""
                print("[All memories wiped]\n")
            else:
                print("[Cancelled]\n")
            continue

        print("Assistant: ", end="", flush=True)

        human_msg = HumanMessage(content=user_input)
        session_messages.append(human_msg)
        message_count += 1

        try:
            result = graph.invoke(
                {
                    "user_input":        user_input,
                    "persona":           persona,
                    "retrieved_context": "",
                    "user_id":           user_id,
                    "ltm_context":       ltm_context,  # injected into prompt
                    "messages":          [human_msg],
                    "plan":              [],
                    "route":             "",
                },
                config=config,
            )

            # track AI response for LTM
            if result.get("messages"):
                session_messages.append(result["messages"][-1])

            # extract facts every 5 messages automatically
            if message_count % 5 == 0:
                extract_and_save_facts(session_messages, user_id, persona)

        except Exception as e:
            print(f"\n[Error: {e}]")

        print()


if __name__ == "__main__":
    run()