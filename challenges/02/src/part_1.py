from models import Game, Draw, Color

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

def draw_is_possible(draw: Draw, reference_draw: Draw) -> bool:
    return all([draw.cubes_per_color[color] <= reference_draw.cubes_per_color[color] for color in list(Color)])

def game_is_possible(game: Game, reference_draw: Draw) -> bool:
    return all([draw_is_possible(draw, reference_draw) for draw in game.draws])

# EXPORTED PROCESS FUNCTION

def process(input: str):
    reference_draw = Draw(cubes_per_color={
        'red' : 12,
        'green': 13,
        'blue': 14,
        })
    games = parse_games(input)
    possible_ids = [game.id for game in games if game_is_possible(game, reference_draw)]
    return sum(possible_ids)