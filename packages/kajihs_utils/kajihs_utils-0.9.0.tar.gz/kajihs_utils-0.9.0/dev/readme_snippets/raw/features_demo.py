# Useful protocols for structural subtyping
from kajihs_utils.protocols import SupportsAllComparisons, SupportsDunderLT

x: SupportsAllComparisons[int]

# === Core Algorithm Features ===
from kajihs_utils import get_first, is_sorted

# Get first key existing in a dict
d = {"a": 1, "b": 2, "c": 3}
print(get_first(d, ["x", "a", "b"]))

# Check if an iterable is sorted
print(is_sorted([1, 2, 2, 3]))
print(is_sorted("cba", reverse=True))
print(is_sorted([0, 1, 0]))

from kajihs_utils.core import bisect_predicate

# Find partition points in sorted data
numbers = [1, 3, 5, 7, 9]
first_big = bisect_predicate(numbers, lambda x: x < 6)
print(f"First number >= 6 is at index {first_big}")

# Works with custom objects and complex predicates
records = [
    {"temp": 12, "rain": 0.1},
    {"temp": 15, "rain": 0.3},
    {"temp": 18, "rain": 0.0},  # First "nice" day: temp >15 AND rain <0.2
    {"temp": 20, "rain": 0.1},
]
nice_day_idx = bisect_predicate(records, lambda day: not (day["temp"] > 15 and day["rain"] < 0.2))
print(f"First nice day at index {nice_day_idx}")

# === Loguru features ===
from kajihs_utils.loguru import prompt, setup_logging

# Better logged and formatted prompts
prompt("Enter a number")  # snippet: no-exec

# Simply setup well formatted logging in files and console
setup_logging(prefix="app", log_dir="logs")

# === Numpy features ===
import numpy as np

from kajihs_utils.numpy_utils import Vec2d, find_closest

x = np.array([[0, 0], [10, 10], [20, 20]])
print(find_closest(x, [[-1, 2], [15, 12]]))

# Vec2d class
v = Vec2d(3.0, 4.0)
print(v)
print(tuple(v))
print(v.x)
print(v.y)
print(v.magnitude())
print(v.normalized())
print(v.angle())
print(v.rotate(90, center=(1, 1)))

# === Whenever features ===
from datetime import datetime

from kajihs_utils.whenever import AllDateTime, ExactDateTime, dt_to_system_datetime  # Useful types

print(dt_to_system_datetime(datetime.now()))
