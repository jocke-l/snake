import random

import time

from snake import Coordinate
from snake.body import Body


class Candy:
    position: Coordinate = None
    count: int = 0
    points: int = 50

    def __init__(self, body: Body, plane_width: int, plane_height: int):
        self.plane_width = plane_width
        self.plane_height = plane_height
        self._body = body

        self.make_new()

    def make_new(self, increase_count=True) -> None:
        while True:
            position = Coordinate(
                random.randint(1, self.plane_width - 1),
                random.randint(1, self.plane_height - 1)
            )

            if not self._body.crosses_point(position):
                break

        self.position = position
        if increase_count:
            self.count += 1


class Bonus(Candy):
    time_left = 10
    start_time = None
    eaten = False

    @property
    def is_visible(self) -> bool:
        return not self.eaten and self.time_left > 0 and self.start_time

    @property
    def points(self) -> int:
        return 70 + 5 * self.count

    def reset(self) -> None:
        self.time_left = 10
        self.start_time = None
        self.eaten = False

    def show(self) -> None:
        if not self.is_visible and not self.eaten:
            self.make_new(increase_count=False)
            self.start_time = time.time()

    def nom(self) -> None:
        self.make_new()
        self.eaten = True

    def countdown(self) -> None:
        self.time_left -= int(time.time() - self.start_time) / 2
