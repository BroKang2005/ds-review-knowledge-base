from __future__ import annotations

from difflib import SequenceMatcher
from typing import Any

from agents.schemas import AgentResult, compact_question


class ErrorDiagnosisAgent:
    """Checks an answer and maps errors back to weak concepts."""

    def __init__(self, kb: dict[str, Any]):
        self.kb = kb
        self.error_by_id = {item["error_id"]: item for item in kb.get("errors", [])}

    def diagnose(self, question: dict[str, Any], student_answer: str) -> AgentResult:
        standard = str(question.get("answer", "")).strip()
        answer = str(student_answer).strip()
        is_correct = self._is_correct(answer, standard)
        errors = [self.error_by_id[item] for item in question.get("common_errors", []) if item in self.error_by_id]
        involved = list(question.get("knowledge_points", []))
        diagnosis = {
            "is_correct": is_correct,
            "student_answer": student_answer,
            "question": {**compact_question(question), "answer": question.get("answer"), "analysis": question.get("analysis")},
            "involved_concepts": involved,
            "error_reasons": [] if is_correct else [self._error_reason(item) for item in errors],
            "correction": "答案正确，继续保持步骤表达。" if is_correct else question.get("analysis", "请回到标准答案，对照关键条件和步骤。"),
            "review_advice": self._review_advice(is_correct, errors),
        }
        return AgentResult("ErrorDiagnosisAgent", diagnosis, ["已完成答案正误判断和错因定位。"])

    def _is_correct(self, answer: str, standard: str) -> bool:
        if not standard:
            return False
        if answer == standard:
            return True
        if answer and (answer in standard or standard in answer):
            return True
        return SequenceMatcher(None, answer, standard).ratio() >= 0.82

    def _error_reason(self, error: dict[str, Any]) -> dict[str, Any]:
        return {
            "error_id": error.get("error_id"),
            "name": error.get("name"),
            "description": error.get("error_description"),
            "typical_behavior": error.get("typical_behavior", [])[:2],
        }

    def _review_advice(self, is_correct: bool, errors: list[dict[str, Any]]) -> list[str]:
        if is_correct:
            return ["把本题解法压缩成一句复习卡片，后续用同类题检验迁移能力。"]
        advice = []
        for error in errors:
            advice.extend(error.get("remediation", [])[:2])
        return advice or ["复盘题干条件、操作步骤和边界情况，再完成 1-2 道同知识点练习。"]

