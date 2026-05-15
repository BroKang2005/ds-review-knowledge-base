from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


@dataclass
class AgentResult:
    agent: str
    data: dict[str, Any]
    messages: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {"agent": self.agent, "data": self.data, "messages": self.messages}


def concept_id(concept: dict[str, Any]) -> str:
    return str(concept.get("id") or concept.get("concept_id") or "")


def question_id(question: dict[str, Any]) -> str:
    return str(question.get("question_id") or question.get("id") or "")


def question_concept_ids(question: dict[str, Any]) -> list[str]:
    values = question.get("knowledge_points", question.get("concept_ids", []))
    return [str(item) for item in values if item]


def compact_concept(concept: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": concept_id(concept),
        "name": concept.get("name", concept_id(concept)),
        "granularity": concept.get("granularity", ""),
        "module": concept.get("module", ""),
        "topic": concept.get("topic", ""),
        "difficulty": concept.get("difficulty", ""),
        "importance": concept.get("importance", ""),
        "exam_frequency": concept.get("exam_frequency", ""),
        "description": concept.get("description", ""),
        "formulas": concept.get("formulas", []),
        "common_mistakes": concept.get("common_mistakes", []),
        "learning_suggestion": concept.get("learning_suggestion", ""),
    }


def compact_question(question: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": question_id(question),
        "question_id": question_id(question),
        "type": question.get("type", question.get("question_type", "")),
        "question_type": question.get("question_type", question.get("type", "")),
        "stem": question.get("stem", ""),
        "options": question.get("options", []),
        "answer": question.get("answer", ""),
        "analysis": question.get("analysis", ""),
        "difficulty": question.get("difficulty", ""),
        "concept_ids": question_concept_ids(question),
        "knowledge_points": question_concept_ids(question),
    }

