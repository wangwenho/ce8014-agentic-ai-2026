# Homework 5

Assignment 5 extends the knowledge-graph-based QA system from HW4 into a **multi-agent architecture** with 7 specialized agents for robust question answering.

## 🚀 Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) : make sure it is installed.
- Python 3.11
- Docker Desktop

### 1. Clone the repository

```bash
git clone https://github.com/wangwenho/ce8014-agentic-ai-2026.git
cd hw5
```

### 2. Start Neo4j

```bash
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Build the database and knowledge graph

```bash
uv run python setup_data.py
uv run python build_kg.py
```

### 5. Run the multi-agent query system

```bash
uv run python main.py
# Then type questions interactively, e.g.:
# Question: What is the fee for replacing a lost Mifare student ID?
# Answer: 100 NTD.
```

### 6. Run the automatic evaluation

```bash
uv run python auto_test_a5.py
```

---

## 🤖 Multi-Agent Architecture

The system implements 7 agents in a pipeline:

| Agent | Purpose |
| ------- | --------- |
| **NL Understanding Agent** | Converts questions to structured intent |
| **Security Agent** | Validates queries against unsafe patterns |
| **Query Planning Agent** | Generates Neo4j Cypher queries |
| **Query Execution Agent** | Executes read-only queries |
| **Diagnosis Agent** | Detects query failures |
| **Repair Agent** | Attempts query regeneration |
| **Explanation Agent** | Generates final answers |

---

## 📊 Evaluation Results

```text
==================================================
A5 Evaluation Summary
==================================================
Total Cases: 40
End-to-End Success Rate: 40/40 (100.0%)
Normal QA accuracy: 20/20 (100.0%)
Failure-handling pass rate: 10/10 (100.0%)
Unsafe rejection rate: 10/10 (100.0%)
Diagnosis label validity: 40/40 (100.0%)
Repair success rate (attempted only): N/A (no repair attempts)
--------------------------------------------------
Weighted Score (System Performance = 60)
Task Success Rate: 25.00 / 25
Security & Validation: 15.00 / 15
Error Detection Quality: 8.00 / 8
Query Regeneration: 0.00 / 6
Correct Resolution After Repair: 0.00 / 6
System Performance Subtotal: 48.00 / 60
```

---

## 📁 Project Structure

```text
hw5/
├── main.py                    # Entry point
├── query_system_multiagent.py # Multi-agent pipeline
├── agents/
│   ├── a5_template.py         # 7-agent implementation
│   └── __init__.py
├── build_kg.py                # Knowledge graph builder
├── setup_data.py              # Database setup
├── auto_test_a5.py            # Evaluation script
└── test_data_a5.json          # Test cases
```
