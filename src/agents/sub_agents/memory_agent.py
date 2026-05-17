# agents/sub_agents/memory_agent.py
from agents.sub_agents.base import BaseSubAgent
from agents.supervisor_state import SubAgentResult
from memory.ltm_manager import summarize_and_save


class MemoryAgent(BaseSubAgent):
    name = "memory"

    def run(self, idea: str, context: str) -> SubAgentResult:
        try:
            # context should contain user_id and thread_id
            lines = context.split('\n') if context else []
            user_id = ""
            thread_id = ""
            
            for line in lines:
                if line.startswith("USER_ID:"):
                    user_id = line.replace("USER_ID:", "").strip()
                elif line.startswith("THREAD_ID:"):
                    thread_id = line.replace("THREAD_ID:", "").strip()
            
            if user_id and thread_id:
                summarize_and_save(user_id, thread_id)
                output = f"Memory saved for user {user_id}, thread {thread_id}"
                return SubAgentResult(
                    agent_name=self.name,
                    output=output,
                    success=True,
                    error=None
                )
            else:
                return SubAgentResult(
                    agent_name=self.name,
                    output="",
                    success=False,
                    error="Missing user_id or thread_id in context"
                )
        except Exception as e:
            return SubAgentResult(
                agent_name=self.name,
                output="",
                success=False,
                error=str(e)
            )
