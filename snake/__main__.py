import curses

import time

from snake import render
from snake.body import Body, Coordinate, Direction


def main(stdscr):
    curses.curs_set(False)
    stdscr.nodelay(True)

    body = Body(Coordinate(3, 5), 4)

    plane = curses.newwin(15, 40, 3, 0)
    plane.nodelay(True)

    scoreboard = curses.newwin(3, 40, 0, 0)
    scoreboard.nodelay(True)

    score = 0

    start_time = time.time()
    while True:
        keypress = stdscr.getch()

        # if time.time() - start_time >= 0.5:
        if keypress == curses.KEY_RIGHT:
            body.turn(Direction.RIGHT)
        elif keypress == curses.KEY_LEFT:
            body.turn(Direction.LEFT)
        elif keypress == curses.KEY_UP:
            body.turn(Direction.UP)
        elif keypress == curses.KEY_DOWN:
            body.turn(Direction.DOWN)

        plane.clear()
        plane.border()

        render.draw_body(body, plane)

        scoreboard.border()
        scoreboard.addstr(1, 2, f'{keypress}')

        plane.refresh()
        scoreboard.refresh()

        body.forward()

        time.sleep(0.14)

curses.wrapper(main)
