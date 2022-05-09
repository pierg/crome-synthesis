import os
from pathlib import Path

output_folder: Path = Path(os.path.dirname(__file__)).parent.parent / "output"

persistence_path: Path = output_folder / "persistence"
