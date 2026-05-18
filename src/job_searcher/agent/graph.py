from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from job_searcher.agent.prompts import SYSTEM_PROMPT
from job_searcher.agent.state import AgentState
from job_searcher.config import Settings, get_settings
from job_searcher.tools.filter_jobs import filter_jobs
from job_searcher.tools.search_jobs import search_jobs
from job_searcher.tools.summarize_jobs import summarize_jobs

TOOLS = [search_jobs, filter_jobs, summarize_jobs]


def build_graph(settings: Settings | None = None):
    """Build and compile the job-search agent graph."""
    settings = settings or get_settings()
    model_args: dict[str, object] = {
        "model": settings.openai_model,
        "temperature": 0,
    }
    if settings.openai_api_key is not None:
        model_args["api_key"] = settings.openai_api_key.get_secret_value()

    model = ChatOpenAI(**model_args).bind_tools(TOOLS)

    def call_model(state: AgentState) -> dict[str, object]:
        """Call the chat model with the system prompt and conversation state."""
        messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
        response = model.invoke(messages)
        return {"messages": [response]}

    graph = StateGraph(AgentState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")

    return graph.compile()
