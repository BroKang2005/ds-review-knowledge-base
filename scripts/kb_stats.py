from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.services import load_knowledge_base


def main() -> None:
    kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
    modules = Counter(item.get("module") for item in kb["concepts"])
    print("Knowledge base stats")
    print("concepts:", len(kb["concepts"]))
    print("atomic concepts:", sum(1 for item in kb["concepts"] if item.get("granularity") == "atomic"))
    print("questions:", len(kb["questions"]))
    print("relations:", len(kb["relations"]))
    print("errors:", len(kb["errors"]))
    print("modules:")
    for name, count in modules.most_common():
        print(f"- {name}: {count}")


if __name__ == "__main__":
    main()

