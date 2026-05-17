# agents/sub_agents/chat_agent.py
from langchain_core.runnables import RunnableConfig
from agents.sub_agents.base import BaseSubAgent
from agents.supervisor_state import SubAgentResult
from agents.node.chat_node import chat_node
from agents.state import AgentState


class ChatAgent(BaseSubAgent):
    name = "chat"

    def run(self, idea: str, context: str) -> SubAgentResult:
        state = AgentState(
            messages=[],
            user_input=idea,
            ready_to_plan=False,
            plan="",
            cost="",
            edges="",
            prd="",
            mode="chat"
        )
        config = RunnableConfig(configurable={"ltm_context": context})
        result = chat_node(state, config)
        messages = result.get("messages", [])
        output = messages[-1].content if messages else ""
        return SubAgentResult(
            agent_name=self.name,
            output=output,
            success=bool(output),
            error=None
        )
