"""Expand silicat_chat.jsonl to ~2500 examples.

Targets the gaps identified in testing:
  - fibonacci / recursion (8+ phrasings)
  - context managers / with statement (8+ phrasings)
  - generators (8+ more phrasings)
  - sorting dict by value (8+ phrasings)
  - decorators (more phrasings)
  - new topics: f-strings, pathlib, dataclasses, typing, async, regex, comprehensions,
    argparse, logging, itertools, functools, sets, namedtuple, slots
"""
import sys as _sys

if "--force-append" not in _sys.argv:
    raise SystemExit("legacy one-shot generator, already applied to data/silicat_chat.jsonl (see data/legacy/README.md); pass --force-append to run it again")
from __future__ import annotations
import json
from pathlib import Path

PATH = Path("data/silicat_chat.jsonl")


def st(user: str, silicat: str) -> dict:
    return {"messages": [{"role": "user", "content": user}, {"role": "silicat", "content": silicat}]}


def mt(*pairs: tuple[str, str]) -> dict:
    msgs = []
    for role, content in pairs:
        msgs.append({"role": role, "content": content})
    return {"messages": msgs}


FIB_CODE = """```python
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
```"""

FIB_ITER = """```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```"""

CTX_CODE = """```python
with open("file.txt") as f:
    data = f.read()
```"""

CTX_CUSTOM = """```python
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield
    print(f"elapsed: {time.time() - start:.2f}s")

with timer():
    result = sum(range(1_000_000))
```"""

GEN_CODE = """```python
def gen_squares(n):
    for i in range(n):
        yield i * i

for sq in gen_squares(5):
    print(sq)
```"""

SORT_DICT = """```python
d = {"alice": 90, "bob": 75, "carol": 85}
by_value = dict(sorted(d.items(), key=lambda x: x[1]))
# or just a sorted list of tuples:
top = sorted(d.items(), key=lambda x: x[1], reverse=True)
```"""

EXAMPLES: list[dict] = [

    # ── FIBONACCI ────────────────────────────────────────────────────────────
    st("write a fibonacci function in python", FIB_CODE),
    st("fibonacci sequence python", FIB_CODE),
    st("how do i compute fibonacci in python", FIB_CODE),
    st("python fibonacci recursive", FIB_CODE),
    st("code for fibonacci numbers", FIB_CODE),
    st("fibonacci python code", FIB_CODE),
    st("write fibonacci", FIB_CODE),
    st("fibonacci number python", FIB_CODE),
    st("iterative fibonacci python", FIB_ITER),
    st("fast fibonacci python", FIB_ITER),
    st("write an iterative fibonacci function", FIB_ITER),

    # ── CONTEXT MANAGERS ─────────────────────────────────────────────────────
    st("how do i use a context manager in python", CTX_CODE),
    st("what is a context manager", "A context manager runs setup before `with` and teardown after it. Most common use:\n" + CTX_CODE),
    st("context manager python", CTX_CODE),
    st("python with statement example", CTX_CODE),
    st("how does the with statement work", "Python calls `__enter__` at the start of the block and `__exit__` at the end — even if an exception occurs.\n" + CTX_CODE),
    st("write a custom context manager", CTX_CUSTOM),
    st("how to make a context manager", CTX_CUSTOM),
    st("contextmanager decorator example", CTX_CUSTOM),
    st("python with open file", CTX_CODE),
    st("how to open a file safely in python", CTX_CODE),

    # ── GENERATORS (extra phrasings) ─────────────────────────────────────────
    st("what does yield do in python", "A generator is a function that yields values lazily instead of returning a list. Each `yield` pauses the function; the next call resumes it.\n\n" + GEN_CODE),
    st("how do generators work in python", "A generator is a function that yields values lazily instead of returning a list. Each `yield` pauses the function; the next call resumes it.\n\n" + GEN_CODE),
    st("write a python generator", GEN_CODE),
    st("python generator example", GEN_CODE),
    st("yield keyword python", GEN_CODE),
    st("lazy iteration python", GEN_CODE),
    st("infinite generator python", """```python
def counter(start=0):
    n = start
    while True:
        yield n
        n += 1
```"""),

    # ── SORTING DICT BY VALUE ─────────────────────────────────────────────────
    st("how do i sort a dictionary by value in python", SORT_DICT),
    st("sort dict by value python", SORT_DICT),
    st("python sort dictionary", SORT_DICT),
    st("order a dict by value", SORT_DICT),
    st("sort a python dict", SORT_DICT),
    st("dictionary sorted by value", SORT_DICT),
    st("how to sort dict values", SORT_DICT),
    st("python sort dict by value descending", """```python
d = {"alice": 90, "bob": 75, "carol": 85}
top = sorted(d.items(), key=lambda x: x[1], reverse=True)
print(top)  # [('alice', 90), ('carol', 85), ('bob', 75)]
```"""),

    # ── DECORATOR (more phrasings) ────────────────────────────────────────────
    st("show me a python decorator", """```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@my_decorator
def greet(name):
    return f"Hello, {name}!"
```"""),
    st("what is a decorator in python", "A decorator is a function that wraps another function to add behaviour without modifying the original.\n\n```python\nimport functools\n\ndef log(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f'calling {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n\n@log\ndef add(a, b):\n    return a + b\n```"),
    st("python decorator tutorial", """```python
import functools

def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("hi")

say_hi()  # prints "hi" three times
```"""),

    # ── F-STRINGS ─────────────────────────────────────────────────────────────
    st("how do i use f-strings in python", "F-strings let you embed expressions directly in string literals:\n\n```python\nname = 'Alice'\nage = 30\nprint(f'My name is {name} and I am {age} years old.')\nprint(f'2 + 2 = {2 + 2}')\nprint(f'Pi is approximately {3.14159:.2f}')\n```"),
    st("python f string example", "```python\nname = 'world'\nprint(f'Hello, {name}!')\nvalue = 3.14159\nprint(f'{value:.2f}')  # '3.14'\n```"),
    st("string formatting python", "```python\n# f-string (recommended, Python 3.6+)\nname = 'Alice'\nprint(f'Hello, {name}!')\n\n# format() method\nprint('Hello, {}!'.format(name))\n\n# % operator (old style)\nprint('Hello, %s!' % name)\n```"),
    st("format a float python", "```python\npi = 3.14159265\nprint(f'{pi:.2f}')   # '3.14'\nprint(f'{pi:.4f}')   # '3.1416'\nprint(f'{pi:10.3f}') # '     3.142' (width 10)\n```"),
    st("how to format numbers in python", "```python\nn = 1234567\nprint(f'{n:,}')      # '1,234,567'\nprint(f'{n:010}')    # '0001234567'\nprint(f'{n:#x}')     # '0x12d687' (hex)\nprint(f'{n:b}')      # binary\n```"),

    # ── PATHLIB ───────────────────────────────────────────────────────────────
    st("how do i use pathlib in python", "```python\nfrom pathlib import Path\n\np = Path('data/file.txt')\nprint(p.name)      # 'file.txt'\nprint(p.stem)      # 'file'\nprint(p.suffix)    # '.txt'\nprint(p.parent)    # Path('data')\n\n# Read / write\ntext = p.read_text()\np.write_text('hello')\n\n# List files\nfor f in Path('.').glob('*.py'):\n    print(f)\n```"),
    st("python path manipulation", "```python\nfrom pathlib import Path\n\nbase = Path('/home/user/project')\nfile = base / 'data' / 'input.txt'  # path joining\nfile.parent.mkdir(parents=True, exist_ok=True)\nfile.write_text('data')\nprint(file.exists())   # True\nprint(file.stat().st_size)\n```"),
    st("list files in directory python", "```python\nfrom pathlib import Path\n\n# All .py files recursively\nfor f in Path('.').rglob('*.py'):\n    print(f)\n\n# Direct children only\nfor f in Path('.').iterdir():\n    if f.is_file():\n        print(f)\n```"),

    # ── DATACLASSES ───────────────────────────────────────────────────────────
    st("how do i use dataclasses in python", "```python\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass Point:\n    x: float\n    y: float\n    label: str = ''\n\n    def distance(self) -> float:\n        return (self.x**2 + self.y**2)**0.5\n\np = Point(3.0, 4.0)\nprint(p)              # Point(x=3.0, y=4.0, label='')\nprint(p.distance())   # 5.0\n```"),
    st("python dataclass example", "```python\nfrom dataclasses import dataclass\n\n@dataclass\nclass User:\n    name: str\n    age: int\n    email: str = ''\n\nu = User('Alice', 30, 'alice@example.com')\nprint(u.name)   # Alice\n```"),
    st("frozen dataclass python", "```python\nfrom dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Config:\n    host: str\n    port: int = 8080\n\ncfg = Config('localhost')\n# cfg.port = 9000  # raises FrozenInstanceError\nprint(cfg)  # Config(host='localhost', port=8080)\n```"),

    # ── TYPING / TYPE HINTS ───────────────────────────────────────────────────
    st("how do i add type hints in python", "```python\nfrom typing import Optional, Union\n\ndef greet(name: str, times: int = 1) -> str:\n    return (f'Hello, {name}! ' * times).strip()\n\ndef find(items: list[int], target: int) -> Optional[int]:\n    for i, x in enumerate(items):\n        if x == target:\n            return i\n    return None\n```"),
    st("python type annotations", "```python\ndef add(a: int, b: int) -> int:\n    return a + b\n\ndef process(data: list[str]) -> dict[str, int]:\n    return {s: len(s) for s in data}\n\n# Optional value\nfrom typing import Optional\ndef first(lst: list[int]) -> Optional[int]:\n    return lst[0] if lst else None\n```"),
    st("what are type hints for in python", "Type hints let you annotate variables and function signatures with expected types. Python doesn't enforce them at runtime, but tools like `mypy` use them to catch bugs:\n\n```python\ndef divide(a: float, b: float) -> float:\n    return a / b\n```\n\nRun `mypy script.py` to check for type errors."),

    # ── ASYNC / AWAIT ─────────────────────────────────────────────────────────
    st("how do i use async await in python", "```python\nimport asyncio\n\nasync def fetch(url: str) -> str:\n    await asyncio.sleep(1)  # simulates I/O\n    return f'data from {url}'\n\nasync def main():\n    result = await fetch('https://example.com')\n    print(result)\n\nasyncio.run(main())\n```"),
    st("python async example", "```python\nimport asyncio\n\nasync def greet(name: str) -> None:\n    await asyncio.sleep(0.1)\n    print(f'Hello, {name}!')\n\nasync def main():\n    # Run concurrently\n    await asyncio.gather(\n        greet('Alice'),\n        greet('Bob'),\n        greet('Carol'),\n    )\n\nasyncio.run(main())\n```"),
    st("asyncio gather python", "```python\nimport asyncio\n\nasync def task(n: int) -> int:\n    await asyncio.sleep(n * 0.1)\n    return n * 2\n\nasync def main():\n    results = await asyncio.gather(task(1), task(2), task(3))\n    print(results)  # [2, 4, 6]\n\nasyncio.run(main())\n```"),

    # ── REGEX ─────────────────────────────────────────────────────────────────
    st("how do i use regex in python", "```python\nimport re\n\ntext = 'Contact: alice@example.com or bob@test.org'\n\n# Search for a pattern\nm = re.search(r'\\w+@\\w+\\.\\w+', text)\nif m:\n    print(m.group())  # 'alice@example.com'\n\n# Find all matches\nemails = re.findall(r'\\w+@\\w+\\.\\w+', text)\nprint(emails)  # ['alice@example.com', 'bob@test.org']\n\n# Substitute\ncleaned = re.sub(r'\\s+', ' ', 'too  many   spaces')\n```"),
    st("python regex example", "```python\nimport re\n\n# Match digits\nn = re.findall(r'\\d+', 'abc123def456')\nprint(n)  # ['123', '456']\n\n# Groups\nm = re.match(r'(\\w+)\\s(\\w+)', 'John Doe')\nif m:\n    print(m.group(1), m.group(2))  # John  Doe\n\n# Compile for reuse\npattern = re.compile(r'\\b\\w{5}\\b')  # 5-letter words\n```"),

    # ── COMPREHENSIONS (dict/set) ─────────────────────────────────────────────
    st("how do i write a dict comprehension", "```python\n# Map each word to its length\nwords = ['apple', 'banana', 'cherry']\nlengths = {w: len(w) for w in words}\n# {'apple': 5, 'banana': 6, 'cherry': 6}\n\n# Filter and transform\nsquares = {x: x**2 for x in range(10) if x % 2 == 0}\n```"),
    st("python set comprehension", "```python\nwords = ['apple', 'banana', 'apple', 'cherry']\nunique_first_letters = {w[0] for w in words}\n# {'a', 'b', 'c'}\n\n# Only even squares\nevens = {x**2 for x in range(10) if x % 2 == 0}\n```"),
    st("dict comprehension python", "```python\n# Invert a dict\noriginal = {'a': 1, 'b': 2, 'c': 3}\ninverted = {v: k for k, v in original.items()}\n# {1: 'a', 2: 'b', 3: 'c'}\n```"),

    # ── ARGPARSE ──────────────────────────────────────────────────────────────
    st("how do i parse command line arguments in python", "```python\nimport argparse\n\np = argparse.ArgumentParser(description='My CLI tool')\np.add_argument('name', help='Your name')\np.add_argument('--count', type=int, default=1)\np.add_argument('--verbose', action='store_true')\nargs = p.parse_args()\n\nfor _ in range(args.count):\n    print(f'Hello, {args.name}!')\n```"),
    st("python argparse example", "```python\nimport argparse\n\nparser = argparse.ArgumentParser()\nparser.add_argument('--input', required=True)\nparser.add_argument('--output', default='out.txt')\nparser.add_argument('--workers', type=int, default=4)\nargs = parser.parse_args()\nprint(args.input, args.output, args.workers)\n```"),

    # ── LOGGING ───────────────────────────────────────────────────────────────
    st("how do i use logging in python", "```python\nimport logging\n\nlogging.basicConfig(level=logging.INFO,\n                    format='%(asctime)s %(levelname)s %(message)s')\nlog = logging.getLogger(__name__)\n\nlog.info('starting up')\nlog.warning('disk space low')\nlog.error('connection failed')\n```"),
    st("python logging example", "```python\nimport logging\n\nlogging.basicConfig(\n    level=logging.DEBUG,\n    format='%(levelname)s: %(message)s'\n)\n\nlogging.debug('debug info')\nlogging.info('process started')\nlogging.warning('something odd')\nlogging.error('an error occurred')\n```"),

    # ── ITERTOOLS ─────────────────────────────────────────────────────────────
    st("how do i use itertools in python", "```python\nimport itertools\n\n# chain — flatten iterables\nfor x in itertools.chain([1, 2], [3, 4], [5]):\n    print(x)  # 1 2 3 4 5\n\n# combinations\nfor combo in itertools.combinations('ABC', 2):\n    print(combo)  # ('A','B'), ('A','C'), ('B','C')\n\n# groupby\ndata = [('a', 1), ('a', 2), ('b', 3)]\nfor key, grp in itertools.groupby(data, key=lambda x: x[0]):\n    print(key, list(grp))\n```"),

    # ── FUNCTOOLS ─────────────────────────────────────────────────────────────
    st("how do i use functools in python", "```python\nimport functools\n\n# lru_cache — memoize expensive calls\n@functools.lru_cache(maxsize=128)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n-1) + fib(n-2)\n\n# partial — pre-fill arguments\ndouble = functools.partial(pow, exp=2)\nprint(double(5))  # 25\n\n# reduce\ntotal = functools.reduce(lambda a, b: a + b, range(1, 6))  # 15\n```"),

    # ── SETS ──────────────────────────────────────────────────────────────────
    st("how do i use sets in python", "```python\na = {1, 2, 3, 4}\nb = {3, 4, 5, 6}\n\nprint(a | b)   # union:        {1,2,3,4,5,6}\nprint(a & b)   # intersection: {3,4}\nprint(a - b)   # difference:   {1,2}\nprint(a ^ b)   # symmetric:    {1,2,5,6}\n\n# Membership test is O(1)\nprint(3 in a)  # True\n```"),
    st("python set operations", "```python\ns = {1, 2, 3}\ns.add(4)\ns.discard(2)  # no error if missing\nprint(s)  # {1, 3, 4}\n\n# Remove duplicates from a list\nuniq = list(set([1, 2, 2, 3, 3, 3]))\n```"),

    # ── SLOTS ─────────────────────────────────────────────────────────────────
    st("what are __slots__ in python", "```python\nclass Point:\n    __slots__ = ('x', 'y')  # restricts attributes, saves memory\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\np = Point(1, 2)\n# p.z = 3  # AttributeError — only x, y allowed\n```"),

    # ── NAMEDTUPLE ────────────────────────────────────────────────────────────
    st("how do i use namedtuple in python", "```python\nfrom collections import namedtuple\n\nPoint = namedtuple('Point', ['x', 'y'])\np = Point(3, 4)\nprint(p.x, p.y)  # 3 4\nprint(p)         # Point(x=3, y=4)\n\n# Unpack like a tuple\nx, y = p\n```"),

    # ── ENUMERATE / ZIP ───────────────────────────────────────────────────────
    st("how do i use enumerate in python", "```python\nfruits = ['apple', 'banana', 'cherry']\nfor i, fruit in enumerate(fruits):\n    print(i, fruit)\n# 0 apple\n# 1 banana\n# 2 cherry\n\n# Start from 1\nfor i, fruit in enumerate(fruits, start=1):\n    print(i, fruit)\n```"),
    st("python zip example", "```python\nnames = ['Alice', 'Bob', 'Carol']\nscores = [90, 75, 85]\n\nfor name, score in zip(names, scores):\n    print(f'{name}: {score}')\n\n# Create a dict from two lists\nresult = dict(zip(names, scores))\n# {'Alice': 90, 'Bob': 75, 'Carol': 85}\n```"),

    # ── MAP / FILTER ──────────────────────────────────────────────────────────
    st("how do i use map and filter in python", "```python\nnumbers = [1, 2, 3, 4, 5, 6]\n\n# map: apply a function to each element\nsquares = list(map(lambda x: x**2, numbers))\n# [1, 4, 9, 16, 25, 36]\n\n# filter: keep elements where condition is True\nevens = list(filter(lambda x: x % 2 == 0, numbers))\n# [2, 4, 6]\n\n# Python style: list comprehensions are usually clearer\nsquares = [x**2 for x in numbers]\nevens = [x for x in numbers if x % 2 == 0]\n```"),

    # ── LAMBDA ────────────────────────────────────────────────────────────────
    st("what is a lambda in python", "A lambda is an anonymous one-line function:\n\n```python\nsquare = lambda x: x**2\nprint(square(5))  # 25\n\n# Common use: sorting\npeople = [{'name': 'Bob', 'age': 30}, {'name': 'Alice', 'age': 25}]\npeople.sort(key=lambda p: p['age'])\n```"),
    st("python lambda function", "```python\nadd = lambda a, b: a + b\nprint(add(3, 4))  # 7\n\n# Inline in sorted()\nwords = ['banana', 'apple', 'cherry']\nwords.sort(key=lambda w: len(w))\nprint(words)  # ['apple', 'banana', 'cherry']\n```"),

    # ── MORE ALGORITHMS ───────────────────────────────────────────────────────
    st("how do i implement merge sort in python", "```python\ndef merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i]); i += 1\n        else:\n            result.append(right[j]); j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result\n```"),
    st("how do i check if a number is prime", "```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nprimes = [x for x in range(2, 50) if is_prime(x)]\n```"),
    st("depth first search python", "```python\ndef dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    print(start)\n    for neighbor in graph.get(start, []):\n        if neighbor not in visited:\n            dfs(graph, neighbor, visited)\n\ngraph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}\ndfs(graph, 'A')\n```"),
    st("breadth first search python", "```python\nfrom collections import deque\n\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    while queue:\n        node = queue.popleft()\n        print(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n```"),
    st("how do i implement a stack in python", "```python\nstack = []\nstack.append(1)\nstack.append(2)\nstack.append(3)\nprint(stack.pop())  # 3 (LIFO)\nprint(stack)        # [1, 2]\n```"),
    st("how do i implement a queue in python", "```python\nfrom collections import deque\n\nqueue = deque()\nqueue.append(1)\nqueue.append(2)\nqueue.append(3)\nprint(queue.popleft())  # 1 (FIFO)\nprint(queue)            # deque([2, 3])\n```"),

    # ── FILE OPERATIONS ───────────────────────────────────────────────────────
    st("how do i write to a file in python", "```python\nwith open('output.txt', 'w', encoding='utf-8') as f:\n    f.write('Hello, world!\\n')\n    f.write('Second line\\n')\n\n# Append mode\nwith open('output.txt', 'a') as f:\n    f.write('Third line\\n')\n```"),
    st("read a csv file python", "```python\nimport csv\n\nwith open('data.csv', newline='') as f:\n    reader = csv.DictReader(f)\n    for row in reader:\n        print(row['name'], row['age'])\n```"),
    st("write a json file python", "```python\nimport json\n\ndata = {'name': 'Alice', 'scores': [90, 85, 92]}\n\nwith open('data.json', 'w') as f:\n    json.dump(data, f, indent=2)\n\n# Read back\nwith open('data.json') as f:\n    loaded = json.load(f)\nprint(loaded['name'])  # Alice\n```"),

    # ── CLASS / OOP ───────────────────────────────────────────────────────────
    st("how do i write a class in python", "```python\nclass Animal:\n    def __init__(self, name, sound):\n        self.name = name\n        self.sound = sound\n\n    def speak(self):\n        return f'{self.name} says {self.sound}'\n\nclass Dog(Animal):\n    def fetch(self):\n        return f'{self.name} fetches the ball!'\n\ndog = Dog('Rex', 'woof')\nprint(dog.speak())   # Rex says woof\nprint(dog.fetch())   # Rex fetches the ball!\n```"),
    st("python inheritance example", "```python\nclass Shape:\n    def area(self) -> float:\n        raise NotImplementedError\n\nclass Circle(Shape):\n    def __init__(self, radius: float):\n        self.radius = radius\n\n    def area(self) -> float:\n        import math\n        return math.pi * self.radius ** 2\n\nclass Rectangle(Shape):\n    def __init__(self, w: float, h: float):\n        self.w, self.h = w, h\n\n    def area(self) -> float:\n        return self.w * self.h\n```"),

    # ── EXCEPTIONS ─────────────────────────────────────────────────────────────
    st("how do i raise a custom exception", "```python\nclass ValidationError(ValueError):\n    pass\n\ndef validate_age(age):\n    if age < 0 or age > 150:\n        raise ValidationError(f'Invalid age: {age}')\n    return age\n\ntry:\n    validate_age(-5)\nexcept ValidationError as e:\n    print(f'Error: {e}')\n```"),

    # ── UNIT TESTING ──────────────────────────────────────────────────────────
    st("how do i write unit tests in python", "```python\nimport unittest\n\ndef add(a, b):\n    return a + b\n\nclass TestAdd(unittest.TestCase):\n    def test_positive(self):\n        self.assertEqual(add(2, 3), 5)\n\n    def test_negative(self):\n        self.assertEqual(add(-1, 1), 0)\n\n    def test_zero(self):\n        self.assertEqual(add(0, 0), 0)\n\nif __name__ == '__main__':\n    unittest.main()\n```"),
    st("python pytest example", "```python\ndef add(a, b):\n    return a + b\n\ndef test_add():\n    assert add(2, 3) == 5\n\ndef test_add_negative():\n    assert add(-1, 1) == 0\n```\n\nRun with: `pytest test_math.py`"),

    # ── GENERAL CHAT / CONCEPTS ───────────────────────────────────────────────
    st("what is the difference between a list and a tuple in python", "Lists are mutable (`[1,2,3]`) — you can add, remove, or change elements. Tuples are immutable (`(1,2,3)`) — you cannot. Use tuples for fixed records and as dict keys; use lists for collections you'll modify."),
    st("what is the difference between is and == in python", "`==` checks value equality. `is` checks identity (same object in memory).\n\n```python\na = [1, 2, 3]\nb = [1, 2, 3]\nprint(a == b)   # True  (same values)\nprint(a is b)   # False (different objects)\n\nx = None\nprint(x is None)  # True — correct way to check for None\n```"),
    st("how does python handle memory management", "Python uses reference counting plus a cyclic garbage collector. When an object's reference count drops to zero, it's freed immediately. `gc` module handles cycles. You rarely need to manage memory manually:\n\n```python\nimport gc\ngc.collect()  # force a garbage collection cycle\n```"),
    st("what is *args and **kwargs", "```python\ndef func(*args, **kwargs):\n    print(args)   # tuple of positional args\n    print(kwargs) # dict of keyword args\n\nfunc(1, 2, 3, name='Alice', age=30)\n# (1, 2, 3)\n# {'name': 'Alice', 'age': 30}\n```"),
    st("how do i unpack a list in python", "```python\na, b, c = [1, 2, 3]\nprint(a, b, c)  # 1 2 3\n\n# Star unpacking\nfirst, *rest = [1, 2, 3, 4, 5]\nprint(first)  # 1\nprint(rest)   # [2, 3, 4, 5]\n\n# Spread into a function\ndef add(x, y, z): return x + y + z\nargs = [1, 2, 3]\nprint(add(*args))  # 6\n```"),

    # ── MULTI-TURN CONVERSATIONS ──────────────────────────────────────────────
    mt(
        ("user", "how do i sort a list of dictionaries by a key"),
        ("silicat", "```python\npeople = [\n    {'name': 'Bob', 'age': 30},\n    {'name': 'Alice', 'age': 25},\n    {'name': 'Carol', 'age': 35},\n]\npeople.sort(key=lambda p: p['age'])\nprint(people)\n```"),
        ("user", "how do i sort it descending"),
        ("silicat", "Add `reverse=True`:\n\n```python\npeople.sort(key=lambda p: p['age'], reverse=True)\n```"),
    ),
    mt(
        ("user", "write a fibonacci function"),
        ("silicat", FIB_CODE),
        ("user", "make it iterative"),
        ("silicat", FIB_ITER),
        ("user", "now add memoization to the recursive version"),
        ("silicat", "```python\nimport functools\n\n@functools.lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n```"),
    ),
    mt(
        ("user", "how do i use a context manager"),
        ("silicat", CTX_CODE),
        ("user", "how do i write my own"),
        ("silicat", CTX_CUSTOM),
        ("user", "can i use a class instead"),
        ("silicat", "```python\nclass Timer:\n    def __enter__(self):\n        import time\n        self.start = time.time()\n        return self\n\n    def __exit__(self, *args):\n        print(f'elapsed: {time.time() - self.start:.2f}s')\n\nwith Timer() as t:\n    result = sum(range(1_000_000))\n```"),
    ),
    mt(
        ("user", "what is a generator"),
        ("silicat", "A generator is a function that yields values lazily instead of returning a list. Each `yield` pauses the function; the next call resumes it.\n\n" + GEN_CODE),
        ("user", "how is that different from a list comprehension"),
        ("silicat", "A list comprehension builds the entire list in memory at once. A generator computes one value at a time — much more memory-efficient for large sequences:\n\n```python\n# List: all 1M numbers in memory\nbig_list = [x**2 for x in range(1_000_000)]\n\n# Generator: one number at a time\nbig_gen = (x**2 for x in range(1_000_000))\n```"),
    ),
    mt(
        ("user", "how do i parse command line args in python"),
        ("silicat", "```python\nimport argparse\n\np = argparse.ArgumentParser()\np.add_argument('--name', required=True)\np.add_argument('--count', type=int, default=1)\nargs = p.parse_args()\n\nfor _ in range(args.count):\n    print(f'Hello, {args.name}!')\n```"),
        ("user", "how do i add a positional argument"),
        ("silicat", "```python\np.add_argument('filename')       # required positional\np.add_argument('output', nargs='?', default='out.txt')  # optional\n```\n\nPositional args have no `--` prefix and are required unless `nargs='?'` is set."),
    ),
]


def main() -> None:
    existing = PATH.read_text(encoding="utf-8") if PATH.exists() else ""
    start_count = existing.count("\n") if existing else 0

    with PATH.open("a", encoding="utf-8") as f:
        for ex in EXAMPLES:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    total = start_count + len(EXAMPLES)
    print(f"Added {len(EXAMPLES)} examples. Total lines now: ~{total}")


if __name__ == "__main__":
    main()
