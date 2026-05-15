from __future__ import annotations

from typing import Any

from agents.schemas import compact_question, question_concept_ids, question_id


class QuestionRecommendationAgent:
    """Recommend exercises by concept, weak points, difficulty, and history."""

    def __init__(self, kb: dict[str, Any], retrieval_agent: Any):
        self.kb = kb
        self.retrieval_agent = retrieval_agent

    def recommend(self, student_profile: dict[str, Any], concept_id: str | None = None, limit: int = 5) -> dict[str, Any]:
        answered = {item.get("question_id") for item in student_profile.get("answer_history", [])}
        target_ids = set()
        if concept_id:
            target_ids.add(concept_id)
            target_ids.update(self.retrieval_agent.get_descendant_ids(concept_id))
        else:
            target_ids.update(student_profile.get("weak_concepts", []))

        candidates = []
        for question in self.kb.get("questions", []):
            qid = question_id(question)
            if qid in answered:
                continue
            points = set(question_concept_ids(question))
            if target_ids and not points.intersection(target_ids):
                continue
            candidates.append((self._score(question, points, student_profile), question))

        if not candidates and not concept_id:
            for question in self.kb.get("questions", []):
                if question_id(question) not in answered:
                    candidates.append((self._score(question, set(question_concept_ids(question)), student_profile), question))

        candidates.sort(key=lambda item: item[0], reverse=True)
        recommendations = [
            {
                "order": index,
                "question": compact_question(question),
                "reason": self._reason(question, student_profile),
            }
            for index, (_, question) in enumerate(candidates[:limit], start=1)
        ]
        return {"recommendations": recommendations}

    def by_difficulty(self, student_profile: dict[str, Any], concept_id: str | None = None) -> dict[str, list[dict[str, Any]]]:
        items = self.recommend(student_profile, concept_id=concept_id, limit=20)["recommendations"]
        layers = {"easy": [], "medium": [], "hard": []}
        for item in items:
            difficulty = item["question"].get("difficulty", 3)
            try:
                difficulty = int(difficulty)
            except (TypeError, ValueError):
                difficulty = 3
            if difficulty <= 2:
                layers["easy"].append(item)
            elif difficulty <= 4:
                layers["medium"].append(item)
            else:
                layers["hard"].append(item)
        return layers

    def _score(self, question: dict[str, Any], points: set[str], profile: dict[str, Any]) -> float:
        score = float(question.get("exam_frequency", 3) or 3)
        weak = set(profile.get("weak_concepts", []))
        if points.intersection(weak):
            score += 5
        try:
            difficulty = int(question.get("difficulty", 3))
        except (TypeError, ValueError):
            difficulty = 3
        return score + max(0, 4 - abs(difficulty - 3))

    def _reason(self, question: dict[str, Any], profile: dict[str, Any]) -> str:
        if set(question_concept_ids(question)).intersection(set(profile.get("weak_concepts", []))):
            return "命中当前薄弱知识点，适合优先练习。"
        return "与当前复习目标相关，难度适合作为配套练习。"

