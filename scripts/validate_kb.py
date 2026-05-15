from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.services import load_knowledge_base


def main() -> None:
    kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
    concept_ids = {item.get("id") for item in kb["concepts"]}
    atomic_ids = {item.get("id") for item in kb["concepts"] if item.get("granularity") == "atomic"}
    problems = []
    for question in kb["questions"]:
        for cid in question.get("knowledge_points", question.get("concept_ids", [])):
            if cid not in concept_ids:
                problems.append(f"Question {question.get('question_id', question.get('id'))} references missing concept {cid}")
            elif cid not in atomic_ids:
                problems.append(f"Question {question.get('question_id', question.get('id'))} references non-atomic concept {cid}")
    for relation in kb["relations"]:
        if relation.get("source") not in concept_ids:
            problems.append(f"Relation source missing: {relation.get('source')}")
        if relation.get("target") not in concept_ids:
            problems.append(f"Relation target missing: {relation.get('target')}")
    if problems:
        print("Knowledge base validation failed:")
        for item in problems[:50]:
            print("-", item)
        raise SystemExit(1)
    print("Knowledge base validation passed.")


if __name__ == "__main__":
    main()

