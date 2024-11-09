from .constants import COLOR_LIST, COLOR
import datetime


class TaskItem:

    def __init__(self, id: int, name: str, description: str) -> None:
        self.id = id
        self.name = name
        self.description = description


class ColorCycler:

    def __init__(self, index: int = 0) -> None:
        self.index = index

    async def use_index(self) -> int:
        i = self.index
        self.index += 1
        return i

    async def get_next_color(self) -> COLOR:
        return COLOR_LIST[await self.use_index() % len(COLOR_LIST)]


__all__ = ["TaskItem", "ColorCycler"]
