import os
from pathlib import Path

from crome_logic.patterns.basic import G
from crome_logic.specification import and_
from crome_synthesis.controller import ControllerSpec, generate_controller

specs_path = Path(os.path.abspath(os.path.dirname(__file__))) / "controller_specs"

o = [f"a{i}" for i in range(0, 50000)]

spec = str(G(and_(o)))
c_info = ControllerSpec(a=[], g=[spec], i=[], o=o)
a, g, i, o = c_info.to_strix
realizable, automaton, synth_time = generate_controller(a, g, i, o)
if realizable:
    print(f"Realizable in {synth_time}")
else:
    print(f"Unrealizable in {synth_time}")
