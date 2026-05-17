# Job Searcher

Small LangGraph-based agent for finding AI jobs in healthcare, summarizing the results, and saving a local report.

## Design

The project is intentionally simple and course-friendly:

- Job search tools fetch structured listings from job APIs
- Filtering tools keep results relevant to AI and healthcare
- An LLM summarizes the selected jobs into a readable report
- Report tools save the output locally
- Optional observability is planned with Opik

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
