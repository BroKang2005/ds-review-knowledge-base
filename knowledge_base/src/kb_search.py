from __future__ import annotations


def search_concepts(kb: dict, keyword: str) -> list[dict]:
    keyword = keyword.strip().lower()
    if not keyword:
        return []
    results = []
    for concept in kb["concepts"]:
        haystack = " ".join(
            [
                concept.get("id", ""),
                concept.get("name", ""),
                concept.get("module", ""),
                concept.get("topic", ""),
                concept.get("description", ""),
                " ".join(concept.get("related_concepts", [])),
            ]
        ).lower()
        if keyword in haystack:
            results.append(concept)
    return results


def get_concepts_by_module(kb: dict, module: str) -> list[dict]:
    return [concept for concept in kb["concepts"] if concept.get("module") == module]


def get_concepts_by_difficulty(kb: dict, difficulty: int) -> list[dict]:
    return [concept for concept in kb["concepts"] if concept.get("difficulty") == difficulty]


def get_questions_by_concept(kb: dict, concept_id: str) -> list[dict]:
    target_ids = {concept_id, *get_descendant_ids(kb, concept_id)}
    return [
        question
        for question in kb["questions"]
        if any(item in target_ids for item in question.get("knowledge_points", []))
    ]


def get_descendant_ids(kb: dict, concept_id: str) -> list[str]:
    children_by_parent: dict[str, list[str]] = {}
    for concept in kb["concepts"]:
        parent_id = concept.get("parent_id")
        if parent_id:
            children_by_parent.setdefault(parent_id, []).append(concept["id"])

    descendants: list[str] = []
    stack = list(children_by_parent.get(concept_id, []))
    while stack:
        current = stack.pop()
        descendants.append(current)
        stack.extend(children_by_parent.get(current, []))
    return descendants


def get_prerequisites(kb: dict, concept_id: str) -> list[dict]:
    concepts = {concept["id"]: concept for concept in kb["concepts"]}
    concept = concepts.get(concept_id)
    if not concept:
        return []
    return [concepts[item] for item in concept.get("prerequisites", []) if item in concepts]


def get_related_concepts(kb: dict, concept_id: str) -> list[dict]:
    concepts = {concept["id"]: concept for concept in kb["concepts"]}
    related_ids = set()
    for relation in kb["relations"]:
        if relation.get("source") == concept_id:
            related_ids.add(relation.get("target"))
        if relation.get("target") == concept_id:
            related_ids.add(relation.get("source"))
    return [concepts[item] for item in related_ids if item in concepts]


def get_relations_by_concept(kb: dict, concept_id: str) -> list[dict]:
    return [
        relation
        for relation in kb["relations"]
        if relation.get("source") == concept_id or relation.get("target") == concept_id
    ]
