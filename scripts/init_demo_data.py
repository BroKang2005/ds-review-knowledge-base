from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.services import ensure_student_data


def main() -> None:
    ensure_student_data(ROOT / "data")
    print("Demo student data initialized in ./data")


if __name__ == "__main__":
    main()

