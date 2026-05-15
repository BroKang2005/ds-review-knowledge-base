from __future__ import annotations

from typing import Any

from agents.schemas import AgentResult


class SummaryAgent:
    """Summarizes one review session and proposes the next step."""

    def summarize(self, session: dict[str, Any], profile_summary: dict[str, Any]) -> AgentResult:
        diagnosis = session.get("diagnosis", {})
        retrieval = session.get("retrieval", {})
        is_correct = diagnosis.get("is_correct")
        weak_points = profile_summary.get("weak_points", [])
        mastered = profile_summary.get("mastered_concepts", [])
        summary = {
            "reviewed_concept": retrieval.get("primary_concept", {}),
            "answer_result": "正确" if is_correct else "需要订正" if is_correct is not None else "未答题",
            "mastered_concepts": mastered[:5],
            "still_weak_concepts": weak_points[:5],
            "next_plan": self._next_plan(is_correct, weak_points),
            "session_messages": session.get("messages", []),
        }
        return AgentResult("SummaryAgent", summary, ["已生成阶段性复习总结。"])

    def _next_plan(self, is_correct: bool | None, weak_points: list[str]) -> list[str]:
        if is_correct is True:
            return ["继续完成 1 道同知识点中等难度题。", "把本题关键步骤加入个人复习卡片。"]
        if weak_points:
            return [f"优先回看薄弱知识点 {weak_points[0]}。", "完成推荐题中的第一题并复盘错因。"]
        return ["先选择一个目标知识点，完成讲解阅读和配套练习。"]

