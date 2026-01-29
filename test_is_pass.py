import os
import subprocess
import sys
import unittest


class TestIsPassModule(unittest.TestCase):
    def test_import_has_no_side_effects(self):
        test_dir = os.path.dirname(__file__)
        result = subprocess.run(
            [sys.executable, "-c", "import is_pass"],
            cwd=test_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


class TestCalculateAverage(unittest.TestCase):
    def test_empty_list_returns_zero(self):
        import is_pass

        self.assertEqual(is_pass.calculate_average([]), 0.0)

    def test_average_computed(self):
        import is_pass

        self.assertEqual(is_pass.calculate_average([1, 2, 3]), 2.0)


if __name__ == "__main__":
    unittest.main()
