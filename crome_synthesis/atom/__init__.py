from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from crome_logic.typelement.basic import Boolean


class Val(Enum):
    true = auto()
    false = auto()
    undefined = auto()


@dataclass
class Atom:
    typelement: Boolean
    value: Val = Val.undefined

    def __invert__(self):
        if self.value == Val.true:
            self.value = Val.false
        elif self.value == Val.false:
            self.value = Val.true
        else:
            raise AttributeError

    def is_compatible_with(self, other: Atom):
        if other.typelement == self.typelement:
            if (self.value == Val.true and other.value == Val.false) or (
                    self.value == Val.false and other.value == Val.true
            ):
                return False
        return True

    def __str__(self):
        if self.value == Val.false:
            return f"{self.typelement.name}!"
        elif self.value == Val.undefined:
            return f"{self.typelement.name}?"
        else:
            return f"{self.typelement.name} "

    def __hash__(self):
        return hash(f"{self.typelement.__hash__()}{str(self.value)}")


@dataclass
class Atoms:
    atoms: frozenset[Atom]

    def is_compatible_with(self, other: Atoms):
        pass

    def determinize_from(self, other: Atoms):
        pass

    @property
    def str_positive_only(self):
        return " ".join([str(a) for a in list(filter(lambda a: a.value == Val.true, self.atoms))])

    def __str__(self):
        return " ".join([str(a) for a in self.atoms])

    def __hash__(self):
        return hash(self.atoms)


class AtomValues:
    def __init__(self, typelement: Boolean):
        self._true: Atom = Atom(typelement=typelement, value=Val.true)
        self._false: Atom = Atom(typelement=typelement, value=Val.false)
        self._undefined: Atom = Atom(typelement=typelement, value=Val.undefined)

    @property
    def true(self):
        return self._true

    @property
    def false(self):
        return self._false

    @property
    def undefined(self):
        return self._undefined
