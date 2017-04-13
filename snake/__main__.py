import curses

import time

from snake import render
from snake.body import Body, Coordinate


def main(stdscr):
    body = Body(Coordinate(3, 5), 4)

    plane = curses.newwin(15, 40, 3, 0)
    scoreboard = curses.newwin(3, 40, 0, 0)

    score = 0
    scoreboard.addstr(f'Score: {score}')

    while True:
        plane.clear()
        plane.border()
        scoreboard.border()
        scoreboard.addstr(1, 2, f'Score: {score}')

        render.draw_body(body, plane)
        body.forward()

        plane.refresh()
        scoreboard.refresh()
        time.sleep(0.07)


curses.wrapper(main)
