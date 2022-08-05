import os, sys

from keyring.backends.Windows import Persistence

from crome_synthesis.src.crome_synthesis.controller import Controller
from pathlib import Path

from crome_synthesis.src.crome_synthesis.tools.persistence import dump_controller

specs_path = Path(os.path.abspath(os.path.dirname(__file__))) / "controller_specs"

if len(sys.argv) > 1:
    controller_name = sys.argv[1]
else:
    controller_name = "6"

controller_path = specs_path / f"{controller_name}.txt"

print(f"controller selected: {controller_path}")


# METHOD 1: MONOLITHIC SYNTHESIS FROM STRIX
controller = Controller.from_file(file_path=controller_path, name=controller_name)
print(controller.mealy)
c = dump_controller(controller_name=controller_name)





#
# # METHOD 2: PARALLEL SYNTHESIS WITH CROME
# pcontrollers = PControllers.from_file(file_path=controller_path, name=controller_name)
# for controller in pcontrollers.controllers:
#     print(controller.name)
#     print(controller.mealy)
#
# print(f"Monolithic synthesis realized in {controller.synth_time} s")
# print(f"Distributed synthesis realized in {pcontrollers.synth_time} s")
#
#
