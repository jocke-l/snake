import unittest

from snake.body import Body, Direction, Coordinate


class TestBody(unittest.TestCase):
    def setUp(self):
        self.body = Body(4)

    def test_initial(self):
        self.assertEqual(len(self.body.segments), 1)

    def test_initial_forward(self):
        self.body.forward()

        self.assertEqual(self.body.head_segment.start.x, 4)
        self.assertEqual(self.body.length, 4)

    def test_forward_and_turn(self):
        self.body.turn(Direction.DOWN)

        self.assertEqual(len(self.body.segments), 2)
        self.body.forward()

        self.assertEqual(len(self.body.segments), 2)
        self.assertEqual(self.body.tail_segment.start, Coordinate(4, 0))
        self.assertEqual(self.body.head_segment.end, Coordinate(7, -1))
        self.assertEqual(self.body.head_segment.length, 1)

        self.body.turn(Direction.LEFT)
        self.body.forward()

        self.assertEqual(len(self.body.segments), 3)
        self.assertEqual(self.body.tail_segment.start, Coordinate(5, 0))
        self.assertEqual(self.body.head_segment.end, Coordinate(6, -1))
        self.assertEqual(self.body.head_segment.length, 1)
        self.assertEqual(self.body.segments[-2].length, 1)

        self.body.forward()
        self.body.forward()

        self.assertEqual(len(self.body.segments), 2)
        self.assertEqual(self.body.tail_segment.start, Coordinate(6, -1))
        self.assertEqual(self.body.head_segment.end, Coordinate(5, -1))
        self.assertEqual(self.body.head_segment.length, 3)






