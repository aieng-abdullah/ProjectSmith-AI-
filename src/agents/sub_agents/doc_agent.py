# agents/sub_agents/doc_agent.py
from agents.sub_agents.base import BaseSubAgent
from agents.supervisor_state import SubAgentResult
from agents.node.doc_node import doc_node
from agents.state import AgentState


class DocAgent(BaseSubAgent):
    name = "doc"

    def run(self, idea: str, context: str) -> SubAgentResult:
        # context should contain plan, cost, edges results
        # Parse context to extract individual components
        lines = context.split('\n') if context else []
        plan = ""
        cost = ""
        edges = ""
        
        for line in lines:
            if line.startswith("PLAN:"):
                plan = line.replace("PLAN:", "").strip()
            elif line.startswith("COST:"):
                cost = line.replace("COST:", "").strip()
            elif line.startswith("EDGES:"):
                edges = line.replace("EDGES:", "").strip()
        
        state = AgentState(
            messages=[],
            user_input=idea,
            ready_to_plan=True,
            plan=plan[:500],
            cost=cost[:500],
            edges=edges[:500],
            prd="",
            mode="plan"
        )
        result = doc_node(state)
        output = result.get("prd", "")
        return SubAgentResult(
            agent_name=self.name,
            output=output,
            success=bool(output),
            error=None
        )
