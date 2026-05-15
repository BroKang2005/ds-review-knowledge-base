from __future__ import annotations

from typing import Any

from agents.schemas import AgentResult, compact_question
from src.kb_search import get_descendant_ids


class QuestionRecommendationAgent:
    """Ranks exercises by weak points, goal relevance, difficulty, and history."""

    def __init__(self, kb: dict[str, Any]):
        self.kb = kb

    def recommend(
        self,
        concept_ids: list[str],
        student_profile: dict[str, Any],
        goal: str = "",
        limit: int = 3,
    ) -> AgentResult:
        history = {item.get("question_id") for item in student_profile.get("question_history", [])}
        weak_scores = student_profile.get("weak_point_scores", {})
        target_ids = set(concept_ids)
        for concept_id in concept_ids:
            target_ids.update(get_descendant_ids(self.kb, concept_id))
        candidates = []
        for question in self.kb.get("questions", []):
            qid = question.get("question_id")
            if qid in history:
                continue
            points = question.get("knowledge_points", [])
            if target_ids and not any(item in target_ids for item in points):
                continue
            score = self._score_question(question, points, weak_scores, goal)
            candidates.append((score, question))

        candidates.sort(key=lambda item: (item[0], -item[1].get("difficulty", 3)), reverse=True)
        recommendations = []
        for order, (_, question) in enumerate(candidates[:limit], start=1):
            points = question.get("knowledge_points", [])
            recommendations.append(
                {
                    "order": order,
                    "question": compact_question(question),
                    "reason": self._reason(question, points, weak_scores),
                    "knowledge_points": points,
                }
            )
        return AgentResult(
            "QuestionRecommendationAgent",
            {"recommendations": recommendations},
            [f"已推荐 {len(recommendations)} 道练习题。"],
        )

    def _score_question(self, question: dict[str, Any], points: list[str], weak_scores: dict[str, int], goal: str) -> float:
        score = question.get("exam_frequency", 3) + question.get("difficulty", 3) * 0.4
        score += sum(weak_scores.get(item, 0) for item in points) * 2
        goal_text = goal.lower()
        if goal_text and any(goal_text in str(value).lower() for value in question.values()):
            score += 2
        if question.get("difficulty", 3) >= 5:
            score -= 0.5
        return score

    def _reason(self, question: dict[str, Any], points: list[str], weak_scores: dict[str, int]) -> str:
        if any(weak_scores.get(item, 0) > 0 for item in points):
            return "覆盖当前薄弱知识点，适合作为针对性巩固题。"
        return f"难度 {question.get('difficulty')}，适合作为当前知识点的配套练习。"
