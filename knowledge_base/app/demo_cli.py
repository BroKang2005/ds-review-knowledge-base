from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestrator.review_orchestrator import ReviewOrchestrator


def print_json(title: str, payload: dict) -> None:
    print(f"\n=== {title} ===")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-agent data-structure review assistant demo.")
    parser.add_argument("--student-id", default="S001")
    parser.add_argument("--query", default="DS_TREE_001", help="知识点关键词或知识点 ID")
    parser.add_argument("--goal", default="期末复习数据结构高频考点")
    parser.add_argument("--answer", default="", help="学生答案；为空时使用一个演示用错误答案")
    args = parser.parse_args()

    orchestrator = ReviewOrchestrator(data_dir=ROOT / "data")
    session = orchestrator.start_review(args.query, student_id=args.student_id, goal=args.goal)
    print_json(
        "1. 检索与讲解",
        {
            "primary_concept": session["retrieval"]["primary_concept"],
            "explanation": session["explanation"],
            "learning_path": session["learning_path"],
        },
    )
    print_json("2. 推荐题目", session["recommendations"])

    recommendations = session["recommendations"].get("recommendations", [])
    if not recommendations:
        print("\n没有可推荐题目，演示结束。")
        return
    question_id = recommendations[0]["question"]["question_id"]
    answer = args.answer or "我认为只要记住结论即可，不需要分析边界条件。"
    finished = orchestrator.submit_answer(args.student_id, question_id, answer, session=session)
    print_json("3. 错题诊断", finished["diagnosis"])
    print_json(
        "4. 画像更新与下一步建议",
        {
            "profile": finished["profile_after_update"],
            "next_recommendations": finished["next_recommendations"],
            "summary": finished["summary"],
        },
    )


if __name__ == "__main__":
    main()

