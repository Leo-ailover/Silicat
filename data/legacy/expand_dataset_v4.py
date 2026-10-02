"""Massive dataset v4 — target 5000+ total examples for 300M model training."""
import sys as _sys

if "--force-append" not in _sys.argv:
    raise SystemExit("legacy one-shot generator, already applied to data/silicat_chat.jsonl (see data/legacy/README.md); pass --force-append to run it again")
import json
from pathlib import Path

JSONL = Path(__file__).resolve().parents[1] / "silicat_chat.jsonl"


def ex(user, silicat):
    return {"messages": [{"role": "user", "content": user}, {"role": "silicat", "content": silicat}]}


examples = []

# ═══════════════════════════════════════════════════════════════════════════════
# CODE EXPLANATION — "what does this code do"
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("what does this do: x = x[::-1]", "It reverses the sequence `x` using slicing. The `[::-1]` means start from the end, go backwards by 1. Works on strings, lists, and tuples."),
    ex("explain: lst = [x**2 for x in range(10)]", "This is a list comprehension. It builds a list of squares: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]. Equivalent to a for loop that appends `x**2` to a list for each x in 0–9."),
    ex("what does enumerate do", "`enumerate` adds an index to an iterable:\n```python\nfor i, item in enumerate(['a','b','c']):\n    print(i, item)\n# 0 a\n# 1 b\n# 2 c\n```"),
    ex("what does zip do in python", "`zip` pairs up items from multiple iterables:\n```python\nnames  = ['Alice', 'Bob']\nscores = [90, 85]\nfor name, score in zip(names, scores):\n    print(name, score)\n```"),
    ex("what does *args do", "`*args` collects extra positional arguments into a tuple:\n```python\ndef add(*args):\n    return sum(args)\nadd(1, 2, 3)  # 6\n```"),
    ex("explain **kwargs", "`**kwargs` collects extra keyword arguments into a dict:\n```python\ndef show(**kwargs):\n    for k, v in kwargs.items():\n        print(f'{k}={v}')\nshow(name='Alice', age=30)\n```"),
    ex("what is the walrus operator :=", "`:=` assigns a value and returns it in one expression (Python 3.8+):\n```python\nif n := len(data):\n    print(f'got {n} items')\n# Avoids calling len() twice\n```"),
    ex("what does _ mean in python", "In a loop, `_` is a throwaway variable — signals you don't care about the value:\n```python\nfor _ in range(5):\n    do_something()\n```\nIn the REPL, `_` holds the last result."),
    ex("what is pass in python", "`pass` is a no-op placeholder. Use it where Python requires a statement but you have nothing to do yet:\n```python\nclass MyError(Exception):\n    pass\n\ndef todo():\n    pass\n```"),
    ex("what does assert do", "`assert` checks a condition and raises `AssertionError` if it's False:\n```python\nassert x > 0, 'x must be positive'\n```\nUsed for debugging and unit tests. Disabled with `python -O`."),
    ex("what is a lambda in python", "A `lambda` is a small anonymous function:\n```python\nsquare = lambda x: x**2\nsquare(5)  # 25\n\n# Common in sorting:\nitems.sort(key=lambda x: x['price'])\n```"),
    ex("explain list slicing", "Slicing extracts a portion of a list (or string):\n```python\nlst = [0, 1, 2, 3, 4, 5]\nlst[2:5]    # [2, 3, 4]\nlst[:3]     # [0, 1, 2]\nlst[3:]     # [3, 4, 5]\nlst[::2]    # [0, 2, 4] — every 2nd\nlst[::-1]   # [5, 4, 3, 2, 1, 0] — reversed\n```"),
    ex("what is a f-string", "An f-string embeds expressions directly in a string literal:\n```python\nname = 'Alice'\nage  = 30\nprint(f'Hello {name}, you are {age} years old.')\nprint(f'Pi = {3.14159:.2f}')  # format specifiers work too\n```"),
    ex("what does try finally do", "`finally` always runs, whether an exception occurred or not — perfect for cleanup:\n```python\nf = open('file.txt')\ntry:\n    data = f.read()\nexcept IOError:\n    print('read failed')\nfinally:\n    f.close()  # always closes the file\n```"),
    ex("what is a class variable vs instance variable", "Class variables are shared across all instances; instance variables belong to one object:\n```python\nclass Dog:\n    species = 'Canis lupus'  # class variable — shared\n\n    def __init__(self, name):\n        self.name = name     # instance variable — unique\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CODE FIXING / DEBUGGING
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("fix this: for i in range(10) print(i)", "Missing colon after the `for` statement:\n```python\nfor i in range(10):\n    print(i)\n```"),
    ex("fix this: if x = 5: print(x)", "Assignment `=` inside `if` is a SyntaxError. Use `==` for comparison:\n```python\nif x == 5:\n    print(x)\n```"),
    ex("why does my list append not work: lst = lst + [item]", "That creates a new list each time. For in-place append:\n```python\nlst.append(item)\n```\nYour version works but is O(n) — use `append` which is O(1)."),
    ex("my function returns None", "Make sure you have a `return` statement. Common mistake:\n```python\n# Wrong — no return:\ndef double(x):\n    x * 2\n\n# Fixed:\ndef double(x):\n    return x * 2\n```"),
    ex("i get 'list index out of range'", "You're accessing an index that doesn't exist. Check bounds:\n```python\nlst = [1, 2, 3]\n# lst[3]  # IndexError — valid indices are 0, 1, 2\nif i < len(lst):\n    print(lst[i])\n```"),
    ex("i get 'dict object is not subscriptable'", "You're treating something as a dict when it's not. Check the type:\n```python\nprint(type(my_var))  # see what it actually is\n```\nCommon cause: a function returns `None` and you try to index the result."),
    ex("my for loop skips the first item", "You're probably calling `next()` before the loop, consuming the first item. Use `enumerate` or just iterate directly:\n```python\nfor item in my_list:\n    print(item)\n```"),
    ex("why does my function modify the original list", "Lists are mutable and passed by reference. Make a copy inside the function:\n```python\ndef process(lst):\n    lst = lst.copy()  # work on a copy\n    lst.append(99)\n    return lst\n```"),
    ex("integer division gives wrong answer", "Use `/` for float division, `//` for integer division:\n```python\n10 / 3    # 3.333...\n10 // 3   # 3 (floor division)\n```"),
    ex("my string comparison is case sensitive", "Convert both sides to the same case:\n```python\nif name.lower() == 'alice':\n    print('found')\n```"),
    ex("i get an infinite loop", "Your `while` condition never becomes False. Make sure the loop variable changes:\n```python\ni = 0\nwhile i < 10:\n    print(i)\n    i += 1  # don't forget this!\n```"),
    ex("why is my variable undefined inside a function", "Variables inside a function are local by default. Either pass them as arguments or use `global` (not recommended):\n```python\n# Better: pass as argument\ndef greet(name):\n    print(f'Hello {name}')\ngreet('Alice')\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# THREADING / MULTIPROCESSING
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("how do i use threads in python", "```python\nimport threading\n\ndef worker(n):\n    print(f'thread {n} running')\n\nthreads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]\nfor t in threads: t.start()\nfor t in threads: t.join()\n```"),
    ex("what is the GIL in python", "The Global Interpreter Lock (GIL) prevents multiple threads from executing Python bytecode simultaneously. Threads are good for I/O-bound tasks (file reads, network calls) but not CPU-bound work. For CPU parallelism, use `multiprocessing`."),
    ex("how do i use multiprocessing", "```python\nfrom multiprocessing import Pool\n\ndef square(x):\n    return x ** 2\n\nwith Pool(4) as p:\n    results = p.map(square, range(10))\nprint(results)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]\n```"),
    ex("thread safe counter python", "```python\nimport threading\n\nclass Counter:\n    def __init__(self):\n        self._value = 0\n        self._lock = threading.Lock()\n\n    def increment(self):\n        with self._lock:\n            self._value += 1\n\n    @property\n    def value(self):\n        return self._value\n```"),
    ex("how do i run a task in the background", "```python\nimport threading\n\ndef background_task():\n    import time\n    time.sleep(5)\n    print('done')\n\nt = threading.Thread(target=background_task, daemon=True)\nt.start()\nprint('main continues immediately')\n```"),
    ex("what is a thread pool", "A thread pool manages a fixed number of worker threads, reusing them for multiple tasks:\n```python\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef fetch(url):\n    import requests\n    return requests.get(url).status_code\n\nurls = ['https://example.com'] * 10\nwith ThreadPoolExecutor(max_workers=4) as ex:\n    results = list(ex.map(fetch, urls))\n```"),
    ex("multiprocessing vs threading python", "- **Threading**: shares memory, limited by GIL, good for I/O (network, files)\n- **Multiprocessing**: separate processes, bypasses GIL, good for CPU-bound work\n- **asyncio**: single thread, cooperative, best for many concurrent I/O operations"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# NETWORKING / SOCKETS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("simple tcp server python", "```python\nimport socket\n\nserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nserver.bind(('localhost', 9000))\nserver.listen(1)\nprint('waiting for connection...')\nconn, addr = server.accept()\nprint(f'connected: {addr}')\ndata = conn.recv(1024)\nconn.send(b'got: ' + data)\nconn.close()\n```"),
    ex("simple tcp client python", "```python\nimport socket\n\nclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nclient.connect(('localhost', 9000))\nclient.send(b'hello')\nresponse = client.recv(1024)\nprint(response.decode())\nclient.close()\n```"),
    ex("how do i check if a port is open", "```python\nimport socket\n\ndef is_port_open(host, port, timeout=2):\n    try:\n        with socket.create_connection((host, port), timeout=timeout):\n            return True\n    except (socket.timeout, ConnectionRefusedError):\n        return False\n```"),
    ex("udp socket python", "```python\nimport socket\n\n# Sender:\nsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\nsock.sendto(b'hello', ('localhost', 9001))\n\n# Receiver:\nsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\nsock.bind(('localhost', 9001))\ndata, addr = sock.recvfrom(1024)\nprint(data.decode())\n```"),
    ex("get local ip address python", "```python\nimport socket\n\ndef get_local_ip():\n    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:\n        s.connect(('8.8.8.8', 80))\n        return s.getsockname()[0]\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("singleton pattern python", "```python\nclass Singleton:\n    _instance = None\n\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n\na = Singleton()\nb = Singleton()\nassert a is b  # True — same object\n```"),
    ex("observer pattern python", "```python\nclass EventEmitter:\n    def __init__(self):\n        self._listeners = {}\n\n    def on(self, event, fn):\n        self._listeners.setdefault(event, []).append(fn)\n\n    def emit(self, event, *args):\n        for fn in self._listeners.get(event, []):\n            fn(*args)\n\nem = EventEmitter()\nem.on('data', lambda d: print('got:', d))\nem.emit('data', 42)\n```"),
    ex("factory pattern python", "```python\nclass Animal:\n    def speak(self): ...\n\nclass Dog(Animal):\n    def speak(self): return 'woof'\n\nclass Cat(Animal):\n    def speak(self): return 'meow'\n\ndef animal_factory(kind):\n    return {'dog': Dog, 'cat': Cat}[kind]()\n\nanimal = animal_factory('dog')\nprint(animal.speak())\n```"),
    ex("strategy pattern python", "```python\nfrom typing import Callable\n\nclass Sorter:\n    def __init__(self, strategy: Callable):\n        self._strategy = strategy\n\n    def sort(self, data):\n        return self._strategy(data)\n\nsorter = Sorter(sorted)\nsorter.sort([3, 1, 2])  # [1, 2, 3]\n\nsorter = Sorter(lambda d: sorted(d, reverse=True))\nsorter.sort([3, 1, 2])  # [3, 2, 1]\n```"),
    ex("decorator pattern python", "```python\nfrom abc import ABC, abstractmethod\n\nclass Logger(ABC):\n    @abstractmethod\n    def log(self, msg): ...\n\nclass ConsoleLogger(Logger):\n    def log(self, msg): print(msg)\n\nclass TimestampLogger(Logger):\n    def __init__(self, logger):\n        self._logger = logger\n\n    def log(self, msg):\n        import datetime\n        self._logger.log(f'[{datetime.datetime.now():%H:%M:%S}] {msg}')\n\nlogger = TimestampLogger(ConsoleLogger())\nlogger.log('hello')\n```"),
    ex("command pattern python", "```python\nfrom abc import ABC, abstractmethod\n\nclass Command(ABC):\n    @abstractmethod\n    def execute(self): ...\n    @abstractmethod\n    def undo(self): ...\n\nclass AddCommand(Command):\n    def __init__(self, lst, item):\n        self.lst, self.item = lst, item\n\n    def execute(self): self.lst.append(self.item)\n    def undo(self): self.lst.remove(self.item)\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MORE ADVANCED PYTHON
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("how do i serialize a python object", "```python\nimport pickle\n\n# Save:\nwith open('obj.pkl', 'wb') as f:\n    pickle.dump(my_object, f)\n\n# Load:\nwith open('obj.pkl', 'rb') as f:\n    my_object = pickle.load(f)\n```\nWarning: only unpickle data you trust."),
    ex("how do i use abc abstract class", "```python\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self) -> float: ...\n\n    @abstractmethod\n    def perimeter(self) -> float: ...\n\nclass Circle(Shape):\n    def __init__(self, r): self.r = r\n    def area(self): return 3.14159 * self.r**2\n    def perimeter(self): return 2 * 3.14159 * self.r\n```"),
    ex("how do i overload operators", "```python\nclass Vector:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\n    def __mul__(self, scalar):\n        return Vector(self.x * scalar, self.y * scalar)\n\n    def __repr__(self):\n        return f'Vector({self.x}, {self.y})'\n\nv = Vector(1, 2) + Vector(3, 4)  # Vector(4, 6)\n```"),
    ex("what is __hash__", "`__hash__` makes objects hashable so they can be used as dict keys or set members:\n```python\nclass Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\n    def __eq__(self, other):\n        return self.x == other.x and self.y == other.y\n\n    def __hash__(self):\n        return hash((self.x, self.y))\n\npoints = {Point(1,2), Point(3,4)}\n```"),
    ex("what is __iter__ and __next__", "`__iter__` returns the iterator object and `__next__` returns the next value:\n```python\nclass Range:\n    def __init__(self, n):\n        self.n, self.i = n, 0\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.i >= self.n:\n            raise StopIteration\n        val = self.i\n        self.i += 1\n        return val\n\nlist(Range(5))  # [0, 1, 2, 3, 4]\n```"),
    ex("how do i use __contains__", "`__contains__` makes the `in` operator work on your class:\n```python\nclass NumberRange:\n    def __init__(self, lo, hi):\n        self.lo, self.hi = lo, hi\n\n    def __contains__(self, item):\n        return self.lo <= item <= self.hi\n\nr = NumberRange(1, 10)\nprint(5 in r)   # True\nprint(15 in r)  # False\n```"),
    ex("how do i use weakref", "```python\nimport weakref\n\nclass Cache:\n    def __init__(self):\n        self._cache = weakref.WeakValueDictionary()\n\n    def get(self, key):\n        return self._cache.get(key)\n\n    def set(self, key, value):\n        self._cache[key] = value\n# Objects are removed from cache when garbage collected\n```"),
    ex("how do i measure memory usage", "```python\nimport tracemalloc\n\ntracemalloc.start()\n\n# code to measure:\ndata = [i**2 for i in range(100000)]\n\ncurrent, peak = tracemalloc.get_traced_memory()\nprint(f'current: {current/1024:.1f} KB')\nprint(f'peak:    {peak/1024:.1f} KB')\ntracemalloc.stop()\n```"),
    ex("how do i use slots for memory efficiency", "```python\nclass Point:\n    __slots__ = ('x', 'y')  # no __dict__ per instance\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n# Uses ~40% less memory than without __slots__\np = Point(1, 2)\n# p.z = 3  # AttributeError — can't add new attributes\n```"),
    ex("how do i copy a class instance", "```python\nimport copy\n\noriginal = MyClass()\n\nshallow = copy.copy(original)    # shallow copy\ndeep    = copy.deepcopy(original) # deep copy — copies nested objects too\n```"),
    ex("how do i use namedtuple", "```python\nfrom collections import namedtuple\n\nPoint = namedtuple('Point', ['x', 'y'])\np = Point(1, 2)\nprint(p.x, p.y)  # 1 2\nprint(p[0])      # 1 — also indexable\nx, y = p         # unpacking works too\n```"),
    ex("how do i use dataclass with frozen", "```python\nfrom dataclasses import dataclass\n\n@dataclass(frozen=True)  # immutable — good for dict keys\nclass Point:\n    x: float\n    y: float\n\np = Point(1.0, 2.0)\n# p.x = 3  # FrozenInstanceError\n```"),
    ex("what is a descriptor", "A descriptor implements `__get__`, `__set__`, or `__delete__` to customize attribute access:\n```python\nclass Positive:\n    def __set_name__(self, owner, name):\n        self.name = name\n\n    def __get__(self, obj, objtype=None):\n        return obj.__dict__.get(self.name)\n\n    def __set__(self, obj, value):\n        if value <= 0:\n            raise ValueError(f'{self.name} must be positive')\n        obj.__dict__[self.name] = value\n\nclass Circle:\n    radius = Positive()\n```"),
    ex("what is __init_subclass__", "`__init_subclass__` is called whenever the class is subclassed — useful for registering subclasses:\n```python\nclass Plugin:\n    _registry = {}\n\n    def __init_subclass__(cls, name=None, **kwargs):\n        super().__init_subclass__(**kwargs)\n        Plugin._registry[name or cls.__name__] = cls\n\nclass MyPlugin(Plugin, name='my'):\n    pass\n\nPlugin._registry  # {'my': MyPlugin}\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MORE ALGORITHMS & DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("lru cache implementation", "```python\nfrom collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cap = capacity\n        self.cache = OrderedDict()\n\n    def get(self, key):\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n\n    def put(self, key, value):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.cap:\n            self.cache.popitem(last=False)\n```"),
    ex("valid parentheses check", "```python\ndef is_valid(s):\n    stack = []\n    pairs = {')':'(', ']':'[', '}':'{'}\n    for c in s:\n        if c in '([{':\n            stack.append(c)\n        elif c in ')]}' :\n            if not stack or stack[-1] != pairs[c]:\n                return False\n            stack.pop()\n    return not stack\n```"),
    ex("find missing number in array", "```python\ndef missing_number(nums):\n    n = len(nums)\n    return n * (n + 1) // 2 - sum(nums)\n```"),
    ex("maximum product subarray", "```python\ndef max_product(nums):\n    best = cur_max = cur_min = nums[0]\n    for n in nums[1:]:\n        candidates = (n, cur_max*n, cur_min*n)\n        cur_max = max(candidates)\n        cur_min = min(candidates)\n        best = max(best, cur_max)\n    return best\n```"),
    ex("find all permutations", "```python\nfrom itertools import permutations\n\nlist(permutations([1, 2, 3]))\n# [(1,2,3),(1,3,2),(2,1,3),(2,3,1),(3,1,2),(3,2,1)]\n\n# Recursive:\ndef perms(lst):\n    if len(lst) <= 1: return [lst]\n    return [[lst[i]] + p\n            for i in range(len(lst))\n            for p in perms(lst[:i] + lst[i+1:])]\n```"),
    ex("top k frequent elements", "```python\nfrom collections import Counter\nimport heapq\n\ndef top_k(nums, k):\n    counts = Counter(nums)\n    return heapq.nlargest(k, counts, key=counts.get)\n```"),
    ex("sliding window maximum", "```python\nfrom collections import deque\n\ndef max_sliding_window(nums, k):\n    dq, result = deque(), []\n    for i, n in enumerate(nums):\n        while dq and dq[0] < i - k + 1:\n            dq.popleft()\n        while dq and nums[dq[-1]] < n:\n            dq.pop()\n        dq.append(i)\n        if i >= k - 1:\n            result.append(nums[dq[0]])\n    return result\n```"),
    ex("longest common subsequence", "```python\ndef lcs(a, b):\n    m, n = len(a), len(b)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if a[i-1] == b[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]\n```"),
    ex("roman to integer python", "```python\ndef roman_to_int(s):\n    vals = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}\n    total = 0\n    for i in range(len(s)):\n        if i+1 < len(s) and vals[s[i]] < vals[s[i+1]]:\n            total -= vals[s[i]]\n        else:\n            total += vals[s[i]]\n    return total\n```"),
    ex("spiral matrix traversal", "```python\ndef spiral_order(matrix):\n    result = []\n    while matrix:\n        result += matrix.pop(0)\n        matrix = list(zip(*matrix))[::-1]\n    return result\n```"),
    ex("word frequency counter", "```python\nfrom collections import Counter\nimport re\n\ndef word_freq(text):\n    words = re.findall(r'\\b\\w+\\b', text.lower())\n    return Counter(words).most_common()\n```"),
    ex("sieve of eratosthenes", "```python\ndef sieve(n):\n    is_prime = [True] * (n + 1)\n    is_prime[0] = is_prime[1] = False\n    for i in range(2, int(n**0.5) + 1):\n        if is_prime[i]:\n            for j in range(i*i, n+1, i):\n                is_prime[j] = False\n    return [i for i, p in enumerate(is_prime) if p]\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MORE WEB / API
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("fastapi with pydantic validation", "```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel, EmailStr\n\napp = FastAPI()\n\nclass User(BaseModel):\n    name: str\n    email: str\n    age: int\n\n@app.post('/users')\ndef create_user(user: User):\n    return {'id': 1, **user.dict()}\n```"),
    ex("fastapi authentication", "```python\nfrom fastapi import FastAPI, Depends, HTTPException\nfrom fastapi.security import OAuth2PasswordBearer\n\napp = FastAPI()\noauth2 = OAuth2PasswordBearer(tokenUrl='token')\n\ndef verify_token(token: str = Depends(oauth2)):\n    if token != 'secret':\n        raise HTTPException(status_code=401)\n    return token\n\n@app.get('/protected')\ndef protected(token: str = Depends(verify_token)):\n    return {'message': 'access granted'}\n```"),
    ex("flask with blueprint", "```python\nfrom flask import Blueprint, jsonify\n\nusers_bp = Blueprint('users', __name__)\n\n@users_bp.route('/users')\ndef list_users():\n    return jsonify([{'id': 1, 'name': 'Alice'}])\n\n# In app.py:\n# app.register_blueprint(users_bp, url_prefix='/api')\n```"),
    ex("parse url query parameters", "```python\nfrom urllib.parse import urlparse, parse_qs\n\nurl = 'https://example.com/search?q=python&page=2'\nparsed = urlparse(url)\nparams = parse_qs(parsed.query)\nprint(params['q'])    # ['python']\nprint(params['page']) # ['2']\n```"),
    ex("download a file with python", "```python\nimport requests\nfrom pathlib import Path\n\ndef download(url, dest):\n    r = requests.get(url, stream=True)\n    r.raise_for_status()\n    with open(dest, 'wb') as f:\n        for chunk in r.iter_content(chunk_size=8192):\n            f.write(chunk)\n```"),
    ex("rate limiting requests python", "```python\nimport time\nimport requests\n\ndef fetch_with_retry(url, max_retries=3, delay=1):\n    for attempt in range(max_retries):\n        r = requests.get(url)\n        if r.status_code == 429:  # too many requests\n            time.sleep(delay * (2 ** attempt))\n            continue\n        r.raise_for_status()\n        return r\n    raise Exception('max retries exceeded')\n```"),
    ex("websocket client python", "```python\nimport asyncio\nimport websockets\n\nasync def connect():\n    async with websockets.connect('ws://localhost:8765') as ws:\n        await ws.send('hello')\n        msg = await ws.recv()\n        print(f'received: {msg}')\n\nasyncio.run(connect())\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MORE EXTRA PHRASINGS FOR ALREADY-COVERED TOPICS
# ═══════════════════════════════════════════════════════════════════════════════
_gen_full = 'A generator is a function that uses `yield` to produce values one at a time. Memory-efficient — values are computed on demand:\n```python\ndef count_up(n):\n    for i in range(n):\n        yield i\n\nfor x in count_up(5):\n    print(x)\n```'
for q in ["python yield", "yield keyword python", "create a generator python",
          "generator function example", "lazy iteration python",
          "how to yield from a function", "python yield vs return"]:
    examples.append(ex(q, _gen_full))

_dec_short = '```python\nimport functools\n\ndef decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        # do something before\n        result = func(*args, **kwargs)\n        # do something after\n        return result\n    return wrapper\n\n@decorator\ndef my_function():\n    pass\n```'
for q in ["python @ symbol function", "wrap a function python",
          "add behavior to function python", "intercept function call python",
          "modify function without changing it"]:
    examples.append(ex(q, _dec_short))

for q in ["how do i use try except finally", "python exception handling example",
          "catch specific error python", "handle runtime error python",
          "try block python", "except clause python"]:
    examples.append(ex(q, '```python\ntry:\n    x = int(input("Enter a number: "))\n    result = 10 / x\nexcept ValueError:\n    print("not a number")\nexcept ZeroDivisionError:\n    print("can\'t divide by zero")\nelse:\n    print(f"result: {result}")  # runs if no exception\nfinally:\n    print("done")  # always runs\n```'))

for q in ["python list comp", "make a list from another list python",
          "filter and transform list python", "one-liner list python",
          "create list with expression"]:
    examples.append(ex(q, '```python\n# Basic:\nsquares = [x**2 for x in range(10)]\n\n# With filter:\nevens = [x for x in range(20) if x % 2 == 0]\n\n# Transform strings:\nwords = ["hello", "world"]\nupper = [w.upper() for w in words]\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# PRACTICAL PROJECTS / MINI APPS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("write a word counter script", "```python\nimport sys\nfrom collections import Counter\n\ndef count_words(filename):\n    with open(filename, encoding='utf-8') as f:\n        words = f.read().lower().split()\n    counts = Counter(words)\n    for word, n in counts.most_common(10):\n        print(f'{word:20} {n}')\n\nif __name__ == '__main__':\n    count_words(sys.argv[1])\n```"),
    ex("write a url shortener", "```python\nimport hashlib\n\nclass URLShortener:\n    def __init__(self):\n        self._map = {}\n\n    def shorten(self, url):\n        key = hashlib.md5(url.encode()).hexdigest()[:6]\n        self._map[key] = url\n        return f'short.ly/{key}'\n\n    def expand(self, key):\n        return self._map.get(key)\n```"),
    ex("write a simple calculator cli", "```python\ndef calc():\n    while True:\n        expr = input('> ').strip()\n        if expr in ('quit', 'exit'): break\n        try:\n            print(eval(expr, {'__builtins__': {}}))\n        except Exception as e:\n            print(f'error: {e}')\n\ncalc()\n```"),
    ex("write a number guessing game", "```python\nimport random\n\ndef guessing_game():\n    secret = random.randint(1, 100)\n    tries = 0\n    while True:\n        guess = int(input('Guess (1-100): '))\n        tries += 1\n        if guess < secret: print('too low')\n        elif guess > secret: print('too high')\n        else:\n            print(f'Correct in {tries} tries!')\n            break\n\nguessing_game()\n```"),
    ex("write a simple json database", "```python\nimport json\nfrom pathlib import Path\n\nclass JsonDB:\n    def __init__(self, path):\n        self.path = Path(path)\n        self._data = json.loads(self.path.read_text()) if self.path.exists() else {}\n\n    def set(self, key, value):\n        self._data[key] = value\n        self.path.write_text(json.dumps(self._data, indent=2))\n\n    def get(self, key, default=None):\n        return self._data.get(key, default)\n\n    def delete(self, key):\n        self._data.pop(key, None)\n        self.path.write_text(json.dumps(self._data, indent=2))\n```"),
    ex("write a file watcher", "```python\nimport time\nfrom pathlib import Path\n\ndef watch(path, callback, interval=1):\n    p = Path(path)\n    last = p.stat().st_mtime\n    while True:\n        current = p.stat().st_mtime\n        if current != last:\n            callback(path)\n            last = current\n        time.sleep(interval)\n\nwatch('config.json', lambda f: print(f'{f} changed'))\n```"),
    ex("write a simple rate limiter", "```python\nimport time\n\nclass RateLimiter:\n    def __init__(self, max_calls, period):\n        self.max_calls = max_calls\n        self.period = period\n        self.calls = []\n\n    def __call__(self, func):\n        import functools\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            now = time.time()\n            self.calls = [t for t in self.calls if now - t < self.period]\n            if len(self.calls) >= self.max_calls:\n                raise Exception('rate limit exceeded')\n            self.calls.append(now)\n            return func(*args, **kwargs)\n        return wrapper\n```"),
    ex("write a markdown to html converter", "```python\nimport re\n\ndef md_to_html(md):\n    md = re.sub(r'^# (.+)$', r'<h1>\\1</h1>', md, flags=re.M)\n    md = re.sub(r'^## (.+)$', r'<h2>\\1</h2>', md, flags=re.M)\n    md = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', md)\n    md = re.sub(r'\\*(.+?)\\*', r'<em>\\1</em>', md)\n    md = re.sub(r'`(.+?)`', r'<code>\\1</code>', md)\n    return md\n```"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MORE CASUAL CHAT
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("do you know machine learning", "I know the basics — neural networks, training loops, loss functions. For ML in Python, the main libraries are PyTorch and TensorFlow. What do you want to build?"),
    ex("can you write a neural network", "Yes, here's a simple one in PyTorch:\n```python\nimport torch.nn as nn\n\nclass Net(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc1 = nn.Linear(784, 128)\n        self.fc2 = nn.Linear(128, 10)\n\n    def forward(self, x):\n        x = torch.relu(self.fc1(x))\n        return self.fc2(x)\n```"),
    ex("what is pytorch", "PyTorch is a deep learning framework — it gives you tensors (like NumPy arrays) that can run on GPUs, plus automatic differentiation for training neural networks:\n```python\nimport torch\nx = torch.tensor([1.0, 2.0, 3.0])\nprint(x.mean(), x.std())\n```"),
    ex("what is a tensor", "A tensor is a multi-dimensional array — a generalization of scalars, vectors, and matrices:\n- 0D: scalar (a number)\n- 1D: vector [1, 2, 3]\n- 2D: matrix [[1,2],[3,4]]\n- 3D+: e.g. a batch of images\n\nIn PyTorch: `torch.tensor([[1,2],[3,4]])`"),
    ex("what is overfitting", "Overfitting is when a model memorizes training data instead of learning general patterns. It performs well on training data but poorly on new data. Fix with:\n- More training data\n- Dropout regularization\n- Early stopping\n- Simpler model"),
    ex("what is gradient descent", "Gradient descent minimizes a loss function by iteratively moving in the direction of steepest descent:\n```\nweights = weights - learning_rate * gradient\n```\nThe gradient tells you which direction increases the loss — move opposite to it."),
    ex("what is backpropagation", "Backpropagation computes gradients through the network using the chain rule. PyTorch does this automatically:\n```python\nloss.backward()  # computes all gradients\noptimizer.step()  # updates weights\n```"),
    ex("what is a learning rate", "The learning rate controls how big each gradient descent step is. Too high: overshoots. Too low: trains very slowly. Typical values: 1e-3 to 1e-5. Use a scheduler to decay it over time."),
    ex("what programming languages do you know", "I specialize in Python. I know the standard library, common frameworks (Flask, FastAPI, Django), data science tools (NumPy, Pandas, PyTorch), algorithms, and general software patterns."),
    ex("write me a python script", "Sure! What should it do? Tell me the goal and I'll write it."),
    ex("i want to build a website", "Python has great web frameworks:\n- **Flask** — lightweight, great for APIs and small apps\n- **FastAPI** — modern, fast, auto-generates docs\n- **Django** — batteries-included, great for full applications\n\nWhat kind of website?"),
    ex("i want to build a game", "Python has Pygame for 2D games:\n```python\nimport pygame\npygame.init()\nscreen = pygame.display.set_mode((800, 600))\nclock  = pygame.time.Clock()\nrunning = True\nwhile running:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            running = False\n    screen.fill((0, 0, 0))\n    pygame.display.flip()\n    clock.tick(60)\npygame.quit()\n```"),
    ex("how do i get a programming job", "Build projects you can show, learn Git, practice data structures & algorithms (LeetCode), contribute to open source, and write clean readable code. Python is great for getting started."),
    ex("what should i build to learn python", "Build things you actually want: a web scraper, a Discord bot, a CLI tool, a data analyzer, a game. Real projects teach you more than tutorials."),
    ex("is python slow", "Python is slower than C/Java for CPU-bound work, but fast enough for most tasks. For performance: use NumPy (C under the hood), PyPy (JIT compiler), or Cython. For most web/scripting/data work, Python's speed is fine."),
    ex("python vs javascript", "Python: great for data science, ML, scripting, back-end. Clean syntax, huge scientific ecosystem. JavaScript: runs in the browser, required for front-end. Both are popular for back-end. Pick based on what you're building."),
    ex("python vs java", "Python: faster to write, less boilerplate, great for data/ML/scripting. Java: faster runtime, strong typing, good for large enterprise systems and Android. Python is generally better for beginners and data work."),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MULTI-TURN
# ═══════════════════════════════════════════════════════════════════════════════
multi_turn = [
    {"messages": [
        {"role": "user", "content": "write a function that finds all prime numbers up to n"},
        {"role": "silicat", "content": "```python\ndef primes_up_to(n):\n    sieve = [True] * (n + 1)\n    sieve[0] = sieve[1] = False\n    for i in range(2, int(n**0.5) + 1):\n        if sieve[i]:\n            for j in range(i*i, n+1, i):\n                sieve[j] = False\n    return [i for i, p in enumerate(sieve) if p]\n```"},
        {"role": "user", "content": "how fast is this"},
        {"role": "silicat", "content": "The Sieve of Eratosthenes is O(n log log n) — very fast. For n=1,000,000 it runs in under a second. The inner loop starts at `i*i` (not `2*i`) which is a key optimization."},
        {"role": "user", "content": "write a test for it"},
        {"role": "silicat", "content": "```python\ndef test_primes_up_to():\n    assert primes_up_to(10) == [2, 3, 5, 7]\n    assert primes_up_to(2)  == [2]\n    assert primes_up_to(1)  == []\n    assert primes_up_to(20) == [2, 3, 5, 7, 11, 13, 17, 19]\n    print('all tests passed')\n\ntest_primes_up_to()\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "explain object oriented programming"},
        {"role": "silicat", "content": "OOP organizes code around objects — bundles of data (attributes) and behaviour (methods). Four core concepts:\n1. **Encapsulation** — hide internal details\n2. **Inheritance** — reuse code from parent classes\n3. **Polymorphism** — same interface, different behaviour\n4. **Abstraction** — expose only what's necessary"},
        {"role": "user", "content": "show me a real example"},
        {"role": "silicat", "content": "```python\nclass Vehicle:\n    def __init__(self, make, speed):\n        self.make = make\n        self.speed = speed\n\n    def describe(self):\n        return f'{self.make} going {self.speed}mph'\n\nclass Car(Vehicle):\n    def __init__(self, make, speed, doors):\n        super().__init__(make, speed)\n        self.doors = doors\n\n    def describe(self):\n        return super().describe() + f' with {self.doors} doors'\n\nclass Bike(Vehicle):\n    def describe(self):\n        return super().describe() + ' (no doors)'\n\nvehicles = [Car('Toyota', 60, 4), Bike('Trek', 15)]\nfor v in vehicles:\n    print(v.describe())  # polymorphism\n```"},
        {"role": "user", "content": "when should i use inheritance vs composition"},
        {"role": "silicat", "content": "Rule of thumb: **favour composition over inheritance**.\n\n- Use **inheritance** when there's a true 'is-a' relationship (Dog is-a Animal)\n- Use **composition** when there's a 'has-a' relationship (Car has-a Engine)\n\nComposition is more flexible and avoids deep inheritance chains:\n```python\n# Composition (preferred):\nclass Engine:\n    def start(self): ...\n\nclass Car:\n    def __init__(self):\n        self.engine = Engine()  # has-a\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "write a simple web scraper"},
        {"role": "silicat", "content": "```python\nimport requests\nfrom bs4 import BeautifulSoup\n\ndef scrape_titles(url):\n    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})\n    r.raise_for_status()\n    soup = BeautifulSoup(r.text, 'html.parser')\n    return [h.get_text(strip=True) for h in soup.find_all('h2')]\n\ntitles = scrape_titles('https://news.ycombinator.com')\nfor t in titles[:5]:\n    print(t)\n```\nInstall: `pip install requests beautifulsoup4`"},
        {"role": "user", "content": "how do i handle pagination"},
        {"role": "silicat", "content": "```python\ndef scrape_all_pages(base_url, max_pages=5):\n    results = []\n    for page in range(1, max_pages + 1):\n        url = f'{base_url}?page={page}'\n        r = requests.get(url)\n        if r.status_code == 404: break\n        soup = BeautifulSoup(r.text, 'html.parser')\n        items = soup.find_all('div', class_='item')\n        if not items: break  # no more results\n        results.extend(i.get_text() for i in items)\n    return results\n```"},
        {"role": "user", "content": "how do i be polite and not get banned"},
        {"role": "silicat", "content": "```python\nimport time, random\n\ndef polite_scraper(urls):\n    for url in urls:\n        r = requests.get(url, headers={'User-Agent': 'MyBot/1.0'})\n        process(r)\n        time.sleep(random.uniform(1, 3))  # random delay\n```\nAlso: check `robots.txt`, set a descriptive `User-Agent`, don't scrape during peak hours, and respect `Retry-After` headers on 429 responses."},
    ]},
    {"messages": [
        {"role": "user", "content": "what is asyncio and when should i use it"},
        {"role": "silicat", "content": "asyncio is Python's built-in library for writing concurrent code using a single thread. Use it when you have many I/O-bound operations (network calls, file reads) that spend most time *waiting*:\n```python\nimport asyncio\n\nasync def fetch(url):\n    await asyncio.sleep(1)  # simulates network wait\n    return f'response from {url}'\n\nasync def main():\n    # These run concurrently:\n    results = await asyncio.gather(fetch('a'), fetch('b'), fetch('c'))\n    print(results)\n\nasyncio.run(main())  # takes ~1s, not 3s\n```"},
        {"role": "user", "content": "how is it different from threads"},
        {"role": "silicat", "content": "- **asyncio**: single thread, cooperative. You explicitly `await` to yield control. No GIL issues. Great for many concurrent network requests.\n- **Threads**: OS-managed, preemptive. Run in parallel but share memory (need locks). Limited by GIL for CPU work.\n- **asyncio wins** when you have 100s of concurrent network calls.\n- **Threads win** when you need blocking calls that don't support async."},
        {"role": "user", "content": "show me a real asyncio http example"},
        {"role": "silicat", "content": "```python\nimport asyncio\nimport aiohttp\n\nasync def fetch(session, url):\n    async with session.get(url) as r:\n        return await r.json()\n\nasync def main(urls):\n    async with aiohttp.ClientSession() as session:\n        tasks = [fetch(session, url) for url in urls]\n        return await asyncio.gather(*tasks)\n\nurls = ['https://httpbin.org/get'] * 5\nresults = asyncio.run(main(urls))\nprint(len(results), 'responses')\n```\nInstall: `pip install aiohttp`"},
    ]},
    {"messages": [
        {"role": "user", "content": "how do i structure a large python project"},
        {"role": "silicat", "content": "```\nmy_project/\n├── src/\n│   └── mypackage/\n│       ├── __init__.py\n│       ├── models.py\n│       ├── services.py\n│       └── utils.py\n├── tests/\n│   ├── test_models.py\n│   └── test_services.py\n├── requirements.txt\n├── pyproject.toml\n└── README.md\n```\nKey principles: separate concerns, one module per responsibility, keep tests next to code."},
        {"role": "user", "content": "what goes in pyproject.toml"},
        {"role": "silicat", "content": "```toml\n[build-system]\nrequires = ['setuptools']\nbuild-backend = 'setuptools.backends.legacy:build'\n\n[project]\nname = 'mypackage'\nversion = '0.1.0'\ndependencies = [\n    'requests>=2.31',\n    'fastapi>=0.110',\n]\n\n[project.scripts]\nmytool = 'mypackage.cli:main'\n```\nReplace `requirements.txt` with `pyproject.toml` for installable packages."},
    ]},
    {"messages": [
        {"role": "user", "content": "write a function that parses a log file"},
        {"role": "silicat", "content": "```python\nimport re\nfrom dataclasses import dataclass\nfrom datetime import datetime\n\n@dataclass\nclass LogEntry:\n    timestamp: datetime\n    level: str\n    message: str\n\ndef parse_log(path):\n    pattern = re.compile(\n        r'(?P<ts>\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}) '\n        r'(?P<level>\\w+) (?P<msg>.+)'\n    )\n    entries = []\n    with open(path) as f:\n        for line in f:\n            m = pattern.match(line.strip())\n            if m:\n                entries.append(LogEntry(\n                    timestamp=datetime.fromisoformat(m['ts']),\n                    level=m['level'],\n                    message=m['msg'],\n                ))\n    return entries\n```"},
        {"role": "user", "content": "filter to only errors"},
        {"role": "silicat", "content": "```python\nerrors = [e for e in parse_log('app.log') if e.level == 'ERROR']\n```"},
        {"role": "user", "content": "count errors per hour"},
        {"role": "silicat", "content": "```python\nfrom collections import Counter\n\nerrors = [e for e in parse_log('app.log') if e.level == 'ERROR']\nhourly = Counter(e.timestamp.strftime('%Y-%m-%d %H:00') for e in errors)\nfor hour, count in sorted(hourly.items()):\n    print(f'{hour}  {count} errors')\n```"},
    ]},
]

with JSONL.open("a", encoding="utf-8") as f:
    for item in examples:
        f.write(json.dumps(item) + "\n")
    for item in multi_turn:
        f.write(json.dumps(item) + "\n")

total = sum(1 for _ in JSONL.open())
print(f"Added {len(examples)} single-turn + {len(multi_turn)} multi-turn examples.")
print(f"Total examples now: {total}")
