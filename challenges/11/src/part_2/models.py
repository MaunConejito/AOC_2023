from attrs import define, field
from enum import Enum
from typing import NamedTuple


def one_norm(point: 'Point') -> int:
    return abs(point.row) + abs(point.col)


def transpose(l: list[list]) -> list[list]:
    return list(map(list, zip(*l)))


class Point(NamedTuple):
    row: int
    col: int

    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.row - other.row, self.col - other.col)


class Tile(str, Enum):
    Space = '.'
    Galaxy = '#'


@define
class Galaxy():
    pos: Point

    def distance_to(self, other: 'Galaxy') -> int:
        return one_norm(other.pos - self.pos)


@define
class Universe():
    tiles: list[list[Tile]]
    empty_row_inds: list[int] = field(init=False)
    empty_col_inds: list[int] = field(init=False)

    def __attrs_post_init__(self):
        self.empty_row_inds = [row for row, tiles in enumerate(self.tiles)
                               if all(tile == Tile.Space for tile in tiles)]
        self.empty_col_inds = [col for col, tiles in enumerate(transpose(self.tiles))
                               if all(tile == Tile.Space for tile in tiles)]

    def empty_between(self, pos_1: Point, pos_2: Point) -> int:
        row_inds = sorted([pos_1.row, pos_2.row])
        col_inds = sorted([pos_1.col, pos_2.col])
        n_rows = len([i for i in self.empty_row_inds
                      if i > row_inds[0] and i < row_inds[1]])
        n_cols = len([i for i in self.empty_col_inds
                      if i > col_inds[0] and i < col_inds[1]])
        return n_rows + n_cols
