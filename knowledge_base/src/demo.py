from __future__ import annotations

import json

from diagnosis import diagnose_student
from kb_loader import load_knowledge_base
from kb_search import get_questions_by_concept, search_concepts
from planner import generate_review_plan


def show(title: str, payload) -> None:
    print(f"\n=== {title} ===")
    if isinstance(payload, str):
        print(payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    kb = load_knowledge_base()
    show("知识库规模", {
        "concepts": len(kb["concepts"]),
        "atomic_concepts": sum(1 for item in kb["concepts"] if item.get("granularity") == "atomic"),
        "questions": len(kb["questions"]),
        "relations": len(kb["relations"]),
        "errors": len(kb["errors"]),
    })

    results = search_concepts(kb, "二叉树")
    show("搜索“二叉树”", [{"id": item["id"], "name": item["name"], "module": item["module"]} for item in results])

    concept_id = results[0]["id"] if results else "DS_TREE_001"
    questions = get_questions_by_concept(kb, concept_id)
    show(f"{concept_id} 相关题目", questions[:2])

    queue_question = next(
        question
        for question in kb["questions"]
        if "DS_STACK_005_A02" in question.get("knowledge_points", [])
    )
    records = [
        {
            "student_id": "S001",
            "question_id": queue_question["question_id"],
            "is_correct": False,
            "student_answer": "front == rear 表示队满",
        }
    ]
    diagnosis = diagnose_student(kb, records)
    show("根据错题定位到原子知识点", {
        "wrong_question": queue_question["question_id"],
        "bound_atomic_points": queue_question["knowledge_points"],
        "diagnosis": diagnosis,
    })

    plan = generate_review_plan(kb, diagnosis["weak_points"], days=7, daily_limit=2)
    show("7天复习计划", plan)


if __name__ == "__main__":
    main()
