from dataclasses import dataclass, field

import pydot
import spot
from crome_logic.specification import Specification
from crome_logic.specification.temporal import LTL
from crome_logic.tools.crome_io import output_folder, save_to_file
from crome_logic.typeset import Typeset
from pygraphviz import AGraph

from crome_synthesis.atom import AtomValues
from crome_synthesis.controller.mealy import Mealy
from crome_synthesis.controller.synthesis import generate_controller
from crome_synthesis.tools.atomic_propositions import extract_in_out_atomic_propositions


@dataclass
class Controller:
    assumptions: Specification | None = None
    guarantees: Specification | None = None
    name: str = ""

    _typeset: Typeset | None = field(init=False, repr=False, default=None)
    _input_aps: dict[str, AtomValues] | None = field(
        init=False, repr=False, default=None
    )
    _output_aps: dict[str, AtomValues] | None = field(
        init=False, repr=False, default=None
    )

    _automaton: spot.twa | None = field(init=False, repr=False, default=None)
    _mealy: Mealy | None = field(init=False, repr=False, default=None)
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
        self._typeset = self.assumptions.typeset + self.guarantees.typeset
        i, o = self.typeset.extract_inputs_outputs()
        self._input_aps, self._output_aps = extract_in_out_atomic_propositions(i, o)

        self.generate_from_spec(self.assumptions, self.guarantees)

    @property
    def realizable(self) -> bool:
        return self._realizable

    @property
    def typeset(self) -> Typeset:
        return self._typeset

    @property
    def input_aps(self) -> dict[str, AtomValues]:
        return self._input_aps

    @property
    def output_aps(self) -> dict[str, AtomValues]:
        return self._output_aps

    @property
    def mealy(self) -> Mealy:
        return self._mealy

    def generate_from_spec(self, assumptions: LTL | None, guarantees: LTL):

        self.assumptions = assumptions
        self.guarantees = guarantees

        a = str(assumptions)
        g = str(guarantees)

        i, o = self.typeset.extract_inputs_outputs(string=True)
        i = ", ".join(i)
        o = ", ".join(o)

        print(
            f"Generating controller for the formula:\n({a}) -> ({g})\ninputs:\t\t{i}\noutputs:\t{o}"
        )

        self._realizable, automaton, self._synth_time = generate_controller(a, g, i, o)

        if self._realizable:
            print(f"Controller generated in {self._synth_time} seconds")

        self._automaton = spot.automaton(automaton)
        self._graph = pydot.graph_from_dot_data(self._automaton.to_str("dot"))[0]
        self._mealy = Mealy.from_pydotgraph(
            self._graph, input_aps=self.input_aps, output_aps=self.output_aps
        )

    def save(self, format: str = "hoa"):
        file_name = f"ctrl_{self.name}.{format}"

        if format in ["png", "eps", "pdf"]:
            graph = AGraph(string=self._automaton.to_str("dot"))
            graph.layout()
            path = graph.draw(path=output_folder / file_name, format=format)
            print(path)
        elif format in ["hoa", "dot", "spin", "lbtt"]:
            file_path = save_to_file(
                file_content=self._automaton.to_str(format), file_name=file_name
            )
            print(f"Controller saved in {file_path}")
