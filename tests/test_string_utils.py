import unittest
from string_utils import reverse_string


class TestReverseString(unittest.TestCase):
    def test_basic_examples(self):
        self.assertEqual(reverse_string("abc"), "cba")
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("a"), "a")
        self.assertEqual(reverse_string("racecar"), "racecar")
        self.assertEqual(reverse_string("Hello 世界"), "界世 olleH")


if __name__ == "__main__":
    unittest.main()
