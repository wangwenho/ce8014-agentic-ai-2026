# HW1

The sample implementation is a simple Financial Assistant.

## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) : ensure it is installed on your machine.
- Python 3.x (installed automatically by `uv`).

### 1. Clone the repository

```bash
git clone https://github.com/wangwenho/ce8007-computer-graphics-2025.git
cd hw1
```

### 2. Install dependencies

```bash
uv sync
```

This command installs all packages required by the project.

### 3. Run the application

```bash
uv run python main.py
```

You should see an interactive prompt similar to the following:

```plain
Welcome to Financial Assistant. type 'exit' to quit.
You: Who are you?
Agent: I am a Financial Assistant here to help you with inquiries related to stock prices, exchange rates, and other financial information. How can I assist you today?
You: What is the price of NVDA?
Agent: The current price of NVIDIA Corporation (NVDA) is $190.00. If you need any more information, feel free to ask!
You: Compare the stock prices of AAPL and TSLA.
Agent: The current stock prices are as follows:
- Apple Inc. (AAPL): $260.00
- Tesla Inc. (TSLA): $430.00

If you need further analysis or information, just let me know!
You: My name is WWH. What is my name?
Agent: Your name is WWH. How can I assist you today, WWH?
You: What is the price of GOOG?
Agent: I currently do not have the stock price for Alphabet Inc. (GOOG). If you have any other inquiries or if there's something else I can assist you with, please let me know!
You: exit
Goodbye!
```

## Testing

Run the test suite with:

```bash
uv run pytest tests
```
