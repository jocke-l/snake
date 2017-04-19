import enum
from typing import List, Optional

from snake import Coordinate


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

    def __repr__(self) -> str:
        return f'<{self}>'

    def __str__(self) -> str:
        return (f'{type(self).__name__}({self.direction}, {self.start}, '
                f'{self.length})')

    @property
    def end(self) -> Coordinate:
        return self.forward_position(self.length - 1)

    def forward_position(self, steps: int = 1) -> Coordinate:
        self.direction.value: Coordinate
        return self.start + self.direction.value * steps

    def forward(self) -> None:
        self.start = self.forward_position()

    def crosses_point(self, point: Coordinate) -> bool:
        s, e = self.start, self.end

        return (max(s.x, e.x) >= point.x >= min(s.x, e.x) and
                max(s.y, e.y) >= point.y >= min(s.y, e.y))


class Body:
    def __init__(self, plane_width, plane_height, head_segment_start,
                 head_segment_length):
        self.plane_width = plane_width
        self.plane_height = plane_height
        self.segments = [Segment(Direction.RIGHT, head_segment_start,
                                 head_segment_length)]

    @property
    def length(self) -> int:
        return sum(segment.length for segment in self.segments)

    @property
    def head_segment(self) -> Segment:
        return self.segments[-1]

    @property
    def tail_segments(self) -> List[Segment]:
        return self.segments[:-2]

    @property
    def tail_segment(self) -> Segment:
        return self.segments[0]

    @tail_segment.deleter
    def tail_segment(self) -> None:
        del self.segments[0]

    def crosses_point(self, point: Coordinate,
                      segments: Optional[List[Segment]] = None) -> bool:
        segments: List[Segment] = \
            segments if segments is not None else self.segments
        for segment in segments:
            if segment.crosses_point(point):
                return True

        return False

    def self_collision(self) -> bool:
        return self.crosses_point(self.head_segment.end,
                                  segments=self.tail_segments)

    def wall_collision(self) -> bool:
        return (self.head_segment.end.x in (0, self.plane_width + 1) or
                self.head_segment.end.y in (0, self.plane_height + 1))

    def forward(self) -> None:
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

    def grow(self) -> None:
        self.tail_segment.length += 1
        self.tail_segment.start = self.tail_segment.forward_position(-1)

    def turn(self, direction) -> None:
        if abs(direction) != abs(self.head_segment.direction):
            self.segments.append(Segment(direction, self.head_segment.end, 0,
                                         initial_forward=True))
