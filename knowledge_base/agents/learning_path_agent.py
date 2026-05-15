from __future__ import annotations

from typing import Any

from agents.schemas import AgentResult, compact_concept


class LearningPathAgent:
    """Builds personalized paths from prerequisite and relation data."""

    def __init__(self, kb: dict[str, Any]):
        self.kb = kb
        self.concept_by_id = {item["id"]: item for item in kb.get("concepts", [])}

    def plan(self, target_concept_ids: list[str], student_profile: dict[str, Any], limit: int = 8) -> AgentResult:
        mastered = set(student_profile.get("mastered_concepts", []))
        weak = set(student_profile.get("weak_points", []))
        path_ids: list[str] = []
        for concept_id in target_concept_ids:
            self._collect_prerequisites(concept_id, path_ids)
            if concept_id not in path_ids:
                path_ids.append(concept_id)

        path = []
        for concept_id in path_ids[:limit]:
            concept = self.concept_by_id.get(concept_id)
            if not concept:
                continue
            if concept_id in mastered:
                status = "已掌握，快速回顾"
            elif concept_id in weak:
                status = "薄弱点，优先复习"
            else:
                status = "待学习"
            path.append({"concept": compact_concept(concept), "status": status})

        confusions = self._confusions(target_concept_ids)
        return AgentResult(
            "LearningPathAgent",
            {
                "path": path,
                "priority_now": path[0] if path else {},
                "confuses_with": [compact_concept(item) for item in confusions],
                "next_advice": "按前置知识 -> 当前重点 -> 易混点对比 -> 配套练习的顺序推进。",
            },
            ["已生成个性化复习路径。"],
        )

    def _collect_prerequisites(self, concept_id: str, output: list[str]) -> None:
        concept = self.concept_by_id.get(concept_id, {})
        for item in concept.get("prerequisites", []):
            self._collect_prerequisites(item, output)
            if item not in output:
                output.append(item)

    def _confusions(self, target_ids: list[str]) -> list[dict[str, Any]]:
        ids = []
        for relation in self.kb.get("relations", []):
            if relation.get("relation") != "confuses_with":
                continue
            if relation.get("source") in target_ids:
                ids.append(relation.get("target"))
            elif relation.get("target") in target_ids:
                ids.append(relation.get("source"))
        return [self.concept_by_id[item] for item in ids if item in self.concept_by_id]

