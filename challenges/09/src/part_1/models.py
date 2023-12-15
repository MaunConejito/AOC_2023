from attrs import define
import numpy as np


@define
class Sequence():
    numbers: list[int]

    def derivative(self) -> 'Sequence':
        return Sequence(numbers=list(np.diff(self.numbers)))

    def next(self) -> int:
        if not any(self.numbers):
            return 0
        return self.numbers[-1] + self.derivative().next()
