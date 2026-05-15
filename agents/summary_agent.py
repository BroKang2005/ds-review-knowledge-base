from __future__ import annotations

from typing import Any


class SummaryAgent:
    """Create session and stage summaries from profile and recent records."""

    def summarize(self, profile_summary: dict[str, Any], sessions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        sessions = sessions or []
        recent = sessions[-3:]
        reviewed = []
        for item in recent:
            session = item.get("session", {})
            concept = session.get("retrieval", {}).get("primary_concept", {})
            if concept:
                reviewed.append(concept)
        return {
            "student_id": profile_summary.get("student_id"),
            "reviewed_concepts": reviewed,
            "mastered_concepts": profile_summary.get("mastered_concepts", []),
            "weak_concepts": profile_summary.get("weak_concepts", []),
            "wrong_question_count": profile_summary.get("wrong_question_count", 0),
            "recent_accuracy": profile_summary.get("recent_accuracy", 0.0),
            "next_suggestions": self._next_suggestions(profile_summary),
        }

    def _next_suggestions(self, profile: dict[str, Any]) -> list[str]:
        weak = profile.get("weak_concepts", [])
        if weak:
            return [f"优先复习薄弱知识点 {weak[0]}。", "完成 2 道基础题和 1 道中等题后再复盘。"]
        if profile.get("recent_accuracy", 0) >= 0.8:
            return ["近期正确率较高，可以进入综合题和高频考点串联复习。"]
        return ["先选择一个章节目标，完成讲解阅读和配套练习。"]

