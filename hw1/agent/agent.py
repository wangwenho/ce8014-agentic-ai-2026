import json

from openai import OpenAI
from tools import available_functions, tools


class FinancialAgent:
    """
    A simple agent that can answer financial questions using provided tools.
    """

    def __init__(self, client: OpenAI):
        self.client = client
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful Financial Assistant. "
                    "You can provide stock prices and exchange rates. "
                    "Use the available tools to answer user queries accurately."
                ),
            }
        ]

    def _execute_tool_call(self, call) -> dict:
        """
        Execute a tool call and return the result as a message.
        """
        name = call.function.name
        args = json.loads(call.function.arguments)
        func = available_functions.get(name)

        if not func:
            result = json.dumps({"error": "Function not found"})
        else:
            try:
                result = func(**args)
            except Exception as e:
                result = json.dumps({"error": str(e)})

        return {
            "tool_call_id": call.id,
            "role": "tool",
            "name": name,
            "content": result,
        }

    def run_once(self, user_input: str) -> str:
        """
        Run one iteration of the agent loop with the given user input.
        """
        self.messages.append({"role": "user", "content": user_input})
        resp = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,  # type: ignore
            tools=tools,  # type: ignore
        )
        msg = resp.choices[0].message

        if msg.tool_calls:
            self.messages.append(msg)  # type: ignore
            for call in msg.tool_calls:
                tool_msg = self._execute_tool_call(call)
                self.messages.append(tool_msg)

            final = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,  # type: ignore
            )
            reply = final.choices[0].message.content
        else:
            reply = msg.content

        self.messages.append({"role": "assistant", "content": reply})  # type: ignore
        return reply  # type: ignore

    def interactive_loop(self):
        """
        Run an interactive loop with the user.
        """
        print("Welcome to Financial Assistant. type 'exit' to quit.")
        while True:
            txt = input("You: ").strip()
            if txt.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            if not txt:
                continue
            print("Agent:", self.run_once(txt))
