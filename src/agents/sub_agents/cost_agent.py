# agents/sub_agents/cost_agent.py
from agents.sub_agents.base import BaseSubAgent
from agents.supervisor_state import SubAgentResult
from agents.node.cost import cost_node
from agents.state import AgentState


class CostAgent(BaseSubAgent):
    name = "cost"

    def run(self, idea: str, context: str) -> SubAgentResult:
        state = AgentState(
            messages=[],
            user_input=idea,
            ready_to_plan=True,
            plan=context,  # Use context as plan for cost node
            cost="",
            edges="",
            prd="",
            mode="plan"
        )
        result = cost_node(state)
        output = result.get("cost", "")
        return SubAgentResult(
            agent_name=self.name,
            output=output,
            success=bool(output),
            error=None
        )
