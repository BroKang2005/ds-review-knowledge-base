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


def compact_concept(concept: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": concept.get("id"),
        "name": concept.get("name"),
        "granularity": concept.get("granularity"),
        "module": concept.get("module"),
        "topic": concept.get("topic"),
        "difficulty": concept.get("difficulty"),
        "importance": concept.get("importance"),
        "exam_frequency": concept.get("exam_frequency"),
        "description": concept.get("description", ""),
        "formulas": concept.get("formulas", []),
        "common_mistakes": concept.get("common_mistakes", []),
        "learning_suggestion": concept.get("learning_suggestion", ""),
    }


def compact_question(question: dict[str, Any]) -> dict[str, Any]:
    return {
        "question_id": question.get("question_id"),
        "question_type": question.get("question_type"),
        "difficulty": question.get("difficulty"),
        "stem": question.get("stem"),
        "options": question.get("options", []),
        "knowledge_points": question.get("knowledge_points", []),
        "estimated_time": question.get("estimated_time"),
    }

