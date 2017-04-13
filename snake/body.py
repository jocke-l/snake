import enum
from collections import namedtuple

Coordinate = namedtuple('Coordinate', 'x y')


class Direction(enum.Enum):
    RIGHT = 1
    LEFT = -1
    UP = 2
    DOWN = -2

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
        return f'Segment({self.direction}, {self.start}, {self.length})'

    @property
    def end(self):
        return self.forward_position(self.length - 1)

    def forward_position(self, steps=1):
        if self.direction == Direction.RIGHT:
            return Coordinate(self.start.x + steps, self.start.y)
        elif self.direction == Direction.LEFT:
            return Coordinate(self.start.x - steps, self.start.y)
        elif self.direction == Direction.UP:
            return Coordinate(self.start.x, self.start.y + steps)
        elif self.direction == Direction.DOWN:
            return Coordinate(self.start.x, self.start.y - steps)

    def forward(self):
        self.start = self.forward_position()


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
        return self.segments[:-1]

    @property
    def tail_segment(self):
        return self.segments[0]

    @tail_segment.deleter
    def tail_segment(self):
        del self.segments[0]

    def self_collision(self):
        raise NotImplemented

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
