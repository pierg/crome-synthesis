# type: ignore
import os
from pathlib import Path

import dill as dill

from crome_synthesis.src.crome_synthesis.controller import Controller
from crome_synthesis.src.crome_synthesis.pcontrollers import PControllers
from crome_synthesis.src.crome_synthesis.tools import persistence_path


def _make_path(folder_name: Path = ""):
    if not os.path.exists(persistence_path / folder_name):
        os.makedirs(persistence_path / folder_name)


def dump_mono_controller(controller: Controller, folder_name: Path = "",
                         absolute_folder_path: Path = ""):
    if absolute_folder_path == "":
        folder_path = persistence_path / folder_name
    else:
        folder_path = absolute_folder_path

    _make_path(folder_path)

    with open(folder_path / f"{controller.name}_s.dat", "wb") as stream:
        dill.dump(controller, stream)


def load_mono_controller(folder_name: str = "", absolute_folder_path: Path = "",
                         controller_name: str = "") -> Controller | None:
    if absolute_folder_path == "":
        file_path = persistence_path / folder_name / f"{controller_name}_s.dat"
    else:
        file_path = absolute_folder_path / f"{controller_name}_s.dat"

    if not os.path.exists(file_path):
        return None

    with open(file_path, "rb") as stream:
        controller = dill.load(stream)
    return controller


def dump_parallel_controller(controller: PControllers, folder_name: Path = "", absolute_folder_path: Path = ""):
    if absolute_folder_path == "":
        folder_path = persistence_path / folder_name
    else:
        folder_path = absolute_folder_path

    _make_path(folder_path)

    with open(folder_path / f"{controller.name}_p.dat", "wb") as stream:
        dill.dump(controller, stream)


def load_parallel_controller(folder_name: str = "", absolute_folder_path: Path = "",
                             controller_name: str = "") -> PControllers | None:
    if absolute_folder_path == "":
        file_path = persistence_path / folder_name / f"{controller_name}_p.dat"
    else:
        file_path = absolute_folder_path / f"{controller_name}_p.dat"

    if not os.path.exists(file_path):
        return None

    with open(file_path, "rb") as stream:
        controller = dill.load(stream)
    return controller
