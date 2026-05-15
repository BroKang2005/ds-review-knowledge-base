from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from agents.schemas import now_iso, question_id


class StudentProfileAgent:
    """Read and update student profile, answer history, and wrong-question records."""

    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.profile_path = self.data_dir / "student_profiles.json"
        self.answer_path = self.data_dir / "answer_records.json"
        self.wrong_path = self.data_dir / "wrong_questions.json"
        self.session_path = self.data_dir / "review_sessions.json"
        for path, default in [
            (self.profile_path, {}),
            (self.answer_path, []),
            (self.wrong_path, []),
            (self.session_path, []),
        ]:
            if not path.exists():
                path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_profile(self, student_id: str) -> dict[str, Any]:
        profiles = self._read_json(self.profile_path, {})
        profile = profiles.get(student_id)
        if profile:
            return profile
        profile = {
            "student_id": student_id,
            "learned_concepts": [],
            "weak_concepts": [],
            "wrong_questions": [],
            "answer_history": [],
            "current_goal": "期末复习数据结构",
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        profiles[student_id] = profile
        self._write_json(self.profile_path, profiles)
        return profile

    def update_goal(self, student_id: str, goal: str) -> dict[str, Any]:
        profile = self.get_profile(student_id)
        profile["current_goal"] = goal or profile.get("current_goal", "")
        profile["updated_at"] = now_iso()
        self._save_profile(profile)
        return profile

    def record_reviewed_concepts(self, student_id: str, concept_ids: list[str]) -> dict[str, Any]:
        profile = self.get_profile(student_id)
        learned = set(profile.get("learned_concepts", []))
        learned.update(item for item in concept_ids if item)
        profile["learned_concepts"] = sorted(learned)
        profile["updated_at"] = now_iso()
        self._save_profile(profile)
        return profile

    def update_answer_record(self, student_id: str, question: dict[str, Any], student_answer: str, diagnosis: dict[str, Any]) -> dict[str, Any]:
        profile = self.get_profile(student_id)
        qid = question_id(question)
        concept_ids = diagnosis.get("involved_concepts", [])
        record = {
            "student_id": student_id,
            "question_id": qid,
            "student_answer": student_answer,
            "is_correct": bool(diagnosis.get("is_correct")),
            "concept_ids": concept_ids,
            "answered_at": now_iso(),
        }

        answer_records = self._read_json(self.answer_path, [])
        answer_records.append(record)
        self._write_json(self.answer_path, answer_records)

        profile.setdefault("answer_history", []).append(record)
        if record["is_correct"]:
            weak = set(profile.get("weak_concepts", []))
            weak.difference_update(concept_ids)
            profile["weak_concepts"] = sorted(weak)
        else:
            weak = set(profile.get("weak_concepts", []))
            weak.update(concept_ids)
            profile["weak_concepts"] = sorted(weak)
            wrong_questions = set(profile.get("wrong_questions", []))
            wrong_questions.add(qid)
            profile["wrong_questions"] = sorted(wrong_questions)
            wrong_records = self._read_json(self.wrong_path, [])
            wrong_records.append({**record, "error_reasons": diagnosis.get("error_reasons", [])})
            self._write_json(self.wrong_path, wrong_records)

        profile["updated_at"] = now_iso()
        self._save_profile(profile)
        return profile

    def summarize(self, student_id: str) -> dict[str, Any]:
        profile = self.get_profile(student_id)
        history = profile.get("answer_history", [])
        total = len(history)
        correct = sum(1 for item in history if item.get("is_correct"))
        weak_counter = Counter()
        for item in history:
            if not item.get("is_correct"):
                weak_counter.update(item.get("concept_ids", []))
        return {
            "student_id": student_id,
            "current_goal": profile.get("current_goal", ""),
            "learned_concepts": profile.get("learned_concepts", []),
            "mastered_concepts": self._mastered_from_history(history),
            "weak_concepts": [item for item, _ in weak_counter.most_common()] or profile.get("weak_concepts", []),
            "weak_scores": dict(weak_counter.most_common()),
            "wrong_question_count": len(profile.get("wrong_questions", [])),
            "answer_count": total,
            "recent_accuracy": round(correct / total, 2) if total else 0.0,
        }

    def record_session(self, student_id: str, session: dict[str, Any]) -> None:
        sessions = self._read_json(self.session_path, [])
        sessions.append({"student_id": student_id, "created_at": now_iso(), "session": session})
        self._write_json(self.session_path, sessions)

    def get_sessions(self, student_id: str) -> list[dict[str, Any]]:
        return [item for item in self._read_json(self.session_path, []) if item.get("student_id") == student_id]

    def _mastered_from_history(self, history: list[dict[str, Any]]) -> list[str]:
        counts = Counter()
        correct = Counter()
        for item in history:
            for cid in item.get("concept_ids", []):
                counts[cid] += 1
                if item.get("is_correct"):
                    correct[cid] += 1
        return sorted(cid for cid, total in counts.items() if total and correct[cid] / total >= 0.8)

    def _save_profile(self, profile: dict[str, Any]) -> None:
        profiles = self._read_json(self.profile_path, {})
        profiles[profile["student_id"]] = profile
        self._write_json(self.profile_path, profiles)

    def _read_json(self, path: Path, default: Any) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            return default

    def _write_json(self, path: Path, payload: Any) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

