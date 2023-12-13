from pydantic import BaseModel
from enum import Enum

class Color(str, Enum):
    red = 'red'
    green = 'green'
    blue = 'blue'

class Draw(BaseModel):
    cubes_per_color: dict[Color, int] = {
        Color.red: 0,
        Color.green: 0,
        Color.blue: 0,
        }

class Game(BaseModel):
    id: int
    draws: list[Draw]