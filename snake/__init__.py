from typing import Union


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __add__(self, other: Union['Coordinate', int]) -> 'Coordinate':
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Coordinate(self.x + other, self.y + other)
        else:
            raise ValueError(f'Cannot add Coordinate with '
                             f'{type(other).__name__}')

    def __mul__(self, other: Union['Coordinate', int]) -> 'Coordinate':
        if isinstance(other, Coordinate):
            return Coordinate(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Coordinate(self.x * other, self.y * other)
        else:
            raise ValueError(f'Cannot multiply Coordinate with '
                             f'{type(other).__name__}')

    def __abs__(self) -> 'Coordinate':
        return Coordinate(abs(self.x), abs(self.y))

