import pytest
from pygottado.utils.classes import TaskItem
import pytest_asyncio
from typing import Generator, AsyncGenerator


def create_tasks(task_n: int = 5) -> list[TaskItem]:
    return [TaskItem(id, "<Name>", "<Description>") for id in range(task_n)]
