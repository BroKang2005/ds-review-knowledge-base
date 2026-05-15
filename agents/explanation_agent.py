from __future__ import annotations

from typing import Any


class ExplanationAgent:
    """Generate rule-based explanations suitable for exam review."""

    def explain(self, concept: dict[str, Any], student_profile: dict[str, Any] | None = None) -> dict[str, Any]:
        student_profile = student_profile or {}
        weak = set(student_profile.get("weak_concepts", []))
        concept_id = concept.get("id", "")
        reminders = list(concept.get("common_mistakes", []))[:3]
        if concept_id in weak:
            reminders.insert(0, "这是你当前画像中的薄弱点，建议先看定义，再做低难度题。")
        return {
            "concept_id": concept_id,
            "title": concept.get("name", concept_id),
            "definition": concept.get("description") or f"{concept.get('name', concept_id)} 是数据结构期末复习中的一个考点。",
            "exam_focus": [
                f"所属模块：{concept.get('module', '未知模块')}",
                f"所属主题：{concept.get('topic', '未知主题')}",
                f"重要度：{concept.get('importance', '未知')}，考试频率：{concept.get('exam_frequency', '未知')}",
            ],
            "examples": self._examples(concept),
            "common_mistakes": reminders,
            "summary": concept.get("learning_suggestion") or "复习时按“定义 -> 条件 -> 步骤 -> 边界情况 -> 典型题”推进。",
        }

    def _examples(self, concept: dict[str, Any]) -> list[str]:
        formulas = concept.get("formulas", [])
        if formulas:
            return [f"常用公式/规则：{item}" for item in formulas[:2]]
        return ["先用一个小规模样例手算，再检查空结构、单元素、边界位置等情况。"]

