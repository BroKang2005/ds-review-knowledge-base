from __future__ import annotations

from typing import Any

from agents.schemas import AgentResult, compact_concept, compact_question
from src.kb_search import get_prerequisites, get_questions_by_concept, get_related_concepts, search_concepts


class KnowledgeRetrievalAgent:
    """Retrieves concepts, questions, prerequisites, and related nodes from the KB."""

    def __init__(self, kb: dict[str, Any]):
        self.kb = kb
        self.concept_by_id = {item["id"]: item for item in kb.get("concepts", [])}
        self.question_by_id = {item["question_id"]: item for item in kb.get("questions", [])}

    def retrieve(
        self,
        query: str = "",
        concept_id: str = "",
        question_id: str = "",
        limit: int = 5,
    ) -> AgentResult:
        concepts = self._resolve_concepts(query=query, concept_id=concept_id, question_id=question_id, limit=limit)
        primary = concepts[0] if concepts else {}
        primary_id = primary.get("id", "")
        prerequisites = get_prerequisites(self.kb, primary_id) if primary_id else []
        related = get_related_concepts(self.kb, primary_id) if primary_id else []
        questions = self._questions_for_concepts([item["id"] for item in concepts], limit=limit)
        confuses_with = self._related_by_type(primary_id, "confuses_with") if primary_id else []
        data = {
            "query": query,
            "primary_concept": compact_concept(primary) if primary else {},
            "related_concepts": [compact_concept(item) for item in concepts],
            "prerequisites": [compact_concept(item) for item in prerequisites],
            "associated_concepts": [compact_concept(item) for item in related[:limit]],
            "confuses_with": [compact_concept(item) for item in confuses_with[:limit]],
            "questions": [compact_question(item) for item in questions],
        }
        return AgentResult(
            agent="KnowledgeRetrievalAgent",
            data=data,
            messages=[f"检索到 {len(concepts)} 个相关知识点和 {len(questions)} 道关联题目。"],
        )

    def get_question(self, question_id: str) -> dict[str, Any]:
        return self.question_by_id.get(question_id, {})

    def _resolve_concepts(self, query: str, concept_id: str, question_id: str, limit: int) -> list[dict[str, Any]]:
        if concept_id and concept_id in self.concept_by_id:
            return [self.concept_by_id[concept_id]]
        if question_id and question_id in self.question_by_id:
            ids = self.question_by_id[question_id].get("knowledge_points", [])
            return [self.concept_by_id[item] for item in ids if item in self.concept_by_id]
        if query:
            exact = self.concept_by_id.get(query.strip())
            if exact:
                return [exact]
            results = search_concepts(self.kb, query)[:limit]
            if results:
                return results
        return sorted(
            [item for item in self.kb.get("concepts", []) if item.get("granularity") == "atomic"],
            key=lambda item: (item.get("importance", 0), item.get("exam_frequency", 0)),
            reverse=True,
        )[:limit]

    def _questions_for_concepts(self, concept_ids: list[str], limit: int) -> list[dict[str, Any]]:
        seen = set()
        questions: list[dict[str, Any]] = []
        for concept_id in concept_ids:
            for question in get_questions_by_concept(self.kb, concept_id):
                question_id = question.get("question_id")
                if question_id not in seen:
                    questions.append(question)
                    seen.add(question_id)
                if len(questions) >= limit:
                    return questions
        return questions

    def _related_by_type(self, concept_id: str, relation_type: str) -> list[dict[str, Any]]:
        ids = []
        for relation in self.kb.get("relations", []):
            if relation.get("relation") != relation_type:
                continue
            if relation.get("source") == concept_id:
                ids.append(relation.get("target"))
            elif relation.get("target") == concept_id:
                ids.append(relation.get("source"))
        return [self.concept_by_id[item] for item in ids if item in self.concept_by_id]

