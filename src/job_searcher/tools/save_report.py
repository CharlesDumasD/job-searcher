import json
from datetime import UTC, datetime
from pathlib import Path

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from langgraph.types import Command

REPORTS_DIR = Path("reports")


@tool
def save_report(runtime: ToolRuntime, title: str | None = None) -> Command:
    """Save a Markdown job-search report locally.

    Use this after summarize_jobs to persist the final formatted report. The
    tool reads the latest summary from graph state, creates the reports
    directory if needed, and returns the saved file path.
    """
    summary = runtime.state.get("summary")
    if not summary:
        content = "No summary is available in state. Call summarize_jobs first."
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        content=content,
                        name="save_report",
                        tool_call_id=runtime.tool_call_id,
                    )
                ]
            }
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
    safe_title = _slugify(title or "job_report")
    path = REPORTS_DIR / f"{timestamp}_{safe_title}.md"
    path.write_text(summary, encoding="utf-8")

    result = {
        "path": str(path),
        "filename": path.name,
    }
    return Command(
        update={
            "report_path": str(path),
            "messages": [
                ToolMessage(
                    content=json.dumps(result),
                    name="save_report",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )


def _slugify(value: str) -> str:
    """Return a simple filename-safe slug."""
    slug = "".join(
        character.lower() if character.isalnum() else "_" for character in value.strip()
    )
    slug = "_".join(part for part in slug.split("_") if part)
    return slug[:60] or "job_report"
