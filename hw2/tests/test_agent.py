from typing import cast

from agent.agent import ParsedStep, ReActAgent
from openai import OpenAI
from tools.tools import TavilySearchTool


class DummyClient:
    """
    A dummy OpenAI client that returns predefined responses for testing.
    """

    class Chat:
        """
        A dummy chat interface that simulates OpenAI's chat completions.
        """

        def __init__(self, response_text):
            self.response_text = response_text

        class Completions:
            def __init__(self, response_text):
                self.response_text = response_text

            def create(self, **_kwargs):
                """
                Simulate the creation of a chat completion by returning a predefined response.
                """

                class Choice:
                    def __init__(self, text):
                        self.message = type("M", (), {"content": text})()

                return type(
                    "Resp",
                    (),
                    {"choices": [Choice(self.response_text)]},
                )()

        @property
        def completions(self):
            """ "
            Return the dummy completions interface.
            """
            return DummyClient.Chat.Completions(self.response_text)

    def __init__(self, response_text=""):
        object.__init__(self)
        self.chat = DummyClient.Chat(response_text)


class DummySearchTool(TavilySearchTool):
    """
    A dummy search tool that simulates the Tavily search API for testing.
    """

    def __init__(self):
        self.called = []

    def search(self, query):
        """
        Simulate a search by recording the query and returning a dummy result.
        """
        self.called.append(query)
        return f"Search result for: {query}"


def test_parse_step_final_answer():
    """
    Test that the _parse_step method correctly extracts the final answer from the model's response.
    """
    parser = ReActAgent(
        client=cast(OpenAI, DummyClient()), search_tool=DummySearchTool()
    )
    parsed = parser._parse_step("Final Answer: 42")

    assert isinstance(parsed, ParsedStep)
    assert parsed.final_answer == "42"
    assert parsed.action == ""
    assert parsed.action_input == ""


def test_parse_step_action_input():
    """
    Test that the _parse_step method correctly extracts the thought, action, and action input from the model's response.
    """
    parser = ReActAgent(
        client=cast(OpenAI, DummyClient()), search_tool=DummySearchTool()
    )
    parsed = parser._parse_step(
        "Thought: calc\nAction: Search\nAction Input: Japan population 2025"
    )

    assert parsed.thought == "calc"
    assert parsed.action == "Search"
    assert parsed.action_input == "Japan population 2025"
    assert parsed.final_answer == ""


def test_execute_search_path(monkeypatch):
    """
    Test that the execute method correctly processes a search action and returns the final answer.
    """
    search_tool = DummySearchTool()
    agent = ReActAgent(client=cast(OpenAI, DummyClient("")), search_tool=search_tool)

    responses = [
        "Thought: First query\nAction: Search\nAction Input: test query\n===STEP_END===",
        "Final Answer: All set\n===STEP_END===",
    ]

    def fake_call_model(self, stop=None):
        return responses.pop(0)

    monkeypatch.setattr(ReActAgent, "_call_model", fake_call_model)

    answer = agent.execute("What is this?", verbose=False)

    assert answer == "All set\n===STEP_END==="
    assert search_tool.called == ["test query"]
