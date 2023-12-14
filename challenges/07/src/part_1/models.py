from typing import ForwardRef
from pydantic import BaseModel, computed_field
from functools import total_ordering, cached_property
from enum import Enum


Card = ForwardRef('Card')


@total_ordering
class Card(int, Enum):
    A = 14
    K = 13
    Q = 12
    J = 11
    T = 10
    _9 = 9
    _8 = 8
    _7 = 7
    _6 = 6
    _5 = 5
    _4 = 4
    _3 = 3
    _2 = 2

    def __lt__(self, other: Card):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


card_dict: dict[str, Card] = {
    'A': Card.A,
    'K': Card.K,
    'Q': Card.Q,
    'J': Card.J,
    'T': Card.T,
    '9': Card._9,
    '8': Card._8,
    '7': Card._7,
    '6': Card._6,
    '5': Card._5,
    '4': Card._4,
    '3': Card._3,
    '2': Card._2,
}


HandType = ForwardRef('HandType')


@total_ordering
class HandType(int, Enum):
    FiveOfKind = 6
    FourOfKind = 5
    FullHouse = 4
    ThreeOfKind = 3
    TwoPair = 2
    OnePair = 1
    HighCard = 0

    def __lt__(self, other: HandType):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


def get_contained_times(hand: tuple[Card, ...], n: int, exceptions: list[Card] = []) -> Card | None:
    try:
        return next(ref for ref in Card if not ref in exceptions and sum(card == ref for card in hand) >= n)
    except StopIteration:
        return None


def is_type(type: HandType, hand: tuple[Card, Card, Card, Card, Card]) -> bool:
    match type:
        case HandType.FiveOfKind:
            return get_contained_times(hand, 5) is not None
        case HandType.FourOfKind:
            return get_contained_times(hand, 4) is not None
        case HandType.FullHouse:
            first = get_contained_times(hand, 3)
            second = get_contained_times(hand, 2, exceptions=[first])
            return first is not None and second is not None
        case HandType.ThreeOfKind:
            return get_contained_times(hand, 3) is not None
        case HandType.TwoPair:
            first = get_contained_times(hand, 2)
            second = get_contained_times(hand, 2, exceptions=[first])
            return first is not None and second is not None
        case HandType.OnePair:
            return get_contained_times(hand, 2) is not None
        case HandType.HighCard:
            return True
        case _:
            raise Exception('HandType not recognized')


Hand = ForwardRef('Hand')


@total_ordering
class Hand(BaseModel):
    cards: tuple[Card, Card, Card, Card, Card]

    @computed_field
    @cached_property
    def type(self) -> HandType:
        for type in HandType:
            if is_type(type, self.cards):
                return type
        return HandType.HighCard

    def __eq__(self, other: Hand):
        if self.__class__ is other.__class__:
            return self.cards == other.cards
        return NotImplemented

    def __lt__(self, other: Hand):
        if self.__class__ is other.__class__:
            if self.type != other.type:
                return self.type < other.type
            for (own, of_other) in zip(self.cards, other.cards):
                if own == of_other:
                    continue
                return own < of_other
            raise Exception('Error comparing hands: ' +
                            'it should not be possible for hands to have all the same cards but different types. ' +
                            'Compared hands:\n{hand_1}\n{hand_2}'.format(self, other))
        return NotImplemented


HandWithBid = ForwardRef('HandWithBid')


@total_ordering
class HandWithBid(BaseModel):
    hand: Hand
    bid: int

    def __eq__(self, other: HandWithBid):
        if self.__class__ is other.__class__:
            return self.hand == other.hand
        return NotImplemented

    def __lt__(self, other: HandWithBid):
        if self.__class__ is other.__class__:
            return self.hand < other.hand
        return NotImplemented
