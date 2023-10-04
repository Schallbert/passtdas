import unittest
import cncpathpreview as cnc

class TestParsers(unittest.TestCase):
    def setUp(self):
        pass

    def test_ismove_G00_returns_linearmove(self):
        line = 'G00 X100 Y100 Z25 '
        self.assertEqual(cnc.MoveType.LINEAR, cnc.is_move(line))

    def test_ismove_G0_returns_linearmove(self):
        line = 'G0 X100 Y100 Z25 '
        self.assertEqual(cnc.MoveType.LINEAR, cnc.is_move(line))

    def test_ismove_G01_returns_linearmove(self):
        line = 'G01 Z10'
        self.assertEqual(cnc.MoveType.LINEAR, cnc.is_move(line))

    def test_ismove_G1_returns_linearmove(self):
        line = 'G1 Z10'
        self.assertEqual(cnc.MoveType.LINEAR, cnc.is_move(line))

    def test_ismove_G02_returns_arcclockwise(self):
        line = 'G02 X2 Y2 R12'
        self.assertEqual(cnc.MoveType.ARC_CLOCKWISE, cnc.is_move(line))

    def test_ismove_G2_returns_arcclockwise(self):
        line = 'G2 X2 Y2 R12'
        self.assertEqual(cnc.MoveType.ARC_CLOCKWISE, cnc.is_move(line))

    def test_ismove_G03_returns_arcanticlock(self):
        line = 'G03 X2 Y2 R12'
        self.assertEqual(cnc.MoveType.ARC_ANTICLOCK, cnc.is_move(line))

    def test_ismove_G3_returns_arcanticlock(self):
        line = 'G03 X2 Y2 R12'
        self.assertEqual(cnc.MoveType.ARC_ANTICLOCK, cnc.is_move(line))

    def test_ismove_G10_returns_None(self):
        line = 'G10 L20 X100 Y0'
        self.assertEqual(cnc.MoveType.NONE, cnc.is_move(line))

    def test_iscoordinateshift_G01_returns_false(self):
        line = 'G01 L20 X100 Y0'
        self.assertEqual(False, cnc.is_coordinate_shift(line))

    def test_iscoordinateshift_G92_returns_false(self):
        line = 'G92 X100 Y0'
        self.assertEqual(True, cnc.is_coordinate_shift(line))

    def test_parsecoordinates_nonegiven_returns_fieldofnones(self):
        line = 'M05'
        self.assertEqual([None, None, None, None, None, None], cnc.parse_coordinates(line))

    def test_parsecoordinates_linearmove_returns_xyz(self):
        line = 'G00 X10 Y20 Z30'
        self.assertEqual([10, 20, 30, None, None, None], cnc.parse_coordinates(line))

    def test_parsecoordinates_arcij_returns_xyzij(self):
        line = 'G02 X10 Y20 Z30 I15 J25'
        self.assertEqual([10, 20, 30, 15, 25, None], cnc.parse_coordinates(line))

    def test_parsecoordinates_arc_returns_xyz(self):
        line = 'G03 X10 Y20 Z30 R35'
        self.assertEqual([10, 20, 30, None, None, 35], cnc.parse_coordinates(line))

    def test_fillcoordinates_nonegiven_fillsprevious(self):
        prev = [10, 20, 30]
        coor = [None, None, None]
        shift = [0, 0, 0]
        self.assertEqual(prev, cnc.fill_coordinates(coor, prev, shift))

    def test_fillcoordinates_given_notoverwritten(self):
        prev = [10, 20, 30]
        coor = [5, 15, 25]
        shift = [0, 0, 0]
        self.assertEqual(coor, cnc.fill_coordinates(coor, prev, shift))

    def test_fillcoordinates_givenandshifted_updated(self):
        prev = [10, 20, 30]
        coor = [5, 15, 25]
        shift = [10, 10, 10]
        self.assertEqual([15, 25, 35], cnc.fill_coordinates(coor, prev, shift))

class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        pass

    def test_getmax_returnsmax(self):
        minlist = [10, 20, 30]
        maxlist = [15, 25, 35]
        self.assertEqual(maxlist, cnc.get_max_by_column([minlist, maxlist], 1))

    def test_getmax_returnsmaxwithinmin(self):
        minlist = [10, 20, 30]
        maxlist = [0, 0, 35]
        self.assertEqual(maxlist, cnc.get_max_by_column([minlist, maxlist], 2))

    def test_getmin_returnsmin(self):
        minlist = [10, 20, 30]
        maxlist = [15, 25, 35]
        self.assertEqual(minlist, cnc.get_min_by_column([minlist, maxlist], 1))

    def test_getmin_returnsminwithinmax(self):
        minlist = [100, 200, 30]
        maxlist = [15, 25, 35]
        self.assertEqual(minlist, cnc.get_min_by_column([minlist, maxlist], 2))

    def test_getarcdegrees_inputradiusis0_returns0(self):
        coordinates = [0, 0, 0, 0, 0, 0]
        self.assertEqual(0, cnc.get_arc_degrees(coordinates))

    def test_getardegrees_inputcreatescosoutofrange_raisesvalueerror(self):
        coordinates = [10, 0, 0, 1, 0, 1]
        with self.assertRaises(ValueError): (
            cnc.get_arc_degrees(coordinates))

    def test_getarcdegrees_inputspanis0_returns0(self):
        coordinates = [5.66, 0, 0, 0, 0, 5.66]
        self.assertEqual(0, round(cnc.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis45_returns45(self):
        coordinates = [4, 4, 0, 0, 0, 5.66]
        self.assertEqual(45, round(cnc.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis135_returns135(self):
        coordinates = [-4, 4, 0, 0, 0, 5.66]
        self.assertEqual(135, round(cnc.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis90_returns90(self):
        coordinates = [0, 5.66, 0, 0, 0, 5.66]
        self.assertEqual(90, round(cnc.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis225_returns225(self):
        coordinates = [-4, -4, 0, 0, 0, 5.66]
        self.assertEqual(225, round(cnc.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis315_returns315(self):
        coordinates = [4, -4, 0, 0, 0, 5.66]
        self.assertEqual(315, round(cnc.get_arc_degrees(coordinates), 0))

    def test_getextremesfromarc_arccrossesno90degpole_returnstargetxyz(self):
        coordinates = [4, 4, 0, 0, 0, 5.66]
        self.assertEqual([[4, 4, 0]], cnc.get_extremes_from_arc(45, 35, coordinates))

    def test_getextremesfromarc_arccrossesone90degpole_returns90pole(self):
        coordinates = [4, 4, 0, 0, 0, 5.66]
        self.assertEqual([[0, 5.66, 0], [4, 4, 0]], cnc.get_extremes_from_arc(135, 35, coordinates))

    def test_getextremesfromarc_arccrossesthree90degpoles_returnsthreepoles(self):
        coordinates = [4, -4, 0, 0, 0, 5.66]
        self.assertEqual([[0, 5.66, 0], [-5.66, 0, 0], [0, -5.66, 0], [4, -4, 0]],
                         cnc.get_extremes_from_arc(300, 35, coordinates))


