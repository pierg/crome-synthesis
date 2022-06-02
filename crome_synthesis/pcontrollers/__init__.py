from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path

from crome_logic.specification.temporal import LTL
from crome_logic.typelement.basic import BooleanUncontrollable, BooleanControllable
from crome_logic.typeset import Typeset
from crome_synthesis.controller import Controller
from crome_synthesis.controller.controller_info import ControllerInfo, _check_header


@dataclass
class PControllers:
    name: str = ""
    controllers: set[Controller] = field(default_factory=set)

    _synth_time: float = field(init=False, default_factory=float)

    @classmethod
    def from_ltl(cls, guarantees: LTL, assumptions: LTL | None = None, name: str = ""):
        if assumptions is None:
            assumptions = LTL("TRUE")
        if not isinstance(assumptions, LTL) or not isinstance(
                guarantees, LTL
        ):
            raise AttributeError
        ltl_formula = assumptions >> guarantees
        controllers = set()
        print("SUMMARY")
        print(ltl_formula.summary)
        for i, spec in enumerate(ltl_formula.cnf.to_set):
            controllers.add(Controller.from_ltl(guarantees=spec, name=f"{name}_spec_{i}"))

        return cls(name=name, controllers=controllers)

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
        set_ap_i = set(map(lambda x: BooleanUncontrollable(name=x), info.i))
        set_ap_o = set(map(lambda x: BooleanControllable(name=x), info.o))
        typeset = Typeset(set_ap_i | set_ap_o)
        ltl_formula = LTL(_init_formula=info.formula, _typeset=typeset)
        return PControllers.from_ltl(guarantees=ltl_formula, name=name)

    @property
    def synth_time(self) -> float:
        return reduce((lambda x, y: x + y), [c.synth_time for c in self.controllers])
