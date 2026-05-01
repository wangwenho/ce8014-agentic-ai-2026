from __future__ import annotations

import importlib
import os
import re
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv

load_dotenv()

# Neo4j setup
try:
    neo4j_module = importlib.import_module("neo4j")
    GraphDatabase = neo4j_module.GraphDatabase
    URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    AUTH = (
        os.getenv("NEO4J_USER", "neo4j"),
        os.getenv("NEO4J_PASSWORD", "password"),
    )
    driver = GraphDatabase.driver(URI, auth=AUTH)
except Exception:
    driver = None


@dataclass
class Intent:
    question_type: str
    keywords: list[str]
    aspect: str
    ambiguous: bool = False


# Question categorization patterns from hw4
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "can",
    "do",
    "does",
    "for",
    "from",
    "had",
    "has",
    "have",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "may",
    "must",
    "my",
    "not",
    "of",
    "on",
    "or",
    "should",
    "that",
    "the",
    "their",
    "to",
    "was",
    "what",
    "when",
    "will",
    "with",
    "would",
    "you",
}

SPECIAL_PHRASES = [
    "student id",
    "easycard",
    "mifare",
    "working days",
    "exam room",
    "question paper",
    "electronic devices",
    "communication capabilities",
    "leave the exam room",
    "make-up exam",
    "leave of absence",
    "physical education",
    "graduation credits",
    "passing score",
    "threaten the invigilator",
]

CATEGORY_BOOSTS = {
    "exam_late": ["exam", "late", "minutes", "admit"],
    "exam_leave": ["exam room", "leave", "40 minutes"],
    "id_penalty": ["exam", "student id", "five points deducted", "penalty"],
    "device_penalty": [
        "exam",
        "electronic receivers",
        "mobile phones",
        "five points deducted",
    ],
    "cheating_penalty": ["exam", "copy", "pass notes", "zero grade", "disciplinary"],
    "paper_removal": ["exam", "question paper", "zero grade"],
    "threaten_penalty": ["exam", "proctor", "zero grade", "disciplinary"],
    "id_fee_easycard": ["student id card", "easycard", "fee", "200", "working days"],
    "id_fee_mifare": ["student id card", "mifare", "fee", "100", "working days"],
    "id_turnaround": ["student id card", "working days", "application"],
    "graduation_credit": ["undergraduate", "graduation credits", "128"],
    "pe_semesters": ["physical education", "semesters", "five"],
    "military_training_credit": [
        "military training",
        "graduation credits",
        "not included",
    ],
    "duration_bachelor": ["four years", "undergraduate"],
    "duration_extension": ["two years", "undergraduate", "extension"],
    "passing_undergrad": ["undergraduate", "passing score", "60"],
    "passing_grad": ["graduate", "passing score", "70"],
    "dismissal_rule": ["dismissed", "poor grades", "two semesters", "half"],
    "makeup_exam": ["make-up exam", "no"],
    "leave_of_absence": ["suspension of studies", "two academic years"],
}


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _tokenize_question(question: str) -> list[str]:
    question = question.lower()
    found_phrases: list[str] = []
    for phrase in SPECIAL_PHRASES:
        if phrase in question:
            found_phrases.append(phrase)
    words = [
        token
        for token in re.findall(r"[a-z0-9]+", question)
        if token not in STOP_WORDS and len(token) > 2
    ]
    combined = found_phrases + words
    unique_terms: list[str] = []
    seen: set[str] = set()
    for term in combined:
        cleaned = _normalize_text(term)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        unique_terms.append(cleaned)
    return unique_terms


def _question_category(question: str) -> str:
    q = question.lower()
    if (
        "working days" in q
        or "how many working days" in q
        or "new student id after application" in q
    ):
        return "id_turnaround"
    if "military training" in q:
        return "military_training_credit"
    if "passing score" in q and "undergraduate" in q:
        return "passing_undergrad"
    if "passing score" in q and any(
        word in q for word in ["graduate", "master", "phd"]
    ):
        return "passing_grad"
    if "student id" in q and any(
        word in q
        for word in ["fee", "replacing", "lost", "mifare", "easycard", "new student id"]
    ):
        if "mifare" in q or "non-easycard" in q:
            return "id_fee_mifare"
        return "id_fee_easycard"
    if any(
        word in q
        for word in [
            "minimum total credits",
            "graduation credits",
            "undergraduate graduation",
            "128 credits",
        ]
    ):
        return "graduation_credit"
    if "physical education" in q or ("pe" in q and "semester" in q):
        return "pe_semesters"
    if any(word in q for word in ["standard duration", "bachelor", "study", "degree"]):
        if "extension" in q:
            return "duration_extension"
        return "duration_bachelor"
    if any(
        word in q
        for word in ["dismissed", "expelled", "poor grades", "failing more than half"]
    ):
        return "dismissal_rule"
    if "make-up exam" in q:
        return "makeup_exam"
    if any(word in q for word in ["leave of absence", "suspension of schooling"]):
        return "leave_of_absence"
    if any(word in q for word in ["late", "barred from the exam", "enter the room"]):
        return "exam_late"
    if any(
        word in q
        for word in [
            "leave the exam room",
            "leave 30 minutes",
            "leave after 30 minutes",
        ]
    ):
        return "exam_leave"
    if any(word in q for word in ["forget", "forgot", "student id"]):
        return "id_penalty"
    if any(
        word in q
        for word in [
            "electronic",
            "communication capabilities",
            "mobile phone",
            "devices",
        ]
    ):
        return "device_penalty"
    if any(
        word in q for word in ["cheating", "copying", "passing notes", "cribsheets"]
    ):
        return "cheating_penalty"
    if any(
        word in q for word in ["question paper", "take the question paper", "paper out"]
    ):
        return "paper_removal"
    if any(word in q for word in ["threaten", "invigilator", "proctor"]):
        return "threaten_penalty"
    return "general"


class NLUnderstandingAgent:
    def run(self, question: str) -> Intent:
        """Convert question to structured intent using hw4 logic."""
        category = _question_category(question)
        terms = _tokenize_question(question)
        for boost in CATEGORY_BOOSTS.get(category, []):
            if boost not in terms:
                terms.append(boost)

        aspect_map = {
            "id_fee_easycard": "fee",
            "id_fee_mifare": "fee",
            "id_turnaround": "time",
            "graduation_credit": "graduation",
            "pe_semesters": "graduation",
            "military_training_credit": "credit",
            "duration_bachelor": "duration",
            "duration_extension": "duration",
            "passing_undergrad": "grade",
            "passing_grad": "grade",
            "dismissal_rule": "dismissal",
            "makeup_exam": "exam",
            "leave_of_absence": "leave",
            "exam_late": "exam",
            "exam_leave": "exam",
            "id_penalty": "penalty",
            "device_penalty": "penalty",
            "cheating_penalty": "penalty",
            "paper_removal": "penalty",
            "threaten_penalty": "penalty",
        }

        return Intent(
            question_type=category,
            keywords=terms,
            aspect=aspect_map.get(category, "general"),
            ambiguous=False,
        )


class SecurityAgent:
    def run(self, question: str, intent: Intent) -> dict[str, str]:
        """Check for unsafe query patterns."""
        blocked_patterns = [
            "delete",
            "drop",
            "merge",
            "create",
            "set ",
            "bypass",
            "ignore previous",
            "dump all",
            "export",
            "dump",
            "show all",
            "credentials",
            "password",
            "admin",
            "modify",
            "update",
            "alter",
            "remove",
            "truncate",
            "destroy",
            "wipe",
            "show me every",
        ]
        q = question.lower()
        for p in blocked_patterns:
            if p in q:
                return {
                    "decision": "REJECT",
                    "reason": f"Unsafe query pattern detected: '{p}'",
                }
        return {"decision": "ALLOW", "reason": "Passed security check."}


class QueryPlannerAgent:
    def run(self, intent: Intent) -> dict[str, Any]:
        """Build query plan based on intent."""
        return {
            "strategy": "typed_then_broad",
            "keywords": intent.keywords,
            "aspect": intent.aspect,
            "question_type": intent.question_type,
        }


class QueryExecutionAgent:
    def run(self, plan: dict[str, Any]) -> dict[str, Any]:
        """Execute Neo4j read-only query and return rows."""
        if driver is None:
            return {"rows": [], "error": "Neo4j driver not available"}

        keywords = plan.get("keywords", [])
        if not keywords:
            return {"rows": [], "error": None}

        # Build Lucene query
        cleaned_terms = []
        for term in keywords[:10]:
            safe_term = _normalize_text(term.lower())
            if not safe_term:
                continue
            if " " in safe_term:
                cleaned_terms.append(f'"{safe_term}"')
            else:
                cleaned_terms.append(safe_term)

        if not cleaned_terms:
            return {"rows": [], "error": None}

        search = " OR ".join(cleaned_terms)

        try:
            with driver.session() as session:
                # Typed query (article-first)
                typed_query = """
                CALL db.index.fulltext.queryNodes('article_content_idx', $search) YIELD node AS article, score
                OPTIONAL MATCH (article)-[:CONTAINS_RULE]->(rule:Rule)
                WITH article, rule, score
                RETURN
                    coalesce(rule.rule_id, article.number) AS rule_id,
                    coalesce(rule.type, 'article') AS type,
                    coalesce(rule.action, article.content) AS action,
                    coalesce(rule.result, article.content) AS result,
                    coalesce(rule.art_ref, article.number) AS art_ref,
                    coalesce(rule.reg_name, article.reg_name) AS reg_name,
                    article.content AS article_content,
                    score AS score
                ORDER BY score DESC
                LIMIT 12
                """
                typed_results = list(session.run(typed_query, search=search))

                # Broad query (rule-first)
                broad_query = """
                CALL db.index.fulltext.queryNodes('rule_idx', $search) YIELD node AS rule, score
                OPTIONAL MATCH (article:Article)-[:CONTAINS_RULE]->(rule)
                RETURN
                    rule.rule_id AS rule_id,
                    rule.type AS type,
                    rule.action AS action,
                    rule.result AS result,
                    rule.art_ref AS art_ref,
                    rule.reg_name AS reg_name,
                    article.content AS article_content,
                    score AS score
                ORDER BY score DESC
                LIMIT 12
                """
                broad_results = list(session.run(broad_query, search=search))

                rows = []
                for record in typed_results + broad_results:
                    rows.append(dict(record))

                return {"rows": rows, "error": None}
        except Exception as e:
            return {"rows": [], "error": str(e)}


class DiagnosisAgent:
    def run(self, execution: dict[str, Any]) -> dict[str, str]:
        if execution.get("error"):
            return {"label": "QUERY_ERROR", "reason": str(execution["error"])}
        if not execution.get("rows"):
            return {"label": "NO_DATA", "reason": "No matching rule in KG."}
        return {"label": "SUCCESS", "reason": "Query succeeded."}


class QueryRepairAgent:
    def run(
        self, diagnosis: dict[str, str], original_plan: dict[str, Any], intent: Intent
    ) -> dict[str, Any]:
        """Return revised plan with broader search strategy."""
        repaired = dict(original_plan)
        # Expand keywords for repair
        repaired["strategy"] = "fulltext_only"
        # Add more general terms
        if "general" not in repaired.get("keywords", []):
            repaired["keywords"] = repaired.get("keywords", []) + ["regulation", "rule"]
        return repaired


class ExplanationAgent:
    def run(
        self,
        question: str,
        intent: Intent,
        security: dict[str, str],
        diagnosis: dict[str, str],
        answer: str,
        repair_attempted: bool,
    ) -> str:
        return (
            f"Intent={intent.question_type}, Security={security['decision']}, "
            f"Diagnosis={diagnosis['label']}, Repair={repair_attempted}. "
            f"Answer: {answer}"
        )


def build_template_pipeline() -> dict[str, Any]:
    """Factory for student use in query_system_multiagent_template.py."""
    return {
        "nlu": NLUnderstandingAgent(),
        "security": SecurityAgent(),
        "planner": QueryPlannerAgent(),
        "executor": QueryExecutionAgent(),
        "diagnosis": DiagnosisAgent(),
        "repair": QueryRepairAgent(),
        "explanation": ExplanationAgent(),
    }
