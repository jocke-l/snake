from snake.body import Direction

BODY_BLOCK = 'x'
CANDY = 'o'
FIRST_BONUS_CANDY = 'A'


def draw_candy(candy, scr):
    scr.addch(candy.position.y, candy.position.x, ord(CANDY))


def draw_bonus(bonus, scr):
    if bonus.is_visible:
        scr.addch(bonus.position.y, bonus.position.x,
                  ord(FIRST_BONUS_CANDY) + bonus.count - 1)


def draw_time_left(bonus, scr):
    if bonus.is_visible:
        bonus_text = (f'{chr(ord(FIRST_BONUS_CANDY) + bonus.count - 1)}: '
                      f'{bonus.time_left}')
        scr.addstr(1, bonus.plane_width - len(bonus_text), bonus_text)


def draw_body(body, scr):
    for segment in body.segments:
        for pos in range(segment.length):
            if segment.direction == Direction.RIGHT:
                scr.addch(segment.start.y, segment.start.x + pos,
                          ord(BODY_BLOCK))
            elif segment.direction == Direction.LEFT:
                scr.addch(segment.start.y, segment.start.x - pos,
                          ord(BODY_BLOCK))
            elif segment.direction == Direction.UP:
                scr.addch(segment.start.y + pos, segment.start.x,
                          ord(BODY_BLOCK))
            elif segment.direction == Direction.DOWN:
                scr.addch(segment.start.y - pos, segment.start.x,
                          ord(BODY_BLOCK))
