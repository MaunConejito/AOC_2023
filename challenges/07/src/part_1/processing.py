from .models import *

# PARSING


def parse_hand(cards_string: str) -> Hand:
    return Hand(cards=tuple(card_dict[c] for c in cards_string))


def parse_hand_with_bid(hand_string: str) -> HandWithBid:
    cards_string, bid = hand_string.split()
    return HandWithBid(hand=parse_hand(cards_string), bid=int(bid))


def parse_hands(input: str) -> list[HandWithBid]:
    return [parse_hand_with_bid(line) for line in input.split('\n')]

# UTIL

# EXPORTED PROCESS FUNCTION


def process(input: str):
    hands_with_bids = parse_hands(input)
    return sum((i+1) * hand.bid for i, hand in enumerate(sorted(hands_with_bids)))
