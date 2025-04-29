import unittest
import numpy as np
from transformative_harmonization.core import TransformativeHarmonization

class TestTransformativeHarmonization(unittest.TestCase):
    def setUp(self):
        self.th = TransformativeHarmonization(context={'weight': 1.0, 'scale': 1.0})

    def test_basic_harmonization(self):
        result = self.th.harmonize(3, 4)
        self.assertAlmostEqual(result, 3.50, places=2)

    def test_zero_input(self):
        result = self.th.harmonize(0, 0)
        self.assertEqual(result, 0.0)

    def test_context_weight(self):
        th = TransformativeHarmonization(context={'weight': 2.0, 'scale': 1.0})
        result = th.harmonize(3, 4)
        self.assertNotEqual(result, self.th.harmonize(3, 4))

    def test_commutative(self):
        self.assertTrue(self.th.is_commutative)
        result1 = self.th.harmonize(3, 4)
        result2 = self.th.harmonize(4, 3)
        self.assertAlmostEqual(result1, result2, places=5)

    def test_non_associative(self):
        self.assertFalse(self.th.is_associative)
        result1 = self.th.harmonize(self.th.harmonize(3, 4), 5)
        result2 = self.th.harmonize(3, self.th.harmonize(4, 5))
        self.assertNotAlmostEqual(result1, result2, places=5)

    def test_continuity(self):
        self.assertTrue(self.th.continuity(3, 4))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.th.harmonize(5)

if __name__ == "__main__":
    unittest.main()