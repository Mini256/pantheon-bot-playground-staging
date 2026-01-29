import unittest

from is_pass import is_pass


class TestIsPass(unittest.TestCase):
    def test_score_59_fails(self) -> None:
        self.assertFalse(is_pass(59))

    def test_score_60_passes(self) -> None:
        self.assertTrue(is_pass(60))

    def test_score_61_passes(self) -> None:
        self.assertTrue(is_pass(61))


if __name__ == "__main__":
    unittest.main()
