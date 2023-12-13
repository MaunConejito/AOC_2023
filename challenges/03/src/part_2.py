from models import Number, Symbol, Region, Position
from functools import reduce

# PARSING

def is_number(s: str):
    try:
        int(s)
        return True
    except:
        return False
    
def get_number_at(line: str, col_from: int, row: int) -> Number:
    col_to = col_from
    while(is_number(line[col_from : col_to + 2]) and col_to + 1 < len(line)):
        col_to += 1
    return Number(
        region=Region(row=row, from_column=col_from, to_column=col_to),
        value=int(line[col_from : col_to + 1]))

def parse_numbers(line: str, row: int) -> list[Number]:
    size = len(line)
    numbers = []
    col = 0
    while col < size:
        if is_number(line[col]):
            number = get_number_at(line, col, row)
            numbers.append(number)
            col = number.region.to_column + 1
        else:
            col += 1
    return numbers

def parse_symbols(line: str, row: int) -> list[Symbol]:
    size = len(line)
    symbols = []
    for col in range(size):
        token = line[col]
        if not is_number(token) and token != '.':
            symbol = Symbol(token=token, position=Position(column=col, row=row))
            symbols.append(symbol)
    return symbols

# UTIL

def are_adjacent(number: Number, symbol: Symbol) -> bool:
    return abs(symbol.position.row - number.region.row) <= 1 and\
        (symbol.position.column >= number.region.from_column - 1 and\
         symbol.position.column <= number.region.to_column + 1)

def get_adjacent_numbers(symbol: Symbol, numbers: list[Number]) -> list[Number]:
    adjacent_numbers = [number for number in numbers if are_adjacent(number, symbol)]
    if len(adjacent_numbers) > 1:
        return adjacent_numbers
    return [Number(region=Region(to_column=0, from_column=0, row=0), value=0)]

# EXPORTED PROCESS FUNCTION

def process(input: str):
    lines = input.split()
    numbers = [number for (i, line) in enumerate(lines) for number in parse_numbers(line, i)]
    gears = [symbol for (i, line) in enumerate(lines) for symbol in parse_symbols(line, i) if symbol.token == '*']
    return sum([reduce(lambda x, y: x*y, [n.value for n in get_adjacent_numbers(gear, numbers)]) for gear in gears])