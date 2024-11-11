from typing import List, Tuple
from pygottado.utils import DoOption, COLOR
from pygottado.utils.classes import TaskItem
import pytest_asyncio
import asyncio
import pytest

test_case_get_do_option: List[Tuple[int, DoOption | None]] = [
    (1, DoOption.ADD),
    (2, DoOption.DELETE),
    (3, DoOption.SHOW),
    (5, None),
    (-1, None),
    (0, None),
]

test_case_get_do_option_name: List[Tuple[DoOption | None, str | None]] = [
    (DoOption.ADD, "add"),
    (DoOption.DELETE, "delete"),
    (DoOption.SHOW, "show"),
    (None, None),
]

test_case_prompt: List[Tuple[str, COLOR, str]] = [
    ("1", "light_green", "1"),
    ("2", "light_green", "2"),
    ("3", "light_green", "3"),
]

test_case_validate_prompt: List[Tuple[str, bool]] = [
    ("1", True),
    ("2", True),
    ("3", True),
    ("4", False),
    ("5", False),
]

test_case_should_exit: Tuple[Tuple[str, bool], ...] = (
    ("quit", True),
    ("exit", True),
    ("Quit", True),
    ("qUit", True),
    ("eXIt", True),
    ("ext", False),
    ("q", False),
    ("back", False),
    ("ex", False),
    ("1", False),
)


def create_tasks(task_n: int = 5) -> list[TaskItem]:
    return [TaskItem(id, "<Name>", "<Description>") for id in range(task_n)]


# Synchronous fixture that provides test case data
def create_test_case_get_task() -> (
    Tuple[Tuple[int, List[TaskItem], TaskItem | None], ...]
):
    # Synchronously create tasks for different cases
    tasks_5 = create_tasks(5)  # List of 5 TaskItem objects
    tasks_1 = create_tasks(1)  # List of 1 TaskItem object
    tasks_0 = create_tasks(0)  # List of 1 TaskItem object

    # Return a tuple of test cases as described
    return (
        (0, tasks_5, TaskItem(0, "Name0", "Description0")),
        (1, tasks_5, TaskItem(1, "Name1", "Description1")),
        (2, tasks_5, TaskItem(2, "Name2", "Description2")),
        (3, tasks_5, TaskItem(3, "Name3", "Description3")),
        (4, tasks_5, TaskItem(4, "Name4", "Description4")),
        (5, tasks_1, None),
        (6, tasks_1, None),
        (7, tasks_1, None),
        (0, tasks_0, None),
    )


test_case_get_task = create_test_case_get_task()
