import os
from pathlib import Path

output_folder_synthesis: Path = Path(os.path.dirname(__file__)).parent.parent / "output"

persistence_path: Path = output_folder_synthesis / "persistence"
