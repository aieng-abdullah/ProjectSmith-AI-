# ProjectSmith AI — Multi-Agent Refactor Spec

**Pattern:** Supervisor + Parallel Fan-out  
**Scope:** Internals only — API and UI contracts unchanged  
**Effort:** ~2 days  

---

## The Problem With the Current System

It's a sequential pipeline, not a multi-agent system. Three things are broken:

- Planner → Cost → Edge run one after another. They're independent. There's no reason for this.
- One node crash kills everything. User gets nothing.
- You can't call any "agent" in isolation. It only works as one monolith.

---

## What Changes, What Doesn't

```
UNCHANGED                         CHANGES
─────────────────────────         ──────────────────────────────
src/api/main.py                   agents/graph.py → supervisor.py
src/chatbot/app.py                agents/node/* → agents/sub_agents/*
src/memory/                       agents/state.py gets SupervisorState added
src/llms/                         New: parallel fan-out via Send()
docker-compose / .env             New: each node becomes a compiled LangGraph
```

---

## Architecture

```
User Message
     │
     ▼
Supervisor Agent  ──── "validate" ──→ ChatAgent
     │
     │ "plan it"  (LangGraph Send — all 3 fire simultaneously)
     │
  ┌──┴──────────────────┐
  ▼          ▼          ▼
Planner    Cost      EdgeCase
Agent      Agent      Agent
  │          │          │
  └──────────┴──────────┘
             │
             ▼
          DocAgent  (waits for all 3, degrades if one failed)
             │
             ▼
        MemoryAgent
```

**Routing:** Deterministic for known commands (`plan it`, `new`, `memories`).
LLM fallback only for ambiguous messages. Unknown response defaults to `validate`.

**Failure policy:** Every sub-agent returns `SubAgentResult(success: bool)` — never raises.
DocAgent generates with whatever arrived. API never returns 500 on a sub-agent failure.

---

## New Files

```
src/agents/
├── supervisor_state.py           ← SupervisorState + SubAgentResult types
├── supervisor/
│   ├── supervisor.py             ← compiled supervisor graph
│   └── router.py                 ← intent classifier
└── sub_agents/
    ├── base.py                   ← BaseSubAgent with _safe_run()
    ├── planner_agent.py          ← wraps existing planner.py
    ├── cost_agent.py             ← wraps existing cost.py
    ├── edge_case_agent.py        ← wraps existing edge_case.py
    ├── doc_agent.py              ← wraps existing doc_node.py
    ├── chat_agent.py             ← wraps existing chat_node.py
    └── memory_agent.py           ← wraps existing memory ops
```

**Key constraint:** Sub-agents import and wrap existing `node/` logic.
Do not rewrite it. Medium refactor means new structure around existing code.

---

## Sub-Agent Contract

Every sub-agent must follow this interface. The supervisor depends on it.

```python
class SubAgentResult(TypedDict):
    agent_name: str
    output: str
    success: bool
    error: Optional[str]   # None if success=True

class BaseSubAgent:
    name: str

    def run(self, idea: str, context: str) -> SubAgentResult:
        raise NotImplementedError

    def _safe_run(self, idea, context) -> SubAgentResult:
        try:
            return self.run(idea, context)
        except Exception as e:
            return SubAgentResult(agent_name=self.name, output="", success=False, error=str(e))
```

---

## API Change — One Line

```python
# src/api/main.py

# Before
from agents.graph import graph

# After
from agents.supervisor.supervisor import supervisor as graph
```

Everything else in the API file stays the same.

---

## Build Order

Do these phases in sequence. Commit after each one.

| Phase | Files | Done When |
|-------|-------|-----------|
| 1 | `supervisor_state.py`, `sub_agents/base.py` | `_safe_run` catches exceptions, returns failure result |
| 2 | All 6 sub-agents in `sub_agents/` | Each runs standalone: `agent.run(idea, context)` returns `SubAgentResult` |
| 3 | `supervisor/router.py` | Unit test: every trigger word → correct intent |
| 4 | `supervisor/supervisor.py` | Invoke graph with "plan it" — all 3 results present in state |
| 5 | `api/main.py` one-line swap | `POST /plan` returns same JSON shape as before |
| 6 | Fault test | Force CostAgent to raise → partial PRD returned, no 500 |

---

## Tests

```
tests/
├── unit/            ← no LLM, runs in ms, run on every save
├── integration/     ← mocked LLM, run before every commit  
└── e2e/             ← real LLM, run manually before deploy only
```

**Must-have tests (write these first):**

```python
# 1. Core fault isolation guarantee
def test_safe_run_never_raises():
    agent = AgentThatAlwaysCrashes()
    result = agent._safe_run("idea", "context")
    assert result["success"] is False   # failure result, not exception

# 2. Parallel fan-out wiring
def test_all_three_agents_produce_results():
    # mock all agents, invoke supervisor with "plan it"
    assert result["planner_result"]["success"] is True
    assert result["cost_result"]["success"] is True
    assert result["edge_case_result"]["success"] is True

# 3. Graceful degradation
def test_cost_failure_still_produces_prd():
    # force CostAgent to fail
    assert result["doc_result"]["success"] is True  # PRD still generated
    assert result["cost_result"]["success"] is False  # failure recorded

# 4. API contract unchanged
def test_plan_endpoint_returns_same_shape():
    response = client.post("/plan", json=payload)
    assert response.status_code == 200
    assert all(k in response.json() for k in ["plan", "cost", "edge_cases", "prd"])

# 5. Router deterministic path
def test_plan_trigger_never_calls_llm():
    with patch("router.llm") as mock:
        classify_intent([HumanMessage("plan it")])
        mock.invoke.assert_not_called()
```

**Coverage target:** 80% on `agents/` — focus on `base.py` (100%) and `router.py` (95%).

---

## Production Readiness

**Before every deploy, run this:**

```bash
# 1. Tests pass
pytest tests/unit/ tests/integration/ --cov=src --cov-fail-under=80

# 2. Graph compiles
python -c "from agents.supervisor.supervisor import supervisor; print('OK')"

# 3. Env vars validated
python -c "from llms.config import validate_environment; print('OK')"

# 4. Docker builds and health check passes
docker-compose up -d && sleep 10 && curl -f http://localhost:8000/health

# 5. Smoke test
curl -X POST http://localhost:8000/plan \
  -d '{"user_id":"smoke","thread_id":"s1","message":"plan it"}'
# Expect: 200, all 4 fields non-empty

docker-compose down && git push origin main
```

**Add to `src/llms/config.py`:**
```python
# Fail loudly on startup if env vars missing — never start broken
REQUIRED = ["GROQ_API_KEY", "POSTGRES_URL", "SUPABASE_URL", "SUPABASE_KEY", "MODEL_NAME"]
missing = [v for v in REQUIRED if not os.getenv(v)]
if missing:
    sys.exit(f"[FATAL] Missing env vars: {missing}")
```

**Extend `/` to `/health` — check Supabase is reachable, return 503 if not.**

**Add to every sub-agent's `_safe_run`:**
```python
logger.info(f"[{self.name}] start")
# ... run ...
logger.info(f"[{self.name}] done in {ms}ms | success={result['success']}")
```

**Rollback:** Render dashboard → previous deploy → Rollback. 2 minutes.

---

## README — What to Update

Replace the current Architecture section with:

```
## Architecture

Supervisor + Parallel Fan-out pattern using LangGraph.

A Supervisor Agent classifies intent and routes to specialist sub-agents.
For planning, three agents run simultaneously via LangGraph's Send() API:

  PlannerAgent + CostAgent + EdgeCaseAgent → run in parallel
  DocAgent waits for all three → generates PRD

Each sub-agent is a compiled LangGraph, independently runnable and testable.
If one fails, the others complete and DocAgent degrades gracefully.
The API surface (/chat, /plan, /plan/stream) is unchanged.

Why parallel? Planner, Cost, and Edge Case are independent.
Sequential execution was 3× slower for no benefit.

Why fault isolation? One bad LLM response used to crash the entire pipeline.
Now every sub-agent wraps its output in SubAgentResult(success: bool).
```

Also add a **Testing** section showing how to run the three test suites,
and a **"What I'd change with more time"** section with 2–3 honest tradeoffs.
These two sections signal engineering maturity more than the code does.

---

## Done When

```
[ ] Planner, Cost, Edge run in parallel — verified by checking all 3 results in state
[ ] Force CostAgent to crash → partial PRD returned, no 500
[ ] Each sub-agent: agent.run(idea, context) works standalone
[ ] POST /plan returns same JSON shape as before refactor
[ ] pytest unit + integration — all green, coverage > 80%
[ ] E2E test run manually with real LLM — full plan generated
[ ] /health returns 200 on Render
[ ] Pre-deploy script passes all 5 steps
[ ] README architecture section updated
```