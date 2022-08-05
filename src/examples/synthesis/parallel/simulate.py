import os
import random
from pathlib import Path

from crome_synthesis.src.crome_synthesis.controller import Controller
from crome_synthesis.src.crome_synthesis.tools.persistence import load_mono_controller

controller_name = "arbiter"
spec_path = Path(os.path.abspath(os.path.dirname(__file__))).parent / f"controller_specs/{controller_name}"
controller_spec = spec_path / f"spec.txt"
print(f"controller selected: {controller_spec}")

controller: Controller = load_mono_controller(absolute_folder_path=spec_path, controller_name=controller_name)


# SIMULATION: USER SELECTS INPUT AT EACH STEP OR RANDOM CHOICE
# Resetting Mealy Machine
controller.mealy.reset()
for i in range(10):
    print(f"Current State: {controller.mealy.current_state.name}")
    possible_inputs = ", ".join([str(a) for a in controller.mealy.current_state.possible_inputs])
    # HERE WE DO A RANDOM CHOICE, BUT IN REALITY THE DESIGNER SHOULD CHOOSE WITCH INPUT TO SEND TO REACT
    print(f"Possible Inputs at current state: {possible_inputs}")
    number_random_choices = 2
    for i in range(number_random_choices):
        choice = random.choice(controller.mealy.current_state.possible_inputs)
        print(f"Input chosen: {choice}")
        outputs = controller.mealy.react(choice)
        print(f"Outputs: {outputs}")
        print(f"New state: {controller.mealy.current_state.name}")
        print(controller.mealy.history)
        print("-------------------------------------------------------------------\n")
