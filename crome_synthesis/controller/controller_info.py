import itertools
from dataclasses import dataclass, field
from pathlib import Path

from crome_logic.specification import and_
from crome_logic.specification.rules_extractors import extract_mutex_rules, extract_adjacency_rules
from crome_logic.specification.string_logic import implies_
from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset
from crome_synthesis.controller.tools import strix_syntax_fix

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
class ControllerInfo:
    a: list[str]
    g: list[str]
    i: list[str]
    o: list[str]
    a_mtx: list[str] = field(default_factory=list)
    a_adj: list[str] = field(default_factory=list)
    g_mtx: list[str] = field(default_factory=list)
    g_adj: list[str] = field(default_factory=list)

    _typeset: dict | None = field(init=False, repr=False)

    @classmethod
    def from_ltl(cls, assumptions: LTL, guarantees: LTL):
        typeset = Typeset.from_typesets([assumptions.typeset, guarantees.typeset])

        # a_ref, t = extract_refinement_rules(assumptions.typeset, output_list=True)
        # typeset += t
        a_mtx, t = extract_mutex_rules(assumptions.typeset, output_list=True)
        typeset += t
        a_adj, t = extract_adjacency_rules(assumptions.typeset, output_list=True)
        typeset += t
        a = [str(assumptions)]
        #
        # g_ref, t = extract_refinement_rules(guarantees.typeset, output_list=True)
        # typeset += t
        g_mtx, t = extract_mutex_rules(guarantees.typeset, output_list=True)
        typeset += t
        g_adj, t = extract_adjacency_rules(guarantees.typeset, output_list=True)
        typeset += t
        g = [str(guarantees)]

        i, o = typeset.extract_inputs_outputs(string=True)

        return cls(a, g, i, o, a_mtx, a_adj, g_mtx, g_adj)

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
    def to_strix(self) -> tuple[str, str, str, str]:
        a = and_(list(itertools.chain(
            self.a,
            self.a_adj,
            self.a_mtx,
        )))

        a = strix_syntax_fix(a)

        g = and_(list(itertools.chain(
            self.g,
            self.g_adj,
            self.g_mtx,
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
        ret += _ltl_list_to_string(self.a_mtx)
        ret += _ltl_list_to_string(self.a_adj)

        ret += f"\n\n{GUARANTEES_HEADER}\n\n"

        ret += _ltl_list_to_string(self.g)
        ret += _ltl_list_to_string(self.g_mtx)
        ret += _ltl_list_to_string(self.g_adj)

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


def _check_header(line: str) -> tuple[str, bool]:
    """Returns a comment-free, tab-replaced line with no whitespace and the number of tabs"""
    COMMENT_CHAR = '#'
    line = line.split(COMMENT_CHAR, 1)[0]
    if line.startswith(HEADER_SYMBOL):
        return line.strip(), True
    return line.strip(), False
