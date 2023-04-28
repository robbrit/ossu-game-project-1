import unittest

from engine.model import shapes


class PolygonTest(unittest.TestCase):
    def test_center_rectangle(self):
        rect = shapes.Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])

        self.assertEqual(rect.center_x, 0.5)
        self.assertEqual(rect.center_y, 0.5)

    def test_center_one_point(self):
        rect = shapes.Polygon([(0, 0)])

        self.assertEqual(rect.center_x, 0)
        self.assertEqual(rect.center_y, 0)

    def test_no_points(self):
        with self.assertRaises(ValueError):
            shapes.Polygon([])
