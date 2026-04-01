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
    user_id: str
    thread_id:str
    message:str
    
    
class PlanRequest(BaseModel):
    user_id:   str
    thread_id: str
    message:   str
    
class SaveRequest(BaseModel):
    user_id:   str
    message:   list
    
    
@app.get("/")
def root():
    return{"status": "ProjectSmith AI Is running"}


@app.post("/chat")
def chat(req:ChatRequst):
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
    ltm_context = load_memories(req.user_id, "advisor")
    config = {
        "configurable": {
            "thread_id": req.thread_id,
            "ltm_context": ltm_context
        }
    }
    human_msg = HumanMessage(content=req.message)

    def generate():
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
    from memory.ltm import list_memories
    mems = list_memories(user_id)
    return {"memories": mems}

    
    

    