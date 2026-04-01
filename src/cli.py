"""
CLI for testing ProjectSmith AI without UI
"""
import logging
import uuid
from langchain_core.messages import HumanMessage
from agents.graph import graph
from memory.ltm_manager import (
    summarize_and_save,
    load_memories,
)
from memory.ltm import init_ltm, delete_memories, list_memories

logging.basicConfig(level=logging.WARNING)

PLAN_TRIGGERS = {"plan it", "plan this", "build it", "let's plan", "lets plan", "go", "start planning"}


def run():
    init_ltm()

    user_id = input("Username: ").strip() or "default_user"

    ltm_context = load_memories(user_id, "advisor")
    if ltm_context:
        print("\n[Past projects loaded from memory]\n")

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id, "ltm_context": ltm_context}}

    print(f"\n🔨 ProjectSmith AI  |  Session: {thread_id}")
    print("Commands: 'new' | 'memories' | 'clearmemory' | 'quit'\n")

    session_messages = []

    while True:
        try:
            user_input = input("Your idea: ").strip()
        except KeyboardInterrupt:
            print("\n")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            if session_messages:
                print("[Saving memory...]")
                summarize_and_save(session_messages, user_id, "advisor")
            print("Bye.")
            break

        if user_input.lower() == "new":
            if session_messages:
                print("[Saving memory...]")
                summarize_and_save(session_messages, user_id, "advisor")
            session_messages = []
            thread_id = str(uuid.uuid4())
            ltm_context = load_memories(user_id, "advisor")
            config = {"configurable": {"thread_id": thread_id, "ltm_context": ltm_context}}
            print(f"[New session: {thread_id}]\n")
            continue

        if user_input.lower().startswith("resume "):
            thread_id = user_input.split(" ", 1)[1].strip()
            config = {"configurable": {"thread_id": thread_id, "ltm_context": ltm_context}}
            print(f"[Resumed: {thread_id}]\n")
            continue

        if user_input.lower() == "memories":
            mems = list_memories(user_id)
            if not mems:
                print("[No past projects found]\n")
            else:
                print(f"\n[Past projects for {user_id}]:")
                for m in mems:
                    print(f"  [{m['created_at']}] {m['content'][:100]}...")
                print()
            continue

        if user_input.lower() == "clearmemory":
            confirm = input("Wipe all past projects? (yes/no): ").strip().lower()
            if confirm == "yes":
                delete_memories(user_id)
                ltm_context = ""
                print("[All memories wiped]\n")
            else:
                print("[Cancelled]\n")
            continue

        # run the agent
        human_msg = HumanMessage(content=user_input)
        session_messages.append(human_msg)

        # only show spinner when planning is triggered
        if any(trigger in user_input.lower() for trigger in PLAN_TRIGGERS):
            print("\n⏳ Building your project plan...\n")
            print("─" * 40)

        try:
            result = graph.invoke(
                {
                    "user_input":    user_input,
                    "messages":      [human_msg],
                    "ready_to_plan": False,
                    "plan":          "",
                    "cost":          "",
                    "edges":         "",
                    "prd":           "",
                },
                config=config,
            )

            if result.get("messages"):
                session_messages.append(result["messages"][-1])

            if result.get("plan"):
                print("\n📋 PLAN\n")
                print(result["plan"])

                print("\n" + "─" * 40)
                print("\n💰 COST & STACK\n")
                print(result["cost"])

                print("\n" + "─" * 40)
                print("\n⚠️  EDGE CASES\n")
                print(result["edges"])

                print("\n" + "─" * 40)
                print("\n📄 YOUR PROJECT BRIEF\n")
                print(result["prd"])

                print("\n" + "─" * 40)
                print("✅ Done! Type 'new' to start a fresh idea.\n")

        except Exception as e:
            print(f"\n[Error: {e}]")

        print()


if __name__ == "__main__":
    run()