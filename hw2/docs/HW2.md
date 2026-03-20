# Assignment 2: Reasoning & Action Taking

**Due Date:** 3/12 - 3/25  

---

## Objective

The goal of this assignment is to move beyond simple automation to building a **Resilient Agent**. You will implement a **ReAct (Reasoning + Acting) Agent** from scratch. However, incorporating lessons from Andrew Ng's Agentic Workflows and Prompt Engineering research, your agent must demonstrate not just tool use, but **Reflection (self-correction)** and **Planning (breaking down complex tasks)**.

---

## Task Description

You need to build a **SINGLE** Python-based ReAct Agent capable of answering complex queries by iterating through a **Thought -> Action -> Observation** loop.

### 1. System Setup

* **LLM Engine:** `gpt-4o-mini` (Standard). Alternative API Options Allowed.
* **External Knowledge:** Integrate a Search API.
  * **Recommended:** Tavily API (Optimized for Agents, returns clean JSON).
  * **Alternative:** Serper.dev / DuckDuckGo.
* **Security:** Keys must be in a `.env` file.

### 2. The ReAct Loop (The Cognitive Engine)

Your `ReActAgent` class must implement the standard loop, but with a focus on **Self-Correction**:

1. **Thought:** "The user asked for population data. I should search for 2025 estimates."
2. **Action:** Search ["Japan population 2025"]
3. **Observation:** "No results found." (Simulated failure)
4. **Reflection (New Thought):** "The search returned nothing. I might have been too specific. I will try searching for 'Japan current population' instead." (**This is the Agentic Workflow**)
5. **Action:** Search ["Japan current population"]...

### 3. Tasks

* **Task 1: Planning & Quantitative Reasoning**
  * Question: "What fraction of Japan's population is Taiwan's population as of 2025?"
* **Task 2: Technical Specificity**
  * Question: "Compare the main display specs of iPhone 15 and Samsung S24."
* **Task 3: Resilience & Reflection Test**
  * Question: "Who is the CEO of the startup 'Morphic' AI search?" (Or any query where a direct keyword match might fail initially).

---

## Critical Requirements

* **Few-Shot Prompting (Crucial):** Your System Prompt **MUST** include at least one full example (One-shot) of a user asking a question and the agent going through the Thought/Action/Observation steps. This "teaches" the model the format via In-Context Learning and drastically improves stability.
* **Stop Sequences:** Implement logic to stop the LLM generation after it emits an "Action" to prevent hallucinated observations.
* **Loop Limits:** Hard limit on iterations (e.g., max 5 steps).

---

## Required Files (GitHub Repository)

Submit a link to your GitHub Repository containing:

* `agent.py`: Your Agent class.
* `tools.py`: Search tool wrapper.
* `main.py`: Execution script.
* `.env.example`: Config template.
* `requirements.txt`: Dependencies.
* `report.pdf`: Analysis report.

**Important:** Ensure your `.gitignore` includes `.env`.

---

## Submission Details

* **Deadline:** 2026/x/xx
* **Submission Method:** Submit the GitHub Link only.
* **Late Policy:** Standard course policy applies.

---

## Report Requirements (report.pdf)

*Note: This file must be included in your GitHub repository.*
To receive full credit, your report must explain how your agent works and provide evidence of its reasoning capabilities.

### Section 1: Implementation Logic

* **System Prompt Strategy:** Paste your System Prompt. Highlight the Few-Shot Example you added. Explain why this example helps the model.
* **The Loop Mechanism:** Briefly explain how your Python script feeds the "Observation" back into the LLM's context window.

### Section 2: Benchmark Traces (The Evidence)

For each task, paste the **Console Trace** and analyze the specific behavior.
**Constraint:** You must use the **SAME** ReActAgent instance to answer all three questions below. You are NOT allowed to create separate agents or use conditional logic to switch prompts. The agent must be general-purpose.

* **Task 1: Planning & Quantitative Reasoning**
  * **Analysis:** Did the agent perform Task Decomposition? (e.g., "First find Japan, then Taiwan, then calculate"). It should not try to guess the ratio directly.
* **Task 2: Technical Specificity**
  * **Analysis:** Look for Data Retrieval. Did it find the specific "60Hz vs 120Hz" difference?
* **Task 3: Resilience & Reflection Test**
  * **Analysis:** If the first search fails, does the agent Reflect and try again? (e.g., Thought: "I didn't find the CEO. I should check the 'About Us' page instead.")

---

## Grading Rubric / 評分標準

| 關鍵檢查點 (Key Checkpoints) | 檢查項目 (Inspection Items) | 分數 (Score) |
| :--- | :--- | :--- |
| **Agent Architecture** | GitHub Structure: Clean repo, no key leaks. Few-Shot Prompting: Does the System Prompt include a clear Example/Shot? | /20 |
| **Mechanism: The Loop** | Reasoning Loop: Implements `while` loop with History update. Stop Logic: Correctly halts generation before hallucinating observations. | /20 |
| **Tool Integration** | Real Search API: Uses Tavily/Serper/DDG. Robustness: Can handle API errors without crashing code. | /15 |
| **Report: Planning** | Task 1 Evidence: Trace shows the agent breaking down the problem into distinct search steps before calculating. | /15 |
| **Report: Accuracy** | Task 2 Evidence: Successfully retrieves specific tech specs (60Hz/120Hz). | /15 |
| **Agentic Reflection** | Self-Correction: The trace shows the agent adapting to search results. It does not blindly repeat the same action. | /15 |

---

## Resources

* **ReAct Paper:** Yao, S., et al. (2023). ReAct: Synergizing Reasoning and Acting in Language Models.
* **Tavily API:** <https://tavily.com>
* **LangChain Logic:** <https://python.langchain.com>
* **Deeplearning.AI:** <http://Deeplearning.Al>
* **ReAct - Prompt Engineering Guide:** <https://www.promptingguide.ai/techniques/react>

---

## Appendix A: Sample Starter Code

```python
import os
import re
from dotenv import load_dotenv

load_dotenv()

class Agent:
    def __init__(self, system_prompt):
        self.system = system_prompt
        self.messages = []

    def construct_prompt(self, query):
        # Implementation required
        pass

    def execute(self, query):
        # The ReAct Loop
        iteration = 0
        while iteration < 5:
            # 1. Call LLM
            # 2. Parse Action
            # 3. Call Tool
            # 4. Update History
            iteration += 1
