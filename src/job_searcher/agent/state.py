from typing import Any, TypedDict


class AgentState(TypedDict):
    """State carried through a single agent run."""

    messages: list[Any]
