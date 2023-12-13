def process_line(line: str):
    numbers = []
    for c in line:
        try:
            numbers.append(int(c))
        except:
            pass
    if not numbers:
        return 0
    return 10 * numbers[0] + numbers[-1]

def process(input: str):
    return sum([process_line(line) for line in input.split()])