from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset

from crome_synthesis.controller import Controller
from crome_synthesis.tools.crome_io import save_to_file


def robot() -> None:
    # a = LTL("G(F(a))", _typeset=Typeset.from_aps(uncontrollable={"a"}))
    g = LTL(
        "G (!g_0 | !g_1) & G(r_0 -> F g_0) & G( r_1 -> F g_1)",
        _typeset=Typeset.from_aps(uncontrollable={"r_1", "r_0"}, controllable={"g_1", "g_0"}),
    )

    spec = g

    c_spec = Controller.from_ltl(guarantees=spec)
    c_spec.save(format="pdf")
    print(c_spec.mealy)
    for i, s in enumerate(spec.cnf.to_set):
        c_s = Controller(guarantees=s, name=f"spec_{i}")
        c_s.save(format="pdf")
        save_to_file(str(s), file_name=f"spec_{i}")
        print(c_s.mealy)
        print("\n\n")
    print("\n\n")




def example_simpler() -> None:
    a = LTL("G(F(a))", _typeset=Typeset.from_aps(uncontrollable={"a"}))
    g = LTL(
        "G(a <-> x) & G(x <-> y)",
        _typeset=Typeset.from_aps(uncontrollable={"a", "b"}, controllable={"x", "y"}),
    )

    spec = a >> g

    c_spec = Controller(guarantees=spec, name="spec_top")
    c_spec.save(format="pdf")
    print(c_spec.mealy)

    print("\n\n")
    for i, s in enumerate(spec.cnf.to_set):
        c_s = Controller(guarantees=s, name=f"spec_{i}")
        c_s.save(format="pdf")
        print(c_s.mealy)
        print("\n\n")


def example() -> None:
    a = LTL("G(F(a)) & G(F(b))", _typeset=Typeset.from_aps(uncontrollable={"a", "b"}))
    g = LTL(
        "G(a <-> x) & F(x) & G(b <->y) & F(y)",
        _typeset=Typeset.from_aps(uncontrollable={"a", "b"}, controllable={"x", "y"}),
    )
    spec = a >> g
    print(spec)
    print("\n")
    c_spec = Controller(guarantees=spec, name="spec")
    c_spec.save(format="dot")
    print(c_spec)
    print("\n")
    for i, s in enumerate(spec.cnf.to_set):
        c_s = Controller(guarantees=s, name=f"spec_{i}")
        c_s.save(format="dot")
        print(c_s)
        print("\n")
        print(f"\n\nMEALY:\n{c_s.mealy.__str__()}")


if __name__ == "__main__":
    robot()
