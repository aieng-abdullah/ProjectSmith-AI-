# agents/supervisor_state.py
from typing import TypedDict, Optional


class SubAgentResult(TypedDict):
    agent_name: str
    output: str
    success: bool
    error: Optional[str]


class SupervisorState(TypedDict):
    messages: list
    idea: str
    context: str
    intent: str
    plan: Optional[str]
    cost: Optional[str]
    edges: Optional[str]
    prd: Optional[str]

    # Sub-agent results
    planner_result: Optional[SubAgentResult]
    cost_result: Optional[SubAgentResult]
    edge_case_result: Optional[SubAgentResult]
    doc_result: Optional[SubAgentResult]
    chat_result: Optional[SubAgentResult]
    memory_result: Optional[SubAgentResult]
