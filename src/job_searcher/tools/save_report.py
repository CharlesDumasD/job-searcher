from datetime import UTC, datetime
from pathlib import Path

from langchain_core.tools import tool

REPORTS_DIR = Path("reports")


@tool
def save_report(content: str, title: str | None = None) -> dict[str, str]:
    """Save a Markdown job-search report locally.

    Use this after summarize_jobs to persist the final formatted report. Pass
    the full Markdown content from summarize_jobs. The tool creates the reports
    directory if needed and returns the saved file path.
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
    safe_title = _slugify(title or "job_report")
    path = REPORTS_DIR / f"{timestamp}_{safe_title}.md"
    path.write_text(content, encoding="utf-8")

    return {
        "path": str(path),
        "filename": path.name,
    }


def _slugify(value: str) -> str:
    """Return a simple filename-safe slug."""
    slug = "".join(
        character.lower() if character.isalnum() else "_" for character in value.strip()
    )
    slug = "_".join(part for part in slug.split("_") if part)
    return slug[:60] or "job_report"
