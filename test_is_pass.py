import subprocess
import sys
import unittest
from contextlib import redirect_stdout
import io


class TestIsPassModule(unittest.TestCase):
    def test_import_has_no_side_effects(self):
        result = subprocess.run(
            [sys.executable, "-c", "import is_pass"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")

    def test_runs_as_script(self):
        result = subprocess.run(
            [sys.executable, "is_pass.py"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("成绩列表:", result.stdout)
        self.assertIn("平均分:", result.stdout)


class TestCalculateAverage(unittest.TestCase):
    def test_empty_list_returns_zero(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            import is_pass

        self.assertEqual(is_pass.calculate_average([]), 0.0)

    def test_average_computed(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            import is_pass

        self.assertEqual(is_pass.calculate_average([1, 2, 3]), 2.0)


if __name__ == "__main__":
    unittest.main()
