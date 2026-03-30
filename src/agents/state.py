# agents/state.py
from typing import Annotated, Optional, Callable
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages:        Annotated[list[BaseMessage], add_messages]
    user_input:      str
    ready_to_plan:   bool
    plan:            str
    cost:            str
    edges:           str
    prd:             str
   