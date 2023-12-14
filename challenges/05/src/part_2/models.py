from pydantic import BaseModel, computed_field
from enum import Enum
from typing import Callable

class ContRange(BaseModel):
    start: int
    length: int

    @computed_field
    def end(self) -> int:
        return self.start + self.length
    
    def add_offset(self, offset: int):
        self.start += offset

class FragRange(BaseModel):
    parts: list[ContRange] = []
    
    def add_offset(self, offset: int):
        for part in self.parts:
            part.add_offset(offset)
    
def intersection_cont_cont(first: ContRange, second: ContRange) -> FragRange:
    max_start = max(first.start, second.start)
    min_end = min(first.end, second.end)
    length = min_end - max_start
    parts = []
    if length > 0:
        parts.append(ContRange(start=max_start, length=length))
    return FragRange(parts=parts)

def difference_cont_cont(subject: ContRange, operand: ContRange) -> FragRange:
    if operand.end <= subject.start or operand.start >= subject.end:
        return FragRange(parts=[subject])
    parts = []
    if operand.start > subject.start:
        parts.append(ContRange(start=subject.start, length=operand.start-subject.start))
    if operand.end < subject.end:
        parts.append(ContRange(start=operand.end, length=subject.end-operand.end))
    return FragRange(parts=parts)
    
def intersection(first: FragRange, second: FragRange) -> FragRange:
    parts = []
    for first_part in first.parts:
        for second_part in second.parts:
            parts += intersection_cont_cont(first_part, second_part).parts
    return FragRange(parts=parts)

def difference_cont(subject: FragRange, operand: ContRange) -> FragRange:
    parts = []
    for part in subject.parts:
        parts += difference_cont_cont(part, operand).parts
    return FragRange(parts=parts)

def difference(subject: FragRange, operand: FragRange) -> FragRange:
    result = FragRange(parts=subject.parts)
    for part in operand.parts:
        result = difference_cont(result, part)
    return result

def union(subject: FragRange, operand: FragRange) -> FragRange:
    return FragRange(parts=subject.parts+operand.parts)

class RangeMap(BaseModel):
    range: FragRange
    offset: int

    def apply_to_range(self, subject: FragRange) -> tuple[FragRange, FragRange]:
        overlap = intersection(self.range, subject)
        rest = difference(subject, overlap)
        overlap.add_offset(self.offset)
        return (overlap, rest)


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
    id_range: FragRange
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

class Transformer(BaseModel):
    source_type: Type
    dest_type: Type
    range_maps: list[RangeMap] = []

    def transform(self, source: IdentifiableType) -> IdentifiableType | None:
        old = source.id_range
        new = FragRange()
        for range_map in self.range_maps:
            (processed, rest) = range_map.apply_to_range(old)
            old = rest
            new = union(new, processed)
        return type_dict[self.dest_type](id_range=union(new, old))