from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from agents.schemas import AgentResult, now_iso


class StudentProfileAgent:
    """Maintains persistent student state for the review workflow."""

    def __init__(self, profile_path: str | Path):
        self.profile_path = Path(profile_path)
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.profile_path.exists():
            self.profile_path.write_text("{}", encoding="utf-8")

    def get_profile(self, student_id: str = "S001") -> dict[str, Any]:
        profiles = self._load_profiles()
        profile = profiles.get(student_id)
        if profile:
            return profile
        return {
            "student_id": student_id,
            "current_goal": "",
            "learned_concepts": [],
            "mastered_concepts": [],
            "weak_points": {},
            "question_history": [],
            "review_sessions": [],
            "updated_at": now_iso(),
        }

    def set_goal(self, student_id: str, goal: str) -> AgentResult:
        profile = self.get_profile(student_id)
        profile["current_goal"] = goal.strip()
        profile["updated_at"] = now_iso()
        self._save_profile(profile)
        return AgentResult(
            agent="StudentProfileAgent",
            data={"profile": self.summarize_profile(student_id), "current_goal": profile["current_goal"]},
            messages=["已更新学生当前复习目标。"],
        )

    def record_learning(self, student_id: str, concept_ids: list[str]) -> AgentResult:
        profile = self.get_profile(student_id)
        learned = set(profile.get("learned_concepts", []))
        learned.update(item for item in concept_ids if item)
        profile["learned_concepts"] = sorted(learned)
        profile["updated_at"] = now_iso()
        self._save_profile(profile)
        return AgentResult(
            agent="StudentProfileAgent",
            data={"learned_concepts": profile["learned_concepts"]},
            messages=["已记录本次学习过的知识点。"],
        )

    def update_after_diagnosis(self, student_id: str, diagnosis: dict[str, Any]) -> AgentResult:
        profile = self.get_profile(student_id)
        question = diagnosis.get("question", {})
        question_id = question.get("question_id")
        involved = diagnosis.get("involved_concepts", [])
        is_correct = bool(diagnosis.get("is_correct"))

        if question_id:
            profile.setdefault("question_history", []).append(
                {
                    "question_id": question_id,
                    "is_correct": is_correct,
                    "student_answer": diagnosis.get("student_answer", ""),
                    "standard_answer": question.get("answer", ""),
                    "concept_ids": involved,
                    "diagnosed_at": now_iso(),
                }
            )

        weak_points = profile.setdefault("weak_points", {})
        mastered = set(profile.get("mastered_concepts", []))
        for concept_id in involved:
            if is_correct:
                mastered.add(concept_id)
                if concept_id in weak_points:
                    weak_points[concept_id] = max(0, int(weak_points[concept_id]) - 1)
            else:
                weak_points[concept_id] = int(weak_points.get(concept_id, 0)) + 1

        profile["weak_points"] = {key: value for key, value in weak_points.items() if value > 0}
        profile["mastered_concepts"] = sorted(mastered)
        profile["updated_at"] = now_iso()
        self._save_profile(profile)
        return AgentResult(
            agent="StudentProfileAgent",
            data={"profile": self.summarize_profile(student_id)},
            messages=["已根据答题诊断更新学生画像。"],
        )

    def summarize_profile(self, student_id: str = "S001") -> dict[str, Any]:
        profile = self.get_profile(student_id)
        weak_counter = Counter(profile.get("weak_points", {}))
        return {
            "student_id": student_id,
            "current_goal": profile.get("current_goal", ""),
            "learned_concepts": profile.get("learned_concepts", []),
            "mastered_concepts": profile.get("mastered_concepts", []),
            "weak_points": [item for item, _ in weak_counter.most_common()],
            "weak_point_scores": dict(weak_counter.most_common()),
            "answered_count": len(profile.get("question_history", [])),
        }

    def _load_profiles(self) -> dict[str, Any]:
        try:
            data = json.loads(self.profile_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        return data if isinstance(data, dict) else {}

    def _save_profile(self, profile: dict[str, Any]) -> None:
        profiles = self._load_profiles()
        profiles[profile["student_id"]] = profile
        self.profile_path.write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")

