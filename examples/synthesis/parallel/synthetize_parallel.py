import os
from pathlib import Path

from crome_synthesis.pcontrollers import PControllers
from crome_synthesis.tools.persistence import dump_controller

controller_name = "test"
spec_path = Path(os.path.abspath(os.path.dirname(__file__))) / f"controller_specs/{controller_name}"
controller_spec = spec_path / f"spec.txt"

print(f"controller selected: {controller_spec}")

# METHOD 2: PARALLEL SYNTHESIS WITH CROME
pcontrollers = PControllers.from_file(file_path=controller_spec, name=controller_name)
for controller in pcontrollers.controllers:
    print(controller.name)
    print(controller.mealy)
c = dump_controller(absolute_folder_path=spec_path, controller=pcontrollers)

print(f"Distributed synthesis realized in {pcontrollers.synth_time} s")
