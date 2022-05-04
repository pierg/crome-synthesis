from crome_logic.specification.temporal import LTL
from crome_logic.typeset import Typeset

from crome_synthesis.controller import Controller


def example_simpler() -> None:
    a = LTL("G(F(a))", _typeset=Typeset.from_aps(uncontrollable={"a"}))
    g = LTL(
        "G(a <-> x) & G(x <-> y)",
        _typeset=Typeset.from_aps(uncontrollable={"a", "b"}, controllable={"x", "y"}),
    )

    spec = a >> g

    print(spec)
    print("\n")
    c_spec = Controller(guarantees=spec, name="spec_top")
    c_spec.save(format="pdf")
    print(c_spec)
    print("\n")
    for i, s in enumerate(spec.cnf.to_set):
        c_s = Controller(guarantees=s, name=f"spec_{i}")
        c_s.save(format="pdf")
        print(c_s)
        print("\n")


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


if __name__ == "__main__":
    example_simpler()
