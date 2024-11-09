import asyncio
from termcolor import cprint
from typing import Tuple, List
import os

from .utils import (
    get_do_options,
    get_do_option,
    display_options,
    DoOption,
    ColorCycler,
    prompt,
    validate_prompt,
    invalid_answer,
    clear_screen,
    prompt_task,
    should_exit,
    TaskItem,
    get_all_tasks,
    show_tasks,
    select_task,
    remove_task,
    save_tasks,
)


async def main() -> None:
    color_cycler: ColorCycler = ColorCycler()
    while True:

        try:
            # Get the avaialble options
            options: Tuple[DoOption, ...] = await get_do_options()

            # Display/Print the options
            await display_options(list(options), color_cycler)

            # Get the user input
            answer: str = await prompt(color_cycler)

            if await should_exit(answer):
                cprint("\tQuitting..\n", color="light_yellow")
                exit()
            if not await validate_prompt(answer):
                await invalid_answer(answer)
                continue

            operation: DoOption | None = await get_do_option(int(answer))

            if operation == DoOption.ADD:
                tasks: List[TaskItem] = await get_all_tasks()
                task: TaskItem = await prompt_task()
                await save_tasks([*tasks, task])
            elif operation == DoOption.DELETE:
                tasks = await get_all_tasks()
                if not tasks:
                    cprint("\tNo availabe task to remove", "light_red")
                    continue
                await show_tasks(tasks)
                selected_task: TaskItem | None = await select_task(tasks)
                # cprint(f"selected task = {selected_task}")
                if selected_task is not None:
                    tasks.remove(selected_task)
                    await save_tasks(tasks)
                    cprint(f"\tTask {selected_task.id} removed", "light_red")
            elif operation == DoOption.SHOW:
                tasks = await get_all_tasks()
                if not tasks:
                    cprint("\tNo tasks saved", "light_red")
                    continue
                await show_tasks(tasks)

        except KeyboardInterrupt:
            raise


def run() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        cprint("\n\t Interrupted!, exiting...", "red", attrs=["bold"])
        exit()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        cprint("\n\t Interrupted!, exiting...", "red", attrs=["bold"])
        exit()
