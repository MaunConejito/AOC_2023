from models import Game, Draw, Color
from functools import reduce

# PARSING

def parse_draw(draw_string: str) -> Draw:
    draw = Draw()
    number_color_string_pairs = [s.strip().split() for s in draw_string.split(',')]
    for (number_string, color_string) in number_color_string_pairs:
        draw.cubes_per_color[color_string] = int(number_string)
    return draw

def parse_draws(draws_string: str) -> list[Draw]:
    return [parse_draw(s.strip()) for s in draws_string.split(';')]

def parse_game_id(game_name: str) -> int:
    return int(game_name.split()[-1])

def parse_game(game_string: str) -> Game | None:
    if not game_string.startswith('Game'):
        return None
    (game_name, draws_string) = game_string.split(':')
    id = parse_game_id(game_name)
    draws = parse_draws(draws_string)
    return Game(id=id, draws=draws)

def parse_games(input: str) -> list[Game]:
    return [game for game in [parse_game(line) for line in input.split('\n')] if game]

# UTIL

def power(game: Game) -> int:
    return reduce(lambda x, y: x*y, [max([draw.cubes_per_color[color] for draw in game.draws]) for color in list(Color)])

# EXPORTED PROCESS FUNCTION

def process(input: str):
    games = parse_games(input)
    powers = [power(game) for game in games]
    return sum(powers)