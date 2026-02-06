"""Small utilities for string manipulation.

This file provides a simple `reverse_string` function and
an example CLI usage when run as a script.
"""

from typing import Any


def reverse_string(s: str) -> str:
    """Return the reverse of the input string `s`.

    Examples:
        >>> reverse_string('abc')
        'cba'
    """
    return s[::-1]


if __name__ == "__main__":
    examples = ["hello", "", "a", "racecar", "12345"]
    for ex in examples:
        print(f"{ex!r} -> {reverse_string(ex)!r}")
