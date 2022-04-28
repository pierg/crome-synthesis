import spot

from crome_logic.specification import Specification
from crome_logic.specification.temporal import LTL
from crome_logic.tools.crome_io import save_to_file
from crome_logic.typeelement.robotic import BooleanAction, BooleanSensor
from crome_logic.typeset import Typeset

from crome_synthesis.controller import Controller
from crome_synthesis.controller.synthesis import generate_controller


def example() -> None:
    a = LTL("G(F(a)) & G(F(b))")
    print(a.represent(Specification.OutputStr.SUMMARY))
    # print(a.boolean.tree)

    g = LTL("G(a <-> x) & F(x) & G(b <->y) & F(y)")
    print(g.represent(Specification.OutputStr.SUMMARY))
    # print(g.boolean.tree)

    spec = a >> g
    spec.cnf()
    # print(g.represent(Specification.OutputStr.SUMMARY))
    print(spec.represent(Specification.OutputStr.SUMMARY))
    print(spec.boolean.tree)


    # controller = Controller(assumptions=a, guarantees=g)
    # print(controller.to_string("dot"))
    # print(controller.to_string("lbtt"))


if __name__ == "__main__":
    example()
