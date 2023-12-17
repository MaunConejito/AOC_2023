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


def galaxies_from_universe(universe: Universe) -> list[Galaxy]:
    galaxies: list[Galaxy] = []
    for row, tiles in enumerate(universe.tiles):
        for col, tile in enumerate(tiles):
            if tile == Tile.Galaxy:
                galaxies.append(Galaxy(Point(row, col)))
    return galaxies


def expanded_distance_between(galaxy_1: Galaxy, galaxy_2: Galaxy,
                              universe: Universe, expansion: int) -> int:
    dist = galaxy_1.distance_to(galaxy_2)
    return dist + universe.empty_between(galaxy_1.pos, galaxy_2.pos) * (expansion-1)

# EXPORTED PROCESS FUNCTION


def process(input: str):
    universe = parse_universe(input)
    galaxies = galaxies_from_universe(universe)
    double_dist_sum = 0
    for galaxy_1 in galaxies:
        for galaxy_2 in galaxies:
            double_dist_sum += expanded_distance_between(
                galaxy_1, galaxy_2, universe, 1000000)
    return int(double_dist_sum / 2)
