from typing import Callable

digits = {
    '0' : 0,
    '1' : 1,
    '2' : 2,
    '3' : 3,
    '4' : 4,
    '5' : 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    'one' : 1,
    'two' : 2,
    'three' : 3,
    'four' : 4,
    'five' : 5,
    'six' : 6,
    'seven' : 7,
    'eight' : 8,
    'nine' : 9,
    }

def extract_digit(s: str) -> str | None:
    for key in digits:
        if key in s:
            return digits[key]
    return None

def search_digit(line: str, traversal_strategy: Callable[[str, int], str]) -> str | None:
    size = len(line)
    for i in range(size):
        digit = extract_digit(traversal_strategy(line, i+1))
        if digit or digit == 0:
            return digit
    return None

def get_first(line: str) -> str | None:
    return search_digit(line, lambda l, i : l[:i])

def get_last(line: str) -> str | None:
    return search_digit(line, lambda l, i : l[-i:])

def process_line(line: str) -> int:
    first = get_first(line)
    last = get_last(line)
    if (first or first == 0) and (last or last == 0):
        return 10 * first + last
    return 0

def process(input: str) -> int:
    return sum([process_line(line) for line in input.split()])