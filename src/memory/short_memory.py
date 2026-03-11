"""
Implements short-term memory for chat. 
It stores structured facts about the user, allows setting a conversation thread, 
and extracts basic facts like the user’s name from their input.
The memory includes a checkpointer for automatic state persistence.

"""
from langgraph.checkpoint.memory import InMemorySaver
import re

class ShortTermMemory:
    """Short-term memory with structured facts."""
    
    def __init__(self):
        self.checkpointer = InMemorySaver()  # not used for save/load
        self.config = {"configurable": {"thread_id": "session1"}}
        self.facts = {}       
        self.buffer_size = 10  # default buffer size

    def set_thread(self, thread_id: str):
        self.config["configurable"]["thread_id"] = thread_id


    def extract_facts(self, user_input: str):
        """Extract basic facts like user name."""
        user_input_lower = user_input.lower()
         # Name
        if "my name is " in user_input_lower:
            name = user_input_lower.split("my name is ")[1].split()[0]
            self.facts["user_name"] = name.capitalize()

        # Age
        age_match = re.search(r"\b(\d{1,3})\s*(?:years|yo|yrs)?\s*old\b", user_input_lower)
        if age_match:
            self.facts["age"] = int(age_match.group(1))

        # Location
        if "i live in " in user_input_lower:
            location = user_input_lower.split("i live in ")[1].split(".")[0].strip()
            self.facts["location"] = location.title()

        # Goals / interests
        goals_match = re.search(r"(i want to|my goal is|i am trying to) ([^.]+)", user_input_lower)
        if goals_match:
            goal = goals_match.group(2).strip()
            self.facts["goal"] = goal

        # Personality traits (optional)
        traits_match = re.findall(r"\bi am (\w+)\b", user_input_lower)
        if traits_match:
            self.facts["traits"] = traits_match



    def get_facts_text(self) -> str:
        """Return formatted facts for prompt prefix."""
        if not self.facts:
            return ""
        return " | ".join(f"{k}: {v}" for k, v in self.facts.items())