from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kb_loader import load_knowledge_base
from kb_search import get_questions_by_concept, search_concepts


class SearchTest(unittest.TestCase):
    def test_search_tree(self):
        kb = load_knowledge_base(ROOT / "data")
        results = search_concepts(kb, "二叉树")
        self.assertTrue(results)

    def test_questions_by_concept(self):
        kb = load_knowledge_base(ROOT / "data")
        questions = get_questions_by_concept(kb, "DS_TREE_001")
        self.assertTrue(questions)


if __name__ == "__main__":
    unittest.main()
