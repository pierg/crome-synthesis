import spot
from crome_logic.specification.temporal import LTL
from crome_logic.tools.io import save_to_file

from crome_synthesis.controller.synthesis import generate_controller


class Controller:
    def __init__(self, assumptions: LTL | None = None, guarantees: LTL | None = None):
        self._assumptions = assumptions
        self._guarantees = guarantees
        self._automaton: spot.automata() | None = None
        self.generate_from_spec(assumptions, guarantees)

    def generate_from_spec(self, assumptions: LTL | None, guarantees: LTL):
        if assumptions is None:
            assumptions = LTL("TRUE")

        self._assumptions = assumptions
        self._guarantees = guarantees

        a = str(assumptions)
        g = str(guarantees)
        i, o = (assumptions.typeset + guarantees.typeset).extract_inputs_outputs(
            string=True
        )
        i = ", ".join(i)
        o = ", ".join(o)

        print(
            f"Generating controller for the formula:\n({a}) -> ({g})\ninputs:\t\t{i}\noutputs:\t{o}"
        )

        realizable, controller, time = generate_controller(a, g, i, o)

        if realizable:
            print(f"Controller generated in {time} seconds")

        file_path = save_to_file(controller, "controller")

        print(f"Controller saved in {file_path}")

        self._automaton = spot.automaton(file_path)

    def to_string(self, format: str) -> str:
        if self._automaton is not None:
            return self._automaton.to_str(format=format)
        return ""
