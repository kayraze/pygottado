from .constants import (
    DoOption,
    COLOR_LIST,
    DO_OPTION_DICT,
    DO_OPTION_NAME,
    COLOR,
    EXIT_CODES,
    TASKS_JSON_PATH,
)
from .classes import ColorCycler, TaskItem
from termcolor import colored, cprint
import os
import aiofiles
import asyncio
from typing import Callable, Awaitable
import json
from typing import List


# Get a DoOption from its option number
async def get_do_option(option_no: int) -> DoOption | None:
    try:
        return DO_OPTION_DICT[option_no]
    except KeyError:
        return None


# Get the string name of a DoOption
async def get_do_option_name(do_option: DoOption) -> str | None:
    try:
        return DO_OPTION_NAME[do_option]
    except KeyError:
        return None


# Get all available DoOptions
async def get_do_options() -> tuple[DoOption, ...]:
    return tuple(DO_OPTION_DICT.values())  # Return as a tuple


# Display the options with color
async def display_options(
    option_list: list[DoOption], color_cyler: ColorCycler
) -> None:
    # print("eyyy")
    cprint("\n\t==== Options ====", color=await color_cyler.get_next_color())
    # print("==== Options ==== ")
    for option in option_list:
        cprint(
            f"\t  {option.value}: {DO_OPTION_NAME[option]}",
            color=await color_cyler.get_next_color(),
        )


# Placeholder function for tasks
async def get_task_list() -> list[TaskItem] | None:
    # Implement your task fetching logic here
    pass


async def prompt(color_cycler: ColorCycler) -> str:
    prompt_text: str = colored(
        "\r\t> ", color=await color_cycler.get_next_color(), attrs=["bold"]
    )
    print("")
    while True:
        try:
            answer: str = await asyncio.to_thread(input, prompt_text)
            if answer.strip():
                return answer
            print("\033[A", end="")
        except KeyboardInterrupt:
            print("\nInterrupt received, exiting...")
            raise  # Re-raise the KeyboardInterrupt to propagate it


async def validate_prompt(prompt_str: str) -> bool:
    try:
        return int(prompt_str) in DO_OPTION_DICT.keys() if prompt_str else False
    except ValueError:
        return False


async def invalid_answer(prompt_str: str) -> None:
    cprint(f'\n\tInvalid answer: "{prompt_str}"', color="light_red", attrs=["bold"])


async def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


async def should_exit(code: str) -> bool:
    return code.lower() in EXIT_CODES


async def prompt_task() -> TaskItem:
    try:
        prompt1: str = colored("\tTask name   > ", "light_blue")
        prompt2: str = colored("\tDescription > ", "light_green")

        task_name: str = input(prompt1)
        description: str = input(prompt2)
        task_id: int = 0
        for task in await get_all_tasks():
            if task_id == task.id:
                task_id += 1
                continue
            break

        return TaskItem(id=task_id, name=task_name, description=description)
    except KeyboardInterrupt:
        raise


async def remove_task(remove_task: TaskItem, tasks: List[TaskItem]) -> List[TaskItem]:
    return [task for task in tasks if task != remove_task]


async def select_task(tasks: List[TaskItem]) -> TaskItem | None:
    try:
        prompt_text: str = colored("\n\tSelect Task > ", "light_blue", attrs=["bold"])
        task_id: int = int(input(prompt_text))
        task: TaskItem | None = await get_task(task_id, tasks)
        # cprint(f"from get task = {task}", "red")
        return task
    except ValueError:
        return None
    except KeyboardInterrupt:
        return None


async def get_all_tasks() -> List[TaskItem]:
    tasks: List[TaskItem] = []
    async with aiofiles.open(TASKS_JSON_PATH, "r+") as file:
        json_str: str = await file.read()
        tasks_dict = json.loads(json_str)
        for task in tasks_dict:
            tasks.append(
                TaskItem(
                    id=task["id"], name=task["name"], description=task["description"]
                )
            )
        return tasks


async def show_tasks(tasks: List[TaskItem]) -> None:
    for task in tasks:
        cprint(f"\n\t[ID]          :\t{task.id}", "light_cyan")
        cprint(f"\t[NAME]        :\t{task.name}", "light_blue")
        cprint(f"\t[DESCRIPTION] :\t{task.description}\n", "light_green")


async def get_task(task_id: int, tasks: List[TaskItem]) -> TaskItem | None:
    for task in tasks:
        if task.id == task_id:
            return task
    return None


async def save_tasks(tasks: List[TaskItem]) -> None:
    async with aiofiles.open(TASKS_JSON_PATH, "w+") as file:
        json_str = json.dumps([task.__dict__ for task in tasks])
        await file.write(json_str)


# async def add_task(task: TaskItem) -> None:
#     async with aiofiles.open("data/tasks.json")


__all__ = [
    "get_do_options",
    "display_options",
    "get_do_option",
    "get_do_option_name",
    "prompt",
    "validate_prompt",
    "invalid_answer",
    "clear_screen",
    "should_exit",
    "show_tasks",
    "select_task",
    "get_task",
    "save_tasks",
    "prompt_task",
    "get_all_tasks",
    "remove_task",
]
