# Travel Planner LLM Multi-Agent

A Streamlit web application that uses multiple AI agents powered by Groq (DeepSeek R1) and Brave Search to generate detailed, personalized day-by-day travel itineraries.

## Features

- Multi-agent pipeline: research, flight search, hotel recommendations, and itinerary planning
- Brave Search MCP integration for real-time web data
- Upload existing plans (CSV, PDF, TXT) for the agents to refine
- Export itinerary as Text, Markdown, HTML, PDF, or PNG image
- Authentication via password (shared keys) or direct API key entry

## Architecture

```
User Input (Streamlit UI)
        │
        ▼
┌───────────────────┐
│   Research Agent  │  ← Brave Search MCP
├───────────────────┤
│   Flight Agent    │  ← Brave Search MCP (optional)
├───────────────────┤
│   Hotel Agent     │  ← Brave Search MCP (optional)
├───────────────────┤
│  Planning Agent   │  ← Brave Search MCP
└───────────────────┘
        │
        ▼
   Travel Itinerary (Markdown table)
```

All agents use the `groq/deepseek-r1-distill-llama-70b` model via [PraisonAI Agents](https://github.com/MervinPraison/PraisonAI).

## Prerequisites

- Python 3.10+
- [Node.js](https://nodejs.org/) (for the Brave Search MCP server via `npx`)
- A [Groq API key](https://console.groq.com/)
- A [Brave Search API key](https://brave.com/search/api/)

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
cp .env_example .env
```

Open `.env` and set the values:

```env
GROQ_API_KEY="gsk_..."        # Your Groq API key
BRAVE_API_KEY="BSA..."        # Your Brave Search API key
PASSWORD="your_password"      # Optional: shared password for the login page
```

`PASSWORD` is only needed if you want to use the "Use Password" login method. You can leave it empty and log in by entering API keys directly in the UI.

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
├── travel_agent.py   # Streamlit app — UI, agent definitions, export logic
├── prompt.py         # System prompt that controls itinerary output format
├── requirements.txt  # Python dependencies
├── .env_example      # Environment variable template
└── .gitignore
```

## Environment Variables Reference

| Variable        | Required | Description                                      |
|-----------------|----------|--------------------------------------------------|
| `GROQ_API_KEY`  | Yes      | API key for Groq inference                       |
| `BRAVE_API_KEY` | Yes      | API key for Brave Search (used by MCP server)    |
| `PASSWORD`      | No       | Shared login password for the "Use Password" flow |

## Troubleshooting

**`npx` not found** — Install Node.js from https://nodejs.org/ and make sure `npx` is on your `PATH`.

**`ModuleNotFoundError`** — Ensure your virtual environment is activated and `pip install -r requirements.txt` completed without errors.

**API key errors** — Double-check that `.env` contains valid, non-expired keys and that the file is in the project root.

**Slow generation** — The multi-agent pipeline makes multiple web searches; generation typically takes 30–90 seconds depending on query complexity and API latency.
