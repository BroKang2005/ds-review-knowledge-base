from __future__ import annotations

import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = BASE_DIR / "data"


def load_json(path: str | Path) -> list | dict:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_knowledge_base(data_dir: str | Path = DEFAULT_DATA_DIR) -> dict[str, Any]:
    data_path = Path(data_dir)
    kb = {
        "concepts": load_json(data_path / "concepts.json"),
        "relations": load_json(data_path / "relations.json"),
        "questions": load_json(data_path / "questions.json"),
        "errors": load_json(data_path / "errors.json"),
        "learning_paths": load_json(data_path / "learning_paths.json"),
        "student_mastery": load_json(data_path / "student_mastery_sample.json"),
    }
    errors = validate_knowledge_base(kb)
    if errors:
        joined = "\n".join(f"- {item}" for item in errors)
        raise ValueError(f"Knowledge base validation failed:\n{joined}")
    return kb


def validate_knowledge_base(kb: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    concepts = kb.get("concepts", [])
    concept_ids = [item.get("id") for item in concepts]
    concept_id_set = set(concept_ids)

    if len(concept_ids) != len(concept_id_set):
        problems.append("Duplicate concept id found.")

    error_ids = {item.get("error_id") for item in kb.get("errors", [])}
    atomic_ids = {item.get("id") for item in concepts if item.get("granularity") == "atomic"}
    allowed_granularity = {"module", "topic", "concept", "atomic"}

    for concept in concepts:
        if concept.get("granularity") not in allowed_granularity:
            problems.append(f"Concept {concept.get('id')} has invalid granularity {concept.get('granularity')}.")
        parent_id = concept.get("parent_id")
        if parent_id and parent_id not in concept_id_set:
            problems.append(f"Concept {concept.get('id')} has missing parent {parent_id}.")
        if concept.get("granularity") == "atomic" and not concept.get("diagnosable"):
            problems.append(f"Atomic concept {concept.get('id')} must be diagnosable.")
        for prerequisite in concept.get("prerequisites", []):
            if prerequisite not in concept_id_set:
                problems.append(f"Concept {concept.get('id')} has missing prerequisite {prerequisite}.")

    for relation in kb.get("relations", []):
        source = relation.get("source")
        target = relation.get("target")
        if source not in concept_id_set:
            problems.append(f"Relation source does not exist: {source}.")
        if target not in concept_id_set:
            problems.append(f"Relation target does not exist: {target}.")

    for question in kb.get("questions", []):
        for concept_id in question.get("knowledge_points", []):
            if concept_id not in concept_id_set:
                problems.append(f"Question {question.get('question_id')} references missing concept {concept_id}.")
            elif concept_id not in atomic_ids:
                problems.append(f"Question {question.get('question_id')} must reference atomic concept {concept_id}.")
        for error_id in question.get("common_errors", []):
            if error_id not in error_ids:
                problems.append(f"Question {question.get('question_id')} references missing error {error_id}.")

    for error in kb.get("errors", []):
        for concept_id in error.get("related_knowledge", []):
            if concept_id not in concept_id_set:
                problems.append(f"Error {error.get('error_id')} references missing concept {concept_id}.")
            elif concept_id not in atomic_ids:
                problems.append(f"Error {error.get('error_id')} must reference atomic concept {concept_id}.")

    return problems


if __name__ == "__main__":
    loaded = load_knowledge_base()
    print(
        "loaded:",
        len(loaded["concepts"]),
        "concepts,",
        len(loaded["questions"]),
        "questions,",
        len(loaded["relations"]),
        "relations",
    )
