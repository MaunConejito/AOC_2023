from pydantic import BaseModel

class Card(BaseModel):
    id: int
    winning_numbers: list[int]
    had_numbers: list[int]

class Deck(BaseModel):
    cards: dict[int, tuple[Card, int]]