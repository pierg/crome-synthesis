import os
from pathlib import Path

from crome_synthesis.pcontrollers import PControllers
from crome_synthesis.tools.persistence import dump_mono_controller

controller_name = "arbiter"
spec_path = Path(os.path.abspath(os.path.dirname(__file__))).parent / f"controller_specs/{controller_name}"
controller_spec = spec_path / f"spec.txt"

print(f"controller selected: {controller_spec}")

# METHOD 2: PARALLEL SYNTHESIS FROM STRIX
controller = PControllers.from_file(file_path=controller_spec, name=controller_name)
print(f"Parallel synthesis realized in {controller.synth_time} s")

print(controller.mealy)
controller.save(format="png", absolute_folder_path=spec_path)
c = dump_mono_controller(absolute_folder_path=spec_path, controller=controller)

