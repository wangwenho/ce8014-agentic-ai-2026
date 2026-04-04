# Homework 3

## 🚀 Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) : ensure it is installed on your machine.
- Python 3.x (installed automatically by `uv`).

### 1. Clone the repository

```bash
git clone https://github.com/wangwenho/ce8014-agentic-ai-2026.git
cd hw3
```

### 2. Install dependencies

```bash
uv sync
```

This command installs all packages required by the project.

### 3. Create a `.env` file

```bash
echo "LLM_PROVIDER=openai" > .env
echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
echo "OPENAI_MODEL=gpt-4o-mini" >> .env
```

### 4. Run the application

```bash
uv run python build_rag.py
uv run python langgraph_agent.py
```

> [!NOTE]
>
> - You can switch between the "GRAPH" and "LEGACY" modes in [`evaluator.py`](./evaluator.py) to compare the performance of the LangGraph-based agent against a traditional retrieval-based agent.
> - You can switch between different embedding models by changing the `EMBEDDING_MODEL` variable in [`config.py`](./config.py).

## Benchmark Tasks

### 1. Embedding Model Comparison

I compare `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` and `sentence-transformers/paraphrase-multilingual-MPNet-base-v2` for embedding generation. The former is faster and often good enough for direct financial keyword matching, while the latter is expected to be stronger on more nuanced semantic comparisons. In this 14-question benchmark, the results were mixed: MiniLM achieved `8/14` in legacy mode and `9/14` in graph mode, while MPNet achieved `10/14` in legacy mode and `8/14` in graph mode. This indicates that the embedding impact is modest on this set, and a stronger model does not always produce higher accuracy for every configuration.

|embedding_model|chunk_size|mode|accuracy|
|---|---|---|---|
|MiniLM|1000|LEGACY|8/14|
|MiniLM|1000|GRAPH|9/14|
|MPNet|1000|LEGACY|10/14|
|MPNet|1000|GRAPH|8/14|

### 2. LangGraph vs. LangChain

LangGraph's graph-based workflow is designed to support dynamic retriever routing and relevance judgment, while the legacy LangChain approach is more linear. In this benchmark, LangGraph improved MiniLM from `8/14` to `9/14`, but the overall change was small because many questions were already handled by straightforward retrieval. The gains are therefore most visible in edge cases and multi-step relevance checks rather than across every question.

|embedding_model|chunk_size|mode|accuracy|
|---|---|---|---|
|MiniLM|1000|LEGACY|8/14|
|MiniLM|1000|GRAPH|9/14|

### 3. Chunk Size Trade-off Analysis

I experimented with chunk sizes of 1000 and 2000 tokens. Smaller chunks (1000) improved precision for legacy mode, raising accuracy from `7/14` at 2000 tokens to `8/14` at 1000 tokens, while graph mode remained stable at `9/14`. Larger chunks can preserve broader context, which helps when the answer spans multiple sections, but they also make retrieval noisier for tightly focused financial lookups. In this dataset, the smaller chunk size was slightly better for legacy retrieval, showing the classic trade-off between context completeness and context precision.

|embedding_model|chunk_size|mode|accuracy|
|---|---|---|---|
|MiniLM|1000|LEGACY|8/14|
|MiniLM|1000|GRAPH|9/14|
|MiniLM|2000|LEGACY|7/14|
|MiniLM|2000|GRAPH|9/14|
