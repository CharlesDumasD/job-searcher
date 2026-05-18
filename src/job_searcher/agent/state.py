from typing import Annotated, NotRequired, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State carried through a single agent run."""

    messages: Annotated[list[AnyMessage], add_messages]
    jobs: NotRequired[list[dict[str, object]]]
    summary: NotRequired[str]
    report_path: NotRequired[str]
