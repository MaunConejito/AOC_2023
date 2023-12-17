from .models import *
import sys

# PARSING


def parse_map(input: str) -> Map:
    tiles: list[list[Tile]] = []
    for i, line in enumerate(input.split('\n')):
        row: list[Tile] = []
        for j, char in enumerate(line):
            pos = Position(i, j)
            row.append(Pipe(pos, PipeSymbol(char)) if char in PipeSymbol
                       else Tile(pos, NonPipeSymbol(char)))
        tiles.append(row)
    map = Map(tiles)
    map.connect_pipes()
    map.connect_start()
    return map

# UTIL


def recursion_test(counter: int):
    try:
        recursion_test(counter + 1)
    except RecursionError:
        print('reached depth {}'.format(counter))


# EXPORTED PROCESS FUNCTION


def process(input: str):
    sys.setrecursionlimit(20000)
    map = parse_map(input)
    return int(map.get_start_loop_length() / 2)
