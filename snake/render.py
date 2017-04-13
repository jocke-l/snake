import curses

from snake.body import Direction

BODY_BLOCK = 'x'


def draw_body(body, scr):
    for segment in body.segments:
        for pos in range(segment.length):
            if segment.direction in (Direction.RIGHT, Direction.LEFT):
                scr.addch(segment.start.y, segment.start.x + pos,
                          ord(BODY_BLOCK))
            else:
                scr.addch(segment.start.y + pos, segment.start.x,
                          ord(BODY_BLOCK))

