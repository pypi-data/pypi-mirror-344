import unittest
import numpy as np
from transformative_harmonization.vector import VectorHarmonization

class TestVectorHarmonization(unittest.TestCase):
    def setUp(self):
        self.vh = VectorHarmonization(context={'weight': 1.0, 'scale': 1.0})

    def test_vector_harmonization(self):
        v1 = np.array([1, 0])
        v2 = np.array([0, 1])
        result = self.vh.harmonize(v1, v2)
        self.assertEqual(result.shape, v1.shape)

    def test_invalid_shape(self):
        v1 = np.array([1, 0])
        v2 = np.array([0, 1, 0])
        with self.assertRaises(ValueError):
            self.vh.harmonize(v1, v2)

    def test_context_scale(self):
        vh = VectorHarmonization(context={'weight': 1.0, 'scale': 2.0})
        v1 = np.array([1, 0])
        v2 = np.array([0, 1])
        result = vh.harmonize(v1, v2)
        self.assertGreater(np.linalg.norm(result), np.linalg.norm(self.vh.harmonize(v1, v2)))

if __name__ == "__main__":
    unittest.main()