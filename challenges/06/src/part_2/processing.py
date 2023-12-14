from .models import *
from functools import reduce
from math import sqrt, floor, ceil

# PARSING


def parse_numbers(number_str: str) -> str:
    return [int(number) for number in [''.join(number_str.split()[1:])]]


def parse_races(input: str) -> str:
    lines = input.split("\n")
    times_string = lines[0]
    records_string = lines[1]
    times = parse_numbers(times_string)
    records = parse_numbers(records_string)
    return [Race(time=time, record=record) for (time, record) in zip(times, records)]


# UTIL


def distance(waiting_time: int, racing_time: int) -> int:
    return racing_time * waiting_time


def number_of_possible_wins(race: Race) -> int:
    T = race.time
    R = race.record
    lower = int(floor(round(0.5*(T - sqrt(T**2 - 4*R)), 6)))
    upper = int(ceil(round(0.5*(T + sqrt(T**2 - 4*R)), 6)))
    return upper - lower - 1

# EXPORTED PROCESS FUNCTION


def process(input: str):
    races = parse_races(input)
    return reduce(lambda x, y: x*y, [number_of_possible_wins(race) for race in races])
