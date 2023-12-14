from .models import *
from math import lcm

# PARSING


def parse_instructions(instruction_string: str) -> list[Direction]:
    return [direction_dict[c] for c in instruction_string]


def parse_node(node_string: str) -> tuple[str, str, str]:
    key, link_string = node_string.split('=')
    l, r = link_string.split(',')
    return key.strip(), l.strip(' ()'), r.strip(' ()')


def parse_nodes(node_strings: list[str]) -> dict[str, tuple[str, str]]:
    return {key: (l, r) for (key, l, r) in (parse_node(node_string) for node_string in node_strings)}


def parse_map(map_string: str) -> Map:
    lines = map_string.split('\n')
    instruction_string = lines[0]
    node_strings = lines[2:]
    return Map(instructions=parse_instructions(instruction_string), nodes=parse_nodes(node_strings))

# UTIL


def traverse(map: Map, start_id: str = 'AAA'):
    i = 0
    n_instructions = len(map.instructions)
    prev_id = start_id
    while not prev_id.endswith('Z'):
        next_id = map.nodes[prev_id][map.instructions[i % n_instructions]]
        yield next_id
        prev_id = next_id
        i += 1

# EXPORTED PROCESS FUNCTION


def process(input: str):
    map = parse_map(input)
    starts = [id for id in map.nodes if id.endswith('A')]
    periods = [sum(1 for _ in traverse(map, start)) for start in starts]
    return lcm(*periods)
