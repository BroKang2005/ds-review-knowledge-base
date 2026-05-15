from __future__ import annotations

from collections import defaultdict
import re
from typing import Any

from agents.schemas import compact_concept, compact_question, concept_id, question_concept_ids, question_id


STOP_WORDS = {
    "怎么",
    "如何",
    "什么",
    "为什么",
    "一下",
    "理解",
    "介绍",
    "讲讲",
    "区别",
    "关系",
    "算法",
    "知识点",
    "题目",
    "复习",
}


ALIASES: dict[str, list[str]] = {
    "dijkstra": ["DS_GRAPH_005", "DS_GRAPH_005_A01", "DS_GRAPH_005_A02", "最短路径", "单源最短路径"],
    "迪ijkstra": ["DS_GRAPH_005", "DS_GRAPH_005_A01", "最短路径"],
    "迪杰斯特拉": ["DS_GRAPH_005", "DS_GRAPH_005_A01", "最短路径"],
    "floyd": ["DS_GRAPH_005", "DS_GRAPH_005_A03", "最短路径", "多源最短路径"],
    "最短路": ["DS_GRAPH_005", "最短路径"],
    "最短路径": ["DS_GRAPH_005"],
    "prim": ["DS_GRAPH_004", "最小生成树"],
    "kruskal": ["DS_GRAPH_004", "最小生成树"],
    "最小生成树": ["DS_GRAPH_004"],
    "dfs": ["DS_GRAPH_002", "深度优先"],
    "深度优先": ["DS_GRAPH_002"],
    "bfs": ["DS_GRAPH_003", "广度优先"],
    "广度优先": ["DS_GRAPH_003"],
    "栈": ["DS_STACK_MODULE", "DS_STACK_001", "后进先出", "LIFO"],
    "队列": ["DS_STACK_004", "DS_STACK_005", "先进先出", "FIFO"],
    "循环队列": ["DS_STACK_005"],
    "二叉树": ["DS_TREE_001", "DS_TREE_MODULE", "树与二叉树"],
    "遍历": ["DS_TREE_002", "DS_GRAPH_002", "DS_GRAPH_003"],
    "哈夫曼": ["DS_TREE_005", "哈夫曼树", "哈夫曼编码"],
    "查找": ["DS_SEARCH_MODULE"],
    "哈希": ["DS_SEARCH_004", "散列表", "哈希表"],
    "散列": ["DS_SEARCH_004", "散列表", "哈希表"],
    "折半": ["DS_SEARCH_002", "二分查找", "折半查找"],
    "二分查找": ["DS_SEARCH_002", "折半查找"],
    "排序": ["DS_SORT_MODULE"],
    "快速排序": ["DS_SORT_002", "快排"],
    "快排": ["DS_SORT_002", "快速排序"],
    "堆排序": ["DS_SORT_003", "堆"],
    "归并排序": ["DS_SORT_004", "归并"],
    "稳定性": ["DS_SORT_005", "排序稳定性"],
    "kmp": ["DS_STRING_002", "KMP", "next数组"],
    "next": ["DS_STRING_002", "KMP", "next数组"],
    "串": ["DS_STRING_MODULE", "字符串"],
    "数组": ["DS_STRING_003", "数组"],
    "线性表": ["DS_LIST_MODULE", "顺序表", "链表"],
    "顺序表": ["DS_LIST_001"],
    "链表": ["DS_LIST_002", "单链表", "双链表"],
}


class KnowledgeRetrievalAgent:
    """Keyword and graph retrieval over the JSON knowledge base."""

    def __init__(self, kb: dict[str, Any]):
        self.kb = kb
        self.concepts = kb.get("concepts", [])
        self.questions = kb.get("questions", [])
        self.relations = kb.get("relations", [])
        self.concept_by_id = {concept_id(item): item for item in self.concepts}
        self.question_by_id = {question_id(item): item for item in self.questions}
        self.children = defaultdict(list)
        for item in self.concepts:
            parent = item.get("parent_id")
            if parent:
                self.children[parent].append(concept_id(item))

    def search_concepts(self, keyword: str, limit: int = 8) -> list[dict[str, Any]]:
        keyword = (keyword or "").strip()
        if not keyword:
            return self._important_concepts(limit)
        if keyword in self.concept_by_id:
            return [compact_concept(self.concept_by_id[keyword])]

        normalized_query = self._normalize(keyword)
        terms = self._expand_terms(keyword)
        scores: dict[str, float] = defaultdict(float)

        for item in self.concepts:
            cid = concept_id(item)
            text = self._concept_text(item)
            normalized_text = self._normalize(text)
            score = 0.0
            if normalized_query and normalized_query in normalized_text:
                score += 30
            for term in terms:
                if term in self.concept_by_id and term == cid:
                    score += 45
                elif self._normalize(term) and self._normalize(term) in normalized_text:
                    score += 12
                else:
                    score += self._soft_overlap(term, text)
            score += self._soft_overlap(keyword, text) * 1.5
            if score:
                score += int(item.get("importance", 0)) * 0.8 + int(item.get("exam_frequency", 0)) * 0.8
                scores[cid] += score

        for question in self.questions:
            question_text = " ".join(
                str(question.get(field, ""))
                for field in ["stem", "analysis", "answer", "question_type", "type"]
            )
            qscore = self._soft_overlap(keyword, question_text)
            if qscore >= 2:
                for cid in question_concept_ids(question):
                    scores[cid] += qscore * 1.5

        ranked = sorted(
            ((score, self.concept_by_id[cid]) for cid, score in scores.items() if cid in self.concept_by_id),
            key=lambda item: item[0],
            reverse=True,
        )
        if not ranked:
            return self._module_fallback(keyword, limit)
        return [compact_concept(item) for _, item in ranked[:limit]]

    def get_concept(self, target_concept_id: str) -> dict[str, Any]:
        return compact_concept(self.concept_by_id.get(target_concept_id, {}))

    def get_atomic_concepts(self, target_concept_id: str) -> list[dict[str, Any]]:
        ids = self.get_descendant_ids(target_concept_id)
        return [compact_concept(self.concept_by_id[item]) for item in ids if self.concept_by_id.get(item, {}).get("granularity") == "atomic"]

    def get_related_questions(self, target_concept_id: str, limit: int = 10) -> list[dict[str, Any]]:
        target_ids = {target_concept_id, *self.get_descendant_ids(target_concept_id)}
        results = []
        for question in self.questions:
            if any(item in target_ids for item in question_concept_ids(question)):
                results.append(compact_question(question))
            if len(results) >= limit:
                break
        return results

    def get_prerequisites(self, target_concept_id: str) -> list[dict[str, Any]]:
        concept = self.concept_by_id.get(target_concept_id, {})
        ids = list(concept.get("prerequisites", []))
        ids.extend(rel.get("source") for rel in self.relations if rel.get("relation") == "prerequisite" and rel.get("target") == target_concept_id)
        return [compact_concept(self.concept_by_id[item]) for item in dict.fromkeys(ids) if item in self.concept_by_id]

    def get_confusing_concepts(self, target_concept_id: str) -> list[dict[str, Any]]:
        relation_names = {"confuses_with", "contrast_with", "similar_to"}
        ids = []
        for rel in self.relations:
            if rel.get("relation") not in relation_names:
                continue
            if rel.get("source") == target_concept_id:
                ids.append(rel.get("target"))
            elif rel.get("target") == target_concept_id:
                ids.append(rel.get("source"))
        return [compact_concept(self.concept_by_id[item]) for item in dict.fromkeys(ids) if item in self.concept_by_id]

    def retrieve(self, query: str) -> dict[str, Any]:
        concepts = self.search_concepts(query, limit=5)
        primary = concepts[0] if concepts else {}
        cid = primary.get("id", "")
        return {
            "query": query,
            "primary_concept": primary,
            "related_concepts": concepts,
            "atomic_concepts": self.get_atomic_concepts(cid)[:8] if cid else [],
            "prerequisites": self.get_prerequisites(cid) if cid else [],
            "confusing_concepts": self.get_confusing_concepts(cid) if cid else [],
            "questions": self.get_related_questions(cid, limit=5) if cid else [],
        }

    def get_question(self, target_question_id: str) -> dict[str, Any]:
        return self.question_by_id.get(target_question_id, {})

    def get_descendant_ids(self, target_concept_id: str) -> list[str]:
        descendants = []
        stack = list(self.children.get(target_concept_id, []))
        while stack:
            current = stack.pop(0)
            descendants.append(current)
            stack.extend(self.children.get(current, []))
        return descendants

    def _important_concepts(self, limit: int) -> list[dict[str, Any]]:
        ranked = sorted(self.concepts, key=lambda item: (item.get("importance", 0), item.get("exam_frequency", 0)), reverse=True)
        return [compact_concept(item) for item in ranked[:limit]]

    def _concept_text(self, concept: dict[str, Any]) -> str:
        values = [
            concept.get("id", ""),
            concept.get("name", ""),
            concept.get("module", ""),
            concept.get("topic", ""),
            concept.get("description", ""),
            " ".join(concept.get("related_concepts", [])),
            " ".join(concept.get("formulas", [])),
            " ".join(concept.get("common_mistakes", [])),
            concept.get("learning_suggestion", ""),
        ]
        return " ".join(str(item) for item in values if item)

    def _expand_terms(self, query: str) -> list[str]:
        normalized = self._normalize(query)
        terms = [query, normalized]
        terms.extend(self._tokenize(query))
        for alias, expansions in ALIASES.items():
            if self._normalize(alias) in normalized:
                terms.append(alias)
                terms.extend(expansions)
        seen = set()
        output = []
        for term in terms:
            term = str(term).strip()
            if term and term not in STOP_WORDS and term not in seen:
                output.append(term)
                seen.add(term)
        return output

    def _tokenize(self, text: str) -> list[str]:
        raw = re.split(r"[\s,，。！？?、；;：:（）()【】\[\]<>《》\"']+", text.lower())
        tokens = []
        for item in raw:
            item = item.strip()
            if item and item not in STOP_WORDS:
                tokens.append(item)
        return tokens

    def _normalize(self, text: str) -> str:
        return re.sub(r"[\W_]+", "", str(text).lower(), flags=re.UNICODE)

    def _soft_overlap(self, query: str, text: str) -> float:
        query_norm = self._normalize(query)
        text_norm = self._normalize(text)
        if not query_norm or not text_norm:
            return 0.0
        if query_norm in text_norm:
            return min(20.0, len(query_norm) * 2.0)

        query_chars = {char for char in query_norm if char not in STOP_WORDS and not char.isdigit()}
        if not query_chars:
            return 0.0
        text_chars = set(text_norm)
        char_overlap = len(query_chars & text_chars) / max(1, len(query_chars))

        query_bigrams = {query_norm[i : i + 2] for i in range(len(query_norm) - 1)}
        text_bigrams = {text_norm[i : i + 2] for i in range(len(text_norm) - 1)}
        bigram_overlap = len(query_bigrams & text_bigrams) / max(1, len(query_bigrams))

        score = char_overlap * 4 + bigram_overlap * 10
        return score if score >= 1.8 else 0.0

    def _module_fallback(self, query: str, limit: int) -> list[dict[str, Any]]:
        expanded = self._expand_terms(query)
        for term in expanded:
            normalized = self._normalize(term)
            if not normalized:
                continue
            matches = [
                item
                for item in self.concepts
                if normalized in self._normalize(item.get("module", ""))
                or normalized in self._normalize(item.get("topic", ""))
                or normalized in self._normalize(item.get("name", ""))
            ]
            if matches:
                ranked = sorted(matches, key=lambda item: (item.get("importance", 0), item.get("exam_frequency", 0)), reverse=True)
                return [compact_concept(item) for item in ranked[:limit]]
        return self._important_concepts(limit)
