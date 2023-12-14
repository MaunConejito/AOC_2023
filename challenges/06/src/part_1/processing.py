from .models import *
from functools import reduce


# PARSING


def parse_numbers(number_str: str) -> str:
    return [int(number) for number in number_str.split()[1:]]


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


def compute_possible_distances(race: Race):
    time = race.time
    return [
        distance(waiting_time, time - waiting_time) for waiting_time in range(time + 1)
    ]


def number_of_possible_wins(race: Race) -> int:
    possible_distances = compute_possible_distances(race)
    return sum([dist > race.record for dist in possible_distances])


# EXPORTED PROCESS FUNCTION


def process(input: str):
    races = parse_races(input)
    return reduce(lambda x, y: x*y, [number_of_possible_wins(race) for race in races])
