from crome_logic.specification.boolean import Bool
from crome_logic.tools.string_manipulation import pyeda_syntax_fix
from crome_logic.typelement.basic import Boolean

from crome_synthesis.atom import Atoms, AtomValues


def extract_in_out_atomic_propositions(
    inputs_types: set[Boolean], output_types: set[Boolean]
) -> tuple[dict[str, AtomValues], dict[str, AtomValues]]:

    input_aps: dict[str, AtomValues] = {}
    output_aps: dict[str, AtomValues] = {}

    for i in inputs_types:
        input_aps[i.name] = AtomValues(i)

    for o in output_types:
        output_aps[o.name] = AtomValues(o)

    return input_aps, output_aps


def extract_transitions(
    formula: str, input_aps: dict[str, AtomValues], output_aps: dict[str, AtomValues]
) -> set[tuple[Atoms, Atoms]]:

    alternatives: set[tuple[Atoms, Atoms]] = set()

    if pyeda_syntax_fix(formula) == "1":
        return alternatives


    boolean = Bool(formula)


    for clause in boolean.dnf.clauses:

        transition_aps_in: set = set()
        transition_aps_out: set = set()

        for atom in clause:
            typeset = atom.typeset
            if len(typeset) != 1:
                raise AttributeError
            t_name = list(typeset.keys())[0]
            if t_name in input_aps:
                if t_name in output_aps:
                    raise Exception("Inputs and Outputs must be disjoint")
                if "!" in str(atom):
                    transition_aps_in.add(input_aps[t_name].false)
                else:
                    transition_aps_in.add(input_aps[t_name].true)
            elif t_name in output_aps:
                if t_name in input_aps:
                    raise Exception("Inputs and Outputs must be disjoint")
                if "!" in str(atom):
                    transition_aps_out.add(output_aps[t_name].false)
                else:
                    transition_aps_out.add(output_aps[t_name].true)
            else:
                raise Exception(f"{t_name} ap does not exist")

        alt = Atoms(frozenset(transition_aps_in)), Atoms(frozenset(transition_aps_out))
        alternatives.add(alt)

    return alternatives
