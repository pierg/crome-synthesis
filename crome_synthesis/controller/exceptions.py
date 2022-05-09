from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class ControllerException(Exception):
    message: str = ""

    def __post_init__(self):
        header = "*** CONTROLLER EXCEPTION ***"
        print(f"{header}\n{self.message}")


@dataclass(kw_only=True)
class StrixException(ControllerException):
    def __post_init__(self):
        self.message = "*** GENERAL STRIX EXCEPTION ***"


@dataclass(kw_only=True)
class SynthesisTimeout(StrixException):
    command: str
    timeout: int

    def __post_init__(self):
        self.message = (
            f"\n{self.command}\n\n" f"TIMEOUT occurred at {self.timeout} seconds"
        )


@dataclass(kw_only=True)
class OutOfMemoryException(StrixException):
    command: str

    def __post_init__(self):
        self.message = f"\n{self.command}\n\n" f"WENT OUT OF MEMORY"


@dataclass(kw_only=True)
class UnknownStrixResponse(StrixException):
    command: str
    response: str

    def __post_init__(self):
        self.message = (
            f"\n{self.command}\n\n" f"RETURNED THE RESPONSE\n\n" f"{self.response}\n"
        )
