import enum


class Direction(enum.Enum):
    RIGHT = 1
    LEFT = -1
    UP = 2
    DOWN = -2

    def __abs__(self):
        return abs(self.value)


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x, self.y == other.x, other.y

    def __str__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'


class Segment:
    def __init__(self, direction, start, length):
        self.direction = direction
        self.start = start
        self.length = length

    @property
    def end(self):
        if self.direction == Direction.RIGHT:
            return Coordinate(self.start.x + self.length, self.start.y)
        elif self.direction == Direction.LEFT:
            return Coordinate(self.start.x - self.length, self.start.y)
        elif self.direction == Direction.UP:
            return Coordinate(self.start.x, self.start.y + self.length)
        elif self.direction == Direction.DOWN:
            return Coordinate(self.start.x, self.start.y - self.length)

    def forward(self):
        if self.direction == Direction.RIGHT:
            self.start.x += 1
        elif self.direction == Direction.LEFT:
            self.start.x -= 1
        elif self.direction == Direction.UP:
            self.start.y += 1
        elif self.direction == Direction.DOWN:
            self.start.y -= 1


class Body:
    def __init__(self, initial_length):
        self.segments = [Segment(Direction.RIGHT, Coordinate(3, 0),
                                 initial_length)]

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
            if self.tail_segment.length:
                self.tail_segment.forward()
            else:
                del self.tail_segment

            self.head_segment.length += 1

    def turn(self, direction):
        if abs(direction) != abs(self.head_segment.direction):
            self.segments.append(Segment(direction, self.head_segment.start, 0))
