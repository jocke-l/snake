import curses
import random

import time

from snake import render
from snake.body import Body, Coordinate, Direction

WIDTH = 40
HEIGHT = 15


def make_candy(width, height):
    return Coordinate(random.randint(1, width - 2,),
                      random.randint(1, height - 2))


def main(stdscr):
    curses.curs_set(False)
    stdscr.nodelay(True)

    body = Body(Coordinate(3, 5), 4)

    plane = curses.newwin(HEIGHT, WIDTH, 3, 0)
    plane.nodelay(True)

    scoreboard = curses.newwin(3, 40, 0, 0)
    scoreboard.nodelay(True)

    score = 0

    candy = make_candy(WIDTH, HEIGHT)

    while not body.self_collision():
        keypress = stdscr.getch()

        if not body.locked:
            if keypress == curses.KEY_RIGHT:
                body.turn(Direction.RIGHT)
            elif keypress == curses.KEY_LEFT:
                body.turn(Direction.LEFT)
            elif keypress == curses.KEY_UP:
                body.turn(Direction.DOWN)
            elif keypress == curses.KEY_DOWN:
                body.turn(Direction.UP)

        if body.head_segment.end == candy:
            body.grow()
            score += 50
            candy = make_candy(WIDTH, HEIGHT)

        plane.clear()
        plane.border()

        render.draw_body(body, plane)
        render.draw_candy(candy, plane)

        scoreboard.border()
        scoreboard.addstr(1, 2, f'Score: {score}')

        plane.refresh()
        scoreboard.refresh()

        body.forward()

        time.sleep(0.14)

curses.wrapper(main)
