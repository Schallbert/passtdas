import unittest
import passtdas as cpp
from operator import add

def roundlistitems(inputlist):
    rounded = []
    for l in inputlist:
        sublist = []
        for i in l:
            sublist.append(round(i, 2))
        rounded.append(sublist)
    return rounded

def list_to_float(result):
    actual = []
    for element in result:
        actual.append([round(float(i), 3) for i in element])
    return actual


class TestEnd2End(unittest.TestCase):

    top = [0, 5.66]
    bottom = [0, -5.66]
    left = [-5.66, 0]
    right = [5.66, 0]

    def setUp(self) -> None:
        pass

#  ARC tests clockwise, counterclockwise, varying origin, definition per radius (r) and per offset (ij)
    def test_arcg03r_extremescorrect(self):
        with open('test/arcg03r.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_arcg02r_extremescorrect(self):
        with open('test/arcg02r.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_arcg02ij_extremescorrect(self):
        with open('test/arcg02ij.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect,list_to_float(result))

    def test_arcg03ij_extremescorrect(self):
        with open('test/arcg03ij.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect,list_to_float(result))

    def test_arcoffsetg03r_extremescorrect(self):
        with open('test/arcoffsetg03r.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-4.06, 1.31], [-9.6, 6.89], [-3.94, 12.55], [1.6, 6.97]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_arcoffsetg02r_extremescorrect(self):
        with open('test/arcoffsetg02r.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-4.06, 1.31], [-9.6, 6.89], [-3.94, 12.55], [1.6, 6.97]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_arcoffsetg03ij_extremescorrect(self):
        with open('test/arcoffsetg03ij.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-4, 1.27], [-9.66, 6.93], [-4, 12.59], [1.66, 6.93]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_arcoffsetg02ij_extremescorrect(self):
        with open('test/arcoffsetg02ij.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-4, 1.27], [-9.66, 6.93], [-4, 12.59], [1.66, 6.93]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_elipseg03r_extremescorrect(self):
        with open('test/elipseg03r.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, -320], [-200, 0], [0, 320], [200, -0.01]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg02r_extremescorrect(self):
        with open('test/elipseg02r.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, -320], [-200, -0.01 ], [-0, 320], [200, -0]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg03ij_extremescorrect(self):
        with open('test/elipseg03ij.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0.02, -320], [-200, 0.02], [-0.02, 320], [200, -0.02]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg02ij_extremescorrect(self):
        with open('test/elipseg02ij.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0.02, -320], [-200, 0.02], [-0.02, 320], [200, -0.02]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_rectangle_extremescorrect(self):
        with open('test/rectangle.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, 0], [0, 0], [50, 50], [50, 0]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_irregularshapeij_extremescorrect(self):
        with open('test/irregularshapeij.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[30.59, -50], [-50, -50], [-40, 50], [50, -45]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_irregularshaper_extremescorrect(self):
        with open('test/irregularshaper.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[45, -50], [-50, -50], [-40, 50], [50, -45]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_hugefilecoordinateshiftij_extremescorrect(self):
        with open('test/hugefilecoordinateshift.tap', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-79.1, -10.802], [-280.833, 533.76], [-109.93, 631.066], [10.802, 145.35]]
            result = cpp.get_extremes_text(targets, data)
            self.assertEqual(expect, list_to_float(result))

    def test_incompatiblefile_handlegracefully(self):
        with open('test/misformulatedfile.txt', 'r', errors='replace') as f:
            data = cpp.create_dataset_from_input(f)
            self.assertEqual([], data)