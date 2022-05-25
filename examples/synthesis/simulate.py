import os, sys

from tools.persistence import Persistence

path = os.path.abspath(os.path.dirname(__file__))


if len(sys.argv) > 1:
    controller_name = sys.argv[1]
else:
    controller_name = "0"

print(f"controller selected: {path}/controller_specs/{controller_name}.txt")

controller = Persistence.load_controller(folder_path=f"{path}/controller_specs", name=controller_name)

print(controller)
run = controller.simulate()
print(run)

