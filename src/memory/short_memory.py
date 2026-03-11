"""
Implements short-term memory for chat. 
It stores structured facts about the user, allows setting a conversation thread, 
and extracts basic facts like the user’s name from their input.
The memory includes a checkpointer for automatic state persistence.

"""
from langgraph.checkpoint.memory import InMemorySaver

class ShortTermMemory:
    """Short-term memory with structured facts."""
    
    def __init__(self):
        self.checkpointer = InMemorySaver()  # not used for save/load
        self.config = {"configurable": {"thread_id": "session1"}}
        self.facts = {}     

    def set_thread(self, thread_id: str):
        self.config["configurable"]["thread_id"] = thread_id


    def extract_facts(self, user_input: str):
        """Extract basic facts like user name."""
        user_input_lower = user_input.lower()
        if "my name is " in user_input_lower:
            name = user_input_lower.split("my name is ")[1].split()[0]
            self.facts["user_name"] = name.capitalize()