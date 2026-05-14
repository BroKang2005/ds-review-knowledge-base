from __future__ import annotations

from math import ceil


def generate_review_plan(kb: dict, weak_points: list[dict], days: int = 7, daily_limit: int = 3) -> list[dict]:
    concept_by_id = {item["id"]: item for item in kb["concepts"]}
    mastery_by_id = {
        item["knowledge_id"]: item
        for item in kb.get("student_mastery", [])
        if item.get("student_id") == "S001"
    }

    ranked = []
    for weak_point in weak_points:
        concept_id = weak_point.get("knowledge_id")
        concept = concept_by_id.get(concept_id)
        if not concept:
            continue
        mastery_score = mastery_by_id.get(concept_id, {}).get("mastery_score", 0.5)
        priority = concept.get("importance", 3) * 2 + concept.get("exam_frequency", 3) - mastery_score * 5
        ranked.append((priority, concept, weak_point))
    ranked.sort(key=lambda item: item[0], reverse=True)

    if not ranked:
        ranked = [
            (
                concept.get("importance", 3) + concept.get("exam_frequency", 3),
                concept,
                {},
            )
            for concept in kb["concepts"]
            if concept.get("importance", 0) >= 5
        ][: days * daily_limit]

    plan = [{"day": day, "tasks": []} for day in range(1, days + 1)]
    for index, (_, concept, weak_point) in enumerate(ranked[: days * daily_limit]):
        day_index = min(days - 1, index // daily_limit)
        questions = [
            item["question_id"]
            for item in kb["questions"]
            if concept["id"] in item.get("knowledge_points", [])
        ][:3]
        plan[day_index]["tasks"].append(
            {
                "knowledge_id": concept["id"],
                "name": concept["name"],
                "task_type": "review_and_practice",
                "priority_reason": _priority_reason(concept, weak_point),
                "suggested_questions": questions,
            }
        )

    review_day = min(days, max(1, ceil(days * 0.8)))
    plan[review_day - 1]["tasks"].append(
        {
            "knowledge_id": "MIXED_REVIEW",
            "name": "错题复盘与综合测验",
            "task_type": "mixed_review",
            "priority_reason": "集中检查前几天暴露的高频错因。",
            "suggested_questions": [],
        }
    )
    return plan


def _priority_reason(concept: dict, weak_point: dict) -> str:
    return (
        f"重要度 {concept.get('importance')}，考试频率 {concept.get('exam_frequency')}，"
        f"近期错题数 {weak_point.get('wrong_count', 1)}。"
    )
