from .models import *

# PARSING

def parse_starting_seeds(input: str) -> Seed:
    seed_line = input.split('\n')[0]
    if not seed_line.startswith('seeds:'):
        raise Exception('No seed definition found.')
    numbers = [int(number) for number in seed_line.split(':')[-1].strip().split()]
    id_range = FragRange()
    for i in range(len(numbers))[::2]:
        start = numbers[i]
        length = numbers[i+1]
        id_range.parts.append(ContRange(start=start, length=length))
    return Seed(id_range=id_range)

def init_transformer(map_definition: str) -> Transformer:
    (source, dest) = map_definition.split()[0].split('-to-')
    return Transformer(source_type=source, dest_type=dest)

def parse_range_map(map_range_definition: str) -> RangeMap:
    (dest, source, length) = [int(number) for number in map_range_definition.strip().split()]
    cont_range = ContRange(start=source, length=length)
    return RangeMap(range=FragRange(parts=[cont_range]), offset=dest-source)

def parse_tranformer(lines: list[str]) -> Transformer:
    transformer = init_transformer(lines[0])
    for line in lines[1:]:
        if not line.strip():
            break
        transformer.range_maps.append(parse_range_map(line))
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

def transform(entity: IdentifiableType, transformers: list[Transformer]) -> IdentifiableType:
    transformer = find_transformer(transformers, entity.type())
    while(transformer):
        entity = transformer.transform(entity)
        transformer = find_transformer(transformers, entity.type())
    return entity

# EXPORTED PROCESS FUNCTION

def process(input: str):
    entity = parse_starting_seeds(input)
    transformers = parse_tranformers(input)
    entity = transform(entity, transformers)
    return min(p.start for p in entity.id_range.parts)