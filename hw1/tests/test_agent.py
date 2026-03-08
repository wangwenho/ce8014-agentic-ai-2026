import json

from hw1.agent import FinancialAgent


class DummyToolCall:
    def __init__(self, id, name, arguments):
        self.id = id
        self.function = type(
            "F", (), {"name": name, "arguments": json.dumps(arguments)}
        )


class DummyMessage:
    def __init__(self, content="", tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []


class DummyChoice:
    def __init__(self, message):
        self.message = message


class DummyResponse:
    def __init__(self, message):
        self.choices = [DummyChoice(message)]


class SequenceClient:
    """
    client.chat.completions.create returns successive responses
    from a pre‑built list.
    """

    def __init__(self, responses):
        self._responses = responses.copy()

        class Completer:
            def __init__(self, responses):
                self._responses = responses

            def create(self, model, messages, tools=None):
                return self._responses.pop(0)

        self.chat = type("Chat", (), {"completions": Completer(self._responses)})()


def test_run_once_no_tool():
    # 模擬模型回覆 plain text
    resp = DummyResponse(DummyMessage(content="Hello there"))
    client = SequenceClient([resp])
    agent = FinancialAgent(client)  # type: ignore

    reply = agent.run_once("Hi")
    assert reply == "Hello there"
    assert agent.messages[-1]["content"] == "Hello there"


def test_run_once_with_tool():
    # 模擬第一回合返回一個工具呼叫，
    # 第二回合返回最終回答
    tc = DummyToolCall("1", "get_stock_price", {"symbol": "AAPL"})
    resp1 = DummyResponse(DummyMessage(tool_calls=[tc]))
    resp2 = DummyResponse(DummyMessage(content="The price is 260.00"))
    client = SequenceClient([resp1, resp2])
    agent = FinancialAgent(client)  # type: ignore

    reply = agent.run_once("price?")
    assert "260.00" in reply

    # 檢查工具訊息已插入 history
    tool_msgs = [m for m in agent.messages if m.get("role") == "tool"]
    assert len(tool_msgs) == 1
    assert '"symbol": "AAPL"' in tool_msgs[0]["content"]


def test_parallel_calls():
    # 模擬兩個工具同時被呼叫
    tc1 = DummyToolCall("1", "get_stock_price", {"symbol": "AAPL"})
    tc2 = DummyToolCall("2", "get_exchange_rate", {"currency_pair": "EUR_USD"})
    resp1 = DummyResponse(DummyMessage(tool_calls=[tc1, tc2]))
    resp2 = DummyResponse(DummyMessage(content="both done"))
    client = SequenceClient([resp1, resp2])
    agent = FinancialAgent(client)  # type: ignore

    reply = agent.run_once("check both")
    assert reply == "both done"

    tool_msgs = [m for m in agent.messages if m.get("role") == "tool"]
    assert len(tool_msgs) == 2
    # 第一個來自 get_stock_price
    assert "AAPL" in tool_msgs[0]["content"]
    # 第二個來自 get_exchange_rate
    assert "EUR_USD" in tool_msgs[1]["content"]
