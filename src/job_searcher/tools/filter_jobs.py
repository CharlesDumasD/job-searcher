import json

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolRuntime
from langgraph.types import Command
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
    runtime: ToolRuntime,
    criteria: str,
) -> Command:
    """Filter job listings using semantic criteria.

    Use this after search_jobs when the user asks for subjective or fuzzy
    filtering, such as healthcare relevance, AI/ML relevance, technical fit,
    seniority, remote fit, profile fit, or excluding jobs that are not actually
    relevant.

    Describe the filtering criteria in natural language. The tool reads the
    latest jobs from graph state and stores the filtered jobs back in state.
    """
    jobs = runtime.state.get("jobs", [])
    if jobs is None:
        jobs = []

    if not jobs:
        content = "No jobs are available in state. Call search_jobs first."
        return Command(
            update={
                "messages": [
                    ToolMessage(
                        content=content,
                        name="filter_jobs",
                        tool_call_id=runtime.tool_call_id,
                    )
                ]
            }
        )

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

    filtered_jobs = [
        jobs[index] for index in decision.selected_indexes if 0 <= index < len(jobs)
    ]
    content = json.dumps(filtered_jobs, ensure_ascii=False)
    return Command(
        update={
            "jobs": filtered_jobs,
            "messages": [
                ToolMessage(
                    content=content,
                    name="filter_jobs",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
