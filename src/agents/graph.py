from langgraph.graph import StateGraph, START, END
from agents.state import AgentState
from agents.node.chat_node import chat_node
from agents.node.planner import planner_node
from agents.node.cost import cost_node
from agents.node.edge_case import edge_case_node
from agents.node.doc_node import doc_node
from agents.node.router import router_node
from memory.stm import checkpointer


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("chat",      chat_node)
    builder.add_node("planner",   planner_node)
    builder.add_node("cost",      cost_node)
    builder.add_node("edge_case", edge_case_node)
    builder.add_node("doc",       doc_node)

    builder.add_conditional_edges(
        START,
        router_node,
        {
            "chat":      "chat",
            "planner":   "planner",
            "cost":      "cost",
            "edge_case": "edge_case",
            "doc":       "doc",
            END:          END,
        }
    )

    # chat runs ONCE then stops — user replies in next loop iteration
    builder.add_edge("chat", END)

    # planning nodes chain through router
    builder.add_conditional_edges("planner",   router_node, {"cost": "cost", END: END})
    builder.add_conditional_edges("cost",      router_node, {"edge_case": "edge_case", END: END})
    builder.add_conditional_edges("edge_case", router_node, {"doc": "doc", END: END})
    builder.add_conditional_edges("doc",       router_node, {END: END})

    return builder.compile(checkpointer=checkpointer)


graph = build_graph()