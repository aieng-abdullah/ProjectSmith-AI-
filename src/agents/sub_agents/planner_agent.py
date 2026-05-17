# agents/sub_agents/planner_agent.py
from agents.sub_agents.base import BaseSubAgent
from agents.supervisor_state import SubAgentResult
from agents.node.planner import planner_node
from agents.state import AgentState


class PlannerAgent(BaseSubAgent):
    name = "planner"

    def run(self, idea: str, context: str) -> SubAgentResult:
        state = AgentState(
            messages=[],
            user_input=idea,
            ready_to_plan=True,
            plan="",
            cost="",
            edges="",
            prd="",
            mode="plan"
        )
        result = planner_node(state)
        output = result.get("plan", "")
        return SubAgentResult(
            agent_name=self.name,
            output=output,
            success=bool(output),
            error=None
        )
