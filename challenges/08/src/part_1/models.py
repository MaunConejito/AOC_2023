from pydantic import BaseModel
from enum import Enum


class Direction(int, Enum):
    L = 0
    R = 1


direction_dict: dict[str, Direction] = {
    'L': Direction.L,
    'R': Direction.R,
}


class Map(BaseModel):
    instructions: list[Direction]
    nodes: dict[str, tuple[str, str]]
