from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.error_diagnosis_agent import ErrorDiagnosisAgent
from backend.services import load_knowledge_base


class ErrorDiagnosisTest(unittest.TestCase):
    def test_correct_objective_answer(self):
        kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
        agent = ErrorDiagnosisAgent(kb)
        question = kb["questions"][0]
        result = agent.diagnose(question, question["answer"])
        self.assertTrue(result["is_correct"])

    def test_wrong_answer_has_suggestion(self):
        kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
        agent = ErrorDiagnosisAgent(kb)
        question = next(item for item in kb["questions"] if item.get("options") == ["正确", "错误"])
        wrong_answer = "正确" if question["answer"] == "错误" else "错误"
        result = agent.diagnose(question, wrong_answer)
        self.assertFalse(result["is_correct"])
        self.assertTrue(result["suggestion"])


if __name__ == "__main__":
    unittest.main()
