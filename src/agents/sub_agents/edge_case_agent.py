# agents/sub_agents/edge_case_agent.py
from agents.sub_agents.base import BaseSubAgent
from agents.supervisor_state import SubAgentResult
from agents.node.edge_case import edge_case_node
from agents.state import AgentState


class EdgeCaseAgent(BaseSubAgent):
    name = "edge_case"

    def run(self, idea: str, context: str) -> SubAgentResult:
        state = AgentState(
            messages=[],
            user_input=idea,
            ready_to_plan=True,
            plan=context[:500] if context else "",
            cost=context[:500] if context else "",
            edges="",
            prd="",
            mode="plan"
        )
        result = edge_case_node(state)
        output = result.get("edges", "")
        return SubAgentResult(
            agent_name=self.name,
            output=output,
            success=bool(output),
            error=None
        )
