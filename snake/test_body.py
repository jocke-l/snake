import unittest

from snake.body import Body, Direction, Coordinate


class TestBody(unittest.TestCase):
    def setUp(self):
        self.body = Body(Coordinate(3, 5), 4)

    def test_initial(self):
        #    y
        #    7
        #    6
        #    5     x x x o
        #    4
        #    3
        #    2
        #    1
        #  x   1 2 3 4 5 6 7

        self.assertEqual(len(self.body.segments), 1)
        self.assertEqual(self.body.length, 4)
        self.assertEqual(self.body.head_segment.start, Coordinate(3, 5))
        self.assertEqual(self.body.head_segment.end, Coordinate(6, 5))

    def test_initial_forward(self):
        self.body.forward()

        #    y
        #    7
        #    6
        #    5       x x x o
        #    4
        #    3
        #    2
        #    1
        #  x   1 2 3 4 5 6 7 8
        self.assertEqual(self.body.length, 4)
        self.assertEqual(len(self.body.segments), 1)
        self.assertEqual(self.body.head_segment.start, Coordinate(4, 5))
        self.assertEqual(self.body.head_segment.end, Coordinate(7, 5))
        self.assertEqual(self.body.head_segment.length, 4)

    def test_forward_and_turn(self):
        self.body.turn(Direction.DOWN)
        self.body.forward()

        #    y
        #    7
        #    6
        #    5       x x x
        #    4           o
        #    3
        #    2
        #    1
        #  x   1 2 3 4 5 6 7 8
        self.assertEqual(self.body.length, 4)
        self.assertEqual(len(self.body.segments), 2)
        self.assertEqual(self.body.tail_segment.start, Coordinate(4, 5))
        self.assertEqual(self.body.tail_segment.end, Coordinate(6, 5))
        self.assertEqual(self.body.tail_segment.length, 3)
        self.assertEqual(self.body.head_segment.start, Coordinate(6, 4))
        self.assertEqual(self.body.head_segment.end, Coordinate(6, 4))
        self.assertEqual(self.body.head_segment.length, 1)

        self.body.turn(Direction.LEFT)
        self.body.forward()

        #    y
        #    7
        #    6
        #    5         x x
        #    4         o x
        #    3
        #    2
        #    1
        #  x   1 2 3 4 5 6 7 8
        self.assertEqual(self.body.length, 4)
        self.assertEqual(len(self.body.segments), 3)
        self.assertEqual(self.body.tail_segment.start, Coordinate(5, 5))
        self.assertEqual(self.body.tail_segment.end, Coordinate(6, 5))
        self.assertEqual(self.body.tail_segment.length, 2)
        self.assertEqual(self.body.segments[1].start, Coordinate(6, 4))
        self.assertEqual(self.body.segments[1].end, Coordinate(6, 4))
        self.assertEqual(self.body.segments[1].length, 1)
        self.assertEqual(self.body.head_segment.start, Coordinate(5, 4))
        self.assertEqual(self.body.head_segment.end, Coordinate(5, 4))
        self.assertEqual(self.body.head_segment.length, 1)

        self.body.forward()
        self.body.forward()

        #    y
        #    7
        #    6
        #    5
        #    4     o x x x
        #    3
        #    2
        #    1
        #  x   1 2 3 4 5 6 7 8
        self.assertEqual(self.body.length, 4)
        self.assertEqual(len(self.body.segments), 1)
        self.assertEqual(self.body.head_segment.start, Coordinate(6, 4))
        self.assertEqual(self.body.head_segment.end, Coordinate(3, 4))
        self.assertEqual(self.body.head_segment.length, 4)

    def test_self_collision(self):
        body = Body(Coordinate(3, 5), 5)
        self.assertFalse(body.self_collision())

        body.turn(Direction.DOWN)
        self.assertFalse(body.self_collision())
        body.forward()
        self.assertFalse(body.self_collision())

        body.turn(Direction.LEFT)
        self.assertFalse(body.self_collision())
        body.forward()
        self.assertFalse(body.self_collision())

        #    y
        #    7
        #    6
        #    5         x x x
        #    4           o x
        #    3
        #    2
        #    1
        #  x   1 2 3 4 5 6 7 8
        body.turn(Direction.UP)
        self.assertTrue(body.self_collision())
