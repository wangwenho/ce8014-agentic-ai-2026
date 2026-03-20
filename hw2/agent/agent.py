from __future__ import annotations

import os
import re
from dataclasses import dataclass
from textwrap import dedent

from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from tools.tools import TavilySearchTool

console = Console()


@dataclass
class ParsedStep:
    thought: str = ""
    action: str = ""
    action_input: str = ""
    final_answer: str = ""


def build_system_prompt() -> str:
    return dedent(
        """
        You are a single general-purpose ReAct agent.

        Follow this format exactly:
        Thought: explain the next reasoning step briefly.
        Action: Search
        Action Input: the search query when using Search
        Final Answer: the final response when you have enough evidence

        Use Search when you need current information. Use Final Answer only when you have enough evidence.
        If a search fails or returns weak evidence, reflect on the failure, broaden or reframe the query, and search again.
        Never invent observations.
        Keep the reasoning concise but visible so the console trace can be inspected.

        One-shot example:
        User: Who is the CEO of the startup 'Morphic' AI search?
        Thought: I should first search the company name and CEO together.
        Action: Search
        Action Input: Morphic AI search CEO
        Observation: No exact results found.
        Thought: The first query was too specific. I should broaden it and look for an about page or founder reference.
        Action: Search
        Action Input: Morphic AI search founder CEO about page
        Observation: Search results indicate the startup's leadership page and identify the CEO.
        Thought: I have enough evidence now.
        Final Answer: The CEO is identified from the leadership page.
        """
    ).strip()


class ReActAgent:
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
        api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
        return OpenAI(api_key=api_key)

    def construct_prompt(self, query: str) -> list[dict[str, str]]:
        self.messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query},
        ]
        return self.messages

    def execute(self, query: str, verbose: bool = True) -> str:
        self.construct_prompt(query)

        for _ in range(self.max_steps):
            assistant_text = self._call_model(stop=["\nObservation:", "\nUser:"])
            self._append_assistant_text(assistant_text)

            parsed = self._parse_step(assistant_text)
            if parsed.final_answer:
                if verbose:
                    console.print(
                        Panel(
                            parsed.final_answer.strip(),
                            title="Final Answer",
                            style="bold magenta",
                        )
                    )
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
                if parsed.action.lower() in {"search", "web search", "tavily search"}:
                    observation = self.search_tool.search(parsed.action_input)
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
                print(assistant_text.strip())
            return assistant_text.strip()

        fallback = self._synthesize_final_answer()
        if verbose:
            print(fallback.strip())
        return self._extract_final_answer(fallback) or fallback.strip()

    def _call_model(self, stop: list[str] | None = None) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,  # type: ignore
            temperature=0,
            stop=stop,
        )
        message = response.choices[0].message.content or ""
        return message

    def _append_assistant_text(self, text: str) -> None:
        self.messages.append({"role": "assistant", "content": text})

    def _parse_step(self, text: str) -> ParsedStep:
        final_answer = self._extract_final_answer(text)
        if final_answer:
            return ParsedStep(final_answer=final_answer)

        action = self._extract_line_value(text, "Action")
        action_input = self._extract_line_value(text, "Action Input")

        if action.lower() in {"final answer", "finish", "done"}:
            return ParsedStep(final_answer=action_input or text.strip())

        if not action and action_input and text.strip().lower().startswith("search"):
            action = "Search"

        return ParsedStep(action=action, action_input=action_input)

    def _extract_line_value(self, text: str, label: str) -> str:
        pattern = rf"^{re.escape(label)}:\s*(.+)$"
        match = re.search(pattern, text, flags=re.MULTILINE)
        if not match:
            return ""
        value = match.group(1).strip()
        return value.strip(" \"'")

    def _extract_final_answer(self, text: str) -> str:
        match = re.search(
            r"^Final Answer:\s*(.+)$", text, flags=re.MULTILINE | re.DOTALL
        )
        if not match:
            return ""
        return match.group(1).strip()

    def _synthesize_final_answer(self) -> str:
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


Agent = ReActAgent
