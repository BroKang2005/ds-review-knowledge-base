from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.services import load_knowledge_base


def main() -> None:
    kb = load_knowledge_base(ROOT / "knowledge_base" / "data")
    index = {}
    for concept in kb["concepts"]:
        text = " ".join(str(concept.get(field, "")) for field in ["id", "name", "module", "topic", "description"])
        for token in text.lower().split():
            index.setdefault(token, []).append(concept["id"])
    output = ROOT / "data" / "keyword_index.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Index written to {output}")


if __name__ == "__main__":
    main()

