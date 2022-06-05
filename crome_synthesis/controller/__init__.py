from dataclasses import dataclass, field
from pathlib import Path

import pydot
import spot
from pygraphviz import AGraph

from crome_logic.specification.temporal import LTL
from crome_logic.typelement.basic import BooleanUncontrollable, BooleanControllable
from crome_logic.typeset import Typeset
from crome_synthesis.atom import AtomValues
from crome_synthesis.controller.controller_info import ControllerInfo, _check_header
from crome_synthesis.controller.mealy import Mealy
from crome_synthesis.controller.synthesis import generate_controller
from crome_synthesis.tools import output_folder_synthesis
from crome_synthesis.tools.atomic_propositions import extract_in_out_atomic_propositions
from crome_synthesis.tools.crome_io import save_to_file


@dataclass
class Controller:
    name: str = ""
    info: ControllerInfo = None

    _typeset: Typeset | None = field(repr=False, default=None)
    _input_aps: dict[str, AtomValues] | None = field(
        init=False, repr=False, default=None
    )
    _output_aps: dict[str, AtomValues] | None = field(
        init=False, repr=False, default=None
    )

    _realizable: bool = field(init=False, repr=False, default=False)
    _automaton: str | None = field(init=False, repr=False, default=None)
    _spot_automaton: spot.twa | None = field(init=False, repr=False, default=None)
    _synth_time: float = field(init=False, repr=False, default=-1)

    _pydotgraph: pydot.Dot | None = field(init=False, repr=False, default=None)
    _mealy: Mealy | None = field(init=False, repr=False, default=None)

    def __post_init__(self):

        if self._typeset is None:
            set_ap_i = set(map(lambda x: BooleanUncontrollable(name=x), self.info.i))
            set_ap_o = set(map(lambda x: BooleanControllable(name=x), self.info.o))
            self._typeset = Typeset(set_ap_i | set_ap_o)

        i, o = self.typeset.extract_inputs_outputs()

        self._input_aps, self._output_aps = extract_in_out_atomic_propositions(i, o)

        file_path = save_to_file(
            file_content=self.info.to_str, file_name="controller", absolute_folder_path=output_folder_synthesis
        )
        print(file_path)

        a, g, i, o = self.info.to_strix
        self._realizable, self._automaton, self._synth_time = self.generate_from_spec(a, g, i, o)

        self._spot_automaton = spot.automaton(self._automaton)

        self._pydotgraph = pydot.graph_from_dot_data(self._spot_automaton.to_str("dot"))[0]
        self._mealy = Mealy.from_pydotgraph(
            self._pydotgraph, input_aps=self.input_aps, output_aps=self.output_aps
        )
        print(self.mealy)
        print(self.mealy)

    @classmethod
    def from_ltl(cls, guarantees: LTL, assumptions: LTL | None = None, name: str = ""):
        if assumptions is None:
            assumptions = LTL("TRUE")
        if not isinstance(assumptions, LTL) or not isinstance(
                guarantees, LTL
        ):
            raise AttributeError

        info = ControllerInfo.from_ltl(assumptions, guarantees)
        typeset = (assumptions.typeset_complete + guarantees.typeset_complete).get_sub_typeset(formula=info.formula)
        return cls(name=name, info=info, _typeset=typeset)

    @classmethod
    def from_file(cls, file_path: Path, name: str = ""):
        info = ControllerInfo.from_file(file_path)
        if not name:
            with open(file_path, 'r') as ifile:
                name_found = False
                for line in ifile:
                    if name_found:
                        name = line.strip()
                        break
                    line, header = _check_header(line)

                    if not line:
                        continue

                    elif header:
                        if line == "**NAME**":
                            name_found = True

        return cls(name=name, info=info)

    def __hash__(self):
        return hash(self.mealy.__hash__() + self.info.__hash__())

    @property
    def realizable(self) -> bool:
        return self._realizable

    @property
    def synth_time(self) -> float:
        return self._synth_time

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

    def simulate(self, steps: int = 50):
        """Simulate a run of 50 steps."""

        return self.mealy.simulate(steps)

    def generate_from_spec(
            self, a: str, g: str, i: str, o: str
    ) -> tuple[bool, str, float]:

        print(
            f"Generating controller for the formula:\n({a}) -> ({g})\ninputs:\t\t{i}\noutputs:\t{o}"
        )

        realizable, automaton, synth_time = generate_controller(a, g, i, o)

        if realizable:
            print(f"Controller generated in {synth_time} seconds")
        else:
            print(f"The formula is NOT REALIZABLE")

        return realizable, automaton, synth_time

    def save(self, format: str = "hoa"):
        file_name = f"ctrl_{self.name}.{format}"
        if format in ["png", "eps", "pdf"]:
            (graph,) = pydot.graph_from_dot_data(self._spot_automaton.to_str("dot"))
            graph.write_png(output_folder_synthesis / file_name)
            print(f"{file_name} saved in {output_folder_synthesis}")
        elif format in ["eps", "pdf"]:
            (graph,) = pydot.graph_from_dot_data(self._spot_automaton.to_str("dot"))
            graph.imsave(fname=output_folder_synthesis / file_name, format=format)
            print(f"{file_name} saved in {output_folder_synthesis}")
        elif format in ["hoa", "dot", "spin", "lbtt"]:
            file_path = save_to_file(
                file_content=self._spot_automaton.to_str(format), file_name=file_name
            )
            print(f"{file_path} generated")

    def __getstate__(self):
        state = self.__dict__.copy()
        print(state.keys())
        del state["_spot_automaton"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._spot_automaton = spot.automaton(self._automaton)
        object.__setattr__(self, "_spot_automaton", spot.automaton(self._automaton))
