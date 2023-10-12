import unittest
import cncpathpreview as cpp
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

    top = [0, 5.66, 10]
    bottom = [0, -5.66, 10]
    left = [-5.66, 0, 10]
    right = [5.66, 0, 10]

    offset = [-3.95, 6.9, 0]

    def setUp(self) -> None:
        pass

#  ARC tests clockwise, counterclockwise, varying origin, definition per radius (r) and per offset (ij)
    def test_arcg03r_extremescorrect(self):
        with open('arcg03r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_arcg02r_extremescorrect(self):
        with open('arcg02r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_arcg02ij_extremescorrect(self):
        with open('arcg02ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect,list_to_float(result))

    def test_arcg03ij_extremescorrect(self):
        with open('arcg03ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect,list_to_float(result))

    def test_arcoffsetg03r_extremescorrect(self):
        with open('arcoffsetg03r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = roundlistitems([list(map(add, self.offset, self.bottom)), list(map(add, self.offset, self.left)),
                      list(map(add, self.offset, self.top)), list(map(add, self.offset, self.right))])
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_arcoffsetg02r_extremescorrect(self):
        with open('arcoffsetg02r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = roundlistitems([list(map(add, self.offset, self.bottom)), list(map(add, self.offset, self.left)),
                      list(map(add, self.offset, self.top)), list(map(add, self.offset, self.right))])
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_arcoffsetg03ij_extremescorrect(self):
        with open('arcoffsetg03ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-4, 1.27, 10], [-9.66, 6.93, 10], [-4, 12.59, 10], [1.66, 6.93, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_arcoffsetg02ij_extremescorrect(self):
        with open('arcoffsetg02ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-4, 1.27, 10], [-9.66, 6.93, 10], [-4, 12.59, 10], [1.66, 6.93, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_elipseg03r_extremescorrect(self):
        with open('elipseg03r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, -320, 10], [-200, 0, 10], [0, 320, 10], [200, -0.01, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg02r_extremescorrect(self):
        with open('elipseg02r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, -320, 10], [-200, -0.01 , 10], [-0, 320, 10], [200, -0, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg03ij_extremescorrect(self):
        with open('elipseg03ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0.02, -320, 10], [-200, 0.02, 10], [-0.02, 320, 10], [200, -0.02, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg02ij_extremescorrect(self):
        with open('elipseg02ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0.02, -320, 10], [-200, 0.02, 10], [-0.02, 320, 10], [200, -0.02, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_rectangle_extremescorrect(self):
        with open('rectangle.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, 0, 10], [0, 0, 10], [50, 50, 10], [50, 0, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_elipseg03r_extremescorrect(self):
        with open('elipseg03r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, -320, 10], [-200, 0, 10], [0, 320, 10], [200, -0.01, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg02r_extremescorrect(self):
        with open('elipseg02r.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, -320, 10], [-200, -0.01 , 10], [-0, 320, 10], [200, -0, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg03ij_extremescorrect(self):
        with open('elipseg03ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0.02, -320, 10], [-200, 0.02, 10], [-0.02, 320, 10], [200, -0.02, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_elipseg02ij_extremescorrect(self):
        with open('elipseg02ij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0.02, -320, 10], [-200, 0.02, 10], [-0.02, 320, 10], [200, -0.02, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, roundlistitems(list_to_float(result)))

    def test_irregularshapeij_extremescorrect(self):
        with open('irregularshapeij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[30.59, -50, 10], [-50, -50, 10], [-40, 50, 10], [50, -45, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_irregularshaper_extremescorrect(self):
        with open('irregularshaper.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[30.59, -50, 10], [-50, -50, 10], [-40, 50, 10], [50, -45, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    @unittest.skip
    def test_hugefilecoordinateshiftij_extremescorrect(self):
        with open('hugefilecoordinateshift.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-79.1, -10.802, 10], [-280.833, 533.76, 10], [-109.93, 631.066, 10], [10.802, 145.35, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))