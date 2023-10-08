import unittest
import cncpathpreview as cpp

class TestParsers(unittest.TestCase):
    def setUp(self):
        pass

    def test_ismove_G00_returns_linearmove(self):
        line = 'G00 X100 Y100 Z25 '
        self.assertEqual(cpp.MoveType.LINEAR, cpp.is_move(line))

    def test_ismove_G0_returns_linearmove(self):
        line = 'G0 X100 Y100 Z25 '
        self.assertEqual(cpp.MoveType.LINEAR, cpp.is_move(line))

    def test_ismove_G01_returns_linearmove(self):
        line = 'G01 Z10'
        self.assertEqual(cpp.MoveType.LINEAR, cpp.is_move(line))

    def test_ismove_G1_returns_linearmove(self):
        line = 'G1 Z10'
        self.assertEqual(cpp.MoveType.LINEAR, cpp.is_move(line))

    def test_ismove_G02_returns_arcclockwise(self):
        line = 'G02 X2 Y2 R12'
        self.assertEqual(cpp.MoveType.ARC_CLOCKWISE, cpp.is_move(line))

    def test_ismove_G2_returns_arcclockwise(self):
        line = 'G2 X2 Y2 R12'
        self.assertEqual(cpp.MoveType.ARC_CLOCKWISE, cpp.is_move(line))

    def test_ismove_G03_returns_arcanticlock(self):
        line = 'G03 X2 Y2 R12'
        self.assertEqual(cpp.MoveType.ARC_ANTICLOCK, cpp.is_move(line))

    def test_ismove_G3_returns_arcanticlock(self):
        line = 'G03 X2 Y2 R12'
        self.assertEqual(cpp.MoveType.ARC_ANTICLOCK, cpp.is_move(line))

    def test_ismove_G10_returns_None(self):
        line = 'G10 L20 X100 Y0'
        self.assertEqual(cpp.MoveType.NONE, cpp.is_move(line))

    def test_iscoordinateshift_G01_returns_false(self):
        line = 'G01 L20 X100 Y0'
        self.assertEqual(False, cpp.is_coordinate_shift(line))

    def test_iscoordinateshift_G92_returns_false(self):
        line = 'G92 X100 Y0'
        self.assertEqual(True, cpp.is_coordinate_shift(line))

    def test_parsecoordinates_nonegiven_returns_fieldofnones(self):
        line = 'M05'
        self.assertEqual([None, None, None, None, None, None], cpp.parse_coordinates(line))

    def test_parsecoordinates_linearmove_returns_xyz(self):
        line = 'G00 X10 Y20 Z30'
        self.assertEqual([10, 20, 30, None, None, None], cpp.parse_coordinates(line))

    def test_parsecoordinates_arcij_returns_xyzij(self):
        line = 'G02 X10 Y20 Z30 I15 J25'
        self.assertEqual([10, 20, 30, 15, 25, None], cpp.parse_coordinates(line))

    def test_parsecoordinates_arc_returns_xyz(self):
        line = 'G03 X10 Y20 Z30 R35'
        self.assertEqual([10, 20, 30, None, None, 35], cpp.parse_coordinates(line))

    def test_fillcoordinates_nonegiven_fillsprevious(self):
        prev = [10, 20, 30]
        coor = [None, None, None]
        shift = [0, 0, 0]
        self.assertEqual(prev, cpp.fill_coordinates(coor, prev, shift))

    def test_fillcoordinates_given_notoverwritten(self):
        prev = [10, 20, 30]
        coor = [5, 15, 25]
        shift = [0, 0, 0]
        self.assertEqual(coor, cpp.fill_coordinates(coor, prev, shift))

    def test_fillcoordinates_givenandshifted_updated(self):
        prev = [10, 20, 30]
        coor = [5, 15, 25]
        shift = [10, 10, 10]
        self.assertEqual([15, 25, 35], cpp.fill_coordinates(coor, prev, shift))

class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        pass

    top = [0, 5.66, 0]
    bottom = [0, -5.66, 0]
    left = [-5.66, 0, 0]
    right = [5.66, 0, 0]


    def test_getmax_returnsmax(self):
        minlist = [10, 20, 30]
        maxlist = [15, 25, 35]
        self.assertEqual(maxlist, cpp.get_max_by_column([minlist, maxlist], 1))

    def test_getmax_returnsmaxwithinmin(self):
        minlist = [10, 20, 30]
        maxlist = [0, 0, 35]
        self.assertEqual(maxlist, cpp.get_max_by_column([minlist, maxlist], 2))

    def test_getmin_returnsmin(self):
        minlist = [10, 20, 30]
        maxlist = [15, 25, 35]
        self.assertEqual(minlist, cpp.get_min_by_column([minlist, maxlist], 1))

    def test_getmin_returnsminwithinmax(self):
        minlist = [100, 200, 30]
        maxlist = [15, 25, 35]
        self.assertEqual(minlist, cpp.get_min_by_column([minlist, maxlist], 2))

    def test_getardegrees_inputcreatescosoutofrangepositive_correctsValueTo1(self):
        coordinates = [10, 0, 0, 1, 0, 1]
        self.assertEqual(0, cpp.get_arc_degrees(coordinates))

    def test_getardegrees_inputcreatescosoutofrangenegative_correctsValueToMinus1(self):
        coordinates = [-10, 0, 0, 1, 0, 1]
        self.assertEqual(180, cpp.get_arc_degrees(coordinates))

    def test_getardegrees_inputcreatescosoutofrangepositivey_correctsValueTo1(self):
        coordinates = [0, 10, 0, 0, 1, 1]
        self.assertEqual(90, cpp.get_arc_degrees(coordinates))

    def test_getardegrees_inputcreatescosoutofrangenegativey_correctsValueToMinus1(self):
        coordinates = [0, -10, 0, 0, 1, 1]
        self.assertEqual(270, cpp.get_arc_degrees(coordinates))

    def test_getarcdegrees_inputradiusis0_returns0(self):
        coordinates = [0, 0, 0, 0, 0, 0]
        self.assertEqual(0, cpp.get_arc_degrees(coordinates))

    def test_getarcdegrees_inputspanis0_returns0(self):
        coordinates = [5.66, 0, 0, 0, 0, 5.66]
        self.assertEqual(0, round(cpp.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis45_returns45(self):
        coordinates = [4, 4, 0, 0, 0, 5.66]
        self.assertEqual(45, round(cpp.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis90_returns90(self):
        coordinates = [0, 5.66, 0, 0, 0, 5.66]
        self.assertEqual(90, round(cpp.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis135_returns135(self):
        coordinates = [-4, 4, 0, 0, 0, 5.66]
        self.assertEqual(135, round(cpp.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis180_returns180(self):
        coordinates = [-5.66, 0, 0, 0, 0, 5.66]
        self.assertEqual(180, round(cpp.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis225_returns225(self):
        coordinates = [-4, -4, 0, 0, 0, 5.66]
        self.assertEqual(225, round(cpp.get_arc_degrees(coordinates), 0))

    def test_getarcdegrees_inputspanis315_returns315(self):
        coordinates = [4, -4, 0, 0, 0, 5.66]
        self.assertEqual(315, round(cpp.get_arc_degrees(coordinates), 0))

    def test_getextremesfromarc_arccrossesno90degpole_returnstargetxyz(self):
        coordinates = [4, 4, 0, 0, 0, 5.66]
        self.assertEqual([[4, 4, 0]], cpp.get_extremes_from_arc(45, 35, coordinates))

    def test_getextremesfromarc_arccrossesone90degpole_returns90pole(self):
        coordinates = [4, 4, 0, 0, 0, 5.66]
        self.assertEqual([self.top, [4, 4, 0]], cpp.get_extremes_from_arc(135, 35, coordinates))

    def test_getextremesfromarc_arccrossesthree90degpoles_returnsthreepoles(self):
        coordinates = [4, -4, 0, 0, 0, 5.66]
        self.assertEqual([self.top, self.left, self.bottom, [4, -4, 0]],
                         cpp.get_extremes_from_arc(300, 35, coordinates))

    def test_getextremesfromarc_arccrossesall90degpoles_returnsfourpoles(self):
        coordinates = [4, 4, 0, 0, 0, 5.66]
        self.assertEqual([self.top, self.left,self.bottom, self.right, [4, 4, 0]],
                         cpp.get_extremes_from_arc(20, 21, coordinates))

    def test_getextremesfromarc_0to180_returnsthreepoles(self):
        coordinates = [-5.66, 0, 0, 0, 0, 5.66]
        self.assertEqual([self.right, self.top, self.left],
                         cpp.get_extremes_from_arc(180, 0, coordinates))

    def test_getextremesfromarc_90to270_returnsthreepoles(self):
        coordinates = [0, -5.66, 0, 0, 0, 5.66]
        self.assertEqual([self.top, self.left, self.bottom],
                         cpp.get_extremes_from_arc(270, 90, coordinates))

    def test_getextremesfromarc_180to0_returnsthreepoles(self):
        coordinates = [5.66, 0, 0, 0, 0, 5.66]
        self.assertEqual([self.left, self.bottom, self.right],
                         cpp.get_extremes_from_arc(0, 180, coordinates))

    def test_getextremesfromarc_270to90_returnsthreepoles(self):
        coordinates = [0, 5.66, 0, 0, 0, 5.66]
        self.assertEqual([self.bottom, self.right, self.top],
                         cpp.get_extremes_from_arc(90, 270, coordinates))
class TestGenerators(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_handlecoordinateshift_noinputshift_returnsoriginalshift(self):
        coordinates = 'G01 X0 Y0 Z0'
        shift = [10, 20, 30]
        self.assertEqual(shift, cpp.handle_coordinate_shift(coordinates, shift))

    def test_handlecoordinateshift_shift_returnsshift(self):
        coordinates = 'G01 X10 Y20 Z30'
        shift = [0, 0, 0]
        self.assertEqual([-10, -20, -30], cpp.handle_coordinate_shift(coordinates, shift))

    def test_handlecoordinateshift_superposition_returnsshift(self):
        coordinates = 'G01 X10 Y20 Z30'
        shift = [15, 25, 35]
        self.assertEqual([5, 5, 5], cpp.handle_coordinate_shift(coordinates, shift))

    def test_getcoordinatestring_returnscorrectoutput(self):
        axis = 'ymin'
        coordinate = ['1', '2', '3']
        expectedstring = 'MSG "PathPreview: Hit START to go to ymin: [\'1\', \'2\', \'3\']"\nM00\nG00 X1 Y2 Z3\n\n'
        self.assertEqual(expectedstring, cpp.get_command_strings(axis, coordinate))


