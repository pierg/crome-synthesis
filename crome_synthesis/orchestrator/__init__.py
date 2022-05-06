from dataclasses import dataclass, field

from crome_synthesis.controller.mealy import Mealy


@dataclass
class Orchestrator:
    mealy: Mealy
    n_steps: int = 50
    t_min_context: int = 10
