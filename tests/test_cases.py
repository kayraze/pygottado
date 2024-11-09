from typing import List, Tuple
from pygottado.utils import DoOption, COLOR


test_case_get_do_option: List[Tuple[int, DoOption | None]] = [
    (1, DoOption.ADD),
    (2, DoOption.DELETE),
    (3, DoOption.SHOW),
    # (4, DoOption.SAVE),
    (5, None),
    (-1, None),
    (0, None),
]

test_case_get_do_option_name: List[Tuple[DoOption | None, str | None]] = [
    (DoOption.ADD, "add"),
    (DoOption.DELETE, "delete"),
    (DoOption.SHOW, "show"),
    # (DoOption.SAVE, "save"),
    (None, None),
]

test_case_prompt: List[Tuple[str, COLOR, str]] = [
    ("1", "light_green", "1"),
    ("2", "light_green", "2"),
    ("3", "light_green", "3"),
    ("4", "light_green", "4"),
    ("5", "light_green", "5"),
]

test_validate_prompt: List[Tuple[str, bool]] = [
    ("1", True),
    ("2", True),
    ("3", True),
    ("4", True),
    ("5", False),
]
