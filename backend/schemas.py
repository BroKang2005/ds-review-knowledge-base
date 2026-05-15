from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppPaths:
    root_dir: Path
    kb_data_dir: Path
    student_data_dir: Path

    @classmethod
    def default(cls) -> "AppPaths":
        root = Path(__file__).resolve().parents[1]
        return cls(
            root_dir=root,
            kb_data_dir=root / "knowledge_base" / "data",
            student_data_dir=root / "data",
        )


DEFAULT_STUDENT_ID = "demo_student"

