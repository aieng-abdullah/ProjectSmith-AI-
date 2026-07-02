# AGENTS.md — ProjectSmith AI

## Quick commands

```bash
# Run tests (always set PYTHONPATH)
PYTHONPATH=src python -m pytest tests/ -v

# Run only unit tests
PYTHONPATH=src python -m pytest tests/unit/ -v

# Run only integration tests
PYTHONPATH=src python -m pytest tests/integration/ -v

# Run locally without Docker (two terminals, from repo root)
cd src && uvicorn api.main:app --reload --port 8000
cd src && python -m streamlit run chatbot/app.py

# Docker (recommended)
docker-compose up --build
```

## Architecture — two LangGraph graphs

This repo has **two separate LangGraph state machines** with different state types:

| Graph | Entry point | State type | Used by |
|-------|-------------|------------|---------|
| Sequential | `src/agents/graph.py` | `AgentState` | CLI (`src/cli.py`) |
| Supervisor + parallel fan-out | `src/agents/supervisor/supervisor.py` | `SupervisorState` | API (`src/api/main.py`) |

**Do not confuse them.** Adding a field to `AgentState` won't affect the supervisor graph, and vice versa.

- **API path**: `api/main.py` → `supervisor.py` → parallel `PlannerAgent`, `CostAgent`, `EdgeCaseAgent` → `DocAgent`
- **CLI path**: `cli.py` → `graph.py` → sequential `chat_node` → `planner_node` → `cost_node` → `edge_case_node` → `doc_node`
- The sequential graph router (`src/agents/node/router.py`) requires `MIN_MESSAGES >= 4` before allowing plan trigger.

## PYTHONPATH is mandatory

All imports assume `src/` as the root. Every test run and the CI pipeline must set `PYTHONPATH=src`. Without it, imports like `from agents.graph import graph` will fail.

## Two state TypedDicts

- `AgentState` (`src/agents/state.py`): has `ready_to_plan`, `plan`, `cost`, `edges`, `prd`
- `SupervisorState` (`src/agents/supervisor_state.py`): has `idea`, `context`, `intent`, `planner_result`, `cost_result`, etc.

`SubAgentResult` is defined in `supervisor_state.py` — used by all sub-agents.

## Sub-agents and fault tolerance

Every sub-agent inherits from `BaseSubAgent` (`src/agents/sub_agents/base.py`) and wraps output in `SubAgentResult(success: bool)`. The `_safe_run` method catches all exceptions. If one parallel agent fails, `DocAgent` still generates a PRD from whatever arrived. The API never returns 500 on sub-agent failure.

## Plan trigger

Known triggers: `plan it`, `plan this`, `build it`, `let's plan`, `lets plan`, `go`, `start planning`.

Deterministic routing skips the LLM for these exact phrases. Unknown messages fall back to LLM classification, defaulting to `validate` (chat mode).

## Memory system

- **STM** (`src/memory/stm.py`): In-memory `MemorySaver` — lost on restart. Not persisted.
- **LTM** (`src/memory/ltm.py`): Supabase PostgreSQL. Gracefully degrades if `SUPABASE_URL`/`SUPABASE_KEY` are missing — no crash, just empty memories.
- `init_ltm()` must be called at startup (both API and CLI do this).

## Environment variables

Required (from `.env` or environment):
- `GROQ_API_KEY` — Groq API for LLM
- `POSTGRES_URL` — local Postgres for STM (Docker Compose provides this)
- `SUPABASE_URL`, `SUPABASE_KEY` — for LTM (optional for local dev)

Optional with defaults:
- `MODEL_NAME` → `openai/gpt-oss-120b`
- `TEMPERATURE` → `0.7`
- `FAST_API` → `http://localhost:8000`

## Testing notes

- **Unit tests**: Mocked LLM, no DB or network calls. Fast.
- **Integration tests**: Mocked LLM, real graph execution. Tests API contracts.
- **No e2e test directory exists** despite what the README claims. E2E tests require real LLM + real Supabase.
- CI (`.github/workflows/ci.yml`) runs with `PYTHONPATH: src` and a Postgres service container.
- Coverage target: 80% across `agents/` module.
- The `conftest.py` adds `src/` to `sys.path` as a fallback, but `PYTHONPATH=src` is the correct approach.

## Dead code

`src/core/workflow.py` and `src/core/utils.py` are empty files. `src/core/__init__.py` exists but nothing uses this package.

## Docker details

- `Dockerfile` — Streamlit frontend, exposes port 7860 (but docker-compose maps 8501)
- `Dockerfile.api` — FastAPI backend, respects `$PORT` env var, defaults to 8000
- Docker Compose runs three services: `postgres`, `backend`, `frontend`
- The API has a keep-alive ping to prevent Render free-tier sleeping

## CI / PR conventions

- CI triggers on push/PR to `main` or `develop`
- Conventional commits: `feat:`, `fix:`, etc.
- No linting, formatting, or type-checking tools are configured in this repo.
