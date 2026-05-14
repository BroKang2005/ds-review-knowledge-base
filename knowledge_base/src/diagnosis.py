from __future__ import annotations

from collections import defaultdict


def diagnose_student(kb: dict, records: list[dict]) -> dict:
    question_by_id = {item["question_id"]: item for item in kb["questions"]}
    concept_by_id = {item["id"]: item for item in kb["concepts"]}
    error_by_id = {item["error_id"]: item for item in kb["errors"]}
    student_id = records[0].get("student_id", "UNKNOWN") if records else "UNKNOWN"
    grouped: dict[str, dict] = {}
    counts = defaultdict(int)

    for record in records:
        if record.get("is_correct", True):
            continue
        question = question_by_id.get(record.get("question_id"))
        if not question:
            continue
        for concept_id in question.get("knowledge_points", []):
            counts[concept_id] += 1
            concept = concept_by_id.get(concept_id, {})
            error_id = next(iter(question.get("common_errors", [])), None)
            error = error_by_id.get(error_id, {})
            grouped[concept_id] = {
                "knowledge_id": concept_id,
                "name": concept.get("name", concept_id),
                "error_id": error_id,
                "error_name": error.get("name", "待进一步定位的综合性错因"),
                "wrong_count": counts[concept_id],
                "evidence": question.get("stem", ""),
                "suggestion": _build_suggestion(concept, error),
            }

    weak_points = sorted(grouped.values(), key=lambda item: item["wrong_count"], reverse=True)
    return {"student_id": student_id, "weak_points": weak_points}


def _build_suggestion(concept: dict, error: dict) -> str:
    if error.get("remediation"):
        return "；".join(error["remediation"][:2])
    if concept.get("learning_suggestion"):
        return concept["learning_suggestion"]
    return "回到知识点定义、操作过程和典型题，完成针对性练习。"
