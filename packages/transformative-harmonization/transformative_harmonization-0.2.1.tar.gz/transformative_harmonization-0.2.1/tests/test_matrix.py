import unittest
import numpy as np
from transformative_harmonization.matrix import MatrixHarmonization

class TestMatrixHarmonization(unittest.TestCase):
    def setUp(self):
        self.mh = MatrixHarmonization(context={'weight': 1.0, 'scale': 1.0})

    def test_matrix_harmonization(self):
        m1 = np.array([[1, 0], [0, 1]])
        m2 = np.array([[0, 1], [1, 0]])
        result = self.mh.harmonize(m1, m2)
        self.assertEqual(result.shape, m1.shape)

    def test_invalid_shape(self):
        m1 = np.array([[1, 0], [0, 1]])
        m2 = np.array([[0, 1]])
        with self.assertRaises(ValueError):
            self.mh.harmonize(m1, m2)

if __name__ == "__main__":
    unittest.main()