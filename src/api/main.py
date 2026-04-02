"""
FastAPI entry point — exposes chat, planning, streaming, and memory endpoints.
 Connects the LangGraph agent (graph), short-term config, and long-term memory (LTM).
"""



from fastapi import FastAPI , HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agents.graph import graph
from memory.ltm_manager import summarize_and_save, load_memories
from memory.ltm import init_ltm
from langchain_core.messages import HumanMessage
import uuid
import json


#defin tha app
app = FastAPI(title="ProjectSmith AI", version="1.0.0")



#initialize short tearm memory
init_ltm()

class ChatRequst(BaseModel):
    """Request body for /chat — basic conversational message from a user."""
    user_id: str
    thread_id:str
    message:str
    
    
class PlanRequest(BaseModel):
    """ Request body for /plan and /plan/stream — triggers the full planning pipeline"""
    user_id:   str
    thread_id: str
    message:   str
    
class SaveRequest(BaseModel):
    """Request body for /memory/save — persists a conversation to long-term memory."""
    user_id:   str
    message:   list
    
    
@app.get("/")
def root():
    """Health check endpoint — confirms the server is running."""
    return{"status": "ProjectSmith AI Is running"}


@app.post("/chat")
def chat(req:ChatRequst):
    """Loads user LTM, invokes the agent graph, and returns the last AI message."""
    ltm_context = load_memories(req.user_id,"advisor")
    config ={
        "configurable": {
            "thread_id": req.thread_id,
            "ltm_context": ltm_context
        }
    }
    human_msg= HumanMessage(content=req.message)
    try:
        result = graph.invoke(
            {
                "user_input":    req.message,
                "messages":      [human_msg],
                "ready_to_plan": False,
                "plan":          "",
                "cost":          "",
                "edges":         "",
                "prd":           "",
            },
            config=config,
        )
        response = result["messages"][-1].content if result.get("messages") else ""
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/plan")
def plan(req:PlanRequest):
    """Runs the full planning pipeline and returns plan, cost, edges, and PRD in one response."""
    ltm_context = load_memories(req.user_id, "advisor")
    config = {
        "configurable": {
            "thread_id": req.thread_id,
            "ltm_context": ltm_context
        }
    }
    human_msg = HumanMessage(content=req.message)
    try:
        result = graph.invoke(
            {
                "user_input":    req.message,
                "messages":      [human_msg],
                "ready_to_plan": False,
                "plan":          "",
                "cost":          "",
                "edges":         "",
                "prd":           "",
            },
            config=config,
        )
        return {
            "plan":  result.get("plan", ""),
            "cost":  result.get("cost", ""),
            "edges": result.get("edges", ""),
            "prd":   result.get("prd", ""),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@app.post("/plan/stream")
def plan_stream(req: PlanRequest):
    """Streams planning results node-by-node as NDJSON (newline-delimited JSON)."""

    ltm_context = load_memories(req.user_id, "advisor")
    config = {
        "configurable": {
            "thread_id": req.thread_id,
            "ltm_context": ltm_context
        }
    }
    human_msg = HumanMessage(content=req.message)

    def generate():
        """Generator that yields graph node updates as JSON lines."""
        for event in graph.stream(
            {
                "user_input":    req.message,
                "messages":      [human_msg],
                "ready_to_plan": False,
                "plan":          "",
                "cost":          "",
                "edges":         "",
                "prd":           "",
            },
            config=config,
            stream_mode="updates"
        ):
            for node, update in event.items():
                if node in ("planner", "cost", "edge_case", "doc"):
                    yield json.dumps({"node": node, "data": update}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")


@app.post("/memory/save")
def save_memory(req: SaveRequest):
    """Converts message dicts to LangChain objects, summarizes, and saves to user LTM."""
    try:
        from langchain_core.messages import HumanMessage, AIMessage
        msgs = [HumanMessage(content=m["content"]) if m["role"] == "user"
                else AIMessage(content=m["content"])
                for m in req.messages]
        summarize_and_save(msgs, req.user_id, "advisor")
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/memory/{user_id}")
def get_memory(user_id: str):
    """Returns all stored long-term memories for the given user."""
    from memory.ltm import list_memories
    mems = list_memories(user_id)
    return {"memories": mems}

    
    

    