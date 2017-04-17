import curses
import random

import time

from snake import render
from snake.body import Body, Coordinate, Direction

WIDTH = 18
HEIGHT = 14


def make_candy(body, width, height):
    while True:
        candy = Coordinate(random.randint(1, width - 2),
                           random.randint(1, height - 2))

        if not body.crosses_point(candy):
            return candy


def main(stdscr):
    curses.curs_set(False)
    stdscr.nodelay(True)

    body = Body(WIDTH, HEIGHT, Coordinate(3, 5), 4)

    plane = curses.newwin(HEIGHT + 2, WIDTH + 2, 3, 0)

    scoreboard = curses.newwin(3, WIDTH + 2, 0, 0)

    score = 0

    candy = make_candy(body, WIDTH, HEIGHT)

    while not body.self_collision() and not body.wall_collision():
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
            elif keypress == 27:
                break

        if body.head_segment.end == candy:
            body.grow()
            score += 50
            candy = make_candy(body, WIDTH, HEIGHT)

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
    else:
        game_over_text = 'Game over!'
        plane.addstr(0, (WIDTH - len(game_over_text) + 3) // 2,
                     game_over_text)
        plane.refresh()
        time.sleep(5)

curses.wrapper(main)
