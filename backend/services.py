from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.schemas import AppPaths


def load_json(path: str | Path, default: Any) -> Any:
    path = Path(path)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: str | Path, payload: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_knowledge_base(data_dir: str | Path) -> dict[str, Any]:
    data_dir = Path(data_dir)
    return {
        "concepts": load_json(data_dir / "concepts.json", []),
        "questions": load_json(data_dir / "questions.json", []),
        "relations": load_json(data_dir / "relations.json", []),
        "errors": load_json(data_dir / "errors.json", []),
        "learning_paths": load_json(data_dir / "learning_paths.json", []),
        "student_mastery": load_json(data_dir / "student_mastery_sample.json", []),
    }


def ensure_student_data(data_dir: str | Path) -> None:
    data_dir = Path(data_dir)
    defaults = {
        "student_profiles.json": {
            "demo_student": {
                "student_id": "demo_student",
                "learned_concepts": [],
                "weak_concepts": [],
                "wrong_questions": [],
                "answer_history": [],
                "current_goal": "期末复习数据结构",
            }
        },
        "answer_records.json": [],
        "review_sessions.json": [],
        "wrong_questions.json": [],
    }
    for filename, payload in defaults.items():
        path = data_dir / filename
        if not path.exists():
            write_json(path, payload)


class ReviewService:
    """Stable backend facade used by Streamlit pages and tests."""

    def __init__(self, paths: AppPaths | None = None):
        from orchestrator.review_orchestrator import ReviewOrchestrator

        self.paths = paths or AppPaths.default()
        ensure_student_data(self.paths.student_data_dir)
        self.orchestrator = ReviewOrchestrator(
            kb_data_dir=self.paths.kb_data_dir,
            student_data_dir=self.paths.student_data_dir,
        )
        from backend.agent_api_manager import AgentAPIManager

        self.agent_api_manager = AgentAPIManager(
            self.orchestrator,
            log_path=str(self.paths.student_data_dir / "agent_api_calls.json"),
        )

    def answer_question(self, student_id: str, question: str) -> dict[str, Any]:
        return self.orchestrator.answer_question(student_id, question)

    def recommend_questions(self, student_id: str, concept_id: str | None = None) -> dict[str, Any]:
        return self.orchestrator.recommend_questions(student_id, concept_id)

    def submit_answer(self, student_id: str, question_id: str, student_answer: str) -> dict[str, Any]:
        return self.orchestrator.submit_answer(student_id, question_id, student_answer)

    def generate_learning_path(self, student_id: str, target_concept_id: str) -> dict[str, Any]:
        return self.orchestrator.generate_learning_path(student_id, target_concept_id)

    def generate_summary(self, student_id: str) -> dict[str, Any]:
        return self.orchestrator.generate_summary(student_id)

    def get_profile(self, student_id: str) -> dict[str, Any]:
        return self.orchestrator.profile_agent.summarize(student_id)

    def list_modules(self) -> list[str]:
        modules = {item.get("module") for item in self.orchestrator.kb.get("concepts", []) if item.get("module")}
        return sorted(modules)

    def list_concepts_by_module(self, module: str) -> list[dict[str, Any]]:
        return [
            self.orchestrator.retrieval_agent.get_concept(item.get("id"))
            for item in self.orchestrator.kb.get("concepts", [])
            if item.get("module") == module and item.get("granularity") in {"topic", "concept"}
        ]

    def list_agent_apis(self) -> list[dict[str, Any]]:
        return self.agent_api_manager.list_endpoints()

    def call_agent_api(self, endpoint_name: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.agent_api_manager.call(endpoint_name, payload or {})
