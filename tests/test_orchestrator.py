from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator.review_orchestrator import ReviewOrchestrator


class OrchestratorTest(unittest.TestCase):
    def test_full_review_loop(self):
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = ReviewOrchestrator(ROOT / "knowledge_base" / "data", Path(tmp))
            answer = orchestrator.answer_question("demo_student", "Dijkstra 算法怎么理解？")
            self.assertTrue(answer["retrieval"]["primary_concept"])
            self.assertTrue(answer["recommendations"]["recommendations"])
            qid = answer["recommendations"]["recommendations"][0]["question"]["question_id"]
            diagnosis = orchestrator.submit_answer("demo_student", qid, "错误答案")
            self.assertIn("diagnosis", diagnosis)
            summary = orchestrator.generate_summary("demo_student")
            self.assertIn("next_suggestions", summary)


if __name__ == "__main__":
    unittest.main()

