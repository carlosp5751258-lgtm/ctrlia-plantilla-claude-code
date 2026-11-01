import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from app import sumar  # noqa: E402


class TestSumar(unittest.TestCase):
    def test_suma_enteros(self):
        self.assertEqual(sumar(2, 3), 5)


if __name__ == "__main__":
    unittest.main()
