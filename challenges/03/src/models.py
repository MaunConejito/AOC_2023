from typing import NamedTuple
from pydantic import BaseModel

class Position(BaseModel):
    row: int
    column: int

class Region(BaseModel):
    row: int
    from_column: int
    to_column: int

class Symbol(BaseModel):
    position: Position
    token: str

class Number(BaseModel):
    region: Region
    value: int