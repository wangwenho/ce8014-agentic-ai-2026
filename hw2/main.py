import argparse

from agent.agent import ReActAgent, build_system_prompt
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

console = Console()

DEMO_QUESTIONS = [
    "What fraction of Japan's population is Taiwan's population as of 2025?",
    "Compare the main display specs of iPhone 15 and Samsung S24.",
    "Who is the CEO of the startup 'Morphic' AI search?",
]


def build_agent() -> ReActAgent:
    return ReActAgent(
        system_prompt=build_system_prompt(),
        model="gpt-4o-mini",
        max_steps=5,
    )


def run_demo(
    agent: ReActAgent,
    verbose: bool = False,
) -> None:
    """
    Run the demo tasks with the given agent.
    """
    for index, question in enumerate(DEMO_QUESTIONS, start=1):
        console.rule(f"Task {index}", style="bold blue")
        console.print(Panel(question, title="User", style="bold green"))
        answer = agent.execute(question, verbose=verbose)
        console.print(Panel(answer, title="Final Answer", style="bold magenta"))


def run_interactive(
    agent: ReActAgent,
    verbose: bool = False,
) -> None:
    """
    Run the interactive mode with the given agent.
    """
    console.print("ReAct Agent ready. Type 'exit' to quit.", style="bold green")
    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            console.print("Goodbye!", style="bold yellow")
            return
        answer = agent.execute(question, verbose=verbose)
        console.print(Panel(answer, title="Final Answer", style="bold magenta"))


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run the HW2 ReAct agent.")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the three assignment benchmark tasks.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed agent reasoning steps and tool calls.",
    )
    args = parser.parse_args()

    agent = build_agent()
    if args.demo:
        run_demo(agent, verbose=args.verbose)
    else:
        run_interactive(agent, verbose=args.verbose)


if __name__ == "__main__":
    main()
