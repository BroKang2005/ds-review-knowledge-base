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
from src.kb_loader import DEFAULT_DATA_DIR, load_knowledge_base


class ReviewOrchestrator:
    """Coordinates all review agents for one student-facing workflow."""

    def __init__(
        self,
        data_dir: str | Path = DEFAULT_DATA_DIR,
        profile_path: str | Path | None = None,
    ):
        self.data_dir = Path(data_dir)
        self.kb = load_knowledge_base(self.data_dir)
        self.profile_agent = StudentProfileAgent(profile_path or self.data_dir / "student_profiles.json")
        self.retrieval_agent = KnowledgeRetrievalAgent(self.kb)
        self.explanation_agent = ExplanationAgent()
        self.question_agent = QuestionRecommendationAgent(self.kb)
        self.error_agent = ErrorDiagnosisAgent(self.kb)
        self.path_agent = LearningPathAgent(self.kb)
        self.summary_agent = SummaryAgent()

    def start_review(self, user_query: str, student_id: str = "S001", goal: str = "") -> dict[str, Any]:
        messages = []
        if goal:
            messages.extend(self.profile_agent.set_goal(student_id, goal).messages)
        profile = self.profile_agent.summarize_profile(student_id)
        retrieval_result = self.retrieval_agent.retrieve(query=user_query)
        retrieval = retrieval_result.data
        concept_ids = [item["id"] for item in retrieval.get("related_concepts", []) if item.get("id")]
        self.profile_agent.record_learning(student_id, concept_ids[:1])
        explanation = self.explanation_agent.explain(retrieval, profile, user_query).data
        path = self.path_agent.plan(concept_ids[:1], profile).data
        recommendations = self.question_agent.recommend(
            concept_ids=concept_ids,
            student_profile=profile,
            goal=goal or profile.get("current_goal", ""),
        ).data
        messages.extend(retrieval_result.messages)
        return {
            "student_id": student_id,
            "query": user_query,
            "profile": profile,
            "retrieval": retrieval,
            "explanation": explanation,
            "learning_path": path,
            "recommendations": recommendations,
            "messages": messages,
        }

    def submit_answer(
        self,
        student_id: str,
        question_id: str,
        student_answer: str,
        session: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        question = self.retrieval_agent.get_question(question_id)
        if not question:
            raise ValueError(f"Unknown question_id: {question_id}")
        diagnosis = self.error_agent.diagnose(question, student_answer).data
        profile_update = self.profile_agent.update_after_diagnosis(student_id, diagnosis).data
        profile = profile_update["profile"]
        full_profile = self.profile_agent.get_profile(student_id)
        involved = diagnosis.get("involved_concepts", [])
        next_questions = self.question_agent.recommend(involved, full_profile, limit=3).data
        updated_session = dict(session or {})
        updated_session.update(
            {
                "student_id": student_id,
                "diagnosis": diagnosis,
                "profile_after_update": profile,
                "next_recommendations": next_questions,
            }
        )
        summary = self.summary_agent.summarize(updated_session, profile).data
        updated_session["summary"] = summary
        return updated_session
