"""Generate a large synthetic Python pretraining corpus.

Writes data/corpus_synth.txt: the UNIQUE snippets (~40 KB, 261 snippets), each once, separated
by a form-feed line ("\\n\\x0c\\n") so build_corpus.py --include-synth can recover
snippet boundaries. Do not append it to corpus_v2.txt by hand (already done once
in the committed corpus; data/build_corpus.py handles it).
Usage: python data/gen_pretrain_corpus.py [out_path]
"""
import random
import sys
from pathlib import Path

random.seed(42)
OUT = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent / "corpus_synth.txt")

lines = []

def w(text):
    lines.append(text)


# ── helpers ──────────────────────────────────────────────────────────────────

NAMES = ["Alice","Bob","Carol","Dave","Eve","Frank","Grace","Heidi","Ivan","Judy",
         "Karl","Laura","Mallory","Nina","Oscar","Peggy","Quinn","Ruth","Sam","Trent"]
FRUITS = ["apple","banana","cherry","date","elderberry","fig","grape","honeydew","kiwi","lemon"]
ANIMALS = ["cat","dog","bird","fish","rabbit","hamster","turtle","snake","lizard","parrot"]
COLORS = ["red","green","blue","yellow","orange","purple","pink","brown","black","white"]
CITIES = ["Paris","London","Tokyo","Berlin","Rome","Madrid","Sydney","Cairo","Seoul","Moscow"]

def rname(): return random.choice(NAMES)
def rint(lo=1, hi=100): return random.randint(lo, hi)
def ritem(lst): return random.choice(lst)

TYPES = ["int","str","float","bool","list","dict","tuple","set","bytes","None"]
BUILTINS = ["len","range","enumerate","zip","map","filter","sorted","reversed","sum","max","min","abs","round","type","isinstance","print","input","open","hasattr","getattr"]

# ── 1. Basic function definitions (many variations) ──────────────────────────

def gen_functions():
    snippets = []

    # arithmetic
    ops = [("+","add","sum"),("-","subtract","difference"),("*","multiply","product"),("//","floor_divide","quotient"),("%","modulo","remainder")]
    for sym, fname, desc in ops:
        for _ in range(8):
            a, b = rname().lower()[:3], rname().lower()[:3]
            snippets.append(f"""def {fname}_{a}_{b}(x, y):
    return x {sym} y
""")

    # comparisons
    comps = [("<","less_than"),("<=","at_most"),(">","greater_than"),(">=","at_least"),("==","equal_to"),("!=","not_equal")]
    for sym, fname in comps:
        snippets.append(f"""def {fname}(a, b):
    return a {sym} b
""")

    # string ops
    for _ in range(20):
        snippets.append(f"""def reverse_string(s):
    return s[::-1]
""")
        snippets.append(f"""def count_vowels(s):
    return sum(1 for c in s if c in 'aeiouAEIOU')
""")
        snippets.append(f"""def is_palindrome(s):
    s = s.lower().replace(' ', '')
    return s == s[::-1]
""")
        snippets.append(f"""def title_case(s):
    return ' '.join(w.capitalize() for w in s.split())
""")
        snippets.append(f"""def count_words(text):
    return len(text.split())
""")
        snippets.append(f"""def remove_duplicates(lst):
    return list(dict.fromkeys(lst))
""")

    # fibonacci variations
    for _ in range(15):
        snippets.append("""def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
""")
        snippets.append("""def fib_sequence(n):
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq
""")
        snippets.append("""def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)
""")

    # factorial
    for _ in range(10):
        snippets.append("""def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
""")
        snippets.append("""def factorial_recursive(n):
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)
""")

    # sorting
    snippets.append("""def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
""")
    snippets.append("""def insertion_sort(arr):
    arr = arr[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
""")
    snippets.append("""def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
""")
    snippets.append("""def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)
""")

    # search
    snippets.append("""def binary_search(arr, target):
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
""")
    snippets.append("""def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
""")

    # math
    for _ in range(10):
        snippets.append("""def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
""")
        snippets.append("""def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]
""")
        snippets.append("""def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
""")
        snippets.append("""def lcm(a, b):
    return a * b // gcd(a, b)
""")
        snippets.append("""def is_even(n):
    return n % 2 == 0
""")
        snippets.append("""def clamp(value, lo, hi):
    return max(lo, min(hi, value))
""")

    return snippets


# ── 2. Classes ────────────────────────────────────────────────────────────────

def gen_classes():
    snippets = []

    snippets.append("""class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack({self._data})"
""")

    snippets.append("""class Queue:
    def __init__(self):
        self._data = []

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)

    def front(self):
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)
""")

    snippets.append("""class LinkedListNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, value):
        node = LinkedListNode(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self._size += 1

    def prepend(self, value):
        self.head = LinkedListNode(value, self.head)
        self._size += 1

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __repr__(self):
        return "LinkedList([" + ", ".join(str(v) for v in self) + "])"
""")

    for animal in ANIMALS[:5]:
        snippets.append(f"""class {animal.capitalize()}:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return f"{{self.name}} makes a sound"

    def __repr__(self):
        return f"{animal.capitalize()}(name={{self.name!r}}, age={{self.age}})"

    def __eq__(self, other):
        return isinstance(other, {animal.capitalize()}) and self.name == other.name and self.age == other.age
""")

    snippets.append("""class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = BinaryTreeNode(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = BinaryTreeNode(value)
            else:
                self._insert(node.left, value)
        else:
            if node.right is None:
                node.right = BinaryTreeNode(value)
            else:
                self._insert(node.right, value)

    def contains(self, value):
        node = self.root
        while node:
            if value == node.value:
                return True
            elif value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def inorder(self):
        result = []
        def _walk(node):
            if node:
                _walk(node.left)
                result.append(node.value)
                _walk(node.right)
        _walk(self.root)
        return result
""")

    snippets.append("""class Counter:
    def __init__(self):
        self._counts = {}

    def add(self, item):
        self._counts[item] = self._counts.get(item, 0) + 1

    def count(self, item):
        return self._counts.get(item, 0)

    def most_common(self, n=None):
        items = sorted(self._counts.items(), key=lambda x: x[1], reverse=True)
        return items[:n] if n is not None else items

    def __repr__(self):
        return f"Counter({self._counts})"
""")

    snippets.append("""from dataclasses import dataclass, field
from typing import List


@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)


@dataclass
class Rectangle:
    top_left: Point
    bottom_right: Point

    @property
    def width(self) -> float:
        return abs(self.bottom_right.x - self.top_left.x)

    @property
    def height(self) -> float:
        return abs(self.bottom_right.y - self.top_left.y)

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
""")

    snippets.append("""class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache = {}
        self._order = []

    def get(self, key):
        if key not in self._cache:
            return -1
        self._order.remove(key)
        self._order.append(key)
        return self._cache[key]

    def put(self, key, value):
        if key in self._cache:
            self._order.remove(key)
        elif len(self._cache) >= self.capacity:
            oldest = self._order.pop(0)
            del self._cache[oldest]
        self._cache[key] = value
        self._order.append(key)
""")

    return snippets


# ── 3. Context managers ───────────────────────────────────────────────────────

def gen_context_managers():
    snippets = []
    for _ in range(20):
        snippets.append("""import contextlib


@contextlib.contextmanager
def timer(label=""):
    import time
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{label} took {elapsed:.3f}s")
""")
        snippets.append("""import contextlib


@contextlib.contextmanager
def temp_directory():
    import tempfile
    import shutil
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
""")
        snippets.append("""class ManagedResource:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"Acquiring {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing {self.name}")
        return False  # don't suppress exceptions
""")
        snippets.append("""import contextlib


@contextlib.contextmanager
def suppress_errors(*exceptions):
    try:
        yield
    except exceptions:
        pass
""")
    return snippets


# ── 4. Decorators ────────────────────────────────────────────────────────────

def gen_decorators():
    snippets = []
    for _ in range(20):
        snippets.append("""import functools


def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times - 1:
                        raise
            return None
        return wrapper
    return decorator
""")
        snippets.append("""import functools
import time


def cache(func):
    memo = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]
    return wrapper
""")
        snippets.append("""import functools


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper
""")
        snippets.append("""import functools


def validate_positive(*arg_names):
    def decorator(func):
        import inspect
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            for name in arg_names:
                val = bound.arguments.get(name)
                if val is not None and val < 0:
                    raise ValueError(f"{name} must be positive, got {val}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
""")
        snippets.append("""import time
import functools


def throttle(seconds):
    def decorator(func):
        last_call = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_call[0] < seconds:
                return None
            last_call[0] = now
            return func(*args, **kwargs)
        return wrapper
    return decorator
""")
    return snippets


# ── 5. Generators ────────────────────────────────────────────────────────────

def gen_generators():
    snippets = []
    for _ in range(20):
        snippets.append("""def count_up(start=0, step=1):
    n = start
    while True:
        yield n
        n += step
""")
        snippets.append("""def fibonacci_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
""")
        snippets.append("""def chunked(iterable, size):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
""")
        snippets.append("""def flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item
""")
        snippets.append("""def take(n, iterable):
    for i, item in enumerate(iterable):
        if i >= n:
            break
        yield item
""")
        snippets.append("""def sliding_window(seq, size):
    window = []
    for item in seq:
        window.append(item)
        if len(window) == size:
            yield tuple(window)
            window.pop(0)
""")
        snippets.append("""def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.rstrip('\\n')
""")
    return snippets


# ── 6. Error handling ────────────────────────────────────────────────────────

def gen_error_handling():
    snippets = []
    errors = ["ValueError","TypeError","KeyError","IndexError","AttributeError","RuntimeError","IOError","OSError","NotImplementedError","PermissionError"]
    for err in errors:
        for _ in range(5):
            fname = err.lower().replace("error","")
            snippets.append(f"""def safe_{fname}_operation(value):
    try:
        return process_{fname}(value)
    except {err} as e:
        print(f"Error: {{e}}")
        return None
""")
    snippets.append("""class AppError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

    def __str__(self):
        if self.code:
            return f"[{self.code}] {super().__str__()}"
        return super().__str__()


class ValidationError(AppError):
    pass


class NotFoundError(AppError):
    pass
""")
    for _ in range(10):
        snippets.append("""def parse_int(s, default=0):
    try:
        return int(s)
    except (ValueError, TypeError):
        return default
""")
        snippets.append("""def safe_divide(a, b, default=None):
    try:
        return a / b
    except ZeroDivisionError:
        return default
""")
        snippets.append("""def load_json_file(path):
    import json
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}") from e
""")
    return snippets


# ── 7. Comprehensions ────────────────────────────────────────────────────────

def gen_comprehensions():
    snippets = []
    for _ in range(30):
        n = rint(5, 20)
        snippets.append(f"squares = [x**2 for x in range({n})]\n")
        snippets.append(f"evens = [x for x in range({n*2}) if x % 2 == 0]\n")
        snippets.append(f"words = ['hello', 'world', 'python', 'code']\nupper = [w.upper() for w in words]\n")
        snippets.append(f"pairs = [(x, y) for x in range({rint(2,5)}) for y in range({rint(2,5)}) if x != y]\n")
        snippets.append(f"word_lengths = {{word: len(word) for word in ['python', 'java', 'rust', 'go']}}\n")
        snippets.append(f"unique = {{x % {rint(3,8)} for x in range({n})}}\n")
        snippets.append(f"matrix = [[i * j for j in range({rint(3,6)})] for i in range({rint(3,6)})]\n")
        snippets.append(f"flat = [x for row in matrix for x in row]\n")
        snippets.append(f"gen = (x**2 for x in range({n}))\ntotal = sum(gen)\n")
        snippets.append(f"filtered = list(filter(lambda x: x > {rint(1,10)}, range({n})))\n")
    return snippets


# ── 8. Standard library usage ─────────────────────────────────────────────────

def gen_stdlib():
    snippets = []

    # os/pathlib
    for _ in range(15):
        snippets.append("""import os
from pathlib import Path


def list_python_files(directory):
    return list(Path(directory).rglob("*.py"))


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def write_text(path, content):
    Path(path).write_text(content, encoding="utf-8")
""")

    # json
    for _ in range(15):
        snippets.append("""import json


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path, indent=2):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def json_roundtrip(obj):
    return json.loads(json.dumps(obj))
""")

    # datetime
    for _ in range(10):
        snippets.append("""from datetime import datetime, timedelta, date


def days_between(d1: date, d2: date) -> int:
    return abs((d2 - d1).days)


def add_business_days(start: date, days: int) -> date:
    current = start
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Mon-Fri
            added += 1
    return current


def format_date(d: date, fmt: str = "%Y-%m-%d") -> str:
    return d.strftime(fmt)
""")

    # collections
    for _ in range(10):
        snippets.append("""from collections import defaultdict, Counter, deque, OrderedDict


def word_frequency(text: str) -> dict:
    return dict(Counter(text.lower().split()))


def group_by(items, key_func):
    groups = defaultdict(list)
    for item in items:
        groups[key_func(item)].append(item)
    return dict(groups)


def most_common_words(text: str, n: int = 10):
    return Counter(text.lower().split()).most_common(n)
""")

    # itertools
    for _ in range(10):
        snippets.append("""import itertools


def batched(iterable, n):
    it = iter(iterable)
    while True:
        batch = list(itertools.islice(it, n))
        if not batch:
            break
        yield batch


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def round_robin(*iterables):
    return itertools.chain.from_iterable(zip(*iterables))
""")

    # typing
    for _ in range(10):
        snippets.append("""from typing import Optional, List, Dict, Tuple, Union, Any, Callable, TypeVar

T = TypeVar("T")


def first(lst: List[T], default: Optional[T] = None) -> Optional[T]:
    return lst[0] if lst else default


def last(lst: List[T], default: Optional[T] = None) -> Optional[T]:
    return lst[-1] if lst else default


def flatten_dict(d: Dict, prefix: str = "", sep: str = ".") -> Dict[str, Any]:
    result = {}
    for key, value in d.items():
        full_key = f"{prefix}{sep}{key}" if prefix else key
        if isinstance(value, dict):
            result.update(flatten_dict(value, full_key, sep))
        else:
            result[full_key] = value
    return result
""")

    # argparse
    for _ in range(5):
        snippets.append("""import argparse


def make_parser():
    p = argparse.ArgumentParser(description="A simple CLI tool")
    p.add_argument("input", help="Input file path")
    p.add_argument("-o", "--output", default="output.txt", help="Output file path")
    p.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    p.add_argument("-n", "--count", type=int, default=10, help="Number of items")
    return p


if __name__ == "__main__":
    args = make_parser().parse_args()
    print(f"Input: {args.input}, Output: {args.output}, Verbose: {args.verbose}")
""")

    return snippets


# ── 9. async/await ───────────────────────────────────────────────────────────

def gen_async():
    snippets = []
    for _ in range(20):
        snippets.append("""import asyncio


async def fetch_data(url: str) -> str:
    await asyncio.sleep(0.1)  # simulate network delay
    return f"data from {url}"


async def fetch_all(urls: list) -> list:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
""")
        snippets.append("""import asyncio


async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
        await asyncio.sleep(0.01)
    await queue.put(None)  # sentinel


async def consumer(queue: asyncio.Queue) -> list:
    results = []
    while True:
        item = await queue.get()
        if item is None:
            break
        results.append(item * 2)
    return results


async def run_pipeline(items: list) -> list:
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue, items), consumer(queue))
""")
        snippets.append("""import asyncio
from typing import AsyncIterator


async def async_range(n: int) -> AsyncIterator[int]:
    for i in range(n):
        await asyncio.sleep(0)
        yield i


async def async_sum(n: int) -> int:
    total = 0
    async for i in async_range(n):
        total += i
    return total
""")
        snippets.append("""import asyncio


class AsyncCache:
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    async def get(self, key, loader):
        async with self._lock:
            if key not in self._cache:
                self._cache[key] = await loader(key)
            return self._cache[key]
""")
    return snippets


# ── 10. Testing ───────────────────────────────────────────────────────────────

def gen_tests():
    snippets = []
    for _ in range(20):
        snippets.append("""import pytest


def test_fibonacci_base_cases():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1


def test_fibonacci_sequence():
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert [fibonacci(i) for i in range(10)] == expected


def test_fibonacci_large():
    assert fibonacci(50) == 12586269025
""")
        snippets.append("""import pytest


def test_reverse_string():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"
    assert reverse_string("racecar") == "racecar"


def test_reverse_string_unicode():
    assert reverse_string("café") == "éfac"
""")
        snippets.append("""import pytest


@pytest.fixture
def sample_list():
    return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]


def test_sort_returns_sorted(sample_list):
    result = bubble_sort(sample_list)
    assert result == sorted(sample_list)


def test_sort_does_not_mutate(sample_list):
    original = sample_list[:]
    bubble_sort(sample_list)
    assert sample_list == original
""")
        snippets.append("""import pytest


class TestStack:
    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_empty_pop_raises(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.pop()

    def test_len(self):
        s = Stack()
        assert len(s) == 0
        s.push(42)
        assert len(s) == 1
""")
        snippets.append("""import pytest
from unittest.mock import patch, MagicMock


def test_api_call_success():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"key": "value"}
        result = fetch_from_api("https://example.com/data")
        assert result == {"key": "value"}


def test_api_call_failure():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        with pytest.raises(ValueError):
            fetch_from_api("https://example.com/missing")
""")
    return snippets


# ── 11. Type annotations ──────────────────────────────────────────────────────

def gen_typed():
    snippets = []
    for _ in range(20):
        snippets.append("""from typing import Optional, List, Dict, TypeVar, Generic

T = TypeVar("T")


class Maybe(Generic[T]):
    def __init__(self, value: Optional[T]):
        self._value = value

    @classmethod
    def just(cls, value: T) -> 'Maybe[T]':
        return cls(value)

    @classmethod
    def nothing(cls) -> 'Maybe[T]':
        return cls(None)

    def map(self, func) -> 'Maybe':
        if self._value is None:
            return Maybe.nothing()
        return Maybe.just(func(self._value))

    def get_or(self, default: T) -> T:
        return self._value if self._value is not None else default
""")
        snippets.append("""from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    def area(self) -> float: ...


@runtime_checkable
class Resizable(Protocol):
    def resize(self, factor: float) -> None: ...


class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(r={self.radius})"

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def resize(self, factor: float) -> None:
        self.radius *= factor
""")
        snippets.append("""from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    allowed_hosts: List[str] = field(default_factory=list)
    secret_key: Optional[str] = None

    def __post_init__(self):
        if self.port < 0 or self.port > 65535:
            raise ValueError(f"Invalid port: {self.port}")
        if not self.allowed_hosts:
            self.allowed_hosts = [self.host]
""")
    return snippets


# ── 12. File I/O patterns ─────────────────────────────────────────────────────

def gen_file_io():
    snippets = []
    for _ in range(15):
        snippets.append("""import csv
from pathlib import Path


def read_csv(path: str) -> list:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return rows


def write_csv(path: str, rows: list, fieldnames: list = None) -> None:
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
""")
        snippets.append("""import json
from pathlib import Path
from typing import Any


class JSONStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self._data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            return json.loads(self.path.read_text(encoding="utf-8"))
        return {}

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
""")
        snippets.append("""import pickle
from pathlib import Path


def save_object(obj, path: str) -> None:
    Path(path).write_bytes(pickle.dumps(obj))


def load_object(path: str):
    return pickle.loads(Path(path).read_bytes())
""")
    return snippets


# ── 13. Regex ─────────────────────────────────────────────────────────────────

def gen_regex():
    snippets = []
    for _ in range(15):
        snippets.append("""import re


EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}")
URL_RE = re.compile(r"https?://[^\\s]+")
PHONE_RE = re.compile(r"\\+?[0-9][\\s\\-\\(\\)0-9]{7,15}")


def extract_emails(text: str) -> list:
    return EMAIL_RE.findall(text)


def extract_urls(text: str) -> list:
    return URL_RE.findall(text)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_RE.fullmatch(email))
""")
        snippets.append("""import re


def snake_to_camel(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def camel_to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\\1_\\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\\1_\\2", s1).lower()


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\\w\\s-]", "", text)
    text = re.sub(r"[\\s_-]+", "-", text)
    return re.sub(r"^-+|-+$", "", text)
""")
    return snippets


# ── 14. Design patterns ───────────────────────────────────────────────────────

def gen_patterns():
    snippets = []

    snippets.append("""class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.value = None
""")

    snippets.append("""class EventEmitter:
    def __init__(self):
        self._listeners = {}

    def on(self, event: str, callback):
        self._listeners.setdefault(event, []).append(callback)

    def off(self, event: str, callback):
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args, **kwargs):
        for cb in self._listeners.get(event, []):
            cb(*args, **kwargs)
""")

    snippets.append("""class Observable:
    def __init__(self):
        self._observers = []
        self._state = None

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self._state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.notify()
""")

    snippets.append("""class Builder:
    def __init__(self):
        self._config = {}

    def set(self, key, value):
        self._config[key] = value
        return self  # fluent interface

    def build(self):
        return dict(self._config)


class QueryBuilder:
    def __init__(self, table):
        self._table = table
        self._conditions = []
        self._columns = ["*"]
        self._limit = None

    def select(self, *columns):
        self._columns = list(columns)
        return self

    def where(self, condition):
        self._conditions.append(condition)
        return self

    def limit(self, n):
        self._limit = n
        return self

    def build(self):
        sql = f"SELECT {', '.join(self._columns)} FROM {self._table}"
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        if self._limit:
            sql += f" LIMIT {self._limit}"
        return sql
""")

    return snippets


# ── 15. Larger programs ───────────────────────────────────────────────────────

def gen_programs():
    snippets = []

    snippets.append("""#!/usr/bin/env python3
\"\"\"Word frequency counter.\"\"\"
import sys
import re
from collections import Counter
from pathlib import Path


def count_words(text: str) -> Counter:
    words = re.findall(r"\\b[a-z]+\\b", text.lower())
    return Counter(words)


def main():
    if len(sys.argv) < 2:
        text = sys.stdin.read()
    else:
        text = Path(sys.argv[1]).read_text()

    freq = count_words(text)
    for word, count in freq.most_common(20):
        print(f"{count:6d}  {word}")


if __name__ == "__main__":
    main()
""")

    snippets.append("""#!/usr/bin/env python3
\"\"\"Simple key-value store backed by a JSON file.\"\"\"
import json
import sys
from pathlib import Path

DB_FILE = Path("store.json")


def load():
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text())
    return {}


def save(data):
    DB_FILE.write_text(json.dumps(data, indent=2))


def main():
    data = load()
    if len(sys.argv) < 2:
        print("Usage: store.py get <key> | set <key> <value> | del <key> | list")
        return
    cmd = sys.argv[1]
    if cmd == "get":
        print(data.get(sys.argv[2], "(not found)"))
    elif cmd == "set":
        data[sys.argv[2]] = sys.argv[3]
        save(data)
    elif cmd == "del":
        data.pop(sys.argv[2], None)
        save(data)
    elif cmd == "list":
        for k, v in data.items():
            print(f"{k} = {v}")


if __name__ == "__main__":
    main()
""")

    snippets.append("""#!/usr/bin/env python3
\"\"\"A simple task manager.\"\"\"
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class TaskManager:
    def __init__(self, path: str = "tasks.json"):
        self.path = Path(path)
        self.tasks = self._load()

    def _load(self):
        if self.path.exists():
            data = json.loads(self.path.read_text())
            return [Task(**t) for t in data]
        return []

    def _save(self):
        self.path.write_text(json.dumps([asdict(t) for t in self.tasks], indent=2))

    def add(self, title: str) -> Task:
        task_id = max((t.id for t in self.tasks), default=0) + 1
        task = Task(id=task_id, title=title)
        self.tasks.append(task)
        self._save()
        return task

    def complete(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.done = True
                self._save()
                return True
        return False

    def list_pending(self):
        return [t for t in self.tasks if not t.done]

    def list_all(self):
        return list(self.tasks)
""")

    return snippets


# ── assemble ──────────────────────────────────────────────────────────────────

all_snippets = (
    gen_functions() +
    gen_classes() +
    gen_context_managers() +
    gen_decorators() +
    gen_generators() +
    gen_error_handling() +
    gen_comprehensions() +
    gen_stdlib() +
    gen_async() +
    gen_tests() +
    gen_typed() +
    gen_file_io() +
    gen_regex() +
    gen_patterns() +
    gen_programs()
)

# shuffle so patterns are spread out during training
random.shuffle(all_snippets)

# unique snippets only (loops with constant bodies emit identical text)
all_snippets = [x for x in dict.fromkeys(all_snippets) if x.strip()]

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n\x0c\n".join(all_snippets) + "\n")

import os
size = os.path.getsize(OUT)
print(f"Wrote {len(all_snippets)} unique snippets -> {OUT}  ({size/1024/1024:.2f} MB)", file=sys.stderr)
