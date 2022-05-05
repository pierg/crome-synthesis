from dataclasses import dataclass, field

import spot
from crome_logic.specification import Specification
from crome_logic.specification.temporal import LTL
from crome_logic.tools.crome_io import output_folder, save_to_file
from pygraphviz import AGraph

from crome_synthesis.controller.synthesis import generate_controller


@dataclass
class Controller:
    assumptions: Specification | None = None
    guarantees: Specification | None = None
    name: str = ""

    _automaton: str | None = field(init=False, repr=False, default=None)
    _realizable: bool = field(init=False, repr=False, default=False)
    _synth_time: float = field(init=False, repr=False, default=-1)

    def __post_init__(self):
        if self.assumptions is None:
            self.assumptions = LTL("TRUE")
        if self.guarantees is None:
            self.guarantees = LTL("TRUE")
        if not isinstance(self.assumptions, LTL) or not isinstance(
            self.guarantees, LTL
        ):
            raise AttributeError
        self.generate_from_spec(self.assumptions, self.guarantees)

    @property
    def realizable(self) -> bool:
        return self._realizable

    def generate_from_spec(self, assumptions: LTL | None, guarantees: LTL):
        if assumptions is None:
            assumptions = LTL("TRUE")

        self.assumptions = assumptions
        self.guarantees = guarantees

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

        self._realizable, self._automaton, self._synth_time = generate_controller(
            a, g, i, o
        )

        if self._realizable:
            print(f"Controller generated in {self._synth_time} seconds")

        file_path = save_to_file(
            file_content=self._automaton, file_name=f"ctrl_{self.name}"
        )
        print(f"Controller saved in {file_path}")

        # self._automaton = spot.automaton(file_path)
        # TODO [PIER] FIX

    def save(self, format: str = "hoa"):
        automaton = spot.automaton(self._automaton)
        file_name = f"ctrl_{self.name}.{format}"

        if format in ["png", "eps", "pdf"]:
            graph = AGraph(string=automaton.to_str("dot"))
            graph.layout()
            path = graph.draw(path=output_folder / file_name, format=format)
            print(path)
        elif format in ["hoa", "dot", "spin", "lbtt"]:
            file_path = save_to_file(
                file_content=automaton.to_str(format), file_name=file_name
            )
            print(f"Controller saved in {file_path}")
