import json
import os

from dotenv import load_dotenv
from openai import OpenAI

# 1. Setup & Security
# Make sure you have a .env file with OPENAI_API_KEY=sk-...
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 2. Mock Functions (Reference for your Financial Functions)
def get_current_time(location):
    """Mock function to get time."""
    print(f"[Mock] Getting time for {location}...")
    # In your assignment, you will look up Stock/Rate data here
    if "Taipei" in location:
        return json.dumps({"location": "Taipei", "time": "14:00"})
    elif "New York" in location:
        return json.dumps({"location": "New York", "time": "02:00"})
    else:
        return json.dumps({"location": location, "time": "Unknown"})


def calculate_sum(a, b):
    """Mock function to add numbers."""
    print(f"[Mock] Calculating {a} + {b}...")
    return json.dumps({"result": a + b})


# 3. Function Map (CRITICAL: Use this pattern)
# This allows dynamic execution without if-else chains
available_functions = {
    "get_current_time": get_current_time,
    "calculate_sum": calculate_sum,
}

# 4. Tool Schemas
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get current time in a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"}
                },
                "required": ["location"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]


def run_agent():
    # 5. System Prompt (Persona)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful Assistant can tell time and do calculation. Use tools when needed.",
        }
    ]

    print("Agent Started. Type 'exit' to quit.")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        messages.append({"role": "user", "content": user_input})

        # First API Call
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=tools, tool_choice="auto"
        )

        response_msg = response.choices[0].message
        tool_calls = response_msg.tool_calls

        if tool_calls:
            # IMPORTANT: Add the assistant's "thought" (tool call request) to history
            messages.append(response_msg)

            # 6. Handle Parallel Tool Calls
            # The model might call multiple tools in one go (e.g. "Time in Taipei and NY")
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Dynamic Dispatch using Function Map
                function_to_call = available_functions.get(function_name)

                if function_to_call:
                    try:
                        tool_result = function_to_call(**function_args)
                    except Exception as e:
                        tool_result = json.dumps({"error": str(e)})
                else:
                    tool_result = json.dumps({"error": "Function not found"})

                # Append RESULT to history
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result,
                    }
                )

            # Second API Call (Get final answer)
            final_response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages
            )
            final_content = final_response.choices[0].message.content
            print(f"Agent: {final_content}")
            messages.append({"role": "assistant", "content": final_content})

        else:
            # No tool needed
            print(f"Agent: {response_msg.content}")
            messages.append({"role": "assistant", "content": response_msg.content})


if __name__ == "__main__":
    run_agent()
