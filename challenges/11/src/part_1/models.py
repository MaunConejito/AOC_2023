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
    expanded: bool = False

    def insert_space_row_at(self, i: int):
        new_row = [Tile.Space] * len(self.tiles[0])
        self.tiles.insert(i, new_row)

    def insert_space_col_at(self, i: int):
        for row in self.tiles:
            row.insert(i, Tile.Space)

    def expand(self):
        rows_to_expand = [row for row, tiles in enumerate(self.tiles)
                          if all(tile == Tile.Space for tile in tiles)]
        cols_to_expand = [row for row, tiles in enumerate(transpose(self.tiles))
                          if all(tile == Tile.Space for tile in tiles)]
        for i, row in enumerate(rows_to_expand):
            self.insert_space_row_at(row + i)
        for j, col in enumerate(cols_to_expand):
            self.insert_space_col_at(col + j)
        self.expanded = True
