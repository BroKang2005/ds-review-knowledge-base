from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from diagnosis import diagnose_student
from kb_loader import load_knowledge_base


class DiagnosisTest(unittest.TestCase):
    def test_diagnose_student(self):
        kb = load_knowledge_base(ROOT / "data")
        question = next(item for item in kb["questions"] if "DS_STACK_005" in item["knowledge_points"])
        result = diagnose_student(
            kb,
            [{"student_id": "S001", "question_id": question["question_id"], "is_correct": False, "student_answer": "front == rear"}],
        )
        self.assertTrue(result["weak_points"])


if __name__ == "__main__":
    unittest.main()
