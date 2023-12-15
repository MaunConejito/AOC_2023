from .models import *

# PARSING


def parse_sequence(line: str) -> Sequence:
    return Sequence([int(n) for n in line.split()])


def parse_sequences(input: str) -> list[Sequence]:
    return [parse_sequence(line) for line in input.split('\n')]

# UTIL

# EXPORTED PROCESS FUNCTION


def process(input: str):
    return sum(seq.prev() for seq in parse_sequences(input))
