import os, sys

from crome_synthesis.tools.persistence import load_controller

path = os.path.abspath(os.path.dirname(__file__))


if len(sys.argv) > 1:
    controller_name = sys.argv[1]
else:
    controller_name = "5"

print(f"controller selected: {path}/controller_specs/{controller_name}.txt")

c = load_controller(controller_name=controller_name)
# print(c.mealy)

c.save("pdf")
print(c.mealy)
tab = c.simulate()
print(tab)
#
# controller = Persistence.load_controller(folder_path=f"{path}/controller_specs", name=controller_name)
#
# print(controller)
# run = controller.simulate()
# print(run)

