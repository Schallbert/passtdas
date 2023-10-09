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

    offset = [-4.05, 6.96, 0]

    def setUp(self) -> None:
        pass

    def test_arcr_extremescorrect(self):
        with open('arcr.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_arcij_extremescorrect(self):
        with open('arcij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [self.bottom, self.left, self.top, self.right]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect,list_to_float(result))

    def test_arcoffsetr_extremescorrect(self):
        with open('arcoffsetr.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = roundlistitems([list(map(add, self.offset, self.bottom)), list(map(add, self.offset, self.left)),
                      list(map(add, self.offset, self.top)), list(map(add, self.offset, self.right))])
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_arcoffsetij_extremescorrect(self):
        with open('arcoffsetij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[-4, 1.27, 10], [-9.66, 6.93, 10], [-4, 12.59, 10], [1.66, 6.93, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_rectangle_extremescorrect(self):
        with open('rectangle.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, 0, 10], [0, 0, 10], [50, 50, 10], [50, 0, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))


    def test_elipser_extremescorrect(self):
        with open('elipser.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0, -320, 10], [-200, 0, 10], [0, 320, 10], [200, 0, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_elipseij_extremescorrect(self):
        with open('elipseij.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            targets = ['Ymin', 'Xmin', 'Ymax', 'Xmax']
            expect = [[0.02, -320.002, 10], [-200.003, 0.02, 10], [-0.02, 320.002, 10], [200.003, -0.02, 10]]
            result = cpp.get_extremes_text(targets, data, 10)
            self.assertEqual(expect, list_to_float(result))

    def test_irregularshape_extremescorrect(self):
        with open('cncpathpreview_testcad.tap', 'r') as f:
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