import argparse

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage

from job_searcher.agent.graph import build_graph


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run the Job Searcher agent.")
    parser.add_argument(
        "request",
        nargs="*",
        help="Optional one-shot request. Omit it to start interactive mode.",
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


def run_one_shot(user_text: str) -> None:
    """Run a single request and print the agent response."""
    graph = build_graph()
    messages = run_turn(graph, [], user_text)
    print(get_last_assistant_text(messages))


def run_interactive() -> None:
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

        messages = run_turn(graph, messages, user_text)
        print(get_last_assistant_text(messages))


def main() -> None:
    """Run the agent CLI."""
    args = parse_args()
    user_text = " ".join(args.request).strip()
    if user_text:
        run_one_shot(user_text)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
