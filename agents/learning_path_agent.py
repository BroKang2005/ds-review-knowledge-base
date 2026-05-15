from __future__ import annotations

from typing import Any


class LearningPathAgent:
    """Plan prerequisite and personalized review paths."""

    def __init__(self, retrieval_agent: Any):
        self.retrieval_agent = retrieval_agent

    def plan(self, student_profile: dict[str, Any], target_concept_id: str) -> dict[str, Any]:
        path = []
        for item in self._walk_prerequisites(target_concept_id):
            path.append({"concept": item, "status": self._status(item.get("id"), student_profile)})
        target = self.retrieval_agent.get_concept(target_concept_id)
        if target:
            path.append({"concept": target, "status": self._status(target_concept_id, student_profile)})
        atomic = self.retrieval_agent.get_atomic_concepts(target_concept_id)[:6]
        confusions = self.retrieval_agent.get_confusing_concepts(target_concept_id)
        return {
            "target_concept": target,
            "prerequisite_path": path,
            "atomic_steps": [{"concept": item, "status": self._status(item.get("id"), student_profile)} for item in atomic],
            "confusing_concepts": confusions,
            "next_action": self._next_action(path, atomic, student_profile),
        }

    def expand_chapter(self, module_name: str) -> list[dict[str, Any]]:
        return [
            item
            for item in self.retrieval_agent.search_concepts(module_name, limit=50)
            if item.get("module") == module_name or item.get("topic") == module_name or item.get("name") == module_name
        ]

    def _walk_prerequisites(self, concept_id: str) -> list[dict[str, Any]]:
        output = []
        seen = set()

        def visit(cid: str) -> None:
            for pre in self.retrieval_agent.get_prerequisites(cid):
                pid = pre.get("id")
                if pid and pid not in seen:
                    seen.add(pid)
                    visit(pid)
                    output.append(pre)

        visit(concept_id)
        return output

    def _status(self, concept_id: str, profile: dict[str, Any]) -> str:
        if concept_id in profile.get("mastered_concepts", []):
            return "已掌握"
        if concept_id in profile.get("weak_concepts", []):
            return "薄弱点"
        if concept_id in profile.get("learned_concepts", []):
            return "已学习"
        return "待复习"

    def _next_action(self, path: list[dict[str, Any]], atomic: list[dict[str, Any]], profile: dict[str, Any]) -> str:
        for item in path:
            if item["status"] in {"薄弱点", "待复习"}:
                return f"先复习前置知识：{item['concept'].get('name', item['concept'].get('id'))}"
        for item in atomic:
            if item.get("id") not in profile.get("mastered_concepts", []):
                return f"进入原子知识点练习：{item.get('name', item.get('id'))}"
        return "完成一组综合题并生成复习总结。"

