# Assignment 1: Build Your First Question Answering Agent (Raw Python & Function Calling)

**Due Date:** 3/5 - 3/11

---

## 🎯 Objective

The goal of this assignment is to understand the fundamental mechanics of LLM Agents without relying on high-level frameworks like LangChain. You will implement a **"Financial Assistant"** that can answer questions about exchange rates and stock prices.

You must implement best coding practices, including:

* **Function Maps** for routing.
* **Environment Variables** for security.
* **Handling Parallel Tool Calls**.

---

## 💻 Task Description

You need to build a Command Line Interface (CLI) chatbot in Python.

### 1. System Setup

* **LLM API:** Connect using a model that supports Tool Use / Function Calling (e.g., OpenAI `gpt-4o-mini`, Gemini, or Groq). It must support the OpenAI Python SDK interface.
* **Security:** Use `python-dotenv` to manage API keys. **Do not upload keys to Git.**

### 2. Mock Data Functions (Standardized)

Implement the following two functions. Use this exact data (do not fetch real-time web data):

**Function A: `get_exchange_rate(currency_pair: str)`**

* **Data:** * `USD_TWD` -> `32.0`
  * `JPY_TWD` -> `0.2`
  * `EUR_USD` -> `1.2`
* **Return:** JSON string, e.g., `{"currency_pair": "USD_TWD", "rate": "32.0"}`

**Function B: `get_stock_price(symbol: str)`**

* **Data:** * `AAPL` -> `260.00`
  * `TSLA` -> `430.00`
  * `NVDA` -> `190.00`
* **Return:** JSON string, e.g., `{"symbol": "AAPL", "price": "260.00"}`

> **Error Handling:** If a symbol/pair is not found, return `{"error": "Data not found"}`.

### 3. Tool Schema (Structured Outputs)

* Define JSON schemas using the `tools` parameter.
* **Strict Mode:** Set `"strict": true` in function definitions.
* **Constraints:** Ensure all tool parameters include `"additionalProperties": false`.

### 4. Robust Agent Loop

* **Function Map:** Use a Python Dictionary to dispatch calls (Avoid long if-else chains).
* **Parallel Tool Calls:** Must handle multiple tool calls in one turn (e.g., "Check AAPL and TSLA"). Execute all, append to history, then call LLM again.
* **Context Window:** The agent must maintain conversation memory.

---

## 📹 Demo Video Requirements

Record a screen recording (< 3 mins) showing the following tasks in order:

* **Task A (Persona):** Input "Who are you?" -> Reply as Financial Assistant.
* **Task B (Single Tool):** Input "What is the price of NVDA?" -> Return 190.00.
* **Task C (Parallel Tools):** Input "Compare the stock prices of AAPL and TSLA." -> Show logs executing both tools.
* **Task D (Memory):** Tell the agent your name, then ask "What is my name?".
* **Task E (Error Handling):** Input "What is the price of GOOG?" -> Handle "Data not found" gracefully.

---

## 📊 Grading Rubric

| Test Item                  | Key Checkpoints                                      | Weight |
| :------------------------- | :--------------------------------------------------- | :----- |
| **Environment & Security** | No hardcoded keys, `requirements.txt` included.      | 10%    |
| **Code Structure**         | Uses a **Function Map** (Dictionary) for routing.    | 10%    |
| **Tool Definition**        | Correct JSON schema with `strict: true`.             | 10%    |
| **Tasks A & B**            | Correct single query results (NVDA = 190.00).        | 20%    |
| **Task C**                 | Successfully handles **Parallel Calls** in one turn. | 20%    |
| **Task D**                 | Correctly remembers user name and maintains persona. | 10%    |
| **Task E**                 | Robust error handling for unknown data (GOOG).       | 20%    |

---

## 📁 Submission

* **Deadline:** 2026/03/12 23:30
* **Required:** GitHub Repo Link & Demo Video Link.
