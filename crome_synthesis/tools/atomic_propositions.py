from crome_logic.specification.boolean import Bool
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


def extract_transition_aps(
    formula: str, input_aps: dict[str, AtomValues], output_aps: dict[str, AtomValues]
) -> tuple[Atoms, Atoms]:
    transition_aps_in: set = set()
    transition_aps_out: set = set()

    boolean = Bool(formula[1:-1])

    for clause in boolean.cnf.clauses:
        if len(clause) != 1:
            raise AttributeError
        atom = list(clause)[0]
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

    return Atoms(frozenset(transition_aps_in)), Atoms(frozenset(transition_aps_out))
