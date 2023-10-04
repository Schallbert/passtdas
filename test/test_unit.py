import unittest
import cncpathpreview as cnc

class TestIsMove(unittest.TestCase):
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




