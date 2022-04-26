import spot
from crome_logic.specification.temporal import LTL
from crome_logic.tools.crome_io import save_to_file

from crome_synthesis.controller.synthesis import generate_controller


class Controller:
    def __init__(self, assumptions: LTL | None = None, guarantees: LTL | None = None):
        self._assumptions = assumptions
        self._guarantees = guarantees

        self._automaton: spot.automata() | None = None  # type: ignore
        self._realizable: bool = False
        self._synth_time: float = -1

        self.generate_from_spec(assumptions, guarantees)

    @property
    def realizable(self) -> bool:
        return self._realizable

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

        self._realizable, controller, self._synth_time = generate_controller(a, g, i, o)

        if self._realizable:
            print(f"Controller generated in {self._synth_time} seconds")

        file_path = save_to_file(file_content=controller, file_name="controller")

        print(f"Controller saved in {file_path}")

        # self._automaton = spot.automaton(file_path)
        # TODO [PIER] FIX

    def to_string(self, format: str) -> str:
        if self._automaton is not None:
            return self._automaton.to_str(format=format)
        return ""
