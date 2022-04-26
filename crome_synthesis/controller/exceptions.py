from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ControllerException(Exception):
    message: str

    def __post_init__(self):
        header = "*** CONTROLLER EXCEPTION ***"
        print(f"{header}\n{self.message}")


@dataclass
class StrixException(ControllerException):
    message: str

    def __post_init__(self):
        message = "*** GENERAL STRIX EXCEPTION ***"
        super().__init__(message)


class SynthesisTimeout(StrixException):
    def __init__(self, command: str, timeout: int):
        self.command = command
        self.timeout = timeout
        message = f"\n{command}\n\n" f"TIMEOUT occurred at {timeout} seconds"
        super().__init__(message=message)


class OutOfMemoryException(StrixException):
    def __init__(self, command: str):
        self.command = command
        message = f"\n{command}\n\n" f"WENT OUT OF MEMORY"
        super().__init__(message=message)


class UnknownStrixResponse(StrixException):
    def __init__(self, command: str, response: str):
        self.command = command
        self.response = response
        message = f"\n{command}\n\n" f"RETURNED THE RESPONSE\n\n" f"{response}\n"
        super().__init__(message=message)
