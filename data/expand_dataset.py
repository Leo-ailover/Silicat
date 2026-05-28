"""Generate additional coding examples and append to silicat_chat.jsonl."""
import json
from pathlib import Path

JSONL = Path(__file__).parent / "silicat_chat.jsonl"


def ex(user, silicat):
    return json.dumps({"messages": [{"role": "user", "content": user}, {"role": "silicat", "content": silicat}]})


new_examples = [
    # ── OOP ──────────────────────────────────────────────────────────────────
    ex("write a python class", """\
```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says woof!"
```"""),
    ex("how do i inherit from a class in python", """\
```python
class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "meow"
```"""),
    ex("what is a class method", """\
A `@classmethod` receives the class (`cls`) instead of an instance:

```python
class Counter:
    count = 0

    @classmethod
    def increment(cls):
        cls.count += 1
```"""),
    ex("what is a static method", """\
A `@staticmethod` has no implicit first argument — it's just a regular function namespaced inside the class:

```python
class Math:
    @staticmethod
    def add(a, b):
        return a + b
```"""),
    ex("what is __str__ in python", """\
`__str__` controls what `str()` and `print()` show for your object:

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Point({self.x}, {self.y})"
```"""),
    ex("what is __repr__", """\
`__repr__` is the developer-facing string — used in the REPL and `repr()`:

```python
class Point:
    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"
```
Aim to make it unambiguous and ideally eval-able."""),
    ex("how do i use property in python", """\
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("radius must be non-negative")
        self._radius = value
```"""),
    ex("what is a dataclass", """\
`@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__`:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```"""),
    ex("how do i make a class iterable", """\
Implement `__iter__` and `__next__`:

```python
class CountUp:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        self.current += 1
        return self.current
```"""),
    ex("what is __len__", """\
`__len__` makes `len()` work on your class:

```python
class Stack:
    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)
```"""),

    # ── Decorators ───────────────────────────────────────────────────────────
    ex("write a simple decorator", """\
```python
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def greet(name):
    return f"Hello, {name}!"
```"""),
    ex("write a timer decorator", """\
```python
import time, functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - t0:.4f}s")
        return result
    return wrapper
```"""),
    ex("write a retry decorator", """\
```python
import functools, time

def retry(times=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
```"""),
    ex("what is functools.wraps", """\
`@functools.wraps(func)` copies the original function's `__name__`, `__doc__`, etc. onto the wrapper so introspection still works:

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```"""),

    # ── Generators ───────────────────────────────────────────────────────────
    ex("write a generator in python", """\
```python
def count_up(n):
    for i in range(n):
        yield i

for x in count_up(5):
    print(x)
```"""),
    ex("what is yield from", """\
`yield from` delegates to a sub-generator:

```python
def chain(*iterables):
    for it in iterables:
        yield from it

list(chain([1, 2], [3, 4]))  # [1, 2, 3, 4]
```"""),
    ex("what is a generator expression", """\
Like a list comprehension but lazy — values computed on demand:

```python
squares = (x * x for x in range(10))
print(next(squares))  # 0
print(next(squares))  # 1
```"""),
    ex("infinite counter generator", """\
```python
def counter(start=0):
    n = start
    while True:
        yield n
        n += 1
```"""),

    # ── Context managers ─────────────────────────────────────────────────────
    ex("write a context manager", """\
```python
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    t0 = time.perf_counter()
    yield
    print(f"elapsed: {time.perf_counter() - t0:.3f}s")

with timer():
    sum(range(1_000_000))
```"""),
    ex("write a context manager class", """\
```python
class TempDir:
    import tempfile, shutil, os

    def __enter__(self):
        self.path = tempfile.mkdtemp()
        return self.path

    def __exit__(self, *_):
        import shutil
        shutil.rmtree(self.path)
```"""),

    # ── Error handling ───────────────────────────────────────────────────────
    ex("how do i catch exceptions in python", """\
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"error: {e}")
finally:
    print("always runs")
```"""),
    ex("how do i raise a custom exception", """\
```python
class ValidationError(Exception):
    pass

def validate_age(age):
    if age < 0:
        raise ValidationError(f"age {age} is negative")
```"""),
    ex("how do i catch multiple exceptions", """\
```python
try:
    x = int(input())
    result = 10 / x
except (ValueError, ZeroDivisionError) as e:
    print(f"bad input: {e}")
```"""),

    # ── Comprehensions ───────────────────────────────────────────────────────
    ex("list comprehension with filter", """\
```python
evens = [x for x in range(20) if x % 2 == 0]
```"""),
    ex("dict comprehension", """\
```python
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```"""),
    ex("set comprehension", """\
```python
unique_lens = {len(word) for word in ["hello", "hi", "world"]}
```"""),
    ex("nested list comprehension", """\
```python
matrix = [[1, 2, 3], [4, 5, 6]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6]
```"""),

    # ── Lambda / functional ──────────────────────────────────────────────────
    ex("how do i use map in python", """\
```python
nums = [1, 2, 3, 4]
doubled = list(map(lambda x: x * 2, nums))
# [2, 4, 6, 8]
```"""),
    ex("how do i use filter in python", """\
```python
nums = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, nums))
```"""),
    ex("how do i use reduce", """\
```python
from functools import reduce
product = reduce(lambda a, b: a * b, [1, 2, 3, 4])
# 24
```"""),
    ex("sort by key in python", """\
```python
words = ["banana", "apple", "cherry"]
words.sort(key=len)          # by length
words.sort(key=str.lower)    # case-insensitive
```"""),
    ex("sorted with reverse", """\
```python
nums = [3, 1, 4, 1, 5, 9]
desc = sorted(nums, reverse=True)
```"""),

    # ── String operations ─────────────────────────────────────────────────────
    ex("how do i split a string", """\
```python
s = "hello world foo"
parts = s.split()        # ["hello", "world", "foo"]
parts = s.split(" ", 1)  # ["hello", "world foo"]
```"""),
    ex("how do i join a list into a string", """\
```python
words = ["hello", "world"]
s = " ".join(words)  # "hello world"
```"""),
    ex("how do i strip whitespace", """\
```python
s = "  hello  "
s.strip()   # "hello"
s.lstrip()  # "hello  "
s.rstrip()  # "  hello"
```"""),
    ex("how do i check if a string starts with something", """\
```python
s = "hello world"
s.startswith("hello")  # True
s.endswith("world")    # True
```"""),
    ex("how do i replace in a string", """\
```python
s = "hello world"
s.replace("world", "python")  # "hello python"
```"""),
    ex("f-strings in python", """\
```python
name = "Alice"
age = 30
print(f"My name is {name} and I am {age} years old.")
print(f"Pi is approximately {3.14159:.2f}")
```"""),
    ex("how do i check if a substring exists", """\
```python
s = "hello world"
"world" in s   # True
"python" in s  # False
```"""),
    ex("how do i count occurrences in a string", """\
```python
s = "banana"
s.count("a")  # 3
```"""),
    ex("how do i pad a string", """\
```python
s = "42"
s.zfill(5)    # "00042"
s.ljust(5)    # "42   "
s.rjust(5)    # "   42"
s.center(5)   # " 42  "
```"""),

    # ── Dictionary operations ─────────────────────────────────────────────────
    ex("how do i merge two dicts", """\
```python
a = {"x": 1}
b = {"y": 2}
merged = {**a, **b}          # Python 3.5+
merged = a | b               # Python 3.9+
```"""),
    ex("how do i get a value from a dict with a default", """\
```python
d = {"a": 1}
d.get("b", 0)   # 0 — no KeyError
```"""),
    ex("how do i iterate over a dict", """\
```python
d = {"a": 1, "b": 2}
for key in d:             # keys
    pass
for val in d.values():    # values
    pass
for k, v in d.items():   # both
    pass
```"""),
    ex("how do i invert a dictionary", """\
```python
d = {"a": 1, "b": 2}
inv = {v: k for k, v in d.items()}
```"""),
    ex("defaultdict example", """\
```python
from collections import defaultdict

groups = defaultdict(list)
for item in ["apple", "banana", "avocado", "blueberry"]:
    groups[item[0]].append(item)
```"""),
    ex("Counter example", """\
```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
print(c.most_common(2))  # [('apple', 3), ('banana', 2)]
```"""),
    ex("OrderedDict example", """\
```python
from collections import OrderedDict

d = OrderedDict()
d["first"] = 1
d["second"] = 2
# Preserves insertion order (same as plain dict in Python 3.7+)
```"""),

    # ── List / set operations ─────────────────────────────────────────────────
    ex("how do i remove duplicates from a list", """\
```python
lst = [1, 2, 2, 3, 3, 3]
unique = list(dict.fromkeys(lst))  # preserves order
unique = list(set(lst))            # may reorder
```"""),
    ex("how do i flatten a nested list", """\
```python
nested = [[1, 2], [3, 4], [5]]
flat = [x for sub in nested for x in sub]
# or:
import itertools
flat = list(itertools.chain.from_iterable(nested))
```"""),
    ex("how do i find the intersection of two lists", """\
```python
a = [1, 2, 3, 4]
b = [3, 4, 5, 6]
common = list(set(a) & set(b))  # [3, 4]
```"""),
    ex("how do i chunk a list", """\
```python
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

list(chunks([1, 2, 3, 4, 5], 2))  # [[1,2],[3,4],[5]]
```"""),

    # ── File / IO ─────────────────────────────────────────────────────────────
    ex("how do i read a csv file", """\
```python
import csv

with open("data.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```"""),
    ex("how do i write a csv file", """\
```python
import csv

rows = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
with open("out.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)
```"""),
    ex("how do i read json from a file", """\
```python
import json

with open("data.json", encoding="utf-8") as f:
    data = json.load(f)
```"""),
    ex("how do i write json to a file", """\
```python
import json

data = {"name": "Alice", "scores": [1, 2, 3]}
with open("out.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
```"""),
    ex("how do i list files in a directory", """\
```python
from pathlib import Path

for p in Path(".").iterdir():
    print(p)

# Only .py files:
for p in Path(".").glob("*.py"):
    print(p)
```"""),
    ex("how do i check if a file exists", """\
```python
from pathlib import Path

if Path("myfile.txt").exists():
    print("found")
```"""),
    ex("how do i read lines from a file", """\
```python
with open("file.txt", encoding="utf-8") as f:
    lines = f.readlines()

# Or iterate without loading everything:
with open("file.txt", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip())
```"""),

    # ── Async ─────────────────────────────────────────────────────────────────
    ex("how do i write async code in python", """\
```python
import asyncio

async def fetch(url):
    await asyncio.sleep(1)  # simulate IO
    return f"response from {url}"

async def main():
    result = await fetch("http://example.com")
    print(result)

asyncio.run(main())
```"""),
    ex("how do i run async tasks concurrently", """\
```python
import asyncio

async def task(n):
    await asyncio.sleep(n)
    return n

async def main():
    results = await asyncio.gather(task(1), task(2), task(3))
    print(results)  # [1, 2, 3]

asyncio.run(main())
```"""),
    ex("what is async with", """\
`async with` is for async context managers (like async file/db handles):

```python
async def save(data):
    async with aiofiles.open("out.txt", "w") as f:
        await f.write(data)
```"""),

    # ── Type hints ────────────────────────────────────────────────────────────
    ex("how do i add type hints to a function", """\
```python
def greet(name: str, times: int = 1) -> str:
    return (name + " ") * times
```"""),
    ex("how do i type hint a list or dict", """\
```python
from typing import Optional

def process(items: list[int], mapping: dict[str, int]) -> Optional[int]:
    return mapping.get(items[0]) if items else None
```
In Python 3.9+ you can use `list[int]` directly without importing from `typing`."""),
    ex("what is Optional in typing", """\
`Optional[X]` means the value is either `X` or `None`:

```python
from typing import Optional

def find(lst: list[int], target: int) -> Optional[int]:
    try:
        return lst.index(target)
    except ValueError:
        return None
```"""),
    ex("what is Union in typing", """\
`Union[A, B]` means the value can be `A` or `B`. In Python 3.10+ use `A | B`:

```python
from typing import Union

def stringify(value: Union[int, float]) -> str:
    return str(value)
```"""),

    # ── Algorithms ───────────────────────────────────────────────────────────
    ex("binary search in python", """\
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```"""),
    ex("write bubble sort", """\
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```"""),
    ex("write quicksort in python", """\
```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```"""),
    ex("write merge sort in python", """\
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(a, b):
    result, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    return result + a[i:] + b[j:]
```"""),
    ex("fibonacci with memoization", """\
```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```"""),
    ex("check if a number is prime", """\
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
```"""),
    ex("two sum problem", """\
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
```"""),
    ex("how do i find the max subarray sum", """\
Kadane's algorithm:

```python
def max_subarray(nums):
    best = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        best = max(best, cur)
    return best
```"""),
    ex("check if a string is a palindrome", """\
```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]
```"""),
    ex("count words in a string", """\
```python
def word_count(text):
    from collections import Counter
    return Counter(text.lower().split())
```"""),

    # ── Data structures ───────────────────────────────────────────────────────
    ex("implement a stack in python", """\
```python
class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        return self._data.pop()

    def peek(self):
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)
```"""),
    ex("implement a queue in python", """\
Use `collections.deque` for O(1) popleft:

```python
from collections import deque

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        return self._data.popleft()

    def is_empty(self):
        return not self._data
```"""),
    ex("implement a linked list node", """\
```python
class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        node = Node(val)
        if not self.head:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node
```"""),
    ex("implement a binary tree", """\
```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)
```"""),
    ex("implement a min heap", """\
Python's `heapq` module is a min-heap:

```python
import heapq

h = []
heapq.heappush(h, 3)
heapq.heappush(h, 1)
heapq.heappush(h, 2)
print(heapq.heappop(h))  # 1
```"""),

    # ── Regex ─────────────────────────────────────────────────────────────────
    ex("how do i use regex in python", """\
```python
import re

pattern = r"\\d+"
text = "I have 3 cats and 12 dogs"
matches = re.findall(pattern, text)  # ['3', '12']
```"""),
    ex("how do i match an email with regex", """\
```python
import re

pattern = r"[\\w.+-]+@[\\w-]+\\.[\\w.]+"
emails = re.findall(pattern, "reach me at alice@example.com or bob@test.org")
```"""),
    ex("how do i replace with regex", """\
```python
import re

text = re.sub(r"\\s+", " ", "too   many   spaces")
# "too many spaces"
```"""),

    # ── datetime ─────────────────────────────────────────────────────────────
    ex("how do i get the current date and time", """\
```python
from datetime import datetime

now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))
```"""),
    ex("how do i parse a date string", """\
```python
from datetime import datetime

dt = datetime.strptime("2024-01-15", "%Y-%m-%d")
print(dt.year, dt.month, dt.day)
```"""),
    ex("how do i add days to a date", """\
```python
from datetime import datetime, timedelta

dt = datetime(2024, 1, 15)
future = dt + timedelta(days=30)
```"""),

    # ── Itertools ─────────────────────────────────────────────────────────────
    ex("itertools combinations", """\
```python
from itertools import combinations

list(combinations([1, 2, 3], 2))
# [(1, 2), (1, 3), (2, 3)]
```"""),
    ex("itertools permutations", """\
```python
from itertools import permutations

list(permutations("ABC", 2))
# [('A','B'),('A','C'),('B','A'),('B','C'),('C','A'),('C','B')]
```"""),
    ex("itertools product", """\
```python
from itertools import product

list(product([0, 1], repeat=3))
# all 3-bit binary strings
```"""),
    ex("itertools groupby", """\
```python
from itertools import groupby

data = [("a", 1), ("a", 2), ("b", 3)]
for key, group in groupby(data, key=lambda x: x[0]):
    print(key, list(group))
```"""),

    # ── Testing ───────────────────────────────────────────────────────────────
    ex("how do i write a unit test in python", """\
```python
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0

if __name__ == "__main__":
    unittest.main()
```"""),
    ex("how do i use pytest", """\
```python
# test_math.py
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0
```
Run with: `pytest test_math.py`"""),
    ex("how do i mock in python", """\
```python
from unittest.mock import patch, MagicMock

def get_user(user_id):
    ...  # calls an external API

def test_get_user():
    with patch("mymodule.requests.get") as mock_get:
        mock_get.return_value = MagicMock(json=lambda: {"id": 1})
        result = get_user(1)
    assert result["id"] == 1
```"""),

    # ── Pathlib ───────────────────────────────────────────────────────────────
    ex("how do i use pathlib", """\
```python
from pathlib import Path

p = Path("data/file.txt")
p.parent      # Path("data")
p.name        # "file.txt"
p.stem        # "file"
p.suffix      # ".txt"
p.read_text()            # read content
p.write_text("hello")    # write content
p.mkdir(parents=True, exist_ok=True)
```"""),
    ex("how do i find all python files recursively", """\
```python
from pathlib import Path

py_files = list(Path(".").rglob("*.py"))
```"""),

    # ── Environment / subprocess ──────────────────────────────────────────────
    ex("how do i read environment variables", """\
```python
import os

value = os.environ.get("MY_VAR", "default")
```"""),
    ex("how do i run a shell command from python", """\
```python
import subprocess

result = subprocess.run(
    ["ls", "-la"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.stdout)
```"""),

    # ── Logging ───────────────────────────────────────────────────────────────
    ex("how do i use logging in python", """\
```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

log.info("server started")
log.warning("disk almost full")
log.error("connection failed")
```"""),

    # ── argparse ─────────────────────────────────────────────────────────────
    ex("how do i parse command line args", """\
```python
import argparse

p = argparse.ArgumentParser(description="My tool")
p.add_argument("input", help="input file")
p.add_argument("--verbose", action="store_true")
p.add_argument("--count", type=int, default=1)
args = p.parse_args()
print(args.input, args.verbose, args.count)
```"""),

    # ── Miscellaneous Python ──────────────────────────────────────────────────
    ex("what is *args and **kwargs", """\
`*args` collects extra positional arguments, `**kwargs` collects extra keyword arguments:

```python
def func(*args, **kwargs):
    print(args)    # tuple
    print(kwargs)  # dict

func(1, 2, x=3, y=4)
# (1, 2)
# {'x': 3, 'y': 4}
```"""),
    ex("what is the walrus operator", """\
`:=` assigns and returns a value in one expression (Python 3.8+):

```python
import re

if m := re.search(r"\\d+", text):
    print(m.group())
```"""),
    ex("how do i unpack a list", """\
```python
a, b, c = [1, 2, 3]
first, *rest = [1, 2, 3, 4, 5]
# first=1, rest=[2,3,4,5]
```"""),
    ex("how do i zip two lists", """\
```python
names = ["Alice", "Bob"]
ages  = [30, 25]
pairs = list(zip(names, ages))
# [("Alice", 30), ("Bob", 25)]
```"""),
    ex("how do i enumerate a list", """\
```python
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
```"""),
    ex("how do i copy a list", """\
```python
original = [1, 2, 3]
shallow = original.copy()   # or original[:]
import copy
deep = copy.deepcopy(original)
```"""),
    ex("what is the difference between is and ==", """\
`==` checks value equality. `is` checks identity (same object in memory):

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b   # True  — same values
a is b   # False — different objects
```"""),
    ex("how do i profile python code", """\
```python
import cProfile

cProfile.run("my_function()")

# Or from the command line:
# python -m cProfile -s cumulative myscript.py
```"""),
    ex("what is __name__ == '__main__'", """\
It guards code that should only run when the script is executed directly, not when it's imported as a module:

```python
def main():
    print("running!")

if __name__ == "__main__":
    main()
```"""),
    ex("how do i deep copy an object", """\
```python
import copy

original = {"a": [1, 2, 3]}
deep = copy.deepcopy(original)
deep["a"].append(4)
print(original["a"])  # [1, 2, 3] — unchanged
```"""),
    ex("how do i measure execution time", """\
```python
import time

t0 = time.perf_counter()
# ... code to time ...
elapsed = time.perf_counter() - t0
print(f"{elapsed:.4f}s")
```"""),

    # ── Mini multi-turn ──────────────────────────────────────────────────────
]

# Multi-turn examples
multi_turn = [
    {"messages": [
        {"role": "user", "content": "write a function to check if a number is even"},
        {"role": "silicat", "content": "```python\ndef is_even(n):\n    return n % 2 == 0\n```"},
        {"role": "user", "content": "how do i check if it's odd too"},
        {"role": "silicat", "content": "```python\ndef is_odd(n):\n    return n % 2 != 0\n# or simply: not is_even(n)\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "how do i make a list of squares"},
        {"role": "silicat", "content": "```python\nsquares = [x**2 for x in range(10)]\n```"},
        {"role": "user", "content": "what if i only want even squares"},
        {"role": "silicat", "content": "```python\neven_squares = [x**2 for x in range(10) if x % 2 == 0]\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "write a function that counts vowels"},
        {"role": "silicat", "content": "```python\ndef count_vowels(s):\n    return sum(1 for c in s.lower() if c in 'aeiou')\n```"},
        {"role": "user", "content": "also count consonants"},
        {"role": "silicat", "content": "```python\ndef count_letters(s):\n    vowels = set('aeiou')\n    v = sum(1 for c in s.lower() if c in vowels)\n    c = sum(1 for ch in s.lower() if ch.isalpha() and ch not in vowels)\n    return {'vowels': v, 'consonants': c}\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "implement a simple calculator"},
        {"role": "silicat", "content": "```python\ndef calc(a, op, b):\n    if op == '+':\n        return a + b\n    if op == '-':\n        return a - b\n    if op == '*':\n        return a * b\n    if op == '/':\n        if b == 0:\n            raise ValueError('division by zero')\n        return a / b\n    raise ValueError(f'unknown operator: {op}')\n```"},
        {"role": "user", "content": "add power and modulo"},
        {"role": "silicat", "content": "```python\ndef calc(a, op, b):\n    match op:\n        case '+': return a + b\n        case '-': return a - b\n        case '*': return a * b\n        case '/':\n            if b == 0: raise ValueError('division by zero')\n            return a / b\n        case '**': return a ** b\n        case '%': return a % b\n        case _: raise ValueError(f'unknown operator: {op}')\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "how do i open a url in python"},
        {"role": "silicat", "content": "```python\nimport urllib.request\nwith urllib.request.urlopen('http://example.com') as r:\n    html = r.read().decode()\n```\nOr use `requests` (third-party, easier API)."},
        {"role": "user", "content": "show me the requests version"},
        {"role": "silicat", "content": "```python\nimport requests\n\nr = requests.get('https://httpbin.org/get')\nr.raise_for_status()\nprint(r.json())\n```"},
    ]},
]

with JSONL.open("a", encoding="utf-8") as f:
    for example in new_examples:
        f.write(example + "\n")
    for row in multi_turn:
        f.write(json.dumps(row) + "\n")

print(f"Added {len(new_examples)} single-turn + {len(multi_turn)} multi-turn examples.")
