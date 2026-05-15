from __future__ import annotations

from backend.services import ReviewService
from backend.schemas import DEFAULT_STUDENT_ID


def main() -> None:
    service = ReviewService()
    result = service.answer_question(DEFAULT_STUDENT_ID, "Dijkstra 算法怎么理解？")
    print("数据结构智能复习助手 CLI smoke demo")
    print("命中知识点：", result.get("retrieval", {}).get("primary_concept", {}).get("name"))
    print("讲解摘要：", result.get("explanation", {}).get("definition"))
    print("推荐题数：", len(result.get("recommendations", {}).get("recommendations", [])))


if __name__ == "__main__":
    main()

