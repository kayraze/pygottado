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
    select_task_id,
    save_tasks,
    get_task,
    CLEAR_SCREEN_COMMANDS,
)


async def handle_operation(operation: DoOption) -> None:
    # IF WE WANT TO ADD A TASK
    if operation == DoOption.ADD:
        tasks: List[TaskItem] = await get_all_tasks()
        task: TaskItem = await prompt_task()
        await save_tasks([*tasks, task])

    # IF WE WANT TO DELETE A TASK
    elif operation == DoOption.DELETE:
        tasks = await get_all_tasks()
        if not tasks:
            cprint("\tNo availabe task to remove", "light_red")
            return

        await show_tasks(tasks)
        selected_task_id: int | None = await select_task_id()
        if selected_task_id is None:
            cprint(
                f"\tInvalid Task ID ( select a given ID from above )",
                "light_red",
                attrs=["bold"],
            )
            return

        selected_task: TaskItem | None = await get_task(selected_task_id, tasks)

        if selected_task is not None:
            tasks.remove(selected_task)
            await save_tasks(tasks)
            cprint(f"\tTask {selected_task_id} removed", "light_red", attrs=["bold"])
        else:
            cprint(
                f"\tTask {selected_task_id} does not exist", "light_red", attrs=["bold"]
            )

    # IF WE WANT TO SHOW ALL TASKS
    elif operation == DoOption.SHOW:
        tasks = await get_all_tasks()
        if not tasks:
            cprint("\tNo tasks saved", "light_red")
            return

        await show_tasks(tasks)


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

            # CHECK IF USER WANTS TO EXIT
            if await should_exit(answer):
                cprint("\tQuitting..\n", color="light_yellow")
                exit()

            # CHECK IF USER WANTS TO CLEAR SCREEN
            if answer.lower() in CLEAR_SCREEN_COMMANDS:
                await clear_screen()
                continue

            # CHECK IF THE USER INPUT IS A VALID DoOption
            if not await validate_prompt(answer):
                await invalid_answer(answer)
                continue

            # JUST GET THE DoOption FROM THE USER INPUT
            operation: DoOption | None = await get_do_option(int(answer))
            if not operation:
                await invalid_answer(answer)
                continue

            try:
                await handle_operation(operation)
            except Exception:
                raise

        except KeyboardInterrupt:
            raise


# JUST A SYNCHRONOUS FUNCTION TO CALL TO RUN THE ASYNC MAIN FUNCTION
def run() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        raise


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        cprint("\n\t Interrupted!, exiting...", "red", attrs=["bold"])
        exit()
