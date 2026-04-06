# Multi-Agent Content Pipeline

A multi-agent AI system that takes a topic and produces a polished, publication-ready blog post. Built with LangGraph, FastAPI, and three different LLM providers working in a coordinated pipeline.

---

## How It Works

The pipeline runs 4 specialized agents in sequence, each with a distinct job:

```
START → Supervisor → Researcher → Supervisor → Outliner → Supervisor → Writer → Supervisor → Editor → Supervisor → END
                                                                                      ↑                    |
                                                                                      └────────────────────┘
                                                                                         (if rejected)
```

| Agent | Model | Job |
|-------|-------|-----|
| **Researcher** | Tavily Search | Searches the web for current information on the topic |
| **Outliner** | Groq (Llama 3.3-70b) | Transforms research into a structured article outline |
| **Writer** | Gemini 2.5 Flash Lite | Writes a full draft following the outline |
| **Editor** | Claude Haiku | Reviews the draft for accuracy, completeness, tone, and formatting |

The **Supervisor** is a Python routing function that reads shared state after each agent and decides who runs next. If the Editor rejects the draft, it sends the Writer a reason and loops back. After 3 rejections, the pipeline forces termination.

---

## Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — StateGraph orchestration and conditional routing
- **[FastAPI](https://fastapi.tiangolo.com/)** — REST API endpoint
- **[Tavily](https://tavily.com/)** — Web search for the Researcher agent
- **[LangChain Groq](https://python.langchain.com/docs/integrations/chat/groq)** — Outliner LLM
- **[LangChain Google GenAI](https://python.langchain.com/docs/integrations/chat/google_generative_ai)** — Writer LLM
- **[LangChain Anthropic](https://python.langchain.com/docs/integrations/chat/anthropic)** — Editor LLM
- **[LangSmith](https://smith.langchain.com/)** — Automatic tracing (zero code required)
- **Pydantic** — Structured output parsing for Editor decisions

---

## Project Structure

```
multi-agent-pipeline/
├── app/
│   ├── state.py        # PipelineState TypedDict — shared state across all agents
│   ├── researcher.py   # Researcher agent — Tavily web search
│   ├── outliner.py     # Outliner agent — ChatGroq
│   ├── writer.py       # Writer agent — ChatGoogleGenerativeAI
│   ├── editor.py       # Editor agent — ChatAnthropic + structured output
│   ├── supervisor.py   # Routing function — pure Python logic
│   ├── graph.py        # LangGraph StateGraph assembly and compilation
│   └── main.py         # FastAPI app — POST /generate-article
├── .env
├── .gitignore
└── requirements.txt
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/multi-agent-pipeline.git
cd multi-agent-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_anthropic_key
GROQ_API_KEY=your_groq_key
GOOGLE_API_KEY=your_google_key
TAVILY_API_KEY=your_tavily_key

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_PROJECT=multi-agent-pipeline
```

### 5. Run the server

```bash
cd app
uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000`

---

## API Usage

### `POST /generate-article`

Generates a complete blog post on the given topic.

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/generate-article \
  -H "Content-Type: application/json" \
  -d '{"topic": "Why AI is important in 2026"}'
```

**Request Body:**

```json
{
  "topic": "string"
}
```

**Response:**

```json
{
  "article": "# Why AI is Important in 2026\n\n..."
}
```

The response is a full Markdown-formatted article.

---

## Revision Loop

The Editor agent uses structured output (Pydantic) to return a strict `approved` or `rejected` decision. If rejected, it includes a `reason` explaining what needs fixing. The Writer reads this reason on the next pass and revises accordingly.

```
Editor rejects → reason stored in state → Writer reads reason → improved draft → Editor re-reviews
```

Maximum 3 revision attempts. After that, the pipeline terminates and returns the best available draft.

---

## LangSmith Tracing

Every agent call is automatically traced. No code changes needed — just set the environment variables. View full pipeline runs, per-agent timing, token usage, and LLM inputs/outputs at [smith.langchain.com](https://smith.langchain.com).

---

## Requirements

```
langgraph
langchain
langchain-anthropic
langchain-groq
langchain-google-genai
langchain-community
langchain-tavily
fastapi
uvicorn
python-dotenv
tavily-python
pydantic
```