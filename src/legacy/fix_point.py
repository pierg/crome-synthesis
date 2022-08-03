from src.crome_logic.specification.temporal import LTL
from src.crome_logic.typeset import Typeset

from src.crome_synthesis.controller import Controller


def two_fixed_points() -> None:
    s1 = LTL(
        "G(x <-> y)",
        _typeset=Typeset.from_aps(uncontrollable={"x"}, controllable={"y"}),
    )

    c_spec = Controller(guarantees=s1, name="s1")
    c_spec.save(format="pdf")
    print(c_spec.mealy)

    s2 = LTL(
        "G(y <-> x)",
        _typeset=Typeset.from_aps(uncontrollable={"y"}, controllable={"x"}),
    )

    c_spec = Controller(guarantees=s2, name="s2")
    c_spec.save(format="pdf")
    print(c_spec.mealy)


    s3 = LTL(
        "G(x <-> z)",
        _typeset=Typeset.from_aps(uncontrollable={"x"}, controllable={"z"}),
    )

    c_spec = Controller(guarantees=s3, name="s3")
    c_spec.save(format="pdf")
    print(c_spec.mealy)


def two_fixed_points_conflict() -> None:
    s1 = LTL(
        "G(x <-> y)",
        _typeset=Typeset.from_aps(uncontrollable={"x"}, controllable={"y"}),
    )

    c_spec = Controller(guarantees=s1, name="s1")
    c_spec.save(format="pdf")
    print(c_spec.mealy)

    s2 = LTL(
        "G(y <-> !x)",
        _typeset=Typeset.from_aps(uncontrollable={"y"}, controllable={"x"}),
    )

    c_spec = Controller(guarantees=s2, name="s2'")
    c_spec.save(format="pdf")
    print(c_spec.mealy)


if __name__ == "__main__":
    two_fixed_points_conflict()
