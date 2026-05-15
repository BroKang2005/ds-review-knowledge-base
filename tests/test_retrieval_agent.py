from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.knowledge_retrieval_agent import KnowledgeRetrievalAgent
from backend.services import load_knowledge_base


class RetrievalAgentTest(unittest.TestCase):
    def test_search_dijkstra(self):
        kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
        agent = KnowledgeRetrievalAgent(kb)
        results = agent.search_concepts("Dijkstra 算法怎么理解？", limit=5)
        self.assertTrue(results)
        self.assertTrue(any(item["id"].startswith("DS_GRAPH_005") for item in results))

    def test_natural_language_queries(self):
        kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
        agent = KnowledgeRetrievalAgent(kb)
        cases = {
            "队列和栈有什么区别？": "DS_STACK",
            "二叉树第 i 层最多多少结点？": "DS_TREE",
            "图的广度优先遍历怎么做？": "DS_GRAPH_003",
            "哈希冲突怎么处理？": "DS_SEARCH",
            "KMP 的 next 数组到底怎么用？": "DS_STRING",
        }
        for query, expected_prefix in cases.items():
            with self.subTest(query=query):
                results = agent.search_concepts(query, limit=8)
                self.assertTrue(results)
                self.assertTrue(any(item["id"].startswith(expected_prefix) for item in results), results)

    def test_related_questions(self):
        kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
        agent = KnowledgeRetrievalAgent(kb)
        results = agent.get_related_questions("DS_GRAPH_005", limit=3)
        self.assertTrue(results)


if __name__ == "__main__":
    unittest.main()

