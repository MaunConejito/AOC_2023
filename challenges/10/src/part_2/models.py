from attrs import define, field
from enum import Enum
from typing import NamedTuple, Callable
import math
from functools import cached_property


class NonPipeSymbol(str, Enum):
    Ground = '.'


class PipeSymbol(str, Enum):
    NorthSouth = '|'
    WestEast = '-'
    NorthWest = 'J'
    NorthEast = 'L'
    SouthWest = '7'
    SouthEast = 'F'
    Start = 'S'


class Position(NamedTuple):
    row: int
    col: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.col + other.col)

    def __sub__(self, other: 'Position') -> 'Position':
        return Position(self.row - other.row, self.col - other.col)

    def __neg__(self) -> 'Position':
        return Position(-self.row, -self.col)


class Direction(Position, Enum):
    North = Position(-1,  0)
    South = Position(1,  0)
    West = Position(0, -1)
    East = Position(0,  1)


directions_of_pipe: dict[PipeSymbol, list[Direction]] = {
    PipeSymbol.NorthSouth: [Direction.North, Direction.South],
    PipeSymbol.WestEast: [Direction.West, Direction.East],
    PipeSymbol.NorthWest: [Direction.North, Direction.West],
    PipeSymbol.NorthEast: [Direction.North, Direction.East],
    PipeSymbol.SouthWest: [Direction.South, Direction.West],
    PipeSymbol.SouthEast: [Direction.South, Direction.East],
    PipeSymbol.Start: [Direction.North, Direction.South, Direction.West, Direction.East],
}


@define
class Tile:
    pos: Position
    symbol: PipeSymbol | NonPipeSymbol


@define
class Pipe(Tile):
    symbol: PipeSymbol
    partners: list['Pipe'] = field(factory=list)
    recursion_count: int = 0

    def __str__(self) -> str:
        return '{} ({}, {})'.format(self.symbol.value, self.pos[0], self.pos[1])

    def can_connect_to(self, other: 'Pipe') -> bool:
        dpos = other.pos - self.pos
        if sum(abs(n) for n in dpos) != 1:
            return False
        return dpos in directions_of_pipe[self.symbol] and\
            -dpos in directions_of_pipe[other.symbol]

    def connect_to(self, other: 'Pipe'):
        if not self.can_connect_to(other):
            print('WARNING: connecting non-connectable pipes {} and {}'
                  .format(self, other))
        if not other in self.partners:
            self.partners.append(other)
        if not self in other.partners:
            other.partners.append(self)
        if len(self.partners) > 2 or len(other.partners) > 2:
            raise Exception('Something went wrong...')

    def try_get_chains_to(self, pipe: 'Pipe') -> list[list['Pipe']]:
        if self == pipe:
            return [[self]]
        chains: list[list['Pipe']] = []
        for partner in self.partners:
            chain: list['Pipe'] = [self, partner]
            if partner == pipe:
                chains.append(chain)
                continue
            while (len(chain[-1].partners) > 1):
                next = [p for p in chain[-1].partners if p != chain[-2]][0]
                chain.append(next)
                if next == pipe:
                    chains.append(chain)
                    break
        return chains

    def is_connected_to(self, pipe: 'Pipe') -> bool:
        return len(self.try_get_chains_to(pipe)) > 0

    def distance_to(self, pipe: 'Pipe', dont_ask: 'Pipe') -> float:
        chains = self.try_get_chains_to(pipe)
        if len(chains) == 0:
            return float('inf')
        return min(len(chain)-1 for chain in chains)


@define
class Map:
    tiles: list[list[Tile]]

    def pipes(self) -> list[Pipe]:
        return [tile for row in self.tiles for tile in row if isinstance(tile, Pipe)]

    def start(self) -> Pipe | None:
        for pipe in self.pipes():
            if pipe.symbol == PipeSymbol.Start:
                return pipe

    def __getitem__(self, indices) -> Tile | list[Tile] | None:
        try:
            if not isinstance(indices, tuple):
                if indices < 0:
                    raise IndexError()
                return self.tiles[indices]
            if any(index < 0 for index in indices):
                raise IndexError()
            return self.tiles[indices[0]][indices[1]]
        except IndexError:
            return None

    def connect_pipes(self):
        pipes = self.pipes()
        for pipe in pipes:
            for tile in [self[pipe.pos + dir] for dir in Direction]:
                if isinstance(tile, Pipe):
                    if pipe.can_connect_to(tile):
                        pipe.connect_to(tile)

    def connect_start(self):
        start = self.start()
        if not start:
            raise Exception('Something went wrong...')
        neighbors = [tile for tile in [self[start.pos + dir] for dir in Direction]
                     if isinstance(tile, Pipe)]
        for n1 in neighbors:
            for n2 in neighbors:
                if n1 != n2:
                    if start.can_connect_to(n1) and start.can_connect_to(n2):
                        if n1.is_connected_to(n2):
                            start.connect_to(n1)
                            start.connect_to(n2)
                            return
        print('Start could not be connected')

    def get_main_loop_length(self) -> float:
        start = self.start()
        if not start:
            return 0
        partner = start.partners[0]
        if not partner:
            return 0
        return partner.distance_to(start, start) + 1

    def get_main_loop_chain(self) -> list[Pipe]:
        start = self.start()
        if not start:
            return []
        partner = start.partners[0]
        if not partner:
            return []
        chains = start.try_get_chains_to(partner)
        if not chains:
            return []
        max_ind = max(enumerate(len(chain)
                      for chain in chains), key=lambda x: x[1])[0]
        return chains[max_ind]

    def evaluate_edge_cache(self, edge_cache: list[Pipe]):
        if len(edge_cache) == 1:
            return True
        dirs = [dir for pipe in edge_cache for dir in directions_of_pipe[pipe.symbol]]
        return Direction.North in dirs and Direction.South in dirs

    def count_inner(self) -> int:
        main_chain = self.get_main_loop_chain()
        main_chain_indices = [pipe.pos for pipe in main_chain]
        inner_counter = 0
        for row in self.tiles:
            cross_counter = 0
            edge_cache: list[Pipe] = []
            for tile, next in zip(row[:-1], row[1:]):
                if isinstance(tile, Pipe) and tile.pos in main_chain_indices:
                    edge_cache.append(tile)
                    if not next in tile.partners:
                        if self.evaluate_edge_cache(edge_cache):
                            cross_counter += 1
                        edge_cache = []
                else:
                    inner_counter += (cross_counter % 2)
        return inner_counter
