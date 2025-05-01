[![Build][github-ci-image]][github-ci-link]
[![Coverage Status][codecov-image]][codecov-link]
[![PyPI Version][pypi-image]][pypi-link]
[![PyPI - Python Version][python-image]][pypi-link]
![License][license-image]

# Kajihs Utils

Fully typed, plausibly practical, and remarkably random utilities for me—and maybe for you too.

## ⬇️ Installation

You can install **kajihs_utils** via pip:

```bash
pip install kajihs-utils
```

## 🏃 Getting Started

```python:dev/readme_snippets/formatted/features_demo.py
# Useful protocols for structural subtyping
from kajihs_utils.protocols import SupportsAllComparisons, SupportsDunderLT

x: SupportsAllComparisons[int]

# === Core Algorithm Features ===
from kajihs_utils import get_first, is_sorted

# Get first key existing in a dict
d = {"a": 1, "b": 2, "c": 3}
print(get_first(d, ["x", "a", "b"]))  # Output: 1

# Check if an iterable is sorted
print(is_sorted([1, 2, 2, 3]))  # Output: True
print(is_sorted("cba", reverse=True))  # Output: True
print(is_sorted([0, 1, 0]))  # Output: False

from kajihs_utils.core import bisect_predicate

# Find partition points in sorted data
numbers = [1, 3, 5, 7, 9]
first_big = bisect_predicate(numbers, lambda x: x < 6)
print(f"First number >= 6 is at index {first_big}")  # Output: First number >= 6 is at index 3

# Works with custom objects and complex predicates
records = [
    {"temp": 12, "rain": 0.1},
    {"temp": 15, "rain": 0.3},
    {"temp": 18, "rain": 0.0},  # First "nice" day: temp >15 AND rain <0.2
    {"temp": 20, "rain": 0.1},
]
nice_day_idx = bisect_predicate(records, lambda day: not (day["temp"] > 15 and day["rain"] < 0.2))
print(f"First nice day at index {nice_day_idx}")  # Output: First nice day at index 2

# === Loguru features ===
from kajihs_utils.loguru import prompt, setup_logging

# Better logged and formatted prompts
prompt("Enter a number")  

# Simply setup well formatted logging in files and console
setup_logging(prefix="app", log_dir="logs")

# === Numpy features ===
import numpy as np

from kajihs_utils.numpy_utils import Vec2d, find_closest

x = np.array([[0, 0], [10, 10], [20, 20]])
print(find_closest(x, [[-1, 2], [15, 12]]))  # Output: [0 1]

# Vec2d class
v = Vec2d(3.0, 4.0)
print(v)  # Output: [3. 4.]
print(tuple(v))  # Output: (np.float64(3.0), np.float64(4.0))
print(v.x)  # Output: 3.0
print(v.y)  # Output: 4.0
print(v.magnitude())  # Output: 5.0
print(v.normalized())  # Output: [0.6 0.8]
print(v.angle())  # Output: 53.13010235415598
print(v.rotate(90, center=(1, 1)))  # Output: [-2.  3.]

# === Whenever features ===
from datetime import datetime

from kajihs_utils.whenever import AllDateTime, ExactDateTime, dt_to_system_datetime  # Useful types

print(dt_to_system_datetime(datetime.now()))  # Output: 2025-05-01T09:46:55.165858+00:00
```

## 🧾 License

[MIT license](LICENSE)

<!-- Links -->
[github-ci-image]: https://github.com/Kajiih/kajihs_utils/actions/workflows/build.yml/badge.svg?branch=main
[github-ci-link]: https://github.com/Kajiih/kajihs_utils/actions?query=workflow%3Abuild+branch%3Amain

[codecov-image]: https://img.shields.io/codecov/c/github/Kajiih/kajihs_utils/main.svg?logo=codecov&logoColor=aaaaaa&labelColor=333333
[codecov-link]: https://codecov.io/github/Kajiih/kajihs_utils

[pypi-image]: https://img.shields.io/pypi/v/kajihs-utils.svg?logo=pypi&logoColor=aaaaaa&labelColor=333333
[pypi-link]: https://pypi.python.org/pypi/kajihs-utils

[python-image]: https://img.shields.io/pypi/pyversions/kajihs-utils?logo=python&logoColor=aaaaaa&labelColor=333333
[license-image]: https://img.shields.io/badge/license-MIT_license-blue.svg?labelColor=333333
