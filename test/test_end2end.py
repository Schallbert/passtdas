import unittest
import cncpathpreview as cpp

class TestEnd2End(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_circler_writesfilecorrectly(self):
        targetfilename = 'test_previewcircler.tap'
        with open('circler.tap', 'r') as f:
            data = cpp.create_dataset_from_input(f)
            cpp.generate_output_file(targetfilename, data, 10)
        with open (targetfilename, 'r') as read:

