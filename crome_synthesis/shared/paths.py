from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

output_path: Path = Path(os.path.dirname(__file__)).parent / "output"

storage_path: Path = output_path / "storage"

persistence_path: Path = output_path / "persistence"

# Usage: session_path(_SESSION_ID_)
session_path: Callable[[str], Path] = lambda s: storage_path / f"s_{s}"

# Usage: project_path(_SESSION_ID_, _PROJECT_ID_)
project_path: Callable[[str, str], Path] = (
    lambda s, p: storage_path / f"s_{s}" / f"p_{p}"
)

# Usage: goals_path(_SESSION_ID_, _PROJECT_ID_)
goals_path: Callable[[str, str], Path] = (
    lambda s, p: storage_path / f"s_{s}" / f"p_{p}" / "goals"
)

controller_path: Callable[str, Path] = (
    lambda s: storage_path / f"s_{s}" / "controllers"
)
