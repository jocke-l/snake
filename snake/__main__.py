import curses
import random

import time

from snake import Coordinate
from snake.body import Body, Direction
from snake.candy import Candy, Bonus
from snake.render import draw_body, draw_candy, draw_bonus, draw_time_left

WIDTH = 18
HEIGHT = 14


def main(stdscr):
    curses.curs_set(False)
    stdscr.nodelay(True)

    plane = curses.newwin(HEIGHT + 2, WIDTH + 2, 3, 0)

    scoreboard = curses.newwin(3, WIDTH + 2, 0, 0)
    score = 0

    body = Body(WIDTH, HEIGHT, Coordinate(3, 5), 4)

    candy = Candy(body, WIDTH, HEIGHT)
    bonus = Bonus(body, WIDTH, HEIGHT)
    bonus_interval = random.choice([7, 10])

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

        if body.head_segment.end == candy.position:
            body.grow()
            score += candy.points
            candy.make_new()

            if not bonus.is_visible:
                bonus.reset()

        if bonus.is_visible:
            if body.head_segment.end == bonus.position:
                body.grow()
                score += bonus.points
                bonus.nom()
            else:
                bonus.countdown()
        elif candy.count % bonus_interval == 0:
            bonus.show()

        plane.clear()
        plane.border()

        scoreboard.clear()
        scoreboard.border()

        draw_body(body, plane)
        draw_candy(candy, plane)
        draw_bonus(bonus, plane)
        draw_time_left(bonus, scoreboard,)

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
