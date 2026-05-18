import argparse
import json

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, ToolMessage

from job_searcher.agent.graph import build_graph


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Job Searcher agent.")
    parser.add_argument(
        "request",
        nargs="*",
        help="Optional one-shot request. Omit it to start interactive mode.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print tool calls and tool results after each agent turn.",
    )
    return parser.parse_args()


def run_turn(graph, messages: list[AnyMessage], user_text: str) -> list[AnyMessage]:
    """Run one agent turn and return the updated conversation messages."""
    state = graph.invoke({"messages": [*messages, HumanMessage(content=user_text)]})
    return state["messages"]


def get_last_assistant_text(messages: list[AnyMessage]) -> str:
    """Return the latest assistant text response."""
    for message in reversed(messages):
        if isinstance(message, AIMessage) and message.content:
            if isinstance(message.content, str):
                return message.content
            return str(message.content)
    return "No assistant response was produced."


def get_display_text(messages: list[AnyMessage]) -> str:
    """Return the best user-facing text from the latest agent run."""
    summary = get_latest_tool_content(messages, "summarize_jobs")
    save_result = get_latest_tool_content(messages, "save_report")
    if summary is None:
        return get_last_assistant_text(messages)

    if save_result is None:
        return summary

    try:
        path = json.loads(save_result)["path"]
    except (KeyError, TypeError, json.JSONDecodeError):
        return summary

    return f"{summary}\n\nReport saved to `{path}`."


def get_latest_tool_content(messages: list[AnyMessage], name: str) -> str | None:
    """Return the latest content from a named tool message."""
    for message in reversed(messages):
        if isinstance(message, ToolMessage) and message.name == name:
            if isinstance(message.content, str):
                return message.content
            return str(message.content)
    return None


def print_debug_trace(previous_count: int, messages: list[AnyMessage]) -> None:
    """Print tool calls and results produced during the latest turn."""
    for message in messages[previous_count:]:
        if isinstance(message, AIMessage) and message.tool_calls:
            for tool_call in message.tool_calls:
                tool_args = json.dumps(tool_call["args"], indent=2)
                print(f"[tool call] {tool_call['name']}\n{tool_args}")
        elif isinstance(message, ToolMessage):
            print(f"[tool result] {message.name}")
            print(message.content)


def run_one_shot(user_text: str, debug: bool) -> None:
    """Run a single request and print the agent response."""
    graph = build_graph()
    messages = run_turn(graph, [], user_text)
    if debug:
        print_debug_trace(0, messages)
    print(get_display_text(messages))


def run_interactive(debug: bool) -> None:
    """Run an interactive in-memory conversation."""
    graph = build_graph()
    messages: list[AnyMessage] = []

    print("Job Searcher. Type 'exit' or 'quit' to stop.")
    while True:
        user_text = input("> ").strip()
        if user_text.lower() in {"exit", "quit"}:
            break
        if not user_text:
            continue

        previous_count = len(messages)
        messages = run_turn(graph, messages, user_text)
        if debug:
            print_debug_trace(previous_count, messages)
        print(get_display_text(messages))


def main() -> None:
    """Run the agent CLI."""
    args = parse_args()
    user_text = " ".join(args.request).strip()
    if user_text:
        run_one_shot(user_text, args.debug)
    else:
        run_interactive(args.debug)


if __name__ == "__main__":
    main()
