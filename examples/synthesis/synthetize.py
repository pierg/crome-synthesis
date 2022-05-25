import os, sys

from crome_synthesis.controller import Controller
from pathlib import Path


specs_path = Path(os.path.abspath(os.path.dirname(__file__))) / "controller_specs"

if len(sys.argv) > 1:
    controller_name = sys.argv[1]
else:
    controller_name = "5"

controller_path = specs_path / f"{controller_name}.txt"

print(f"controller selected: {controller_path}")


controller = Controller.from_file(file_path=controller_path)

print(controller.mealy)
