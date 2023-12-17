from .models import *

# PARSING


def parse_universe(input: str) -> Universe:
    tile_rows: list[list[Tile]] = []
    for line in input.split('\n'):
        tile_row: list[Tile] = []
        for c in line:
            tile_row.append(Tile(c))
        tile_rows.append(tile_row)
    return Universe(tile_rows)

# UTIL


def galaxies_from_expanded_universe(universe: Universe) -> list[Galaxy]:
    if not universe.expanded:
        raise ValueError('Universe not expanded.')
    galaxies: list[Galaxy] = []
    for row, tiles in enumerate(universe.tiles):
        for col, tile in enumerate(tiles):
            if tile == Tile.Galaxy:
                galaxies.append(Galaxy(Point(row, col)))
    return galaxies

# EXPORTED PROCESS FUNCTION


def process(input: str):
    universe = parse_universe(input)
    universe.expand()
    galaxies = galaxies_from_expanded_universe(universe)
    double_dist_sum = 0
    for galaxy_1 in galaxies:
        for galaxy_2 in galaxies:
            double_dist_sum += galaxy_1.distance_to(galaxy_2)
    return int(double_dist_sum / 2)
