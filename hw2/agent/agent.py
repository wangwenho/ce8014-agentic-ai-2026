import os
import re
from collections.abc import Callable
from dataclasses import dataclass
from textwrap import dedent

from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from tools.tools import TavilySearchTool

STEP_END_MARKER = "===STEP_END==="
MODEL_STOP = [f"\n{STEP_END_MARKER}"]

console = Console()


@dataclass
class ParsedStep:
    """
    Represents the parsed components of an agent's response step.
    """

    thought: str = ""
    action: str = ""
    action_input: str = ""
    final_answer: str = ""


def build_system_prompt() -> str:
    """
    Build the system prompt that instructs the agent how to respond.
    """
    return dedent(
        """
        You are a single general-purpose ReAct agent.
        Respond only in this strict format (no extra text, no Observation lines):
        Thought: <brief reasoning step>
        Action: Search
        Action Input: <search query>
        Final Answer: <only when you have enough evidence>

        - Do not output Observation; your code will add it.
        - End each response with the marker exactly: ===STEP_END===
        - If you need another tool call, do another Thought/Action/Action Input.
        - If you cannot find enough info in this step, do not output Final Answer.

        One-shot example:
        User: Who is the CEO of the startup 'Morphic' AI search?
        Thought: Search company and CEO.
        Action: Search
        Action Input: Morphic AI search CEO
        """
    ).strip()


class ReActAgent:
    """
    A ReAct agent that can execute tasks using a combination of reasoning and tool usage.
    """

    def __init__(
        self,
        system_prompt: str | None = None,
        model: str = "gpt-4o-mini",
        max_steps: int = 5,
        client: OpenAI | None = None,
        search_tool: TavilySearchTool | None = None,
    ) -> None:
        self.model = model
        self.max_steps = max_steps
        self.system_prompt = system_prompt or build_system_prompt()
        self.client = client or self._build_client()
        self.search_tool = search_tool or TavilySearchTool()
        self.messages: list[dict[str, str]] = []

    def _build_client(self) -> OpenAI:
        """
        Build the OpenAI client using the API key from environment variables.
        """
        api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
        return OpenAI(api_key=api_key)

    def construct_prompt(self, query: str) -> list[dict[str, str]]:
        """
        Construct the initial messages for the conversation with the user query.
        """
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query},
        ]
        return self.messages

    def execute(self, query: str, verbose: bool = True) -> str:
        """
        Execute the agent on the given user query, allowing it to reason and use tools iteratively.
        """
        self.construct_prompt(query)

        for step in range(self.max_steps):
            assistant_text = self._call_model(stop=MODEL_STOP)
            assistant_text = assistant_text.strip()
            self._append_assistant_text(assistant_text)

            parsed = self._parse_step(assistant_text)
            if parsed.final_answer:
                return parsed.final_answer.strip()

            if parsed.action:
                if verbose:
                    console.print(
                        Panel(
                            f"Thought: {parsed.thought or '...'}\nAction: {parsed.action}\nAction Input: {parsed.action_input}",
                            title="Agent Plan",
                            style="bold yellow",
                        )
                    )

                action_handler = self._get_action_handler(parsed.action)
                if action_handler is not None:
                    observation = action_handler(parsed.action_input)
                else:
                    observation = f"Unsupported action: {parsed.action}"

                observation_text = f"Observation: {observation}"
                self.messages.append({"role": "user", "content": observation_text})

                if verbose:
                    console.print(
                        Panel(observation_text, title="Observation", style="bold blue")
                    )
                continue

            if verbose:
                console.print(
                    Panel(
                        "Invalid agent response (missing Action/Final Answer)",
                        title="Agent Error",
                        style="bold red",
                    )
                )
            break

        fallback = self._synthesize_final_answer()
        if verbose:
            console.print(
                Panel(fallback.strip(), title="Fallback Answer", style="bold magenta")
            )
        return self._extract_final_answer(fallback) or fallback.strip()

    def _call_model(self, stop: list[str] | None = None) -> str:
        """
        Call the language model with the current conversation messages and return the assistant's response.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,  # type: ignore
            temperature=0,
            stop=stop,
        )
        message = response.choices[0].message.content or ""
        return self._normalize_model_output(message)

    def _normalize_model_output(self, text: str) -> str:
        """
        Normalize the output from the language model.
        """
        normalized = text.strip()
        if STEP_END_MARKER in normalized:
            normalized = normalized.replace(STEP_END_MARKER, "")
        return normalized.strip()

    def _get_action_handler(self, action: str) -> Callable[[str], str] | None:
        """
        Get the function that handles the given action name.
        """
        action_name = action.strip().lower()
        handlers: dict[str, Callable[[str], str]] = {
            "search": self.search_tool.search,
            "web search": self.search_tool.search,
            "tavily search": self.search_tool.search,
        }
        return handlers.get(action_name)

    def _append_assistant_text(self, text: str) -> None:
        """
        Append the assistant's response text to the conversation messages.
        """
        self.messages.append({"role": "assistant", "content": text})

    def _parse_step(self, text: str) -> ParsedStep:
        """
        Parse the assistant's response text to extract Thought, Action, Action Input, and Final Answer.
        """
        final_answer = self._extract_final_answer(text)
        if final_answer:
            return ParsedStep(final_answer=final_answer)

        thought = self._extract_line_value(text, "Thought")
        action = self._extract_line_value(text, "Action")
        action_input = self._extract_line_value(text, "Action Input")

        if action and action.lower() in {"final answer", "finish", "done"}:
            return ParsedStep(final_answer=action_input or text.strip())

        if not action and action_input and text.strip().lower().startswith("search"):
            action = "Search"

        return ParsedStep(thought=thought, action=action, action_input=action_input)

    def _extract_line_value(self, text: str, label: str) -> str:
        """
        Extract the value of a line that starts with a specific label (e.g., "Thought:", "Action:").
        """
        pattern = rf"^{re.escape(label)}:\s*(.+)$"
        match = re.search(pattern, text, flags=re.MULTILINE)
        if not match:
            return ""
        value = match.group(1).strip()
        return value.strip(" \"'")

    def _extract_final_answer(self, text: str) -> str:
        """
        Extract the Final Answer from the text if it exists.
        """
        match = re.search(
            r"^Final Answer:\s*(.+)$", text, flags=re.MULTILINE | re.DOTALL
        )
        if not match:
            return ""
        return match.group(1).strip()

    def _synthesize_final_answer(self) -> str:
        """
        Synthesize a final answer based on the conversation so far.
        """
        messages = self.messages + [
            {
                "role": "user",
                "content": "Provide the best concise Final Answer using only the evidence in the conversation so far.",
            }
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore
            temperature=0,
        )
        return response.choices[0].message.content or ""
