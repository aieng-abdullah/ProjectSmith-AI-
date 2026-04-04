"""
FastAPI entry point — exposes chat, planning, streaming, and memory endpoints.
Connects the LangGraph agent (graph), short-term config, and long-term memory (LTM).
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
from agents.graph import graph
from memory.ltm_manager import summarize_and_save, load_memories
from memory.ltm import init_ltm, list_memories
from langchain_core.messages import HumanMessage, AIMessage
import json

app = FastAPI(title="ProjectSmith AI", version="1.0.0")

init_ltm()


# ─── Request models ────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Single conversational turn from the user."""
    user_id:   str
    thread_id: str
    message:   str


class PlanRequest(BaseModel):
    """
    Full planning pipeline trigger.
    message should be the FULL conversation log built by the frontend,
    not just the trigger phrase 'plan it'.
    """
    user_id:      str
    thread_id:    str
    message:      str   # full conversation context
    conversation: str = ""  # optional explicit conversation log


class MessageItem(BaseModel):
    role:    str
    content: str


class SaveRequest(BaseModel):
    """Persists a conversation session to long-term memory."""
    user_id:  str
    messages: List[MessageItem]


# ─── Helper ────────────────────────────────────────────────────────────────────

def make_config(user_id: str, thread_id: str) -> dict:
    """Build LangGraph config with LTM context injected."""
    ltm_context = load_memories(user_id, "advisor")
    return {
        "configurable": {
            "thread_id":   thread_id,
            "ltm_context": ltm_context,
        }
    }


def base_state(user_input: str) -> dict:
    """Build a clean initial agent state."""
    return {
        "user_input":    user_input,
        "messages":      [HumanMessage(content=user_input)],
        "ready_to_plan": False,
        "plan":          "",
        "cost":          "",
        "edges":         "",
        "prd":           "",
    }


# ─── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    """Health check — confirms the server is running."""
    return {"status": "ProjectSmith AI is running", "version": "1.0.0"}


@app.post("/chat")
def chat(req: ChatRequest):
    """
    Single conversational turn.
    Loads user LTM, runs chat_node, returns the AI response.
    """
    config = make_config(req.user_id, req.thread_id)
    try:
        result = graph.invoke(base_state(req.message), config=config)
        response = result["messages"][-1].content if result.get("messages") else ""
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/plan")
def plan(req: PlanRequest):
    """
    Full 4-node planning pipeline.

    The frontend passes the FULL conversation as req.message so every node
    (planner, cost, edge_case, doc) has complete context — not just 'plan it'.

    Returns plan, cost, edges, and prd in a single response.
    """
    config = make_config(req.user_id, req.thread_id)

    # use explicit conversation if provided, otherwise use message field
    context = req.conversation if req.conversation else req.message

    try:
        result = graph.invoke(base_state(context), config=config)
        return {
            "plan":  result.get("plan",  ""),
            "cost":  result.get("cost",  ""),
            "edges": result.get("edges", ""),
            "prd":   result.get("prd",   ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/plan/stream")
def plan_stream(req: PlanRequest):
    """
    Streaming version of the planning pipeline.
    Yields node updates as NDJSON (newline-delimited JSON).
    Each line: {"node": "planner", "data": {...}}
    """
    config  = make_config(req.user_id, req.thread_id)
    context = req.conversation if req.conversation else req.message

    def generate():
        for event in graph.stream(
            base_state(context),
            config=config,
            stream_mode="updates"
        ):
            for node, update in event.items():
                if node in ("planner", "cost", "edge_case", "doc"):
                    yield json.dumps({"node": node, "data": update}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")


@app.post("/memory/save")
def save_memory(req: SaveRequest):
    """
    Saves a session conversation to long-term memory.
    Called at session end (logout or new project).
    """
    try:
        msgs = [
            HumanMessage(content=m.content) if m.role == "user"
            else AIMessage(content=m.content)
            for m in req.messages
        ]
        summarize_and_save(msgs, req.user_id, "advisor")
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/{user_id}")
def get_memory(user_id: str):
    """Returns all stored long-term memory entries for the given user."""
    mems = list_memories(user_id)
    return {"memories": mems}