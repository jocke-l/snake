import enum
from collections import namedtuple


class Coordinate(namedtuple('CoordinateBase', 'x y')):
    def __add__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Coordinate(self.x + other, self.y + other)
        else:
            raise ValueError(f'Cannot add Coordinate with '
                             f'{type(other).__name__}')

    def __mul__(self, other):
        if isinstance(other, Coordinate):
            return Coordinate(self.x * other.x, self.y * other.y)
        elif isinstance(other, int):
            return Coordinate(self.x * other, self.y * other)
        else:
            raise ValueError(f'Cannot multiply Coordinate with '
                             f'{type(other).__name__}')

    def __abs__(self):
        return Coordinate(abs(self.x), abs(self.y))

    def cross_product(self, other):
        return self.x * other.y - other.x * self.y



class Direction(enum.Enum):
    RIGHT = Coordinate(1, 0)
    LEFT = Coordinate(-1, 0)
    UP = Coordinate(0, 1)
    DOWN = Coordinate(0, -1)

    def __abs__(self):
        return abs(self.value)


class Segment:
    def __init__(self, direction, start, length, initial_forward=False):
        self.direction = direction
        self.start = start
        self.length = length

        if initial_forward:
            self.forward()

    def __repr__(self):
        return f'<{self}>'

    def __str__(self):
        return (f'{type(self).__name__}({self.direction}, {self.start}, '
                f'{self.length})')

    @property
    def end(self):
        return self.forward_position(self.length - 1)

    def forward_position(self, steps=1) -> Coordinate:
        return self.start + self.direction.value * steps

    def forward(self):
        self.start = self.forward_position()

    def crosses_point(self, point):
        return abs(
            Coordinate(
                self.end.x - self.start.x,
                self.end.y - self.start.y
            ).cross_product(
                Coordinate(
                    point.x - self.start.x,
                    point.y - self.start.y
                )
            )
        ) < 0.0001


class Body:
    def __init__(self, head_segment_start, head_segment_length):
        self.segments = [Segment(Direction.RIGHT, head_segment_start,
                                 head_segment_length)]

    @property
    def length(self):
        return sum(segment.length for segment in self.segments)

    @property
    def head_segment(self):
        return self.segments[-1]

    @property
    def tail_segments(self):
        return self.segments[:-2]

    @property
    def tail_segment(self):
        return self.segments[0]

    @tail_segment.deleter
    def tail_segment(self):
        del self.segments[0]

    def self_collision(self):
        for segment in self.tail_segments:
            if segment.crosses_point(self.head_segment.end):
                return True

        return False

    def forward(self):
        if self.head_segment == self.tail_segment:
            self.head_segment.forward()
        else:
            self.tail_segment.length -= 1
            if self.tail_segment.length > 1:
                self.tail_segment.forward()
            else:
                # Merge last two segments
                del self.tail_segment
                self.tail_segment.start = self.tail_segment.forward_position(-1)
                self.tail_segment.length += 1

            self.head_segment.length += 1

    def turn(self, direction):
        if abs(direction) != abs(self.head_segment.direction):
            self.segments.append(Segment(direction, self.head_segment.end, 0,
                                         initial_forward=True))
