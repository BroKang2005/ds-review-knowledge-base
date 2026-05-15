from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator.review_orchestrator import ReviewOrchestrator


class MultiAgentWorkflowTest(unittest.TestCase):
    def test_review_and_diagnosis_workflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = ReviewOrchestrator(
                data_dir=ROOT / "data",
                profile_path=Path(tmp) / "student_profiles.json",
            )
            session = orchestrator.start_review("DS_TREE_001", student_id="S001", goal="复习树结构")
            self.assertTrue(session["retrieval"]["primary_concept"])
            self.assertTrue(session["explanation"]["overview"])
            self.assertTrue(session["recommendations"]["recommendations"])

            question_id = session["recommendations"]["recommendations"][0]["question"]["question_id"]
            finished = orchestrator.submit_answer("S001", question_id, "错误答案", session=session)
            self.assertIn("diagnosis", finished)
            self.assertIn("summary", finished)
            self.assertGreaterEqual(finished["profile_after_update"]["answered_count"], 1)


if __name__ == "__main__":
    unittest.main()

