import unittest

from is_pass import is_pass


class TestIsPass(unittest.TestCase):
    def test_pass_threshold_inclusive(self):
        self.assertFalse(is_pass(59))
        self.assertTrue(is_pass(60))
        self.assertTrue(is_pass(61))

