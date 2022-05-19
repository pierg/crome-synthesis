import itertools
from dataclasses import dataclass, field

from crome_logic.specification import and_
from crome_logic.specification.rules_extractors import extract_refinement_rules, extract_mutex_rules, \
    extract_adjacency_rules
from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset
from crome_synthesis.controller.tools import strix_syntax_fix

match_LTL_no_spaces = r"((?<=[G|F|X])(?=[^\s]))|((?<=[U])(?=[a-z]))|(?=[U])+(?<=[a-z])"

ASSUMPTIONS_HEADER = "**ASSUMPTIONS**"
GUARANTEES_HEADER = "**GUARANTEES**"
INS_HEADER = "**INPUTS**"
OUTS_HEADER = "**OUTPUTS**"
END_HEADER = "**END**"
HEADER_SYMBOL = "**"
DATA_INDENT = 0


@dataclass
class ControllerInfo:
    a_ref: list[str]
    a_mtx: list[str]
    a_adj: list[str]
    a: list[str]
    g_ref: list[str]
    g_mtx: list[str]
    g_adj: list[str]
    g: list[str]
    i: list[str]
    o: list[str]

    _typeset: dict | None = field(init=False, repr=False)


    @classmethod
    def from_ltl(cls, assumptions: LTL, guarantees: LTL):
        typeset = Typeset.from_typesets([assumptions.typeset, guarantees.typeset])

        a_ref, t = extract_refinement_rules(assumptions.typeset, output_list=True)
        typeset += t
        a_mtx, t = extract_mutex_rules(assumptions.typeset, output_list=True)
        typeset += t
        a_adj, t = extract_adjacency_rules(assumptions.typeset, output_list=True)
        typeset += t
        a = [str(assumptions)]

        g_ref, t = extract_refinement_rules(guarantees.typeset, output_list=True)
        typeset += t
        g_mtx, t = extract_mutex_rules(guarantees.typeset, output_list=True)
        typeset += t
        g_adj, t = extract_adjacency_rules(guarantees.typeset, output_list=True)
        typeset += t
        g = [str(guarantees)]

        i, o = typeset.extract_inputs_outputs(string=True)

        return cls(a_ref, a_mtx, a_adj, a, g_ref, g_mtx, g_adj, g, i, o)


    @property
    def to_strix(self) -> tuple[str, str, str, str]:
        a = and_(list(itertools.chain(
            self.a,
            self.a_adj,
            self.a_mtx,
            self.a_ref
        )))

        a = strix_syntax_fix(a)

        g = and_(list(itertools.chain(
            self.g,
            self.g_adj,
            self.g_mtx,
            self.g_ref
        )))

        g = strix_syntax_fix(g)

        i = " ,".join(self.i)
        o = " ,".join(self.o)

        return a, g, i, o

    @property
    def to_str(self) -> str:

        ret = ""
        ret += f"{ASSUMPTIONS_HEADER}\n\n"
        ret += _ltl_list_to_string(self.a)
        ret += _ltl_list_to_string(self.a_mtx)
        ret += _ltl_list_to_string(self.a_adj)
        ret += _ltl_list_to_string(self.a_ref)

        ret += f"\n\n{GUARANTEES_HEADER}\n\n"

        ret += _ltl_list_to_string(self.g)
        ret += _ltl_list_to_string(self.g_mtx)
        ret += _ltl_list_to_string(self.g_adj)
        ret += _ltl_list_to_string(self.g_ref)

        ret += f"\n\n{INS_HEADER}\n\n"
        ret += "\t" * DATA_INDENT + ", ".join(self.i)

        ret += f"\n\n{OUTS_HEADER}\n\n"
        ret += "\t" * DATA_INDENT + ", ".join(self.o)

        ret += f"\n\n{END_HEADER}\n\n"

        return ret


def _ltl_list_to_string(ltl_list: list[str]) -> str:
    ret = ""
    if len(ltl_list) > 0:
        for p in ltl_list:
            ret += (
                    "\t" * DATA_INDENT + strix_syntax_fix(p) + "\n"
            )
    return ret
