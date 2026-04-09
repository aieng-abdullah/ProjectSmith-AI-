<div align="center">
<img width="300" height="300" alt="chip" src="https://github.com/user-attachments/assets/0fc2082d-f9ed-48d0-931d-d51046a1450b" />



# ProjectSmith AI

**An intelligent startup advisor agent that helps non-technical founders validate, plan, and de-risk their project ideas through deep conversational AI.**

<br/>

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-2E8B57?style=flat-square&logo=chainlink&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Memory-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat-square&logo=lightning&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

</div>

---

## 🚀 Live Demo

> **Try it now:** [your-live-link-here.com](https://your-live-link-here.com --- coming sooon...)

---

## What It Does

ProjectSmith AI is not a chatbot that answers questions. It is an agent that thinks like a senior advisor — it challenges your assumptions, stress-tests your idea, then generates a structured project plan, cost breakdown, edge case analysis, and a downloadable PRD document.

### Example Session

```
You:           I want to build an AI-powered MCQ exam system for students

ProjectSmith:  Who is your first customer and why would a student or educator
               pay you before anyone else does?

You:           My app will be cheap and local-friendly

ProjectSmith:  Being cheap is not a sustainable differentiator in a crowded
               market. Educators already use Moodle, Canvas, Google Forms, and
               Quizlet. What unique advantage makes them switch?

You:           plan it
```

---

### 📋 Plan Output

```
Specific Idea:   AI-powered MCQ exam system for students
Problem:         Educators need a smarter way to create, administer, and grade exams
Target User:     Educators and students
Constraint:      Existing tools handle grading and distribution reliably — a unique
                 advantage like adaptive testing or anti-cheating is required

Phase 1 — Build this first:
  Build a basic web-based MCQ system using Vercel and Supabase.
  Educators create and store questions. No AI yet — just prove the core loop works
  and gather real user feedback.

Phase 2 — Add this next:
  Integrate AI-powered question analysis and adaptive testing.
  Surface weak areas for students, recommend questions for educators.
  Add Stripe for payments and SendGrid for notifications.

First steps this week:
  1. Create a Carrd landing page to define the concept and collect early sign-ups
  2. Sign up for Supabase and explore its schema for storing exam data
  3. Research existing adaptive testing tools to understand integration patterns
```

---

### ⚠️ Edge Cases Output

```
Risk 1 — AI Dependence:
  The model may fail on poorly constructed questions, producing inaccurate results.
  Fix: Add a human review step for AI-generated questions before they go live.

Risk 2 — Integration Challenges:
  Connecting to existing LMS platforms like Moodle or Canvas may take longer
  and cost more than expected.
  Fix: Define clear public APIs and write integration docs from day one.

Risk 3 — Data Security:
  Student data exposure breaks trust immediately and may violate regulations.
  Fix: Implement encryption at rest and in transit. Publish a clear data policy
  before onboarding any institution.
```

---

### 💰 Cost & Stack Output

```
Free to start:
  • Google Forms          — prototype exam creation and distribution
  • Supabase free tier    — 500 MB database storage
  • Vercel hobby plan     — hosting with custom domain

What you'll pay later:
  • Supabase              — $25/month when storage exceeds 500 MB
  • Cloudinary            — $0.25/GB/month for image storage above 100 GB
  • Stripe                — 2.9% + $0.30 per transaction when payments go live
  • Vercel Pro            — $20/month when traffic or team size grows

How to stay free longest:
  Keep image uploads small. Delay payment processing until the product is
  stable and revenue model is validated.
```

---

### 📄 Project Brief Output

```
What you're building:
  An AI-powered MCQ exam system for educators and students who need smarter exam
  creation, adaptive feedback, and anti-cheating capabilities that existing tools
  like Google Forms and Quizlet do not provide.

Build it in this order:
  Start with a no-AI MVP to validate that educators will actually use it.
  Once real users are on the platform, layer in adaptive testing and AI grading
  to differentiate from the free alternatives.

Keep costs low:
  Begin with free tiers across the stack. Trigger paid upgrades only when a
  real usage threshold — such as 1,000 registered users — is crossed.

Watch out for:
  AI dependence is the single biggest risk. If the model fails on edge-case
  questions, trust erodes fast. Implement a human review process before any
  AI output reaches students.

You've got this:
  A clear focus on AI-powered insights and adaptive testing gives you a real
  differentiator in a market that is still running on paper and Google Forms.

⚠️ AI disclaimer: This brief was generated by ProjectSmith AI and should be
reviewed by a qualified business advisor, lawyer, or accountant before you
act on it.
```

---

## Key Features

- **Conversational idea validation** — challenges assumptions and pushes for specifics before any planning begins
- **4-node planning pipeline** — planner, cost advisor, edge case finder, and PRD generator run sequentially via LangGraph
- **Live web search** — cost node fetches real-time pricing data via DuckDuckGo before generating recommendations
- **Dual memory system** — STM (PostgreSQL checkpointer per session) and LTM (cross-session summaries per user)
- **Conditional routing** — `router_node` sequences nodes based on what is missing in state, detects plan triggers automatically
- **FastAPI backend** — REST endpoints with streaming NDJSON support
- **Streamlit UI** — node-level streaming updates, each section appears as soon as its node completes
- **PDF and Markdown export** — downloadable project brief with AI disclaimer footer

---

## Architecture

```
┌─────────────────────────────────────────┐
│           Streamlit UI  :8501            │
└────────────────────┬────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────┐
│           FastAPI Server  :8000          │
│  POST /chat | POST /plan | /plan/stream  │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│            LangGraph Agent               │
│                                          │
│  START --> router_node                   │
│                |                         │
│          chat_node  (conversation)       │
│                |  (on "plan it")         │
│    planner --> cost --> edge --> doc     │
│                |                         │
│               END                        │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│          Dual Memory System              │
│  STM  PostgreSQL Checkpointer            │
│  LTM  PostgreSQL Table                   │
└────────────────────┬────────────────────┘
                     │
┌────────────────────▼────────────────────┐
│      Groq LLM  openai/gpt-oss-120b       │
└─────────────────────────────────────────┘
```

---

## Planning Pipeline

When the user types `plan it`, the agent triggers a sequential 4-node pipeline. Each node reads from state, writes its output back, and passes context forward.

| Step | Node | Output |
|------|------|--------|
| 01 | `planner_node` | Phases, milestones, and 3 concrete first steps |
| 02 | `cost_node` | Free tools + future costs grounded in live web data |
| 03 | `edge_case_node` | 3 critical risks specific to this project with fixes |
| 04 | `doc_node` | One-page PRD exportable as PDF or Markdown |

---

## Prerequisites

- Python 3.10+
- Docker and Docker Compose
- Groq API key — free at [console.groq.com](https://console.groq.com)
- PostgreSQL 15+ (handled automatically via Docker)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aieng-abdullah/ProjectSmith-AI-
cd ProjectSmith-AI-
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/projectsmith
MODEL_NAME=openai/gpt-oss-120b
TEMPERATURE=0.7
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Run with Docker (recommended)

```bash
docker-compose up --build
```

| Service | URL |
|---------|-----|
| Streamlit UI | http://localhost:8501 |
| FastAPI | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

### Run locally without Docker

```bash
# Terminal 1 — FastAPI backend
cd src
uvicorn api.main:app --reload --port 8000

# Terminal 2 — Streamlit UI
cd src
python -m streamlit run chatbot/app.py
```

### Run CLI for testing

```bash
cd src
python main.py
```

### CLI commands

| Command | Action |
|---------|--------|
| `plan it` | Triggers the full 4-node planning pipeline |
| `new` | Saves session to LTM and starts fresh |
| `resume <id>` | Resumes a past session by thread ID |
| `memories` | Lists past project summaries from LTM |
| `clearmemory` | Wipes all LTM for current user |
| `quit` | Saves session and exits |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/chat` | Single conversational turn with LTM context |
| POST | `/plan` | Full 4-node planning pipeline |
| POST | `/plan/stream` | Streaming NDJSON — node updates as they complete |
| POST | `/memory/save` | Save session messages to LTM |
| GET | `/memory/{user_id}` | Retrieve past project summaries |

### Example — chat request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "austin",
    "thread_id": "abc-123",
    "message": "I want to build an app where farmers sell directly to customers"
  }'
```

### Example — plan request

```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "austin",
    "thread_id": "abc-123",
    "message": "plan it"
  }'
```

---

## Project Structure

```
src/
├── main.py                    # CLI entry point
├── api/
│   └── main.py                # FastAPI server
├── agents/
│   ├── graph.py               # LangGraph state machine
│   ├── state.py               # AgentState TypedDict
│   └── node/
│       ├── router.py          # Conditional routing logic
│       ├── chat_node.py       # Conversational advisor node
│       ├── planner.py         # Phase and milestone planner
│       ├── cost.py            # Budget and stack advisor
│       ├── edge_case.py       # Risk analysis node
│       └── doc_node.py        # PRD generator node
├── agents/tools/
│   └── web_search.py          # DuckDuckGo search tool
├── chatbot/
│   └── app.py                 # Streamlit web UI
├── llms/
│   ├── config.py              # Settings from .env
│   ├── model.py               # LLMService wrapper
│   └── prompts.py             # 6 specialized prompt templates
└── memory/
    ├── stm.py                 # PostgreSQL STM checkpointer
    ├── stm_manager.py         # Message trimming (500 tokens)
    ├── ltm.py                 # LTM table schema and CRUD
    └── ltm_manager.py         # Summarize, extract, load memories
```

---

## Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,postgres,docker" />

</div>

<br/>

| Layer | Technology |
|-------|------------|
| LLM | Groq via LangChain |
| Agent framework | LangGraph |
| API | FastAPI + Uvicorn |
| Web UI | Streamlit |
| Short-term memory | LangGraph PostgreSQL Checkpointer |
| Long-term memory | PostgreSQL via psycopg |
| Web search | DuckDuckGo (ddgs) |
| PDF export | fpdf2 |
| Containerization | Docker + Docker Compose |

---

## Contributing

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes using conventional commits

```bash
git commit -m "feat: add your feature description"
```

4. Push to your fork and open a pull request

```bash
git push origin feature/your-feature-name
```

Please keep pull requests focused on a single change and include a clear description of what was changed and why.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  <sub>Built by Abdullah — AI Engineering Portfolio Project</sub>
</div>
