# Travel Planner LLM Multi-Agent

A Streamlit web application that uses multiple AI agents to generate detailed, personalized day-by-day travel itineraries. Supports multiple LLM providers (Groq, Gemini, OpenRouter, OpenAI) and search backends (Firecrawl, Brave Search).

## Features

- **Multi-agent pipeline**: research, flight search, hotel recommendations, and itinerary planning
- **Configurable search provider**: Choose between Firecrawl or Brave Search via `SEARCH_PROVIDER` env var
- **Multi-provider LLM support**: Groq, Google Gemini, OpenRouter, or OpenAI — configure via `LLM_MODEL`
- **Upload existing plans** (CSV, PDF, TXT) for the agents to refine
- **Export itinerary** as Text, Markdown, HTML, PDF, or PNG image
- **Authentication**: Password-based or direct API key entry
- **Clean architecture**: Separated UI (Streamlit) and AI logic (agents)

## Architecture

```
User Input (Streamlit UI)
        │
        ▼
┌───────────────────┐
│   Research Agent  │  ← Search Provider (Firecrawl/Brave)
├───────────────────┤
│   Flight Agent    │  ← Search Provider (optional)
├───────────────────┤
│   Hotel Agent     │  ← Search Provider (optional)
├───────────────────┤
│  Planning Agent   │  ← Search Provider
└───────────────────┘
        │
        ▼
   Travel Itinerary
```

All agents use configurable LLM via [PraisonAI Agents](https://github.com/MervinPraison/PraisonAI) and [LiteLLM](https://github.com/BerriAI/litellm) for multi-provider support.

## Prerequisites

- Python 3.10+
- [Node.js](https://nodejs.org/) (for MCP servers via `npx`)
- At least one LLM API key:
  - [Groq](https://console.groq.com/) (default)
  - [Google Gemini](https://makersuite.google.com/app/apikey)
  - [OpenRouter](https://openrouter.ai/keys)
  - [OpenAI](https://platform.openai.com/api-keys)
- At least one search provider API key:
  - [Firecrawl](https://firecrawl.dev/app/api-keys) (recommended)
  - [Brave Search](https://brave.com/search/api/)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/dipeshpal/travel-planner-llm-multi-agent.git
cd travel-planner-llm-multi-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# Search Provider (firecrawl or brave)
SEARCH_PROVIDER="firecrawl"
FIRECRAWL_API_KEY="..."
BRAVE_API_KEY=""              # Optional if using Firecrawl

# LLM Configuration (groq, gemini, openrouter, or openai)
LLM_MODEL="groq/deepseek-r1-distill-llama-70b"
GROQ_API_KEY="gsk_..."
GOOGLE_API_KEY=""             # For gemini/* models
OPENROUTER_API_KEY=""         # For openrouter/* models
OPENAI_API_KEY=""             # For openai/* models

# Authentication
PASSWORD="your_password"      # Optional: for "Use Password" login
```

**Minimal setup**: You only need:
- One **search provider** API key (Firecrawl recommended)
- One **LLM API key** (Groq is free and fast)

See `.env.example` for all supported models and how to get API keys.

## Running the App

```bash
streamlit run travel_agent.py
```

The app will open at `http://localhost:8501` in your browser.

## Usage

1. **Log in** — use a shared password (requires `PASSWORD` set in `.env`) or enter your API keys directly.
2. **Fill in trip details** in the left sidebar:
   - Destination(s)
   - Travel dates
   - Budget
   - Preferences (e.g., cuisine, vibe, accessibility needs)
   - Toggle flight / hotel agent on or off
3. **Optionally upload** an existing plan (CSV, PDF, or TXT) to have the agents refine it.
4. Click **Generate Travel Plan** and wait for the agents to finish.
5. **Download** the resulting itinerary in your preferred format (Text, Markdown, HTML, PDF, or Image).

## Project Structure

```
travel-planner-llm-multi-agent/
├── travel_agent.py       # Streamlit UI, authentication, export logic
├── ai_agents.py          # AI agent definitions and initialization
├── prompt.py             # System prompt for itinerary format
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template (all options)
└── README.md
```

**Separation of concerns:**
- `travel_agent.py` — Streamlit UI and UX logic only
- `ai_agents.py` — AI/LLM agent logic; reusable for other frontends

## Environment Variables Reference

### Search Provider
| Variable              | Required | Description                                    |
|----------------------|----------|------------------------------------------------|
| `SEARCH_PROVIDER`    | No       | `firecrawl` (default) or `brave`               |
| `FIRECRAWL_API_KEY`  | if using Firecrawl | API key from https://firecrawl.dev       |
| `BRAVE_API_KEY`      | if using Brave     | API key from https://brave.com/search/api |

### LLM Model
| Variable           | Required | Description                                                 |
|--------------------|----------|-------------------------------------------------------------|
| `LLM_MODEL`        | No       | Format: `provider/model` (see `.env.example` for examples) |
| `GROQ_API_KEY`     | if using Groq      | API key from https://console.groq.com                |
| `GOOGLE_API_KEY`   | if using Gemini    | API key from https://makersuite.google.com/app/apikey |
| `OPENROUTER_API_KEY` | if using OpenRouter | API key from https://openrouter.ai/keys              |
| `OPENAI_API_KEY`   | if using OpenAI    | API key from https://platform.openai.com/api-keys    |

### Authentication
| Variable   | Required | Description                               |
|-----------|----------|-------------------------------------------|
| `PASSWORD` | No       | Shared password for "Use Password" login  |

## Troubleshooting

**`npx` not found** — Install Node.js from https://nodejs.org/ and make sure `npx` is on your `PATH`.

**`ModuleNotFoundError`** — Ensure your virtual environment is activated and `pip install -r requirements.txt` completed without errors.

**LLM authentication error** — Verify the correct API key is set for your chosen provider:
- For `groq/*` models: set `GROQ_API_KEY`
- For `gemini/*` models: set `GOOGLE_API_KEY`
- For `openrouter/*` models: set `OPENROUTER_API_KEY`
- For `openai/*` models: set `OPENAI_API_KEY`

**Search provider error** — Make sure `SEARCH_PROVIDER` is set to `firecrawl` or `brave`, and the corresponding API key is valid.

**Slow generation** — The multi-agent pipeline makes multiple web searches; generation typically takes 30–90 seconds depending on query complexity and API latency.

**Provider not found** — Check that the model format in `LLM_MODEL` is correct. See `.env.example` for supported formats and examples.
