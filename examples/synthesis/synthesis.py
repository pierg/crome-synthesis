import spot
from crome_logic.specification.temporal import LTL
from crome_logic.tools.io import save_to_file
from crome_logic.typeset import Typeset
from crome_logic.typesimple import CromeType
from crome_logic.typesimple.subtype.base.boolean import Boolean

from crome_synthesis.controller import Controller
from crome_synthesis.controller.synthesis import generate_controller


def example() -> None:
    a = LTL(
        formula="G(F(sens))",
        typeset=Typeset({Boolean("sens", kind=CromeType.Kind.SENSOR)}),
    )
    g = LTL(
        formula="G(sens -> act)",
        typeset=Typeset({Boolean("act", kind=CromeType.Kind.ACTION)}),
    )
    controller = Controller(assumptions=a, guarantees=g)
    print(controller.to_string("dot"))
    print(controller.to_string("lbtt"))


def example_1() -> None:
    a1: str = "G(F(a1))"
    g1: str = "G(a1 <-> (b1 | c1))"
    i1: str = "a1"
    o1: str = "b1, c1"

    realizable1, controller1, time1 = generate_controller(a1, g1, i1, o1)

    print(f"\n\n{controller1}")
    file_path = save_to_file(controller1, "controller_1")

    automaton = spot.automaton(file_path)
    dotfile = automaton.to_str(format="dot")
    print(f"\n\n{dotfile}")

    lbtt = automaton.to_str(format="lbtt")
    print(f"\n\n{lbtt}")

    sens: str = "G(F(sens))"
    g2: str = "G(sens -> act)"
    i2: str = "sens"
    o2: str = "act"

    realizable2, controller2, time2 = generate_controller(sens, g2, i2, o2)

    print(f"\n\n{controller2}")


if __name__ == "__main__":
    example()
