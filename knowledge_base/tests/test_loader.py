from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kb_loader import load_knowledge_base, validate_knowledge_base


class LoaderTest(unittest.TestCase):
    def test_load_knowledge_base(self):
        kb = load_knowledge_base(ROOT / "data")
        self.assertGreaterEqual(len(kb["concepts"]), 120)
        self.assertGreaterEqual(
            sum(1 for item in kb["concepts"] if item.get("granularity") == "atomic"),
            80,
        )
        self.assertGreaterEqual(len(kb["questions"]), 80)
        self.assertGreaterEqual(len(kb["errors"]), 20)
        self.assertGreaterEqual(len(kb["relations"]), 60)
        self.assertEqual(validate_knowledge_base(kb), [])


if __name__ == "__main__":
    unittest.main()
