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

    def test_handlearcmover_passesonequadrant_returnscorrectresults(self):
        coordinates = [-4, 4, 0, None, None, 5.66]
        previous_coordinates = [5.66, 0, 0]
        expected = [[0, 5.66, 0], [-4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_passesonequadrant_returnscorrectresults(self):
        coordinates = [-4, 4, 0, -5.66, 0, None]
        previous_coordinates = [5.66, 0, 0]
        expected = [[0, 5.66, 0], [-4, 4, 0]]
        actua = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actua))