from __future__ import annotations

from pathlib import Path
from typing import Any

from agents.error_diagnosis_agent import ErrorDiagnosisAgent
from agents.explanation_agent import ExplanationAgent
from agents.knowledge_retrieval_agent import KnowledgeRetrievalAgent
from agents.learning_path_agent import LearningPathAgent
from agents.question_recommendation_agent import QuestionRecommendationAgent
from agents.student_profile_agent import StudentProfileAgent
from agents.summary_agent import SummaryAgent
from backend.services import load_knowledge_base


class ReviewOrchestrator:
    """Coordinate all agents and expose a compact application API."""

    def __init__(self, kb_data_dir: str | Path, student_data_dir: str | Path):
        self.kb = load_knowledge_base(kb_data_dir)
        self.profile_agent = StudentProfileAgent(student_data_dir)
        self.retrieval_agent = KnowledgeRetrievalAgent(self.kb)
        self.explanation_agent = ExplanationAgent()
        self.question_agent = QuestionRecommendationAgent(self.kb, self.retrieval_agent)
        self.error_agent = ErrorDiagnosisAgent(self.kb)
        self.learning_path_agent = LearningPathAgent(self.retrieval_agent)
        self.summary_agent = SummaryAgent()
        self.last_sessions: dict[str, dict[str, Any]] = {}

    def answer_question(self, student_id: str, question: str) -> dict[str, Any]:
        profile = self.profile_agent.get_profile(student_id)
        retrieval = self.retrieval_agent.retrieve(question)
        primary = retrieval.get("primary_concept", {})
        concept_ids = [item.get("id") for item in retrieval.get("related_concepts", []) if item.get("id")]
        if primary.get("id"):
            self.profile_agent.record_reviewed_concepts(student_id, [primary["id"]])
        explanation = self.explanation_agent.explain(primary, profile)
        recommendations = self.question_agent.recommend(profile, concept_id=primary.get("id"), limit=3)
        learning_path = self.learning_path_agent.plan(profile, primary.get("id")) if primary.get("id") else {}
        session = {
            "student_id": student_id,
            "question": question,
            "retrieval": retrieval,
            "explanation": explanation,
            "recommendations": recommendations,
            "learning_path": learning_path,
            "concept_ids": concept_ids,
        }
        self.last_sessions[student_id] = session
        self.profile_agent.record_session(student_id, session)
        return session

    def recommend_questions(self, student_id: str, concept_id: str | None = None) -> dict[str, Any]:
        profile = self.profile_agent.get_profile(student_id)
        return self.question_agent.recommend(profile, concept_id=concept_id)

    def submit_answer(self, student_id: str, question_id: str, student_answer: str) -> dict[str, Any]:
        question = self.retrieval_agent.get_question(question_id)
        if not question:
            return {"error": f"未找到题目：{question_id}"}
        diagnosis = self.error_agent.diagnose(question, student_answer)
        updated_profile = self.profile_agent.update_answer_record(student_id, question, student_answer, diagnosis)
        profile_summary = self.profile_agent.summarize(student_id)
        next_questions = self.question_agent.recommend(updated_profile, concept_id=None, limit=3)
        result = {
            "diagnosis": diagnosis,
            "profile": profile_summary,
            "next_recommendations": next_questions,
            "next_advice": self.summary_agent.summarize(profile_summary, self.profile_agent.get_sessions(student_id))["next_suggestions"],
        }
        self.profile_agent.record_session(student_id, {"answer_result": result})
        return result

    def generate_learning_path(self, student_id: str, target_concept_id: str) -> dict[str, Any]:
        profile = self.profile_agent.summarize(student_id)
        return self.learning_path_agent.plan(profile, target_concept_id)

    def generate_summary(self, student_id: str) -> dict[str, Any]:
        profile = self.profile_agent.summarize(student_id)
        sessions = self.profile_agent.get_sessions(student_id)
        return self.summary_agent.summarize(profile, sessions)

