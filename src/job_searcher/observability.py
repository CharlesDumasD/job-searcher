import os
from typing import Any

from job_searcher.config import Settings


def configure_observability(graph: Any, settings: Settings) -> Any:
    """Return the graph wrapped with Opik tracing when configured."""
    if settings.opik_api_key is None:
        return graph

    try:
        from opik.integrations.langchain import OpikTracer, track_langgraph
    except ImportError as error:
        raise RuntimeError("Opik is not installed. Run `uv sync --dev`.") from error

    os.environ["OPIK_API_KEY"] = settings.opik_api_key.get_secret_value()
    os.environ["OPIK_PROJECT_NAME"] = settings.opik_project_name
    if settings.opik_workspace:
        os.environ["OPIK_WORKSPACE"] = settings.opik_workspace

    opik_tracer = OpikTracer(
        project_name=settings.opik_project_name,
        tags=["job-searcher"],
        metadata={
            "app": "job-searcher",
            "model": settings.openai_model,
        },
    )
    return track_langgraph(graph, opik_tracer)
