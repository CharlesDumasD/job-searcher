import json

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from job_searcher.config import get_settings

SUMMARY_PROMPT = """
You summarize job listings for the user.

Write the summary in the user's language when possible. Keep the format stable
and use Markdown.

For each job, include:
- Title
- Company
- Location
- Contract or work time, if available
- Salary, or "Not specified"
- Posted date, if available
- URL
- Description
- Why it matches the user's request

Do not invent missing salary, contract, remote status, or job details. Use
"Not specified" when important information is missing.
""".strip()


@tool
def summarize_jobs(
    jobs: list[dict[str, object]],
    user_request: str,
) -> str:
    """Summarize selected jobs in a stable format for the user.

    Use this after search_jobs and optional filter_jobs when presenting job
    matches. Preserve factual fields from the job listings, always include
    salary when available, and do not invent missing job details.
    """
    settings = get_settings()
    model_args: dict[str, object] = {
        "model": settings.openai_model,
        "temperature": 0,
    }
    if settings.openai_api_key is not None:
        model_args["api_key"] = settings.openai_api_key.get_secret_value()

    model = ChatOpenAI(**model_args)
    response = model.invoke(
        [
            SystemMessage(content=SUMMARY_PROMPT),
            HumanMessage(
                content=(
                    f"User request:\n{user_request}\n\n"
                    f"Jobs JSON:\n{json.dumps(jobs, ensure_ascii=False)}"
                )
            ),
        ]
    )

    if isinstance(response.content, str):
        return response.content
    return str(response.content)
