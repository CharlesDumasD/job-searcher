import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from job_searcher.config import get_settings

FILTER_PROMPT = """
You filter job listings based on the user's criteria.

Return only job indexes that clearly match the criteria. Prefer keeping a job
when evidence is plausible but incomplete. Do not reject jobs only because a
field like salary or remote status is missing, unless the user made that field
mandatory.
""".strip()


class FilterDecision(BaseModel):
    """Selected job indexes after semantic filtering."""

    selected_indexes: list[int] = Field(
        description="Zero-based indexes of jobs that match the criteria."
    )


@tool
def filter_jobs(
    jobs: list[dict[str, object]],
    criteria: str,
) -> list[dict[str, object]]:
    """Filter job listings semantically while preserving their original format."""
    settings = get_settings()
    model_args: dict[str, object] = {
        "model": settings.openai_model,
        "temperature": 0,
    }
    if settings.openai_api_key is not None:
        model_args["api_key"] = settings.openai_api_key.get_secret_value()

    model = ChatOpenAI(**model_args).with_structured_output(FilterDecision)
    decision = model.invoke(
        [
            SystemMessage(content=FILTER_PROMPT),
            HumanMessage(
                content=(
                    f"Criteria:\n{criteria}\n\n"
                    f"Jobs JSON:\n{json.dumps(jobs, ensure_ascii=False)}"
                )
            ),
        ]
    )

    return [
        jobs[index] for index in decision.selected_indexes if 0 <= index < len(jobs)
    ]
