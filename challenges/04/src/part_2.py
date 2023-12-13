from models import Card, Deck


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

def evaluate_card(deck: Deck, id: int):
    card = deck.cards[id][0]
    winners = number_of_had_winners(card)
    factor = deck.cards[id][1]
    ids_to_add = [id + 1 + i for i in range(winners)]
    for id_to_add in ids_to_add:
        if id_to_add in deck.cards:
            deck.cards[id_to_add] = (deck.cards[id_to_add][0], deck.cards[id_to_add][1] + factor)

# EXPORTED PROCESS FUNCTION

def process(input: str):
    original_cards = parse_cards(input)
    deck = Deck(cards={card.id: (card, 1) for card in original_cards})
    for id in deck.cards:
        evaluate_card(deck, id)
    return sum([deck.cards[id][1] for id in deck.cards])