from __future__ import annotations

from typing import Any

from agents.schemas import AgentResult


class ExplanationAgent:
    """Builds student-facing explanations from retrieved KB snippets."""

    def explain(self, retrieval: dict[str, Any], student_profile: dict[str, Any], user_question: str = "") -> AgentResult:
        concept = retrieval.get("primary_concept") or {}
        if not concept:
            return AgentResult("ExplanationAgent", {"explanation": "暂未检索到明确知识点。"}, ["无法生成精确讲解。"])

        weak_ids = set(student_profile.get("weak_points", []))
        level = "基础巩固" if concept.get("id") in weak_ids else "常规复习"
        formulas = concept.get("formulas", []) or []
        mistakes = concept.get("common_mistakes", []) or []
        suggestion = concept.get("learning_suggestion") or "先理解定义，再结合典型题检查边界条件和操作步骤。"
        explanation = {
            "concept_id": concept.get("id"),
            "title": concept.get("name"),
            "level": level,
            "overview": concept.get("description") or f"本知识点属于 {concept.get('module')} / {concept.get('topic')}。",
            "step_by_step": [
                "先确认题目正在考查的概念、结构或算法操作。",
                "再写出适用条件、关键步骤和可能变化的状态。",
                "最后检查边界情况，并用题目要求的形式表达结论。",
            ],
            "examples": self._examples_from_questions(retrieval.get("questions", [])),
            "formulas": formulas[:3],
            "common_mistakes": mistakes[:3],
            "memory_tip": suggestion,
            "student_adaptation": f"结合当前画像，建议按“{level}”粒度复习：先补概念，再做低到中等难度题。",
            "user_question": user_question,
        }
        return AgentResult("ExplanationAgent", explanation, ["已生成个性化知识讲解。"])

    def _examples_from_questions(self, questions: list[dict[str, Any]]) -> list[str]:
        return [item.get("stem", "") for item in questions[:2] if item.get("stem")]

