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

    def test_handlearcmover_anticlockpassesnoquadrant_returnscorrectresults(self):
        previous_coordinates = self.right  # 0°
        coordinates = [4, 4, 0, None, None, 5.66]  # 45°
        expected = [[4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpassesonequadrant_returnscorrectresults(self):
        previous_coordinates = self.right  # 0°
        coordinates = [-4, 4, 0, None, None, 5.66]  # 135°
        expected = [self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpassesthreequadrants_returnscorrectresults(self):
        previous_coordinates = [-4, -4, 0]  # 225°
        coordinates = [-4, 4, 0, None, None, 5.66]  # 135°
        expected = [self.bottom, self.right, self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpassesallquadrants_returnscorrectresults(self):
        previous_coordinates = [-4, -4, 0]  # 225°
        coordinates = [-5.66, 0, 0, None, None, 5.66]  # 180°
        expected = [self.bottom, self.right, self.top, self.left]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesnoquadrant_returnscorrectresults(self):
        previous_coordinates = [4, 4, 0]  # 45°
        coordinates = [5.66, 0, 0, None, None, 5.66]  # 0°
        expected = [[5.66, 0, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesonequadrant_returnscorrectresults(self):
        previous_coordinates = [-4, 4, 0]  # 135°
        coordinates = [5.66, 0, 0, None, None, 5.66]  # 0°
        expected = [self.top, [5.66, 0, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesthreequadrants_returnscorrectresults(self):
        previous_coordinates = [-4, 4, 0]  # 135°
        coordinates = [-4, -4, 0, None, None, 5.66]  # 225°
        expected = [self.bottom, self.right, self.top, [-4, -4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesallquadrants_returnscorrectresults(self):
        previous_coordinates = [-5.66, 0, 0]  # 180°
        coordinates = [-4, -4, 0, None, None, 5.66]  # 225°
        expected = [self.bottom, self.right, self.top, [-4, -4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_passesonequadrant_returnscorrectresults(self):
        previous_coordinates = [5.66, 0, 0]  # 0°
        coordinates = [-4, 4, 0, -5.66, 0, None]  # 135°
        expected = [self.top, [-4, 4, 0]]
        actua = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actua))
