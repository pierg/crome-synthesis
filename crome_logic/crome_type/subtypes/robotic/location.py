from crome_logic.crome_type.crome_type import CromeType
from crome_logic.crome_type.subtypes.base.boolean import Boolean


class Location(Boolean):
    def __init__(self, name: str, mutex: str = "", adjacency: set[str] | None = None):
        super().__init__(
            name,
            kind=CromeType.Kind.LOCATION,
            mutex_group=mutex,
            adjacency=adjacency,
        )
