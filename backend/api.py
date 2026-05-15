from __future__ import annotations

from backend.services import ReviewService


service = ReviewService()


def answer_question(student_id: str, question: str) -> dict:
    return service.answer_question(student_id, question)


def recommend_questions(student_id: str, concept_id: str | None = None) -> dict:
    return service.recommend_questions(student_id, concept_id)


def submit_answer(student_id: str, question_id: str, student_answer: str) -> dict:
    return service.submit_answer(student_id, question_id, student_answer)


def generate_learning_path(student_id: str, target_concept_id: str) -> dict:
    return service.generate_learning_path(student_id, target_concept_id)


def generate_summary(student_id: str) -> dict:
    return service.generate_summary(student_id)


def list_agent_apis() -> list[dict]:
    return service.list_agent_apis()


def call_agent_api(endpoint_name: str, payload: dict | None = None) -> dict:
    return service.call_agent_api(endpoint_name, payload or {})
