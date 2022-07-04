from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable, Any

from pydot import Dot
from tabulate import tabulate

from crome_synthesis.atom import Atom, Atoms, AtomValues
from crome_synthesis.tools.atomic_propositions import extract_transitions


@dataclass(frozen=True)
class Transition:
    input: Atoms
    new_state: State
    output: Atoms

    def __str__(self) -> str:
        return f"{self.input}/{self.output} => {self.new_state}"


class State:
    def __init__(self, name: str, transitions: Iterable[Transition] | None = None):
        self._name: str = name
        self._transitions: dict[Atoms, set[tuple[State, Atoms]]] = dict()
        self._is_initial = False

        if transitions is not None:
            for t in transitions:
                self.add_transition(t)

    @property
    def name(self):
        return self._name

    @property
    def transitions(self):
        return self._transitions

    @property
    def possible_inputs(self) -> list[Atoms]:
        return list(self._transitions.keys())

    def add_transition(self, transition: Transition):
        if transition.input in self.transitions.keys():
            self.transitions[transition.input].add(
                (transition.new_state, transition.output)
            )
        else:
            self.transitions[transition.input] = {
                (transition.new_state, transition.output)
            }

    @property
    def is_initial(self):
        return self._is_initial

    def set_as_initial(self):
        self._is_initial = True

    def __str__(self) -> str:
        ret = self.name + "\n"
        for t in self.transitions:
            ret += f"\t{str(t)}\n"
        return ret


@dataclass(frozen=True)
class Mealy:
    states: list[State]
    transitions: list[Transition]

    input_aps: dict[str, AtomValues]
    output_aps: dict[str, AtomValues]

    initial_state: State | None = field(init=False, default=None)
    current_state: State | None = field(init=False, default=None)

    _headers: list[list[str]] = field(init=False, default_factory=list)
    _curr_step: int = field(init=False, default_factory=int)
    _history: list[list[str]] = field(init=False, default_factory=list)

    def __post_init__(self):
        for state in self.states:
            if state.is_initial:
                object.__setattr__(self, "initial_state", state)
        self.reset()

        print("Mealy Machine Built!")
        print(f"# STATES:\t{len(self.states)}")
        print(f"# TRANSITIONS:\t{len(self.transitions)}")

    @classmethod
    def from_pydotgraph(
            cls,
            graph: Dot,
            input_aps: dict[str, AtomValues],
            output_aps: dict[str, AtomValues],
    ):
        print("Building the Mealy machine in progress ...")
        states: dict[str, State] = dict()
        mealy_transitions: list[Transition] = []

        for node in graph.get_nodes():
            try:
                state_id = str(int(node.get_name()))
                states[state_id] = State(name=state_id)
            except:
                pass
        for edge in graph.get_edges():
            if edge.get_source() == "I":
                states[edge.get_destination()].set_as_initial()
            else:
                transitions = extract_transitions(
                    edge.get_attributes()["label"], input_aps, output_aps
                )
                for ins, outs in transitions:
                    source = states[edge.get_source()]
                    destination = states[edge.get_destination()]
                    new_transition = Transition(ins, destination, outs)
                    source.add_transition(new_transition)
                    mealy_transitions.append(new_transition)
        return cls(
            states=list(states.values()), transitions=mealy_transitions, input_aps=input_aps, output_aps=output_aps
        )

    @property
    def input_alphabet(self) -> set[Atom]:
        ret = set()
        for atom in self.input_aps.values():
            ret.add(atom.true)
        return ret

    @property
    def output_alphabet(self) -> set[Atom]:
        ret = set()
        for atom in self.output_aps.values():
            ret.add(atom.true)
        return ret

    @property
    def history(self):
        return tabulate(self._history, headers=self._headers)

    @property
    def raw_history(self):
        return self._history

    def react(self, inputs: Atoms | None = None) -> Atoms:
        curr_state = self.current_state.name
        if inputs is None:
            """random choice"""
            inputs = random.choice(list(self.current_state.transitions.keys()))
        alternatives = self.current_state.transitions[inputs]
        next_state, output = random.choice(list(alternatives))
        object.__setattr__(self, "current_state", next_state)
        history = list(self._history)
        history.append([self._curr_step,
                        str(inputs),
                        curr_state, next_state.name,
                        str(output)])
        object.__setattr__(self, "_history", history)
        object.__setattr__(self, "_curr_step", self._curr_step + 1)
        return output

    def reset(self):
        object.__setattr__(self, "current_state", self.initial_state)
        object.__setattr__(self, "_headers", ["t", "inputs", "s", "s'", "outputs"])
        object.__setattr__(self, "_history", [])
        object.__setattr__(self, "_curr_step", 0)

    def export_to_json(self) -> list[dict[str, Any]]:
        json_content = []
        for state in self.states:
            data = {"name": state.name, "transition": []}
            for inputs, alternatives in state.transitions.items():
                for (next_state, outputs) in alternatives:
                    list_input = inputs.str_positive_only.split(" ")
                    list_output = outputs.str_positive_only.split(" ")
                    for elt in list_output:
                        if elt == '':
                            list_output.remove(elt)
                    for elt in list_input:
                        if elt == '':
                            list_input.remove(elt)

                    line = {"next_state": next_state.name,
                            "inputs": ",".join(list_input),
                            "outputs": ", ".join(list_output)}
                    data["transition"].append(line)

            json_content.append(data)
        return json_content

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        output = (
                f"States          \t {', '.join([s.name for s in self.states])}"
                + f"\nInitial State    \t {self.initial_state.name}"
                + f"\nInput  Alphabet \t {', '.join([str(x) for x in self.input_alphabet])}"
                + f"\nOutput Alphabet \t {', '.join([str(x) for x in self.output_alphabet])}\n\n"
        )

        headers = ["ins", "s", "s'", "outs"]
        entries = []
        for state in self.states:
            for inputs, alternatives in state.transitions.items():
                for (next_state, outputs) in alternatives:
                    line = []
                    line.append(inputs.str_positive_only)
                    line.append(state.name)
                    line.append(next_state.name)
                    line.append(outputs.str_positive_only)
                    entries.append(line)

        output += tabulate(entries, headers=headers)

        return output
