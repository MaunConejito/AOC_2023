from models import Card


# PARSING

def parse_id(card_name: str) -> int:
    return int(card_name.split()[-1])

def parse_numbers(numbers_string: str) -> list[int]:
    return [int(number_string) for number_string in numbers_string.split()]

def parse_card(card_str: str) -> Card:
    (card_name, all_numbers_string) = card_str.split(':')
    (winning_numbers_string, had_numbers_string) = all_numbers_string.split('|')
    id = parse_id(card_name.strip())
    winning_numbers = parse_numbers(winning_numbers_string.strip())
    had_numbers = parse_numbers(had_numbers_string.strip())
    return Card(id=id, winning_numbers=winning_numbers, had_numbers=had_numbers)

def parse_cards(input: str) -> list[Card]:
    return [parse_card(line) for line in input.split('\n')]

# UTIL

def number_of_had_winners(card: Card) -> int:
    return sum([number in card.winning_numbers for number in card.had_numbers])

def points(card: Card) -> int:
    n = number_of_had_winners(card)
    return 2**(n - 1) if n > 0 else 0

# EXPORTED PROCESS FUNCTION

def process(input: str):
    cards = parse_cards(input)
    return sum([points(card) for card in cards])