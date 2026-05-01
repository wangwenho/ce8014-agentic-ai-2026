"""KG builder for Assignment 4/5.

Contract kept intact:
- Graph: (Regulation)-[:HAS_ARTICLE]->(Article)-[:CONTAINS_RULE]->(Rule)
- Article properties: number, content, reg_name, category
- Rule properties: rule_id, type, action, result, art_ref, reg_name
- Fulltext indexes: article_content_idx, rule_idx
- SQLite file: ncu_regulations.db
"""

import os
import re
import sqlite3
from typing import Any

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (
    os.getenv("NEO4J_USER", "neo4j"),
    os.getenv("NEO4J_PASSWORD", "password"),
)

CLAUSE_SPLIT_RE = re.compile(
    r"(?:(?<=\.)\s+|(?<=;)\s+|(?<=。)\s+|(?<=；)\s+|(?=\d+\.\s))"
)


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _split_clauses(content: str) -> list[str]:
    text = _normalize_text(content)
    if not text:
        return []

    clauses: list[str] = []
    for part in CLAUSE_SPLIT_RE.split(text):
        cleaned = _normalize_text(re.sub(r"^\d+\.\s*", "", part))
        if cleaned:
            clauses.append(cleaned)
    return clauses


def _classify_clause(clause: str) -> str:
    lower = clause.lower()
    if any(
        token in lower
        for token in [
            "ntd",
            "fee",
            "working day",
            "workday",
            "pay",
            "cost",
            "reissue",
            "replace",
        ]
    ):
        return "fee"
    if any(
        token in lower
        for token in ["zero grade", "zero score", "deducted", "disciplinary", "penalty"]
    ):
        return "penalty"
    if any(
        token in lower
        for token in [
            "not permitted",
            "may not",
            "shall not",
            "must",
            "should",
            "required",
            "barred",
        ]
    ):
        return "requirement"
    if any(
        token in lower
        for token in [
            "may",
            "eligible",
            "can apply",
            "will be given",
            "will be approved",
        ]
    ):
        return "permission"
    if any(
        token in lower
        for token in [
            "semester",
            "years",
            "minutes",
            "credits",
            "points",
            "grade",
            "score",
        ]
    ):
        return "condition"
    return "rule"


def _extract_result(clause: str) -> str:
    patterns = [
        r"(?:zero grade(?: for the exam)?|zero score(?: for the exam)?|score will be zero)",
        r"(?:five points deducted|5 points deducted|five points deduction|5 points deduction)",
        r"(?:NTD\s*200|200\s*NTD|NTD\s*100|100\s*NTD)",
        r"(?:three workdays|3 working days|three working days)",
        r"(?:four years|4 years|two years|2 years|2 academic years)",
        r"(?:128 course credits|128 credits|60 marks|70 marks)",
        r"(?:five semesters|5 semesters)",
    ]

    for pattern in patterns:
        match = re.search(pattern, clause, flags=re.IGNORECASE)
        if match:
            return _normalize_text(match.group(0))

    return _normalize_text(clause)


def _make_rule_record(
    article_number: str, reg_name: str, clause: str, index: int
) -> dict[str, str]:
    clause = _normalize_text(clause)
    return {
        "rule_id": f"{reg_name}:{article_number}:{index:03d}",
        "type": _classify_clause(clause),
        "action": clause,
        "result": _extract_result(clause),
        "art_ref": article_number,
        "reg_name": reg_name,
    }


def build_fallback_rules(article_number: str, content: str) -> list[dict[str, str]]:
    """Split an article into deterministic rule records."""
    clauses = _split_clauses(content)
    rules: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for index, clause in enumerate(clauses, start=1):
        action = _normalize_text(clause)
        result = _extract_result(clause)
        canonical = (action.lower(), result.lower())
        if not action or not result or canonical in seen:
            continue
        seen.add(canonical)
        rules.append(_make_rule_record(article_number, "", clause, index))

    return rules


def extract_entities(
    article_number: str, reg_name: str, content: str
) -> dict[str, Any]:
    """Return rule-like records extracted from a single article."""
    clauses = _split_clauses(content)
    rules: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for index, clause in enumerate(clauses, start=1):
        record = _make_rule_record(article_number, reg_name, clause, index)
        canonical = (record["action"].lower(), record["result"].lower())
        if not record["action"] or not record["result"] or canonical in seen:
            continue
        seen.add(canonical)
        rules.append(record)

    if not rules and content.strip():
        rules.append(
            {
                "rule_id": f"{reg_name}:{article_number}:001",
                "type": "rule",
                "action": _normalize_text(content),
                "result": _normalize_text(content),
                "art_ref": article_number,
                "reg_name": reg_name,
            }
        )

    return {"rules": rules}


def build_graph() -> None:
    """Build KG from SQLite into Neo4j using the fixed assignment schema."""
    sql_conn = sqlite3.connect("ncu_regulations.db")
    cursor = sql_conn.cursor()
    driver = GraphDatabase.driver(URI, auth=AUTH)

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

        cursor.execute("SELECT reg_id, name, category FROM regulations")
        regulations = cursor.fetchall()
        reg_map: dict[int, tuple[str, str]] = {}

        for reg_id, name, category in regulations:
            reg_map[reg_id] = (name, category)
            session.run(
                "MERGE (r:Regulation {id:$rid}) SET r.name=$name, r.category=$cat",
                rid=reg_id,
                name=name,
                cat=category,
            )

        cursor.execute("SELECT reg_id, article_number, content FROM articles")
        articles = cursor.fetchall()

        for reg_id, article_number, content in articles:
            reg_name, reg_category = reg_map.get(reg_id, ("Unknown", "Unknown"))
            session.run(
                """
                MATCH (r:Regulation {id: $rid})
                CREATE (a:Article {
                    number:   $num,
                    content:  $content,
                    reg_name: $reg_name,
                    category: $reg_category
                })
                MERGE (r)-[:HAS_ARTICLE]->(a)
                """,
                rid=reg_id,
                num=article_number,
                content=_normalize_text(content),
                reg_name=reg_name,
                reg_category=reg_category,
            )

        session.run(
            """
            CREATE FULLTEXT INDEX article_content_idx IF NOT EXISTS
            FOR (a:Article) ON EACH [a.content]
            """
        )

        rule_counter = 0
        seen_rule_signatures: set[tuple[str, str, str, str]] = set()

        for reg_id, article_number, content in articles:
            reg_name, _ = reg_map.get(reg_id, ("Unknown", "Unknown"))
            extracted = extract_entities(article_number, reg_name, content)

            for rule in extracted.get("rules", []):
                action = _normalize_text(rule.get("action", ""))
                result = _normalize_text(rule.get("result", ""))
                if not action or not result:
                    continue

                signature = (reg_name, article_number, action.lower(), result.lower())
                if signature in seen_rule_signatures:
                    continue
                seen_rule_signatures.add(signature)

                rule_counter += 1
                session.run(
                    """
                    MATCH (a:Article {number: $article_number, reg_name: $reg_name})
                    CREATE (r:Rule {
                        rule_id: $rule_id,
                        type: $type,
                        action: $action,
                        result: $result,
                        art_ref: $art_ref,
                        reg_name: $reg_name
                    })
                    MERGE (a)-[:CONTAINS_RULE]->(r)
                    """,
                    article_number=article_number,
                    reg_name=reg_name,
                    rule_id=f"{reg_name}:{article_number}:{rule_counter:04d}",
                    type=rule.get("type", "rule"),
                    action=action,
                    result=result,
                    art_ref=article_number,
                )

        session.run(
            """
            CREATE FULLTEXT INDEX rule_idx IF NOT EXISTS
            FOR (r:Rule) ON EACH [r.action, r.result]
            """
        )

        coverage = session.run(
            """
            MATCH (a:Article)
            OPTIONAL MATCH (a)-[:CONTAINS_RULE]->(r:Rule)
            WITH a, count(r) AS rule_count
            RETURN count(a) AS total_articles,
                   sum(CASE WHEN rule_count > 0 THEN 1 ELSE 0 END) AS covered_articles,
                   sum(CASE WHEN rule_count = 0 THEN 1 ELSE 0 END) AS uncovered_articles
            """
        ).single()

        total_articles = int((coverage or {}).get("total_articles", 0) or 0)
        covered_articles = int((coverage or {}).get("covered_articles", 0) or 0)
        uncovered_articles = int((coverage or {}).get("uncovered_articles", 0) or 0)

        print(
            f"[Coverage] covered={covered_articles}/{total_articles}, "
            f"uncovered={uncovered_articles}"
        )

    driver.close()
    sql_conn.close()


if __name__ == "__main__":
    build_graph()
