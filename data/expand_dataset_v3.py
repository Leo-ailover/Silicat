"""Massive dataset expansion v3 — every concept × many phrasings."""
import json
from pathlib import Path

JSONL = Path(__file__).parent / "silicat_chat.jsonl"


def ex(user, silicat):
    return {"messages": [{"role": "user", "content": user}, {"role": "silicat", "content": silicat}]}


examples = []

# ═══════════════════════════════════════════════════════════════════════════════
# REVERSE A STRING — many phrasings so the model learns the concept not the words
# ═══════════════════════════════════════════════════════════════════════════════
_reverse = '```python\ndef reverse_string(s):\n    return s[::-1]\n```'
_reverse2 = 'Use slicing:\n```python\ns = "hello"\nprint(s[::-1])  # "olleh"\n```'
for q in [
    "reverse a string python", "python reverse string", "flip a string in python",
    "how do i reverse a string", "string backwards python", "how to reverse text in python",
    "reverse the characters in a string", "turn a string around python",
    "get a string in reverse order", "invert a string python",
]:
    examples.append(ex(q, _reverse))
examples.append(ex("show me how to reverse a string with slicing", _reverse2))
examples.append(ex("reverse string without slicing", '```python\ndef reverse_string(s):\n    result = ""\n    for c in s:\n        result = c + result\n    return result\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# HELLO WORLD
# ═══════════════════════════════════════════════════════════════════════════════
_hw = '```python\nprint("Hello, World!")\n```'
for q in [
    "hello world python", "print hello world", "write hello world",
    "how do i print hello world", "first python program", "simplest python program",
    "python print statement example", "how do i output text in python",
    "display hello world in python", "python beginner example",
]:
    examples.append(ex(q, _hw))

# ═══════════════════════════════════════════════════════════════════════════════
# FIZZBUZZ
# ═══════════════════════════════════════════════════════════════════════════════
_fb = '```python\nfor i in range(1, 101):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    elif i % 3 == 0:\n        print("Fizz")\n    elif i % 5 == 0:\n        print("Buzz")\n    else:\n        print(i)\n```'
for q in [
    "fizzbuzz python", "write fizzbuzz", "fizzbuzz program", "implement fizzbuzz",
    "code fizzbuzz in python", "fizzbuzz solution", "fizzbuzz challenge python",
    "how to write fizzbuzz", "python fizzbuzz example",
]:
    examples.append(ex(q, _fb))

# ═══════════════════════════════════════════════════════════════════════════════
# LIST COMPREHENSION
# ═══════════════════════════════════════════════════════════════════════════════
_lc = 'A list comprehension builds a list in one line:\n```python\nsquares = [x**2 for x in range(10)]\nevens   = [x for x in range(20) if x % 2 == 0]\n```'
for q in [
    "what is a list comprehension", "list comprehension python", "how do list comprehensions work",
    "explain list comprehension", "python list comprehension example",
    "what does list comprehension mean", "show me a list comprehension",
    "list comprehension syntax", "how to use list comprehension",
    "list comprehension vs for loop", "create list with comprehension",
]:
    examples.append(ex(q, _lc))
examples.append(ex("list comprehension with condition", '```python\n# Only even squares\neven_squares = [x**2 for x in range(10) if x % 2 == 0]\n```'))
examples.append(ex("nested list comprehension example", '```python\nmatrix = [[1,2,3],[4,5,6]]\nflat = [x for row in matrix for x in row]\n# [1, 2, 3, 4, 5, 6]\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# DECORATOR
# ═══════════════════════════════════════════════════════════════════════════════
_dec = '```python\nimport functools\n\ndef my_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print("before")\n        result = func(*args, **kwargs)\n        print("after")\n        return result\n    return wrapper\n\n@my_decorator\ndef greet(name):\n    return f"Hello, {name}!"\n```'
for q in [
    "decorator python", "how do decorators work", "write a decorator",
    "python decorator example", "what is a decorator", "how to use decorator",
    "explain decorators python", "make a python decorator", "function decorator python",
    "decorator pattern python", "what does @ mean in python",
    "how do i decorate a function", "decorator syntax python",
]:
    examples.append(ex(q, _dec))
examples.append(ex("decorator that logs function calls", '```python\nimport functools, logging\n\ndef log_calls(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        logging.info(f"calling {func.__name__}({args}, {kwargs})")\n        return func(*args, **kwargs)\n    return wrapper\n```'))
examples.append(ex("decorator with arguments", '```python\nimport functools\n\ndef repeat(n):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for _ in range(n):\n                func(*args, **kwargs)\n        return wrapper\n    return decorator\n\n@repeat(3)\ndef hi():\n    print("hi")\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# EXCEPTION HANDLING
# ═══════════════════════════════════════════════════════════════════════════════
_exc = '```python\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f"error: {e}")\nfinally:\n    print("always runs")\n```'
for q in [
    "how do i handle an exception", "try except python", "exception handling python",
    "catch error python", "how to catch exceptions", "python error handling",
    "try catch python", "handle errors in python", "what is try except",
    "python exception example", "how do i use try except",
    "catch exception python", "dealing with errors python",
]:
    examples.append(ex(q, _exc))
examples.append(ex("catch multiple exceptions", '```python\ntry:\n    x = int(input())\n    print(10 / x)\nexcept (ValueError, ZeroDivisionError) as e:\n    print(f"error: {e}")\n```'))
examples.append(ex("raise a custom exception", '```python\nclass ValidationError(Exception):\n    pass\n\ndef validate(age):\n    if age < 0:\n        raise ValidationError(f"age cannot be negative: {age}")\n```'))
examples.append(ex("how do i ignore an exception", '```python\ntry:\n    risky_call()\nexcept Exception:\n    pass  # suppress all exceptions\n\n# or more targeted:\ntry:\n    risky_call()\nexcept FileNotFoundError:\n    pass\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
_gen = 'A generator is a function that yields values one at a time instead of returning a list:\n```python\ndef count_up(n):\n    for i in range(n):\n        yield i\n\nfor x in count_up(5):\n    print(x)\n```\nGenerators are memory-efficient — they compute values on demand.'
for q in [
    "what is a generator", "generator python", "how do generators work",
    "yield python", "explain generators", "python generator example",
    "generator vs list", "what does yield do", "how to write a generator",
    "generator function python", "lazy evaluation python",
    "what is yield in python", "generator expression python",
]:
    examples.append(ex(q, _gen))
examples.append(ex("infinite generator python", '```python\ndef integers(start=0):\n    n = start\n    while True:\n        yield n\n        n += 1\n```'))
examples.append(ex("generator expression", '```python\n# Like a list comprehension but lazy:\nsquares = (x**2 for x in range(1000))  # no memory used yet\nprint(next(squares))  # 0\nprint(next(squares))  # 1\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# BINARY SEARCH
# ═══════════════════════════════════════════════════════════════════════════════
_bs = '```python\ndef binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n```'
for q in [
    "binary search python", "write binary search", "implement binary search",
    "binary search algorithm", "how does binary search work",
    "binary search code python", "search sorted list python",
    "bisect python", "search in sorted array",
]:
    examples.append(ex(q, _bs))

# ═══════════════════════════════════════════════════════════════════════════════
# SORTING
# ═══════════════════════════════════════════════════════════════════════════════
_sort = '```python\nlst = [3, 1, 4, 1, 5, 9]\nlst.sort()              # in-place\nsorted_lst = sorted(lst) # new list\nlst.sort(reverse=True)  # descending\n```'
for q in [
    "how do i sort a list", "sort list python", "sorting in python",
    "sort array python", "python sort example", "how to sort",
    "sort numbers python", "order a list python",
]:
    examples.append(ex(q, _sort))
examples.append(ex("sort list of strings", '```python\nwords = ["banana", "apple", "cherry"]\nwords.sort()              # alphabetical\nwords.sort(key=len)       # by length\nwords.sort(key=str.lower) # case-insensitive\n```'))
examples.append(ex("sort list of dicts by key", '```python\npeople = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]\npeople.sort(key=lambda p: p["age"])\n```'))
examples.append(ex("sort descending python", '```python\nlst = [3, 1, 4, 1, 5]\nlst.sort(reverse=True)\n# or: sorted(lst, reverse=True)\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# CLASS / OOP
# ═══════════════════════════════════════════════════════════════════════════════
_cls = '```python\nclass Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n\n    def bark(self):\n        return f"{self.name} says woof!"\n\n    def __str__(self):\n        return f"{self.name} ({self.breed})"\n\ndog = Dog("Rex", "Labrador")\nprint(dog.bark())\n```'
for q in [
    "write a python class", "how to make a class in python", "class example python",
    "python class tutorial", "object oriented python", "how to use classes",
    "create a class python", "define a class python", "oop python example",
    "python class with methods", "how do classes work in python",
]:
    examples.append(ex(q, _cls))
examples.append(ex("class with inheritance", '```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return "..."\n\nclass Dog(Animal):\n    def speak(self):\n        return f"{self.name} says woof!"\n\nclass Cat(Animal):\n    def speak(self):\n        return f"{self.name} says meow!"\n```'))
examples.append(ex("class with property", '```python\nclass Temperature:\n    def __init__(self, celsius):\n        self._celsius = celsius\n\n    @property\n    def celsius(self):\n        return self._celsius\n\n    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError("below absolute zero")\n        self._celsius = value\n\n    @property\n    def fahrenheit(self):\n        return self._celsius * 9/5 + 32\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# DICTIONARY
# ═══════════════════════════════════════════════════════════════════════════════
_dict = '```python\nd = {"name": "Alice", "age": 30}\nprint(d["name"])           # "Alice"\nprint(d.get("email", ""))  # "" — no KeyError\nd["city"] = "London"       # add key\ndel d["age"]               # remove key\n```'
for q in [
    "python dictionary", "how do i use a dict", "dict example python",
    "dictionary python tutorial", "how to create a dictionary",
    "python key value store", "dict operations python",
    "how do dictionaries work python",
]:
    examples.append(ex(q, _dict))
examples.append(ex("loop through a dictionary", '```python\nd = {"a": 1, "b": 2, "c": 3}\nfor key in d:\n    print(key)\nfor val in d.values():\n    print(val)\nfor key, val in d.items():\n    print(key, val)\n```'))
examples.append(ex("check if key exists in dict", '```python\nd = {"a": 1}\nif "a" in d:\n    print("exists")\n# or:\nvalue = d.get("b")  # None if missing\n```'))
examples.append(ex("merge two dicts", '```python\na = {"x": 1}\nb = {"y": 2}\nmerged = {**a, **b}  # Python 3.5+\nmerged = a | b       # Python 3.9+\n```'))
examples.append(ex("count words with dict", '```python\ntext = "the cat sat on the mat"\ncounts = {}\nfor word in text.split():\n    counts[word] = counts.get(word, 0) + 1\n# or:\nfrom collections import Counter\ncounts = Counter(text.split())\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# READING / WRITING FILES
# ═══════════════════════════════════════════════════════════════════════════════
_read = '```python\nwith open("file.txt", "r", encoding="utf-8") as f:\n    content = f.read()\n```'
_write = '```python\nwith open("file.txt", "w", encoding="utf-8") as f:\n    f.write("hello\\n")\n```'
for q in ["read a file python", "how to read a file", "open file python",
          "read text file python", "load file contents python"]:
    examples.append(ex(q, _read))
for q in ["write to a file python", "how to write a file", "save to file python",
          "create file python", "write text to file"]:
    examples.append(ex(q, _write))
examples.append(ex("read file line by line", '```python\nwith open("file.txt", encoding="utf-8") as f:\n    for line in f:\n        print(line.rstrip())\n```'))
examples.append(ex("append to file", '```python\nwith open("log.txt", "a", encoding="utf-8") as f:\n    f.write("new entry\\n")\n```'))
examples.append(ex("read json file", '```python\nimport json\nwith open("data.json", encoding="utf-8") as f:\n    data = json.load(f)\n```'))
examples.append(ex("write json file", '```python\nimport json\ndata = {"name": "Alice", "scores": [1, 2, 3]}\nwith open("out.json", "w") as f:\n    json.dump(data, f, indent=2)\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# LAMBDA / MAP / FILTER
# ═══════════════════════════════════════════════════════════════════════════════
for q in ["lambda function python", "what is lambda", "python lambda example",
          "anonymous function python", "how to write lambda"]:
    examples.append(ex(q, '```python\nsquare = lambda x: x**2\nprint(square(5))  # 25\n\n# Common use: sorting\npeople.sort(key=lambda p: p["age"])\n```'))
for q in ["map function python", "how to use map", "python map example"]:
    examples.append(ex(q, '```python\nnums = [1, 2, 3, 4]\ndoubled = list(map(lambda x: x * 2, nums))\n# [2, 4, 6, 8]\n```'))
for q in ["filter function python", "how to use filter", "python filter list"]:
    examples.append(ex(q, '```python\nnums = [1, 2, 3, 4, 5, 6]\nevens = list(filter(lambda x: x % 2 == 0, nums))\n# [2, 4, 6]\n```'))

# ═══════════════════════════════════════════════════════════════════════════════
# STRINGS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("split string python", '```python\ns = "hello world"\nparts = s.split()        # ["hello", "world"]\nparts = s.split(",")     # split on comma\n```'),
    ex("join list to string", '```python\nwords = ["hello", "world"]\nresult = " ".join(words)  # "hello world"\nresult = ",".join(words)  # "hello,world"\n```'),
    ex("string formatting python", '```python\nname = "Alice"\nage = 30\nprint(f"Name: {name}, Age: {age}")  # f-string (preferred)\nprint("Name: {}, Age: {}".format(name, age))\n```'),
    ex("check if string contains substring", '```python\nif "world" in "hello world":\n    print("found")\n```'),
    ex("string replace python", '```python\ns = "hello world"\ns.replace("world", "python")  # "hello python"\n```'),
    ex("strip whitespace python", '```python\ns = "  hello  "\ns.strip()   # "hello"\ns.lstrip()  # "hello  "\ns.rstrip()  # "  hello"\n```'),
    ex("uppercase lowercase python", '```python\ns = "Hello World"\ns.upper()  # "HELLO WORLD"\ns.lower()  # "hello world"\ns.title()  # "Hello World"\n```'),
    ex("check if string is empty", '```python\ns = ""\nif not s:\n    print("empty")\n```'),
    ex("string length python", '```python\ns = "hello"\nprint(len(s))  # 5\n```'),
    ex("repeat a string python", '```python\n"ha" * 3   # "hahaha"\n"-" * 20   # "--------------------"\n```'),
    ex("string to list python", '```python\ns = "hello"\nchars = list(s)  # ["h", "e", "l", "l", "o"]\n```'),
    ex("multiline string python", '```python\ntext = """\nThis is\na multiline\nstring.\n"""\n```'),
    ex("raw string python", '```python\npath = r"C:\\Users\\Alice\\Documents"  # no need to escape backslashes\n```'),
    ex("string starts with ends with", '```python\ns = "hello world"\ns.startswith("hello")  # True\ns.endswith("world")    # True\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# LOOPS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("for loop python", '```python\nfor i in range(5):\n    print(i)  # 0 1 2 3 4\n```'),
    ex("while loop python", '```python\ni = 0\nwhile i < 5:\n    print(i)\n    i += 1\n```'),
    ex("loop with index python", '```python\nfor i, item in enumerate(["a", "b", "c"]):\n    print(i, item)\n```'),
    ex("break and continue python", '```python\nfor i in range(10):\n    if i == 3:\n        continue  # skip 3\n    if i == 7:\n        break     # stop at 7\n    print(i)\n```'),
    ex("loop backwards python", '```python\nfor i in range(10, 0, -1):\n    print(i)  # 10 9 8 ... 1\n\n# or:\nfor item in reversed(my_list):\n    print(item)\n```'),
    ex("loop with zip python", '```python\nnames = ["Alice", "Bob"]\nscores = [90, 85]\nfor name, score in zip(names, scores):\n    print(f"{name}: {score}")\n```'),
    ex("nested loop python", '```python\nfor i in range(3):\n    for j in range(3):\n        print(i, j)\n```'),
    ex("loop n times python", '```python\nfor _ in range(10):\n    do_something()\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CONDITIONALS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("if else python", '```python\nx = 10\nif x > 0:\n    print("positive")\nelif x == 0:\n    print("zero")\nelse:\n    print("negative")\n```'),
    ex("ternary operator python", '```python\nx = 5\nresult = "even" if x % 2 == 0 else "odd"\n```'),
    ex("match statement python", '```python\ncommand = "quit"\nmatch command:\n    case "quit":\n        print("goodbye")\n    case "help":\n        print("showing help")\n    case _:\n        print(f"unknown: {command}")\n```'),
    ex("and or not python", '```python\nif x > 0 and x < 10:\n    print("single digit")\n\nif not is_valid:\n    raise ValueError("invalid")\n\nif name == "Alice" or name == "Bob":\n    print("known user")\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("define a function python", '```python\ndef greet(name, greeting="Hello"):\n    return f"{greeting}, {name}!"\n\nprint(greet("Alice"))           # "Hello, Alice!"\nprint(greet("Bob", "Hi"))       # "Hi, Bob!"\n```'),
    ex("function with multiple return values", '```python\ndef min_max(lst):\n    return min(lst), max(lst)\n\nlo, hi = min_max([3, 1, 4, 1, 5])\n```'),
    ex("default argument python", '```python\ndef connect(host, port=8080, timeout=30):\n    ...\n\nconnect("example.com")          # uses defaults\nconnect("example.com", port=443)\n```'),
    ex("args and kwargs python", '```python\ndef func(*args, **kwargs):\n    print(args)    # tuple of positional args\n    print(kwargs)  # dict of keyword args\n\nfunc(1, 2, x=3, y=4)\n# (1, 2)\n# {"x": 3, "y": 4}\n```'),
    ex("recursive function python", '```python\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nfactorial(5)  # 120\n```'),
    ex("function annotations python", '```python\ndef add(a: int, b: int) -> int:\n    return a + b\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS / MODULES
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("how to import in python", '```python\nimport math\nprint(math.pi)  # 3.14159...\n\nfrom math import sqrt, pi\nprint(sqrt(16))  # 4.0\n\nimport numpy as np  # with alias\n```'),
    ex("how to import from another file", '```python\n# utils.py\ndef helper():\n    return 42\n\n# main.py\nfrom utils import helper\nprint(helper())\n```'),
    ex("create a python module", 'A module is just a `.py` file. Create `mymodule.py`:\n```python\ndef greet(name):\n    return f"Hello, {name}!"\n\nPI = 3.14159\n```\nImport it:\n```python\nimport mymodule\nprint(mymodule.greet("Alice"))\n```'),
    ex("what is __init__.py", '`__init__.py` makes a directory into a Python package. It can be empty or contain initialization code:\n```\nmypackage/\n    __init__.py\n    utils.py\n    models.py\n```\nThen: `from mypackage import utils`'),
    ex("how do i list installed packages", '```bash\npip list\npip show package-name\n```'),
    ex("install multiple packages", '```bash\npip install requests numpy pandas\n# or from requirements.txt:\npip install -r requirements.txt\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# COMMON BUILT-INS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("range python", '```python\nrange(5)          # 0 1 2 3 4\nrange(2, 8)       # 2 3 4 5 6 7\nrange(0, 10, 2)   # 0 2 4 6 8\nrange(10, 0, -1)  # 10 9 8 ... 1\n```'),
    ex("len python", '```python\nlen([1, 2, 3])  # 3\nlen("hello")    # 5\nlen({"a": 1})   # 1\n```'),
    ex("max and min python", '```python\nmax(3, 1, 4)       # 4\nmin([5, 2, 8, 1])  # 1\nmax("abc", "xyz")  # "xyz"\nmax(items, key=lambda x: x["score"])\n```'),
    ex("sum python", '```python\nsum([1, 2, 3, 4])  # 10\nsum(range(101))    # 5050\n```'),
    ex("abs python", '```python\nabs(-5)   # 5\nabs(3.7)  # 3.7\n```'),
    ex("isinstance python", '```python\nif isinstance(x, int):\n    print("integer")\nif isinstance(x, (int, float)):\n    print("number")\n```'),
    ex("type python", '```python\ntype(42)     # <class "int">\ntype("hi")   # <class "str">\ntype([])     # <class "list">\n```'),
    ex("input python", '```python\nname = input("Enter your name: ")\nage  = int(input("Enter your age: "))\n```'),
    ex("print with sep and end", '```python\nprint("a", "b", "c", sep="-")   # a-b-c\nprint("hello", end="")          # no newline\nprint("world")                  # on same line\n```'),
    ex("enumerate python", '```python\nfor i, val in enumerate(["a", "b", "c"]):\n    print(i, val)  # 0 a, 1 b, 2 c\n\n# Start from 1:\nfor i, val in enumerate(items, start=1):\n    ...\n```'),
    ex("zip python", '```python\nnames  = ["Alice", "Bob", "Carol"]\nscores = [90, 85, 92]\nfor name, score in zip(names, scores):\n    print(f"{name}: {score}")\n\n# Unzip:\nns, ss = zip(*pairs)\n```'),
    ex("map python", '```python\nnums = ["1", "2", "3"]\nints = list(map(int, nums))  # [1, 2, 3]\n```'),
    ex("any all python", '```python\nnums = [2, 4, 6]\nall(n % 2 == 0 for n in nums)  # True\nany(n > 5 for n in nums)       # True\n```'),
    ex("open file modes", '```python\nopen("f", "r")   # read (default)\nopen("f", "w")   # write (truncate)\nopen("f", "a")   # append\nopen("f", "rb")  # read binary\nopen("f", "x")   # create (error if exists)\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# CASUAL CHAT VARIANTS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("what are you", "I'm Silicat — a small AI coding assistant built from scratch. I can help you write Python code, explain concepts, and debug problems."),
    ex("who made you", "I'm Silicat, a from-scratch AI coding assistant. What can I help you build?"),
    ex("how do you work", "I'm a GPT-style transformer model trained on Python code and coding Q&A. I predict the next token given the conversation so far."),
    ex("are you smart", "I'm a small model — I know Python well but I'm not GPT-4. Ask me a coding question and see!"),
    ex("what do you know", "Mostly Python — data structures, algorithms, OOP, file handling, web APIs, testing, and more. Ask me anything code-related!"),
    ex("teach me python", "Sure! Start with the basics. Here's a quick intro:\n```python\n# Variables\nname = \"Alice\"\nage  = 30\n\n# Printing\nprint(f\"Hello, {name}!\")\n\n# Conditionals\nif age >= 18:\n    print(\"adult\")\n\n# Loop\nfor i in range(5):\n    print(i)\n```\nWhat do you want to learn next?"),
    ex("i want to learn coding", "Great! Python is a great first language. Start with: variables, print, if/else, loops, functions. What's your first question?"),
    ex("can you write code for me", "Yes — tell me what you want to build and I'll write it."),
    ex("help", "I'm here! What Python code do you need help with?"),
    ex("hello there", "Hey! What are you coding today?"),
    ex("hi there", "Hi! What can I help you build?"),
    ex("hey there", "Hey! Ask me anything Python."),
    ex("sup", "Hey! What do you need?"),
    ex("yo", "Yo! What are you building?"),
    ex("ok", "Alright — what's next?"),
    ex("ok thanks", "No problem! Let me know if you need anything else."),
    ex("thanks a lot", "Happy to help!"),
    ex("thank you so much", "You're welcome! Come back anytime."),
    ex("this is helpful", "Glad to hear it! What else can I help with?"),
    ex("cool", "Thanks! Anything else you want to build?"),
    ex("great", "Glad it worked! Need anything else?"),
    ex("works", "Glad it worked! What's next?"),
    ex("it works", "Nice! Let me know if you run into anything else."),
    ex("can you explain that", "Sure — what part do you want me to explain more clearly?"),
    ex("i don't understand", "No worries — let me know what's confusing and I'll explain differently."),
    ex("explain more", "Happy to! Which part would you like me to expand on?"),
    ex("give me an example", "Here's an example:\n```python\n# Let me know the topic and I'll tailor it.\n```\nWhat concept do you want an example of?"),
    ex("what's the difference", "I need a bit more context — the difference between what?"),
    ex("which is better", "Depends on the use case! Can you tell me what you're comparing?"),
    ex("i'm confused", "That's okay! What part is confusing? Describe it and I'll help."),
    ex("start over", "Sure! What would you like to build?"),
    ex("never mind", "No problem — let me know when you're ready."),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MORE ALGORITHMS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("quicksort python", '```python\ndef quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left   = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right  = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)\n```'),
    ex("merge sort python", '```python\ndef merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left  = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return _merge(left, right)\n\ndef _merge(a, b):\n    out, i, j = [], 0, 0\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]: out.append(a[i]); i += 1\n        else:             out.append(b[j]); j += 1\n    return out + a[i:] + b[j:]\n```'),
    ex("fibonacci python", '```python\n# Iterative (fast):\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\n# With memoization:\nfrom functools import lru_cache\n\n@lru_cache\ndef fib(n):\n    if n < 2: return n\n    return fib(n-1) + fib(n-2)\n```'),
    ex("prime check python", '```python\ndef is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n```'),
    ex("palindrome python", '```python\ndef is_palindrome(s):\n    s = s.lower().replace(" ", "")\n    return s == s[::-1]\n\nis_palindrome("racecar")  # True\nis_palindrome("A man a plan a canal Panama")  # True\n```'),
    ex("two sum python", '```python\ndef two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        complement = target - n\n        if complement in seen:\n            return [seen[complement], i]\n        seen[n] = i\n```'),
    ex("count vowels python", '```python\ndef count_vowels(s):\n    return sum(1 for c in s.lower() if c in "aeiou")\n```'),
    ex("anagram check python", '```python\nfrom collections import Counter\n\ndef is_anagram(a, b):\n    return Counter(a.lower()) == Counter(b.lower())\n```'),
    ex("flatten list python", '```python\nnested = [[1,2],[3,4],[5]]\nflat = [x for sub in nested for x in sub]\n\n# or:\nimport itertools\nflat = list(itertools.chain.from_iterable(nested))\n```'),
    ex("remove duplicates python", '```python\nlst = [1, 2, 2, 3, 3, 3]\nunique = list(dict.fromkeys(lst))  # preserves order\n# or if order doesn\'t matter:\nunique = list(set(lst))\n```'),
    ex("gcd python", '```python\nimport math\nmath.gcd(48, 18)  # 6\n\n# Manually:\ndef gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n```'),
    ex("power function python", '```python\n2 ** 10         # 1024\npow(2, 10)      # 1024\npow(2, 10, 100) # 24 (mod 100 — efficient for large numbers)\n```'),
    ex("matrix multiplication python", '```python\nimport numpy as np\n\nA = np.array([[1,2],[3,4]])\nB = np.array([[5,6],[7,8]])\nC = A @ B  # matrix multiply\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# DATA SCIENCE BASICS
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("numpy array python", '```python\nimport numpy as np\n\na = np.array([1, 2, 3, 4, 5])\na * 2          # [2, 4, 6, 8, 10]\na.mean()       # 3.0\na.std()        # standard deviation\na.reshape(5,1) # column vector\n```'),
    ex("pandas dataframe", '```python\nimport pandas as pd\n\ndf = pd.DataFrame({\n    "name":  ["Alice", "Bob", "Carol"],\n    "age":   [30, 25, 35],\n    "score": [90, 85, 92],\n})\nprint(df.head())\nprint(df.describe())\n```'),
    ex("read csv pandas", '```python\nimport pandas as pd\ndf = pd.read_csv("data.csv")\nprint(df.shape)    # (rows, cols)\nprint(df.columns)  # column names\nprint(df.head())   # first 5 rows\n```'),
    ex("filter dataframe pandas", '```python\nimport pandas as pd\ndf = pd.read_csv("data.csv")\n\n# Filter rows:\nadults = df[df["age"] >= 18]\nhigh_score = df[df["score"] > 90]\n\n# Multiple conditions:\ndf[(df["age"] > 20) & (df["score"] > 80)]\n```'),
    ex("groupby pandas", '```python\nimport pandas as pd\n\nresult = df.groupby("department")["salary"].mean()\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# GIT BASICS (often asked alongside Python)
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("basic git commands", '```bash\ngit init            # start a repo\ngit add .           # stage all changes\ngit commit -m "msg" # commit\ngit status          # see changes\ngit log --oneline   # history\ngit push            # push to remote\ngit pull            # pull from remote\n```'),
    ex("git branch commands", '```bash\ngit branch             # list branches\ngit branch feature     # create branch\ngit checkout feature   # switch branch\ngit checkout -b new    # create and switch\ngit merge feature      # merge into current\n```'),
    ex("git undo last commit", '```bash\ngit reset HEAD~1       # undo commit, keep changes staged\ngit reset --soft HEAD~1 # keep changes staged\ngit reset --hard HEAD~1 # discard changes (destructive!)\n```'),
    ex("gitignore example", '```\n# .gitignore\n__pycache__/\n*.pyc\n.env\nvenv/\n.DS_Store\n*.log\ndist/\nbuild/\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENT / SETUP
# ═══════════════════════════════════════════════════════════════════════════════
examples += [
    ex("how do i set up a python project", '1. Create a directory\n2. Set up a virtual environment:\n```bash\npython -m venv venv\nsource venv/bin/activate\n```\n3. Install dependencies:\n```bash\npip install requests\npip freeze > requirements.txt\n```\n4. Write your code in `.py` files.'),
    ex("what is requirements.txt", 'A text file listing your project\'s dependencies — one package per line:\n```\nrequests==2.31.0\nnumpy>=1.24\npandas\n```\nInstall all at once: `pip install -r requirements.txt`'),
    ex("how do i use dotenv", '```python\nfrom dotenv import load_dotenv\nimport os\n\nload_dotenv()  # loads .env file\n\nDB_URL = os.getenv("DATABASE_URL")\nAPI_KEY = os.getenv("API_KEY")\n```\nCreate `.env`:\n```\nDATABASE_URL=postgresql://...\nAPI_KEY=your_key_here\n```\nInstall: `pip install python-dotenv`'),
    ex("how do i use argparse", '```python\nimport argparse\n\np = argparse.ArgumentParser(description="My tool")\np.add_argument("input",    help="input file")\np.add_argument("--output", default="out.txt")\np.add_argument("--verbose", action="store_true")\nargs = p.parse_args()\n\nprint(args.input, args.output, args.verbose)\n```'),
    ex("how do i use logging", '```python\nimport logging\n\nlogging.basicConfig(\n    level=logging.INFO,\n    format="%(asctime)s %(levelname)s %(message)s",\n)\nlog = logging.getLogger(__name__)\n\nlog.info("started")\nlog.warning("disk almost full")\nlog.error("connection failed")\n```'),
]

# ═══════════════════════════════════════════════════════════════════════════════
# MORE MULTI-TURN
# ═══════════════════════════════════════════════════════════════════════════════
multi_turn = [
    {"messages": [
        {"role": "user", "content": "how do i reverse a string in python"},
        {"role": "silicat", "content": "```python\nreversed_str = my_string[::-1]\n```"},
        {"role": "user", "content": "what if i want to reverse each word separately"},
        {"role": "silicat", "content": "```python\nsentence = \"hello world\"\nreversed_words = \" \".join(w[::-1] for w in sentence.split())\n# \"olleh dlrow\"\n```"},
        {"role": "user", "content": "and how do i reverse the order of words"},
        {"role": "silicat", "content": "```python\nsentence = \"hello world foo\"\nreversed_order = \" \".join(sentence.split()[::-1])\n# \"foo world hello\"\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "explain what a decorator is"},
        {"role": "silicat", "content": "A decorator is a function that wraps another function to add behaviour without modifying its source:\n```python\nimport functools\n\ndef shout(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        result = func(*args, **kwargs)\n        return result.upper()\n    return wrapper\n\n@shout\ndef greet(name):\n    return f\"hello {name}\"\n\ngreet(\"alice\")  # \"HELLO ALICE\"\n```"},
        {"role": "user", "content": "can i stack decorators"},
        {"role": "silicat", "content": "Yes — decorators apply bottom to top:\n```python\n@decorator_a\n@decorator_b\ndef func():\n    ...\n# equivalent to: decorator_a(decorator_b(func))\n```"},
        {"role": "user", "content": "write a real example with two decorators"},
        {"role": "silicat", "content": "```python\nimport functools, time\n\ndef timer(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        t0 = time.perf_counter()\n        result = func(*args, **kwargs)\n        print(f\"{func.__name__} took {time.perf_counter()-t0:.3f}s\")\n        return result\n    return wrapper\n\ndef log_calls(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f\"calling {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n\n@timer\n@log_calls\ndef slow_add(a, b):\n    time.sleep(0.1)\n    return a + b\n\nslow_add(1, 2)\n# calling slow_add\n# slow_add took 0.100s\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "write a to-do list in python"},
        {"role": "silicat", "content": "```python\ntodos = []\n\ndef add(task): todos.append({\"task\": task, \"done\": False})\ndef complete(i): todos[i][\"done\"] = True\ndef show():\n    for i, t in enumerate(todos):\n        status = \"✓\" if t[\"done\"] else \"○\"\n        print(f\"{i}. [{status}] {t['task']}\")\n\nadd(\"Buy groceries\")\nadd(\"Write code\")\ncomplete(0)\nshow()\n```"},
        {"role": "user", "content": "save it to a file"},
        {"role": "silicat", "content": "```python\nimport json\n\ndef save(path=\"todos.json\"):\n    with open(path, \"w\") as f:\n        json.dump(todos, f, indent=2)\n\ndef load(path=\"todos.json\"):\n    global todos\n    try:\n        with open(path) as f:\n            todos = json.load(f)\n    except FileNotFoundError:\n        todos = []\n```"},
        {"role": "user", "content": "add a delete function"},
        {"role": "silicat", "content": "```python\ndef delete(i):\n    todos.pop(i)\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "what is recursion"},
        {"role": "silicat", "content": "Recursion is when a function calls itself. Every recursive function needs a base case to stop:\n```python\ndef countdown(n):\n    if n <= 0:        # base case\n        print(\"go!\")\n        return\n    print(n)\n    countdown(n - 1)  # recursive call\n\ncountdown(3)  # 3, 2, 1, go!\n```"},
        {"role": "user", "content": "when should i use recursion"},
        {"role": "silicat", "content": "Use recursion when the problem is naturally self-similar — trees, graphs, divide-and-conquer algorithms, nested structures. For simple loops, iteration is faster in Python (no tail-call optimisation). Good candidates:\n- Tree traversal\n- Factorial / Fibonacci\n- Merge sort / quicksort\n- Parsing nested expressions"},
        {"role": "user", "content": "how do i convert recursion to a loop"},
        {"role": "silicat", "content": "Use an explicit stack to simulate the call stack:\n```python\n# Recursive DFS:\ndef dfs(graph, start):\n    visited = set()\n    def _dfs(node):\n        visited.add(node)\n        for n in graph[node]:\n            if n not in visited:\n                _dfs(n)\n    _dfs(start)\n\n# Iterative DFS:\ndef dfs(graph, start):\n    visited = set()\n    stack = [start]\n    while stack:\n        node = stack.pop()\n        if node in visited: continue\n        visited.add(node)\n        stack.extend(graph[node])\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "how do i use classes for a bank account"},
        {"role": "silicat", "content": "```python\nclass BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self._balance = balance\n\n    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError(\"amount must be positive\")\n        self._balance += amount\n\n    def withdraw(self, amount):\n        if amount > self._balance:\n            raise ValueError(\"insufficient funds\")\n        self._balance -= amount\n\n    @property\n    def balance(self):\n        return self._balance\n\n    def __str__(self):\n        return f\"{self.owner}: ${self._balance:.2f}\"\n```"},
        {"role": "user", "content": "add a transaction history"},
        {"role": "silicat", "content": "```python\nclass BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self._balance = balance\n        self._history = []\n\n    def deposit(self, amount):\n        self._balance += amount\n        self._history.append((\"deposit\", amount))\n\n    def withdraw(self, amount):\n        if amount > self._balance:\n            raise ValueError(\"insufficient funds\")\n        self._balance -= amount\n        self._history.append((\"withdraw\", amount))\n\n    def statement(self):\n        for action, amt in self._history:\n            print(f\"{action:10} ${amt:.2f}\")\n        print(f\"Balance: ${self._balance:.2f}\")\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "i keep getting a TypeError"},
        {"role": "silicat", "content": "A TypeError means you applied an operation to the wrong type. Common examples:\n```python\n\"2\" + 2     # TypeError — can't add str and int\nlen(42)     # TypeError — int has no len\n[1,2] / 2  # TypeError — can't divide list\n```\nPaste your error message and I'll tell you exactly what's wrong."},
        {"role": "user", "content": "unsupported operand type(s) for +: 'int' and 'str'"},
        {"role": "silicat", "content": "You're trying to add a number and a string. Convert one to match the other:\n```python\n# If you want a number:\nn = 5\ns = \"3\"\nresult = n + int(s)   # 8\n\n# If you want a string:\nresult = str(n) + s   # \"53\"\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "write a simple password generator"},
        {"role": "silicat", "content": "```python\nimport random, string\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + \"!@#$%^&*\"\n    return \"\".join(random.choice(chars) for _ in range(length))\n\nprint(generate_password())\n```"},
        {"role": "user", "content": "make it more secure"},
        {"role": "silicat", "content": "Use `secrets` instead of `random` — it's cryptographically secure:\n```python\nimport secrets, string\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + \"!@#$%^&*\"\n    return \"\".join(secrets.choice(chars) for _ in range(length))\n```"},
        {"role": "user", "content": "how do i make sure it has at least one number and one symbol"},
        {"role": "silicat", "content": "```python\nimport secrets, string\n\ndef generate_password(length=16):\n    letters = string.ascii_letters\n    digits  = string.digits\n    symbols = \"!@#$%^&*\"\n    all_chars = letters + digits + symbols\n\n    # Guarantee at least one of each required category:\n    password = [\n        secrets.choice(digits),\n        secrets.choice(symbols),\n    ] + [secrets.choice(all_chars) for _ in range(length - 2)]\n\n    secrets.SystemRandom().shuffle(password)\n    return \"\".join(password)\n```"},
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
