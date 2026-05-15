from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from agents.schemas import compact_question, question_concept_ids


class ErrorDiagnosisAgent:
    """Judge objective answers and provide rule-based remediation advice."""

    def __init__(self, kb: dict[str, Any]):
        self.error_by_id = {item.get("error_id"): item for item in kb.get("errors", [])}

    def diagnose(self, question: dict[str, Any], student_answer: str) -> dict[str, Any]:
        standard_answer = str(question.get("answer", "")).strip()
        answer = str(student_answer or "").strip()
        is_correct = self._match_answer(answer, standard_answer)
        errors = [self.error_by_id[item] for item in question.get("common_errors", []) if item in self.error_by_id]
        return {
            "is_correct": is_correct,
            "question": compact_question(question),
            "student_answer": student_answer,
            "standard_answer": standard_answer,
            "analysis": question.get("analysis", ""),
            "involved_concepts": question_concept_ids(question),
            "error_type": "回答正确" if is_correct else self._error_type(errors),
            "error_reasons": [] if is_correct else [self._compact_error(item) for item in errors],
            "suggestion": self._suggestion(is_correct, errors, question),
        }

    def _match_answer(self, answer: str, standard_answer: str) -> bool:
        if not standard_answer:
            return False
        if answer == standard_answer:
            return True
        if answer and (answer in standard_answer or standard_answer in answer):
            return True
        return SequenceMatcher(None, answer, standard_answer).ratio() >= 0.82

    def _error_type(self, errors: list[dict[str, Any]]) -> str:
        if not errors:
            return "答案与标准答案不一致"
        return errors[0].get("name", "概念或步骤错误")

    def _compact_error(self, error: dict[str, Any]) -> dict[str, Any]:
        return {
            "error_id": error.get("error_id"),
            "name": error.get("name"),
            "description": error.get("error_description"),
        }

    def _suggestion(self, is_correct: bool, errors: list[dict[str, Any]], question: dict[str, Any]) -> list[str]:
        if is_correct:
            return ["答案正确。建议再做一道同知识点中等难度题，确认可以迁移。"]
        suggestions = []
        for error in errors:
            suggestions.extend(error.get("remediation", [])[:2])
        if suggestions:
            return suggestions
        return [question.get("analysis") or "回到知识点定义、适用条件和边界情况重新复盘。"]

