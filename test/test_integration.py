import unittest
import cncpathpreview as cpp


def roundlistitems(inputlist):
    rounded = []
    for l in inputlist:
        sublist = []
        for i in l:
            sublist.append(round(i, 2))
        rounded.append(sublist)
    return rounded


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        pass

    top = [0, 5.66, 0]
    bottom = [0, -5.66, 0]
    left = [-5.66, 0, 0]
    right = [5.66, 0, 0]

    def test_handlearcmover_passesonequadrant_returnscorrectresults(self):
        coordinates = [-4, 4, 0, None, None, 5.66]
        previous_coordinates = self.right
        expected = [self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_passesthreequadrantreverse_returnscorrectresults(self):
        coordinates = [-4, 4, 0, None, None, 5.66]
        previous_coordinates = [-4, -4, 0]
        expected = [self.bottom, self.right, self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_passesfourquadrants_returnscorrectresults(self):
        coordinates = [4, 4, 0, None, None, 5.66]
        previous_coordinates = [0.1, 5.65, 0]
        expected = [self.right, self.bottom, self.left, self.top, [4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_passesonequadrant_returnscorrectresults(self):
        coordinates = [-4, 4, 0, -5.66, 0, None]
        previous_coordinates = [5.66, 0, 0]
        expected = [self.top, [-4, 4, 0]]
        actua = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actua))

