from .models import *

# PARSING

def parse_starting_seeds(input: str) -> list[Seed]:
    seed_line = input.split('\n')[0]
    if not seed_line.startswith('seeds:'):
        raise Exception('No seed definition found.')
    return [Seed(id=int(number)) for number in seed_line.split(':')[-1].strip().split()]

def init_transformer(map_definition: str) -> Transformer:
    (source, dest) = map_definition.split()[0].split('-to-')
    return Transformer(source_type=source, dest_type=dest)

def parse_map_range(map_range_definition: str) -> MapRange:
    (dest, source, length) = map_range_definition.strip().split()
    return MapRange(source_start=source, destination_start=dest, length=length)

def parse_tranformer(lines: list[str]) -> Transformer:
    transformer = init_transformer(lines[0])
    for line in lines[1:]:
        if not line.strip():
            break
        transformer.map_ranges.append(parse_map_range(line))
    return transformer

def parse_tranformers(input: str) -> list[Transformer]:
    transformers = []
    lines = input.split('\n')
    for (i, line) in enumerate(lines):
        if 'map' in line:
            transformers.append(parse_tranformer(lines[i:]))
    return transformers

# UTIL

def find_transformer(transformers: list[Transformer], type: Type) -> Transformer:
    for transformer in transformers:
        if transformer.source_type == type:
            return transformer
    return None

def transform_all(entities: list[IdentifiableType], transformers: list[Transformer]):
    for i in range(len(entities)):
        transformer = find_transformer(transformers, entities[i].type())
        while(transformer):
            entities[i] = transformer.transform(entities[i])
            transformer = find_transformer(transformers, entities[i].type())

# EXPORTED PROCESS FUNCTION

def process(input: str):
    entities = parse_starting_seeds(input)
    transformers = parse_tranformers(input)
    transform_all(entities, transformers)
    return min([entity.id for entity in entities])