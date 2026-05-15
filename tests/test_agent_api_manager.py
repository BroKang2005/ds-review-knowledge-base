from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.schemas import AppPaths
from backend.services import ReviewService


class AgentAPIManagerTest(unittest.TestCase):
    def test_list_and_call_agent_endpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            service = ReviewService(
                AppPaths(
                    root_dir=ROOT,
                    kb_data_dir=ROOT / "knowledge_base" / "data",
                    student_data_dir=Path(tmp),
                )
            )
            endpoints = service.list_agent_apis()
            self.assertTrue(any(item["name"] == "knowledge.retrieve" for item in endpoints))
            response = service.call_agent_api("knowledge.retrieve", {"query": "Dijkstra 算法"})
            self.assertTrue(response["ok"])
            self.assertTrue(response["data"]["primary_concept"])

    def test_missing_required_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            service = ReviewService(
                AppPaths(
                    root_dir=ROOT,
                    kb_data_dir=ROOT / "knowledge_base" / "data",
                    student_data_dir=Path(tmp),
                )
            )
            response = service.call_agent_api("knowledge.retrieve", {})
            self.assertFalse(response["ok"])
            self.assertIn("Missing required fields", response["error"])


if __name__ == "__main__":
    unittest.main()

