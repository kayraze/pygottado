from enum import Enum
from typing import Dict, Tuple, Literal, Set
from pathlib import Path
import os
import platform


# Define the DoOption Enum
class DoOption(Enum):
    ADD: int = 1
    DELETE: int = 2
    SHOW: int = 3


EXIT_CODES: Set[str] = {"quit", "exit"}

# Define dictionaries mapping DoOption values to DoOption enum and their names
DO_OPTION_DICT: Dict[int, DoOption] = {
    DoOption.ADD.value: DoOption.ADD,
    DoOption.DELETE.value: DoOption.DELETE,
    DoOption.SHOW.value: DoOption.SHOW,
    # DoOption.SAVE.value: DoOption.SAVE,
}

DO_OPTION_NAME: Dict[DoOption, str] = {
    DoOption.ADD: "add",
    DoOption.DELETE: "delete",
    DoOption.SHOW: "show",
}


COLOR = Literal[
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
]

COLOR_LIST: Tuple[COLOR, ...] = (
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
)

CLEAR_SCREEN_COMMANDS = (
    "clear",
    "cls",
    "clean",
)

BASE_DIR: Path = (
    Path(os.environ["APPDATA"])
    if platform.system().lower() == "windows"
    else Path.home() / ".local" / "share"
)
TASKS_JSON_PATH: Path = BASE_DIR / "pygottado/data.json"

# Expose only necessary elements
__all__ = [
    "DoOption",
    "COLOR_LIST",
    "DO_OPTION_NAME",
    "DO_OPTION_DICT",
    "COLOR",
    "EXIT_CODES",
    "CLEAR_SCREEN_COMMANDS",
]
