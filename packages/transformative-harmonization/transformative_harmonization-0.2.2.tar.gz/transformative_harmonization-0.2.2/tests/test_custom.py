import unittest
from transformative_harmonization.custom import CustomHarmonization

class TestCustomHarmonization(unittest.TestCase):
    def test_custom_function(self):
        def custom_harmony(a, b, context):
            return context.get('scale', 1.0) * (a + b) / 2
        ch = CustomHarmonization(custom_harmony, context={'scale': 2.0})
        result = ch.harmonize(3, 5)
        self.assertEqual(result, 8.0)

    def test_invalid_function(self):
        with self.assertRaises(ValueError):
            CustomHarmonization("not a function")

if __name__ == "__main__":
    unittest.main()