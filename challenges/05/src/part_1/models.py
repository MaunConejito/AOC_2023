from pydantic import BaseModel, Field
from enum import Enum
from typing import Callable

class Type(str, Enum):
    seed = 'seed'
    soil = 'soil'
    fertilizer = 'fertilizer'
    water = 'water'
    light = 'light'
    temperature = 'temperature'
    humidity = 'humidity'
    location = 'location'

class IdentifiableType(BaseModel):
    id: int
    type: Callable[[], Type]

class Seed(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.seed

class Soil(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.soil

class Fertilizer(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.fertilizer

class Water(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.water

class Light(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.light

class Temperature(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.temperature

class Humidity(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.humidity

class Location(IdentifiableType):
    @staticmethod
    def type() -> Type:
        return Type.location

type_dict: dict[Type, type] = {
    Type.seed: Seed,
    Type.soil: Soil,
    Type.fertilizer: Fertilizer,
    Type.water: Water,
    Type.light: Light,
    Type.temperature: Temperature,
    Type.humidity: Humidity,
    Type.location: Location,
}

class MapRange(BaseModel):
    source_start: int
    destination_start: int
    length: int

    def can_map(self, id: int):
        return id - self.source_start in range(self.length)
    
    def map(self, id: int):
        return id - self.source_start + self.destination_start

class Transformer(BaseModel):
    source_type: Type
    dest_type: Type
    map_ranges: list[MapRange] = []

    def transform(self, source: IdentifiableType) -> IdentifiableType | None:
        id = source.id
        for map_range in self.map_ranges:
            if map_range.can_map(id):
                return type_dict[self.dest_type](id=map_range.map(id))
        return type_dict[self.dest_type](id=id)