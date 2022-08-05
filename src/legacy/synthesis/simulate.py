import os, sys

from crome_synthesis.src.crome_synthesis.tools.persistence import load_controller, dump_controller

path = os.path.abspath(os.path.dirname(__file__))


if len(sys.argv) > 1:
    controller_name = sys.argv[1]
else:
    controller_name = "5"

print(f"controller selected: {path}/controller_specs/{controller_name}.txt")

c = dump_controller(folder_name=f"{path}/controller_specs/")
print(tab)
