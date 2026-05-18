# Job Searcher

Small LangGraph-based agent for finding AI jobs in healthcare, summarizing the results, and saving a local report.

## Design

The project is intentionally simple and course-friendly.

The agent is a LangGraph ReAct loop:

- The user sends a job-search request
- The LLM decides which tool to call
- Tool results are added to the conversation state
- The LLM either calls another tool or returns a final answer

Implemented tools:

- `search_jobs`: Searches Adzuna with API-native filters such as keywords,
  location, salary, contract type, recency, and result limit

Planned tools:

- `filter_jobs`: Applies semantic filters that are hard to express in the job
  API, such as healthcare relevance, AI/ML relevance, seniority, and profile fit
- `summarize_jobs`: Creates a concise report from selected listings
- `save_report`: Writes the report to a local markdown file
- `send_email`: Optionally sends the report by email

Current memory model:

- One-shot CLI runs keep memory only for that request
- Interactive CLI runs keep conversation state in memory until exit
- No persistent checkpointing yet

## Setup

Install dependencies with uv:

```bash
uv sync --dev
```

Install pre-commit hooks:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

Create a local environment file:

```bash
cp .env.example .env
```

Then fill in the required values in `.env`.

## Run

Run one request and exit:

```bash
uv run python -m job_searcher "Find remote AI healthcare jobs"
```

Start an interactive conversation:

```bash
uv run python -m job_searcher
```

Print tool calls and tool results:

```bash
uv run python -m job_searcher --debug "Find remote AI healthcare jobs"
```
