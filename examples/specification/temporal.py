from crome_logic.specification import Specification
from crome_logic.specification.temporal import LTL


def example_1() -> None:
    phi = "! z & G(a & b | G(k & l)) & F(c | !d) & (X(e & f) | !X(g | h)) & (l U p)"
    ltl = LTL(phi)
    print(ltl.tree)
    print(ltl.boolean.tree)
    cnf = ltl.cnf()
    print(cnf)
    print(ltl.represent(Specification.OutputStr.DEFAULT))
    print(ltl.represent(Specification.OutputStr.CNF))
    print(ltl.represent(Specification.OutputStr.DNF))
    print(ltl.represent(Specification.OutputStr.SUMMARY))


if __name__ == "__main__":
    example_1()
