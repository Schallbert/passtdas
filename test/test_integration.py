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

    def test_handlearcmover_anticlockpassesnoquadrant_ok(self):
        previous_coordinates = self.right  # 0°
        coordinates = [4, 4, 0, None, None, 5.66]  # 45°
        expected = [self.right, [4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpassesonequadrant_ok(self):
        previous_coordinates = self.right  # 0°
        coordinates = [-4, 4, 0, None, None, 5.66]  # 135°
        expected = [self.right, self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpassesthreequadrants_ok(self):
        previous_coordinates = [-4, -4, 0]  # 225°
        coordinates = [-4, 4, 0, None, None, 5.66]  # 135°
        expected = [self.bottom, self.right, self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpassesallquadrants_ok(self):
        previous_coordinates = [-4, -4, 0]  # 225°
        coordinates = [-5.66, 0, 0, None, None, 5.66]  # 180°
        expected = [self.bottom, self.right, self.top, self.left]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpasses90deg_ok(self):
        previous_coordinates = [9.814, 319.614, 0]  # 95°
        coordinates = [-9.814, 319.614, 0, None, None, 125.003]  # 85°
        expected = [[0, 320, 0], [-9.81, 319.61, 0,]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockoffsetpassesnoquadrant_upper_ok(self):
        previous_coordinates = [-9.814, 319.614, 0]  # 85°
        coordinates = [-19.603, 318.459, 0, None, None, 126.880]  # 80°
        expected = [[-19.6, 318.46, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockpasses270deg_ok(self):
        previous_coordinates = [-9.814, -319.614, 0]  # 265°
        coordinates = [9.814, -319.614, 0, None, None, 125.003]  # 275°
        expected = [[0, -320, 0], [9.81, -319.61, 0,]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepasses270deg_ok(self):
        previous_coordinates = [9.814, -319.614, 0]  # 275°
        coordinates = [-9.814, -319.614, 0, None, None, 125.003]  # 265°
        expected = [[0, -320, 0], [-9.81, -319.61, 0,]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockoffsetpassesnoquadrant_lower_ok(self):
        previous_coordinates = [9.814, -319.614, 0]  # 275°
        coordinates = [19.603, -318.459, 0, None, None, 126.880]  # 280°
        expected = [[19.6, -318.46, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockxarc180start180_ok(self):
        previous_coordinates = [-5.66, 0, 0,]  # 180°
        coordinates = [5.66, 0, 0, None, None, 5.66]  # 0°
        expected = [self.left, self.bottom, self.right]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockyarc180start270_ok(self):
        previous_coordinates = [0, -5.66, 0,]  # 270°
        coordinates = [0, 5.66, 0, None, None, 5.66]  # 90°
        expected = [self.bottom, self.right, self.top]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockxarc180start0_ok(self):
        previous_coordinates = [5.66, 0, 0,]  # 0°
        coordinates = [-5.66, 0, 0, None, None, 5.66]  # 180°
        expected = [self.right, self.top, self.left]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_anticlockyarc180start90_ok(self):
        previous_coordinates = [0, 5.66, 0,]  # 90°
        coordinates = [0, -5.66, 0, None, None, 5.66]  # 270°
        expected = [self.top, self.left, self.bottom]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesnoquadrant_ok(self):
        previous_coordinates = [4, 4, 0]  # 45°
        coordinates = [5.66, 0, 0, None, None, 5.66]  # 0°
        expected = [self.right]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesonequadrant_ok(self):
        previous_coordinates = [-4, 4, 0]  # 135°
        coordinates = [5.66, 0, 0, None, None, 5.66]  # 0°
        expected = [self.right, self.top]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesthreequadrants_ok(self):
        previous_coordinates = [-4, 4, 0]  # 135°
        coordinates = [-4, -4, 0, None, None, 5.66]  # 225°
        expected = [self.bottom, self.right, self.top, [-4, -4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepasses270degquadrant_ok(self):
        previous_coordinates = [4, -4, 0]  # 315°
        coordinates = [-4, -4, 0, None, None, 5.66]  # 225°
        expected = [self.bottom, [-4, -4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisepassesallquadrants_ok(self):
        previous_coordinates = [-5.66, 0, 0]  # 180°
        coordinates = [-4, -4, 0, None, None, 5.66]  # 225°
        expected = [self.bottom, self.right, self.top, self.left, [-4, -4, 0]]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisexarc180_start0_ok(self):
        previous_coordinates = [5.66, 0, 0]  # 0°
        coordinates = [-5.66, 0, 0, None, None, 5.66]  # 180°
        expected = [self.left, self.bottom, self.right]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwiseyarc180_start90_ok(self):
        previous_coordinates = [0, 5.66, 0]  # 90°
        coordinates = [0, -5.66, 0, None, None, 5.66]  # 270°
        expected = [self.bottom, self.right, self.top]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwisexarc180_start180_ok(self):
        previous_coordinates = [-5.66, 0, 0]  # 180°
        coordinates = [5.66, 0, 0, None, None, 5.66]  # 0°
        expected = [self.right, self.top, self.left]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmover_clockwiseyarc180_start270_ok(self):
        previous_coordinates = [0, -5.66, 0]  # 270°
        coordinates = [0, 5.66, 0, None, None, 5.66]  # 90°
        expected = [self.top, self.left, self.bottom]
        actual = cpp.handle_arc_move_r(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockpassesnoquadrant_ok(self):
        previous_coordinates = self.right  # 0°
        coordinates = [4, 4, 0, -5.66, 0, None]  # 45°
        expected = [self.right, [4, 4, 0]]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockpassesonequadrant_ok(self):
        previous_coordinates = self.right  # 0°
        coordinates = [-4, 4, 0, -5.66, 0, None]  # 135°
        expected = [self.right, self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockpassesthreequadrants_ok(self):
        previous_coordinates = [-4, -4, 0]  # 225°
        coordinates = [-4, 4, 0, 4, 4, None ]  # 135°
        expected = [self.bottom, self.right, self.top, [-4, 4, 0]]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockpassesallquadrants_ok(self):
        previous_coordinates = [-4, -4, 0]  # 225°
        coordinates = [-5.66, 0, 0, 4, 4, None]  # 180°
        expected = [self.bottom, self.right, self.top, self.left]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockxarc180start180_ok(self):
        previous_coordinates = [-5.66, 0, 0]  # 180°
        coordinates = [5.66, 0, 0, 5.66, 0, None]  # 0°
        expected = [self.left, self.bottom, self.right]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockyarc180start270_ok(self):
        previous_coordinates = [0, -5.66, 0]  # 270°
        coordinates = [0, 5.66, 0, 0, 5.66, None]  # 90°
        expected = [self.bottom, self.right, self.top]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockxarc180start0_ok(self):
        previous_coordinates = [5.66, 0, 0]  # 0°
        coordinates = [-5.66, 0, 0, -5.66, 0, None]  # 180°
        expected = [self.right, self.top, self.left]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_anticlockyarc180start90_ok(self):
        previous_coordinates = [0, 5.66, 0]
        coordinates = [0, -5.66, 0, 0, -5.66, None]  # 270°
        expected = [self.top, self.left, self.bottom]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_ANTICLOCK)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_clockwisepassesnoquadrant_ok(self):
        previous_coordinates = [4, 4, 0]  # 45°
        coordinates = [5.66, 0, 0, -4, -4, None]  # 0°
        expected = [self.right]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_clockwisepassesonequadrant_ok(self):
        previous_coordinates = [-4, 4, 0]  # 135°
        coordinates = [5.66, 0, 0, 4, -4, None]  # 0°
        expected = [self.right, self.top]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_clockwisepassesthreequadrants_ok(self):
        previous_coordinates = [-4, 4, 0]  # 135°
        coordinates = [-4, -4, 0, 4, -4, None]  # 225°
        expected = [self.bottom, self.right, self.top, [-4, -4, 0]]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoverij_clockwisepassesallquadrants_ok(self):
        previous_coordinates = [-5.66, 0, 0]  # 180°
        coordinates = [-4, -4, 0, 5.66, 0, None]  # 225°
        expected = [self.bottom, self.right, self.top, self.left, [-4, -4, 0]]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_clockwisexarc180_start0_ok(self):
        previous_coordinates = [5.66, 0, 0]  # 0°
        coordinates = [-5.66, 0, 0, -5.66, 0, None]  # 180°
        expected = [self.left, self.bottom, self.right]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_clockwiseyarc180_start90_ok(self):
        previous_coordinates = [0, 5.66, 0]  # 90°
        coordinates = [0, -5.66, 0, 0, -5.66, None]  # 270°
        expected = [self.bottom, self.right, self.top]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_clockwisexarc180_start180_ok(self):
        previous_coordinates = [-5.66, 0, 0]  # 180°
        coordinates = [5.66, 0, 0, 5.66, 0, None]  # 0°
        expected = [self.right, self.top, self.left]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))

    def test_handlearcmoveij_clockwiseyarc180_start270_ok(self):
        previous_coordinates = [0, -5.66, 0]  # 270°
        coordinates = [0, 5.66, 0, 0, 5.66, None]  # 90°
        expected = [self.top, self.left, self.bottom]
        actual = cpp.handle_arc_move_ij(coordinates, previous_coordinates, cpp.MoveType.ARC_CLOCKWISE)
        self.assertEqual(expected, roundlistitems(actual))


