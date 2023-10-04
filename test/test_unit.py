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


