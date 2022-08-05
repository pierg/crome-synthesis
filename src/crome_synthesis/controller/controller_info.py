import itertools
from dataclasses import dataclass, field
from pathlib import Path

from crome_logic.src.crome_logic.specification import and_
from crome_logic.src.crome_logic.specification.rules_extractors import extract_mutex_rules, extract_adjacency_rules
from crome_logic.src.crome_logic.specification.string_logic import implies_
from crome_logic.src.crome_logic.specification.temporal import LTL
from crome_logic.src.crome_logic.typelement.basic import BooleanUncontrollable, BooleanControllable
from crome_logic.src.crome_logic.typeset import Typeset
from crome_synthesis.src.crome_synthesis.controller.tools import strix_syntax_fix
from crome_synthesis.src.crome_synthesis.world import World

match_LTL_no_spaces = r"((?<=[G|F|X])(?=[^\s]))|((?<=[U])(?=[a-z]))|(?=[U])+(?<=[a-z])"

NAME_HEADER = "**NAME**"
ASSUMPTIONS_HEADER = "**ASSUMPTIONS**"
GUARANTEES_HEADER = "**GUARANTEES**"
INS_HEADER = "**INPUTS**"
OUTS_HEADER = "**OUTPUTS**"
END_HEADER = "**END**"
HEADER_SYMBOL = "**"
DATA_INDENT = 0


@dataclass
class ControllerSpec:
    a: list[str]
    g: list[str]
    i: list[str]
    o: list[str]
    a_mtx: list[str] = field(default_factory=list)
    a_adj: list[str] = field(default_factory=list)
    g_mtx: list[str] = field(default_factory=list)
    g_adj: list[str] = field(default_factory=list)
    a_rules: list[tuple[str]] = field(default_factory=list)
    g_rules: list[tuple[str]] = field(default_factory=list)

    _typeset: Typeset | None = None

    def __post_init__(self):
        if self._typeset is None:
            set_ap_i = set(map(lambda x: BooleanUncontrollable(name=x), self.i))
            set_ap_o = set(map(lambda x: BooleanControllable(name=x), self.o))
            self._typeset = Typeset(set_ap_i | set_ap_o)

    @classmethod
    def from_ltl(cls, assumptions: LTL, guarantees: LTL, world: World | None = None):
        typeset = Typeset.from_typesets([assumptions.typeset, guarantees.typeset])

        a_rules = []
        g_rules = []

        if world is not None:
            typeset = assumptions.typeset + guarantees.typeset + world.typeset
            typeset_c, typeset_u = typeset.split_controllable_uncontrollable
            a_mtx, t = extract_mutex_rules(typeset_u, output_list=True)
            typeset += t
            a_adj, t = extract_adjacency_rules(typeset_u, output_list=True)
            typeset += t
            g_mtx, t = extract_mutex_rules(typeset_c, output_list=True)
            typeset += t
            g_adj, t = extract_adjacency_rules(typeset_c, output_list=True)
            typeset += t
            a_rules, t = world.get_rules(environment=True)
            typeset += t
            g_rules, t = world.get_rules(environment=False)
            typeset += t
        else:
            # a_ref, t = extract_refinement_rules(assumptions.typeset, output_list=True)
            # typeset += t
            a_mtx, t = extract_mutex_rules(assumptions.typeset, output_list=True)
            typeset += t
            a_adj, t = extract_adjacency_rules(assumptions.typeset, output_list=True)
            typeset += t
            # g_ref, t = extract_refinement_rules(guarantees.typeset, output_list=True)
            # typeset += t
            g_mtx, t = extract_mutex_rules(guarantees.typeset, output_list=True)
            typeset += t
            g_adj, t = extract_adjacency_rules(guarantees.typeset, output_list=True)
            typeset += t

        a = []
        if not assumptions.is_true_expression:
            a = [str(assumptions)]
        g = []
        if not guarantees.is_true_expression:
            g = [str(guarantees)]

        i, o = typeset.extract_inputs_outputs(string=True)

        return cls(a, g, i, o, a_mtx, a_adj, g_mtx, g_adj, a_rules, g_rules, typeset)

    @classmethod
    def from_file(cls, file_path: Path):

        a = []
        g = []
        i = []
        o = []

        file_header = ""

        with open(file_path, 'r') as ifile:
            for line in ifile:
                line, header = _check_header(line)

                # skip empty lines
                if not line:
                    continue

                # parse file header line
                elif header:

                    if ASSUMPTIONS_HEADER == line:
                        if file_header == "":
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif GUARANTEES_HEADER == line:
                        if file_header == ASSUMPTIONS_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif INS_HEADER == line:
                        if file_header == GUARANTEES_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif OUTS_HEADER == line:
                        if file_header == INS_HEADER:
                            file_header = line
                        else:
                            Exception("File format not supported")

                    elif END_HEADER == line:
                        if file_header == OUTS_HEADER:
                            if len(a) == 0:
                                a.append("true")
                            return cls(a, g, i, o)
                        else:
                            Exception("File format not supported")
                    elif NAME_HEADER == line:
                        continue

                    else:
                        raise Exception("Unexpected File Header: " + line)

                else:

                    if ASSUMPTIONS_HEADER == file_header:
                        a.append(line.strip())

                    if GUARANTEES_HEADER == file_header:
                        g.append(line.strip())

                    if INS_HEADER == file_header:
                        for elem in line.split(","):
                            i.append(elem.strip())

                    if OUTS_HEADER == file_header:
                        for elem in line.split(","):
                            o.append(elem.strip())

    @property
    def formula(self) -> str:
        a, g, i, o = self.to_strix
        return implies_(a, g)


    @property
    def typeset(self) -> Typeset:
        return self._typeset


    @property
    def to_strix(self) -> tuple[str, str, str, str]:
        a = and_(list(itertools.chain(
            self.a,
            self.a_adj,
            self.a_mtx,
            [r[0] for r in self.a_rules]
        )))

        a = strix_syntax_fix(a)

        g = and_(list(itertools.chain(
            self.g,
            self.g_adj,
            self.g_mtx,
            [r[0] for r in self.g_rules]
        )))

        g = strix_syntax_fix(g)

        i = " ,".join(self.i)
        o = " ,".join(self.o)

        return a, g, i, o

    def __hash__(self):
        return hash(self.formula)

    @property
    def to_str(self) -> str:
        ret = ""
        ret += f"{ASSUMPTIONS_HEADER}\n\n"
        ret += _ltl_list_to_string(self.a)
        if len(self.a_mtx) > 0:
            ret += f"\n\n# MUTEX RULES\n"
        ret += _ltl_list_to_string(self.a_mtx)
        if len(self.a_adj) > 0:
            ret += f"\n# ADJACENCY RULES\n"
        ret += _ltl_list_to_string(self.a_adj)
        if len(self.a_rules) > 0:
            ret += f"\n# ENVIRONMENT RULES\n"
        ret += _ltl_list_to_string(self.a_rules)

        ret += f"\n\n{GUARANTEES_HEADER}\n\n"

        ret += _ltl_list_to_string(self.g)
        if len(self.g_mtx) > 0:
            ret += f"\n\n# MUTEX RULES\n"
        ret += _ltl_list_to_string(self.g_mtx)
        if len(self.g_adj) > 0:
            ret += f"\n# ADJACENCY RULES\n"
        ret += _ltl_list_to_string(self.g_adj)
        if len(self.g_rules) > 0:
            ret += f"\n# SYSTEM RULES\n"
        ret += _ltl_list_to_string(self.g_rules)

        ret += f"\n\n{INS_HEADER}\n\n"
        ret += "\t" * DATA_INDENT + ", ".join(self.i)

        ret += f"\n\n{OUTS_HEADER}\n\n"
        ret += "\t" * DATA_INDENT + ", ".join(self.o)

        ret += f"\n\n{END_HEADER}\n\n"

        return ret


def _ltl_list_to_string(ltl_list: list[str] | list[tuple[str, str]]) -> str:
    ret = ""
    if len(ltl_list) > 0:
        for p in ltl_list:
            if isinstance(p, tuple):
                ret += (
                        "\t" * DATA_INDENT + "# " + strix_syntax_fix(p[1]) + "\n"
                )
                ret += (
                        "\t" * DATA_INDENT + strix_syntax_fix(p[0]) + "\n\n"
                )
            else:
                ret += (
                        "\t" * DATA_INDENT + strix_syntax_fix(p) + "\n"
                )
    return ret


def _check_header(line: str) -> tuple[str, bool]:
    """Returns a comment-free, tab-replaced line with no whitespace and the number of tabs"""
    COMMENT_CHAR = '#'
    line = line.split(COMMENT_CHAR, 1)[0]
    if line.startswith(HEADER_SYMBOL):
        return line.strip(), True
    return line.strip(), False
