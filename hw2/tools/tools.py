from __future__ import annotations

import os
from dataclasses import dataclass

from tavily import TavilyClient


@dataclass
class SearchResult:
    title: str
    url: str
    content: str
    score: float | None = None


class TavilySearchTool:
    def __init__(self, api_key: str | None = None, max_results: int = 5) -> None:
        self.api_key = (api_key or os.getenv("TAVILY_API_KEY") or "").strip()
        self.max_results = max_results
        self.client = TavilyClient(api_key=self.api_key) if self.api_key else None

    def search(self, query: str) -> str:
        if not self.client:
            return "Search error: TAVILY_API_KEY is missing."

        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=self.max_results,
                include_answer=True,
                include_raw_content=False,
                auto_parameters=True,
                include_images=False,
                include_favicon=False,
                topic="general",
            )
        except Exception as exc:
            return f"Search error: {exc.__class__.__name__}: {exc}"

        return self._format_response(query, response)

    def _format_response(self, query: str, response: dict) -> str:
        answer = str(response.get("answer") or "").strip()
        results = response.get("results") or []

        lines: list[str] = []
        if answer:
            lines.append(f"Direct answer: {answer}")

        if results:
            lines.append("Top results:")
            for index, result in enumerate(results[: self.max_results], start=1):
                item = SearchResult(
                    title=str(result.get("title") or "Untitled"),
                    url=str(result.get("url") or ""),
                    content=str(
                        result.get("content") or result.get("raw_content") or ""
                    ),
                    score=result.get("score"),
                )
                snippet = item.content.strip().replace("\n", " ")
                if len(snippet) > 280:
                    snippet = snippet[:277].rstrip() + "..."
                score_text = (
                    f" score={item.score:.2f}"
                    if isinstance(item.score, (int, float))
                    else ""
                )
                url_text = f" ({item.url})" if item.url else ""
                lines.append(f"{index}. {item.title}{score_text}{url_text}")
                if snippet:
                    lines.append(f"   {snippet}")

        if not lines:
            return f"No results found for: {query}"

        return "\n".join(lines)
