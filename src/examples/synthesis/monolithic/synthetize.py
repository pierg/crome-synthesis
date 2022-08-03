import os
from pathlib import Path

from src.crome_synthesis.controller import Controller
from src.crome_synthesis.tools.persistence import dump_mono_controller

controller_name = "arbiter"
spec_path = Path(os.path.abspath(os.path.dirname(__file__))).parent / f"controller_specs/{controller_name}"
controller_spec = spec_path / f"spec.txt"

print(f"controller selected: {controller_spec}")

# METHOD 1: MONOLITHIC SYNTHESIS FROM STRIX
controller = Controller.from_file(file_path=controller_spec, name=controller_name)
print(f"Monolithic synthesis realized in {controller.synth_time} s")

print(controller.mealy)
controller.save(format="png", absolute_folder_path=spec_path)
c = dump_mono_controller(absolute_folder_path=spec_path, controller=controller)

