"""Large dataset expansion v2 — paraphrases, casual chat, debugging, more coding topics."""
import sys as _sys

if "--force-append" not in _sys.argv:
    raise SystemExit("legacy one-shot generator, already applied to data/silicat_chat.jsonl (see data/legacy/README.md); pass --force-append to run it again")
import json
from pathlib import Path

JSONL = Path(__file__).resolve().parents[1] / "silicat_chat.jsonl"


def ex(user, silicat):
    return {"messages": [{"role": "user", "content": user}, {"role": "silicat", "content": silicat}]}


examples = []

# ── Paraphrases of core questions ─────────────────────────────────────────────
examples += [
    ex("can you reverse a string in python", "```python\ndef reverse_string(s):\n    return s[::-1]\n```"),
    ex("python reverse string", "Use slicing:\n```python\ns = 'hello'\nprint(s[::-1])  # 'olleh'\n```"),
    ex("how to flip a string", "```python\nflipped = my_string[::-1]\n```"),
    ex("turn a string backwards python", "```python\nbackwards = s[::-1]\n```"),

    ex("how do i write a decorator", "```python\nimport functools\n\ndef my_decorator(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print('before')\n        result = func(*args, **kwargs)\n        print('after')\n        return result\n    return wrapper\n\n@my_decorator\ndef greet():\n    print('hello')\n```"),
    ex("make a decorator python", "```python\nimport functools\n\ndef uppercase(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs).upper()\n    return wrapper\n\n@uppercase\ndef greet(name):\n    return f'hello {name}'\n```"),
    ex("python function decorator example", "```python\nimport functools\n\ndef log(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f'calling {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n```"),

    ex("how to make a list of numbers", "```python\nnums = list(range(10))  # [0,1,2,...,9]\n```"),
    ex("create a list in python", "```python\n# empty list\nlst = []\n\n# with values\nlst = [1, 2, 3, 4, 5]\n\n# from range\nlst = list(range(1, 11))\n```"),
    ex("python make empty list", "```python\nlst = []\n# or\nlst = list()\n```"),

    ex("how to check if something is in a list", "```python\nif 'apple' in fruits:\n    print('found')\n```"),
    ex("find element in list python", "```python\nif item in my_list:\n    print('exists')\nelse:\n    print('not found')\n```"),
    ex("does list contain value python", "```python\n'hello' in ['hello', 'world']  # True\n```"),

    ex("python dictionary get value", "```python\nd = {'name': 'Alice', 'age': 30}\nprint(d['name'])        # 'Alice'\nprint(d.get('email', 'unknown'))  # 'unknown' — no KeyError\n```"),
    ex("access dict key python", "```python\nvalue = my_dict['key']\n# or safely:\nvalue = my_dict.get('key', default_value)\n```"),
    ex("how to get a value from a dictionary", "```python\nd = {'x': 10}\nd.get('x')       # 10\nd.get('y', 0)    # 0 — key missing, returns default\n```"),

    ex("how to print in python", "```python\nprint('hello world')\nprint(f'Name: {name}, Age: {age}')\nprint('a', 'b', 'c', sep=', ')  # a, b, c\n```"),
    ex("python print variable", "```python\nx = 42\nprint(x)\nprint(f'x is {x}')\n```"),

    ex("how to add to a list", "```python\nlst = [1, 2, 3]\nlst.append(4)       # [1, 2, 3, 4]\nlst.extend([5, 6])  # [1, 2, 3, 4, 5, 6]\nlst.insert(0, 0)    # [0, 1, 2, 3, 4, 5, 6]\n```"),
    ex("append to list python", "```python\nmy_list.append(item)\n```"),
    ex("add item to list", "```python\nlst.append('new item')\n```"),

    ex("remove from list python", "```python\nlst = [1, 2, 3, 2]\nlst.remove(2)   # removes first occurrence → [1, 3, 2]\nlst.pop()       # removes and returns last item\nlst.pop(0)      # removes and returns item at index 0\n```"),
    ex("delete element from list", "```python\ndel lst[2]      # delete by index\nlst.remove(val) # delete by value\n```"),

    ex("how do you loop through a list", "```python\nfor item in my_list:\n    print(item)\n```"),
    ex("iterate over list python", "```python\nfor i, item in enumerate(my_list):\n    print(i, item)\n```"),
    ex("for loop python example", "```python\nfor i in range(5):\n    print(i)  # 0 1 2 3 4\n```"),
    ex("while loop python", "```python\ni = 0\nwhile i < 5:\n    print(i)\n    i += 1\n```"),
]

# ── Casual chat ───────────────────────────────────────────────────────────────
examples += [
    ex("hey", "Hey! What are you coding today?"),
    ex("hey silicat", "Hey! What can I help you build?"),
    ex("whats up", "Not much — just ready to help you write some code. What are you working on?"),
    ex("good morning", "Good morning! Ready to code?"),
    ex("good night", "Good night! Come back when you need to code something."),
    ex("i need help", "Of course! What are you working on?"),
    ex("i need help with python", "Happy to help. What's the problem?"),
    ex("i'm learning python", "Great choice! Python is readable and powerful. What do you want to learn first?"),
    ex("im a beginner", "No worries — everyone starts somewhere. What do you want to build?"),
    ex("im stuck", "Tell me what you're trying to do and I'll help you figure it out."),
    ex("i don't know how to start", "Start simple. What should the program do? Describe it in one sentence."),
    ex("python is hard", "It gets easier with practice. What part is tripping you up?"),
    ex("can you help me", "Yes! What do you need?"),
    ex("you're helpful", "Glad to be useful! Anything else you want to build?"),
    ex("nice", "Thanks! Let me know if you need more."),
    ex("awesome", "Glad it helped!"),
    ex("perfect", "Let me know if you need anything else."),
    ex("that worked", "Glad it worked! Anything else?"),
    ex("it doesn't work", "What error are you getting? Paste the message and I'll help fix it."),
    ex("i got an error", "Paste the error and I'll take a look."),
    ex("what should i learn first in python", "Start with: variables, if/else, loops, functions, and lists. Then move to dicts, files, and classes. Practice by building small projects."),
    ex("how long does it take to learn python", "For basics: a few weeks. To build real projects: a few months. The key is practice — write code every day."),
    ex("what can i build with python", "Web apps, scripts, data analysis, machine learning models, automation tools, games, APIs — almost anything."),
    ex("give me a project idea", "Build a to-do list CLI, a password generator, a weather fetcher, a word counter, or a simple web scraper. Pick one that sounds fun!"),
    ex("what is python used for", "Python is used for web development, data science, machine learning, automation, scripting, and more. It's one of the most popular languages in the world."),
    ex("is python good for beginners", "Yes — Python has simple, readable syntax that's close to plain English. It's widely recommended as a first language."),
    ex("should i use python 2 or 3", "Python 3 — always. Python 2 is end-of-life and no longer supported."),
    ex("what version of python should i use", "Use the latest Python 3.x release (3.11 or 3.12 as of 2024). Check python.org for the current stable version."),
    ex("how do i install python", "Download from python.org, run the installer, and make sure to check 'Add Python to PATH'. Verify with `python --version` in your terminal."),
    ex("how do i install a package", "Use pip:\n```\npip install package-name\n```\nFor example: `pip install requests`"),
    ex("how do i use pip", "```\npip install package-name   # install\npip uninstall package-name # remove\npip list                   # see installed\npip show package-name      # details\n```"),
    ex("what is pip", "pip is Python's package manager — it installs libraries from PyPI (the Python Package Index). Run `pip install <name>` to add a package."),
    ex("how do i create a virtual environment", "```\npython -m venv venv\nsource venv/bin/activate   # Mac/Linux\nvenv\\Scripts\\activate      # Windows\n```\nThen install packages inside it."),
    ex("what is a virtual environment", "A virtual environment is an isolated Python installation for your project. It keeps dependencies separate so different projects don't conflict."),
    ex("how do i run a python file", "```\npython myfile.py\n```\nOr `python3 myfile.py` on some systems."),
    ex("how do i open the python interpreter", "Type `python` or `python3` in your terminal. You'll get an interactive `>>>` prompt."),
]

# ── Debugging / errors ────────────────────────────────────────────────────────
examples += [
    ex("what is a NameError", "A `NameError` means you used a variable or function name that hasn't been defined yet:\n```python\nprint(x)  # NameError: name 'x' is not defined\n```\nCheck spelling and make sure you assigned the variable before using it."),
    ex("what is a TypeError", "A `TypeError` means you applied an operation to the wrong type:\n```python\n'hello' + 5  # TypeError: can only concatenate str to str\n```\nConvert types first: `'hello' + str(5)`."),
    ex("what is an IndexError", "An `IndexError` means you accessed a list index that doesn't exist:\n```python\nlst = [1, 2, 3]\nlst[5]  # IndexError: list index out of range\n```\nCheck that your index is within `range(len(lst))`."),
    ex("what is a KeyError", "A `KeyError` means the key doesn't exist in the dict:\n```python\nd = {'a': 1}\nd['b']  # KeyError: 'b'\n```\nUse `d.get('b')` to avoid it — returns `None` instead of raising."),
    ex("what is an AttributeError", "An `AttributeError` means the object doesn't have that attribute or method:\n```python\nx = 5\nx.append(1)  # AttributeError: 'int' object has no attribute 'append'\n```\nCheck the type of your object."),
    ex("what is a ValueError", "A `ValueError` means the value is the right type but invalid:\n```python\nint('hello')  # ValueError: invalid literal for int()\n```\nValidate input before converting."),
    ex("what is an ImportError", "An `ImportError` means Python can't find the module:\n```python\nimport pandas  # ImportError if not installed\n```\nFix: `pip install pandas`."),
    ex("what is a SyntaxError", "A `SyntaxError` means your code has invalid Python syntax:\n```python\nif True\n    print('oops')  # SyntaxError: expected ':'\n```\nCheck for missing colons, brackets, or quotes."),
    ex("how do i debug python code", "Options:\n1. Add `print()` statements to inspect values\n2. Use `breakpoint()` to drop into pdb\n3. Use an IDE debugger (VS Code, PyCharm)\n4. Use `logging` module for structured output"),
    ex("how do i use pdb", "```python\nbreakpoint()  # Python 3.7+ — drops into debugger\n```\nCommands: `n` (next line), `s` (step into), `c` (continue), `p var` (print variable), `q` (quit)."),
    ex("how do i fix indentation error", "Python uses indentation for blocks — be consistent. Use 4 spaces (not tabs):\n```python\nif True:\n    print('indented')  # 4 spaces\n```\nMix of tabs and spaces causes `IndentationError`."),
    ex("why is my loop infinite", "Your loop condition never becomes False. Make sure the loop variable changes:\n```python\n# Infinite — i never changes:\nwhile i < 10:\n    print(i)\n\n# Fixed:\nwhile i < 10:\n    print(i)\n    i += 1\n```"),
    ex("how do i print the type of a variable", "```python\nprint(type(x))\nprint(type(x).__name__)  # just the name as string\n```"),
    ex("how do i check if a variable is a string", "```python\nif isinstance(x, str):\n    print('it is a string')\n```"),
    ex("how do i convert string to int", "```python\nn = int('42')   # 42\nn = int('3.7')  # ValueError — use float() first if needed\nn = int(float('3.7'))  # 3\n```"),
    ex("how do i convert int to string", "```python\ns = str(42)   # '42'\ns = f'{42}'  # '42'\n```"),
    ex("how do i convert string to float", "```python\nf = float('3.14')  # 3.14\n```"),
    ex("how do i round a number", "```python\nround(3.14159, 2)  # 3.14\nround(3.5)         # 4\nimport math\nmath.floor(3.7)    # 3\nmath.ceil(3.2)     # 4\n```"),
    ex("what does None mean in python", "`None` is Python's null value — it represents 'no value'. Functions return `None` by default if they have no `return` statement.\n```python\ndef f():\n    pass\nprint(f())  # None\n```"),
    ex("how do i check if something is None", "```python\nif x is None:\n    print('no value')\n\nif x is not None:\n    print('has value')\n```\nUse `is`, not `==`, to compare with `None`."),
]

# ── More algorithms ───────────────────────────────────────────────────────────
examples += [
    ex("write a function to find the maximum in a list", "```python\ndef find_max(lst):\n    if not lst:\n        raise ValueError('empty list')\n    return max(lst)\n\n# or manually:\ndef find_max(lst):\n    m = lst[0]\n    for x in lst[1:]:\n        if x > m:\n            m = x\n    return m\n```"),
    ex("write a function to find the minimum", "```python\ndef find_min(lst):\n    return min(lst)\n```"),
    ex("how do i find duplicates in a list", "```python\ndef find_duplicates(lst):\n    seen = set()\n    dups = []\n    for x in lst:\n        if x in seen:\n            dups.append(x)\n        seen.add(x)\n    return dups\n```"),
    ex("count occurrences in a list", "```python\nfrom collections import Counter\n\nlst = [1, 2, 2, 3, 3, 3]\ncounts = Counter(lst)  # {3: 3, 2: 2, 1: 1}\n```"),
    ex("how do i find the average of a list", "```python\ndef average(lst):\n    return sum(lst) / len(lst)\n```"),
    ex("how do i rotate a list", "```python\ndef rotate(lst, k):\n    k %= len(lst)\n    return lst[k:] + lst[:k]\n```"),
    ex("write a function to check if a list is sorted", "```python\ndef is_sorted(lst):\n    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))\n```"),
    ex("how do i find the nth fibonacci number", "```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```"),
    ex("greatest common divisor python", "```python\nimport math\nmath.gcd(12, 8)  # 4\n\n# or manually:\ndef gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n```"),
    ex("how do i check if a number is a power of two", "```python\ndef is_power_of_two(n):\n    return n > 0 and (n & (n - 1)) == 0\n```"),
    ex("write a caesar cipher", "```python\ndef caesar(text, shift):\n    result = []\n    for c in text:\n        if c.isalpha():\n            base = ord('A') if c.isupper() else ord('a')\n            result.append(chr((ord(c) - base + shift) % 26 + base))\n        else:\n            result.append(c)\n    return ''.join(result)\n```"),
    ex("write a function to check balanced parentheses", "```python\ndef is_balanced(s):\n    stack = []\n    pairs = {')': '(', ']': '[', '}': '{'}\n    for c in s:\n        if c in '([{':\n            stack.append(c)\n        elif c in ')]}':\n            if not stack or stack[-1] != pairs[c]:\n                return False\n            stack.pop()\n    return not stack\n```"),
    ex("anagram check python", "```python\ndef is_anagram(a, b):\n    return sorted(a.lower()) == sorted(b.lower())\n\n# faster with Counter:\nfrom collections import Counter\ndef is_anagram(a, b):\n    return Counter(a.lower()) == Counter(b.lower())\n```"),
    ex("how do i generate all subsets of a list", "```python\nfrom itertools import combinations\n\ndef subsets(lst):\n    result = []\n    for r in range(len(lst) + 1):\n        result.extend(combinations(lst, r))\n    return result\n```"),
    ex("depth first search python", "```python\ndef dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    print(start)\n    for neighbor in graph[start]:\n        if neighbor not in visited:\n            dfs(graph, neighbor, visited)\n    return visited\n```"),
    ex("breadth first search python", "```python\nfrom collections import deque\n\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    while queue:\n        node = queue.popleft()\n        print(node)\n        for neighbor in graph[node]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n```"),
]

# ── OOP extras ────────────────────────────────────────────────────────────────
examples += [
    ex("python class with constructor", "```python\nclass Car:\n    def __init__(self, make, model, year):\n        self.make = make\n        self.model = model\n        self.year = year\n\n    def __str__(self):\n        return f'{self.year} {self.make} {self.model}'\n\ncar = Car('Toyota', 'Camry', 2022)\nprint(car)\n```"),
    ex("what is self in python class", "`self` refers to the current instance of the class. It's the first parameter of every instance method and lets you access the object's attributes and other methods:\n```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name  # self.name belongs to this specific dog\n\n    def bark(self):\n        return f'{self.name} says woof!'\n```"),
    ex("what is inheritance in python", "Inheritance lets a class reuse code from a parent class:\n```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return '...'\n\nclass Dog(Animal):\n    def speak(self):\n        return f'{self.name} says woof!'\n\nclass Cat(Animal):\n    def speak(self):\n        return f'{self.name} says meow!'\n```"),
    ex("what is super() in python", "`super()` calls a method from the parent class:\n```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n\nclass Dog(Animal):\n    def __init__(self, name, breed):\n        super().__init__(name)  # call Animal.__init__\n        self.breed = breed\n```"),
    ex("what is polymorphism", "Polymorphism means different classes can be used through the same interface:\n```python\nanimals = [Dog('Rex'), Cat('Luna')]\nfor a in animals:\n    print(a.speak())  # each calls its own speak()\n```"),
    ex("what is encapsulation", "Encapsulation hides internal details. Use a leading underscore for private attributes:\n```python\nclass BankAccount:\n    def __init__(self, balance):\n        self._balance = balance  # 'private' by convention\n\n    def deposit(self, amount):\n        self._balance += amount\n\n    @property\n    def balance(self):\n        return self._balance\n```"),
    ex("what is abstraction in python", "Abstraction hides complexity. Use `abc` for abstract base classes:\n```python\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self) -> float:\n        ...\n\nclass Circle(Shape):\n    def __init__(self, r):\n        self.r = r\n\n    def area(self):\n        import math\n        return math.pi * self.r ** 2\n```"),
    ex("python multiple inheritance", "```python\nclass Flyable:\n    def fly(self):\n        return 'flying'\n\nclass Swimmable:\n    def swim(self):\n        return 'swimming'\n\nclass Duck(Flyable, Swimmable):\n    pass\n\nd = Duck()\nprint(d.fly(), d.swim())\n```"),
    ex("what is a mixin", "A mixin is a class that adds methods to other classes through multiple inheritance without being a standalone class:\n```python\nclass JSONMixin:\n    def to_json(self):\n        import json\n        return json.dumps(self.__dict__)\n\nclass User(JSONMixin):\n    def __init__(self, name, email):\n        self.name = name\n        self.email = email\n\nUser('Alice', 'a@b.com').to_json()\n```"),
]

# ── File handling extras ───────────────────────────────────────────────────────
examples += [
    ex("how do i append to a file", "```python\nwith open('log.txt', 'a', encoding='utf-8') as f:\n    f.write('new line\\n')\n```"),
    ex("how do i count lines in a file", "```python\nwith open('file.txt', encoding='utf-8') as f:\n    count = sum(1 for _ in f)\nprint(count)\n```"),
    ex("how do i delete a file", "```python\nimport os\nos.remove('file.txt')\n\n# or with pathlib:\nfrom pathlib import Path\nPath('file.txt').unlink()\n```"),
    ex("how do i rename a file", "```python\nimport os\nos.rename('old.txt', 'new.txt')\n\n# or with pathlib:\nfrom pathlib import Path\nPath('old.txt').rename('new.txt')\n```"),
    ex("how do i copy a file", "```python\nimport shutil\nshutil.copy('src.txt', 'dst.txt')\n```"),
    ex("how do i create a directory", "```python\nimport os\nos.makedirs('path/to/dir', exist_ok=True)\n\n# or:\nfrom pathlib import Path\nPath('path/to/dir').mkdir(parents=True, exist_ok=True)\n```"),
    ex("how do i get the current directory", "```python\nimport os\nprint(os.getcwd())\n\n# or:\nfrom pathlib import Path\nprint(Path.cwd())\n```"),
    ex("how do i get file size", "```python\nimport os\nsize = os.path.getsize('file.txt')  # bytes\n\n# or:\nfrom pathlib import Path\nsize = Path('file.txt').stat().st_size\n```"),
    ex("how do i read yaml", "```python\nimport yaml\n\nwith open('config.yaml') as f:\n    config = yaml.safe_load(f)\n```\nInstall: `pip install pyyaml`"),
    ex("how do i read a config file", "```python\nimport configparser\n\nconfig = configparser.ConfigParser()\nconfig.read('config.ini')\nvalue = config['section']['key']\n```"),
]

# ── Strings extras ────────────────────────────────────────────────────────────
examples += [
    ex("how do i convert a string to uppercase", "```python\ns = 'hello world'\nprint(s.upper())   # 'HELLO WORLD'\nprint(s.lower())   # 'hello world'\nprint(s.title())   # 'Hello World'\n```"),
    ex("how do i check if a string is a number", "```python\ndef is_number(s):\n    try:\n        float(s)\n        return True\n    except ValueError:\n        return False\n\n# or just:\n'42'.isdigit()    # True\n'3.14'.isdigit()  # False\n```"),
    ex("how do i remove special characters from string", "```python\nimport re\nclean = re.sub(r'[^a-zA-Z0-9 ]', '', text)\n```"),
    ex("how do i truncate a string", "```python\ndef truncate(s, max_len, suffix='...'):\n    if len(s) <= max_len:\n        return s\n    return s[:max_len - len(suffix)] + suffix\n```"),
    ex("how do i repeat a string", "```python\n'ha' * 3   # 'hahaha'\n'-' * 20   # '--------------------'\n```"),
    ex("how do i check if string is empty", "```python\ns = ''\nif not s:           # Pythonic\n    print('empty')\nif len(s) == 0:     # explicit\n    print('empty')\n```"),
    ex("how do i get characters from a string", "```python\ns = 'hello'\ns[0]     # 'h'\ns[-1]    # 'o'\ns[1:4]   # 'ell'\ns[::2]   # 'hlo' (every 2nd character)\n```"),
    ex("how to format numbers in python", "```python\npi = 3.14159265\nf'{pi:.2f}'      # '3.14'\nf'{1000000:,}'   # '1,000,000'\nf'{0.05:.1%}'    # '5.0%'\nf'{42:05d}'      # '00042'\n```"),
]

# ── Web / HTTP ─────────────────────────────────────────────────────────────────
examples += [
    ex("how do i make a get request", "```python\nimport requests\n\nr = requests.get('https://api.example.com/data')\nr.raise_for_status()\ndata = r.json()\n```"),
    ex("how do i make a post request", "```python\nimport requests\n\nr = requests.post(\n    'https://api.example.com/users',\n    json={'name': 'Alice', 'email': 'alice@example.com'},\n)\nr.raise_for_status()\nprint(r.json())\n```"),
    ex("how do i add headers to a request", "```python\nimport requests\n\nheaders = {'Authorization': 'Bearer my_token'}\nr = requests.get('https://api.example.com', headers=headers)\n```"),
    ex("how do i handle request timeout", "```python\nimport requests\n\ntry:\n    r = requests.get('https://example.com', timeout=5)\nexcept requests.Timeout:\n    print('request timed out')\n```"),
    ex("how do i scrape a webpage", "```python\nimport requests\nfrom bs4 import BeautifulSoup\n\nr = requests.get('https://example.com')\nsoup = BeautifulSoup(r.text, 'html.parser')\ntitles = soup.find_all('h2')\nfor t in titles:\n    print(t.text)\n```\nInstall: `pip install requests beautifulsoup4`"),
    ex("write a simple flask app", "```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello, World!'\n\n@app.route('/greet/<name>')\ndef greet(name):\n    return f'Hello, {name}!'\n\nif __name__ == '__main__':\n    app.run(debug=True)\n```"),
    ex("write a fastapi endpoint", "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef root():\n    return {'message': 'Hello World'}\n\n@app.get('/items/{item_id}')\ndef get_item(item_id: int):\n    return {'item_id': item_id}\n```"),
    ex("how do i return json from flask", "```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route('/api/users')\ndef users():\n    return jsonify([{'id': 1, 'name': 'Alice'}])\n```"),
]

# ── Databases ─────────────────────────────────────────────────────────────────
examples += [
    ex("how do i use sqlite in python", "```python\nimport sqlite3\n\nconn = sqlite3.connect('mydb.db')\ncur = conn.cursor()\n\ncur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')\ncur.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))\nconn.commit()\n\nfor row in cur.execute('SELECT * FROM users'):\n    print(row)\n\nconn.close()\n```"),
    ex("how do i use sqlalchemy", "```python\nfrom sqlalchemy import create_engine, Column, Integer, String\nfrom sqlalchemy.orm import DeclarativeBase, Session\n\nclass Base(DeclarativeBase):\n    pass\n\nclass User(Base):\n    __tablename__ = 'users'\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n\nengine = create_engine('sqlite:///mydb.db')\nBase.metadata.create_all(engine)\n\nwith Session(engine) as session:\n    session.add(User(name='Alice'))\n    session.commit()\n```"),
    ex("how do i use a context manager with sqlite", "```python\nimport sqlite3\nfrom contextlib import closing\n\nwith sqlite3.connect('mydb.db') as conn:\n    with closing(conn.cursor()) as cur:\n        cur.execute('SELECT * FROM users')\n        rows = cur.fetchall()\n```"),
]

# ── Data structures extras ────────────────────────────────────────────────────
examples += [
    ex("what is a tuple in python", "A tuple is an immutable ordered collection:\n```python\nt = (1, 2, 3)\nt[0]   # 1\n# t[0] = 5  # TypeError — tuples can't be changed\n\n# Named tuple:\nfrom collections import namedtuple\nPoint = namedtuple('Point', ['x', 'y'])\np = Point(1, 2)\nprint(p.x, p.y)\n```"),
    ex("what is a set in python", "A set is an unordered collection of unique elements:\n```python\ns = {1, 2, 3, 2, 1}  # {1, 2, 3}\ns.add(4)\ns.remove(1)\n\na = {1, 2, 3}\nb = {2, 3, 4}\na & b   # intersection: {2, 3}\na | b   # union: {1, 2, 3, 4}\na - b   # difference: {1}\n```"),
    ex("difference between list and tuple", "Lists are mutable (can change), tuples are immutable (can't change):\n```python\nlst = [1, 2, 3]\nlst[0] = 99   # works\n\nt = (1, 2, 3)\nt[0] = 99     # TypeError\n```\nUse tuples for fixed data (coordinates, config), lists for collections that change."),
    ex("what is a deque", "`collections.deque` is a double-ended queue — fast O(1) appends and pops from both ends:\n```python\nfrom collections import deque\n\nd = deque([1, 2, 3])\nd.appendleft(0)   # [0, 1, 2, 3]\nd.popleft()       # returns 0\nd.append(4)       # [1, 2, 3, 4]\nd.pop()           # returns 4\n```"),
    ex("what is a heap", "A heap is a binary tree where the parent is always smaller (min-heap) than its children. Use `heapq`:\n```python\nimport heapq\n\nnums = [3, 1, 4, 1, 5]\nheapq.heapify(nums)\nprint(heapq.heappop(nums))  # 1 (smallest)\n```"),
    ex("how do i implement a graph in python", "```python\n# Adjacency list using a dict:\ngraph = {\n    'A': ['B', 'C'],\n    'B': ['A', 'D'],\n    'C': ['A'],\n    'D': ['B'],\n}\n\n# Or with defaultdict:\nfrom collections import defaultdict\ng = defaultdict(list)\ng['A'].append('B')\n```"),
    ex("what is a trie", "A trie is a tree for storing strings, where each node is a character:\n```python\nclass TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word):\n        node = self.root\n        for c in word:\n            node = node.children.setdefault(c, TrieNode())\n        node.is_end = True\n\n    def search(self, word):\n        node = self.root\n        for c in word:\n            if c not in node.children:\n                return False\n            node = node.children[c]\n        return node.is_end\n```"),
]

# ── Comprehensions / functional extras ────────────────────────────────────────
examples += [
    ex("how do i use any() and all()", "```python\nnums = [2, 4, 6, 8]\nall(n % 2 == 0 for n in nums)  # True — all even\nany(n > 5 for n in nums)       # True — at least one > 5\n```"),
    ex("how do i use zip_longest", "```python\nfrom itertools import zip_longest\n\na = [1, 2, 3]\nb = ['a', 'b']\nlist(zip_longest(a, b, fillvalue=0))\n# [(1, 'a'), (2, 'b'), (3, 0)]\n```"),
    ex("how do i flatten a dict", "```python\ndef flatten(d, parent='', sep='.'):\n    items = {}\n    for k, v in d.items():\n        key = f'{parent}{sep}{k}' if parent else k\n        if isinstance(v, dict):\n            items.update(flatten(v, key, sep))\n        else:\n            items[key] = v\n    return items\n\nflatten({'a': {'b': 1, 'c': 2}, 'd': 3})\n# {'a.b': 1, 'a.c': 2, 'd': 3}\n```"),
    ex("how do i transpose a matrix", "```python\nmatrix = [[1, 2, 3], [4, 5, 6]]\ntransposed = list(zip(*matrix))\n# [(1, 4), (2, 5), (3, 6)]\n```"),
    ex("how do i group a list into chunks", "```python\nfrom itertools import batched  # Python 3.12+\n\n# For older Python:\ndef chunks(lst, n):\n    for i in range(0, len(lst), n):\n        yield lst[i:i+n]\n```"),
]

# ── Type hints extras ─────────────────────────────────────────────────────────
examples += [
    ex("what is TypeVar", "`TypeVar` lets you write generic functions:\n```python\nfrom typing import TypeVar\n\nT = TypeVar('T')\n\ndef first(lst: list[T]) -> T:\n    return lst[0]\n\nfirst([1, 2, 3])       # int\nfirst(['a', 'b'])      # str\n```"),
    ex("what is Protocol in python", "`Protocol` lets you do structural subtyping (duck typing with type hints):\n```python\nfrom typing import Protocol\n\nclass Drawable(Protocol):\n    def draw(self) -> None: ...\n\ndef render(shape: Drawable) -> None:\n    shape.draw()\n```\nAny class with a `draw()` method satisfies `Drawable`, no inheritance needed."),
    ex("what is TypedDict", "`TypedDict` lets you type-hint dictionaries with known keys:\n```python\nfrom typing import TypedDict\n\nclass UserInfo(TypedDict):\n    name: str\n    age: int\n    email: str\n\ndef greet(user: UserInfo) -> str:\n    return f'Hello, {user[\"name\"]}'\n```"),
    ex("what is Literal in typing", "`Literal` restricts a value to specific options:\n```python\nfrom typing import Literal\n\ndef set_direction(d: Literal['left', 'right', 'up', 'down']) -> None:\n    ...\n```"),
]

# ── Async extras ──────────────────────────────────────────────────────────────
examples += [
    ex("what is an event loop", "The event loop is the core of async Python — it schedules and runs coroutines:\n```python\nimport asyncio\n\nasync def main():\n    print('running')\n\nasyncio.run(main())  # starts the event loop\n```"),
    ex("how do i use asyncio.sleep", "```python\nimport asyncio\n\nasync def delayed():\n    print('starting')\n    await asyncio.sleep(2)  # non-blocking pause\n    print('done after 2s')\n```"),
    ex("how do i make async http requests", "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as r:\n            return await r.json()\n\nasyncio.run(fetch('https://api.example.com'))\n```\nInstall: `pip install aiohttp`"),
    ex("difference between async and threading", "Threading uses OS threads and shares memory — good for IO-bound tasks but has GIL limitations. Async uses a single thread with cooperative multitasking — more efficient for many concurrent IO operations but code must use `await`.\n\nUse async for many concurrent network calls; use threading/multiprocessing for CPU-bound work."),
    ex("what is the GIL", "The Global Interpreter Lock (GIL) is a mutex in CPython that allows only one thread to execute Python bytecode at a time. It prevents true parallel execution of Python threads on multiple CPU cores. Workarounds: use `multiprocessing` for CPU-bound tasks, or async for IO-bound."),
]

# ── Testing extras ────────────────────────────────────────────────────────────
examples += [
    ex("what is pytest fixture", "A fixture provides reusable setup/teardown for tests:\n```python\nimport pytest\n\n@pytest.fixture\ndef db():\n    conn = create_connection()\n    yield conn   # test runs here\n    conn.close() # teardown\n\ndef test_insert(db):\n    db.execute('INSERT ...')\n```"),
    ex("how do i parametrize a pytest test", "```python\nimport pytest\n\n@pytest.mark.parametrize('a,b,expected', [\n    (1, 2, 3),\n    (0, 0, 0),\n    (-1, 1, 0),\n])\ndef test_add(a, b, expected):\n    assert a + b == expected\n```"),
    ex("how do i test that an exception is raised", "```python\nimport pytest\n\ndef divide(a, b):\n    return a / b\n\ndef test_divide_by_zero():\n    with pytest.raises(ZeroDivisionError):\n        divide(1, 0)\n```"),
    ex("what is TDD", "Test-Driven Development: write the test first, watch it fail, then write the minimum code to make it pass, then refactor.\n1. Write a failing test\n2. Write code to pass it\n3. Refactor\n4. Repeat"),
]

# ── Advanced Python ───────────────────────────────────────────────────────────
examples += [
    ex("what is __slots__", "`__slots__` restricts an object's attributes and saves memory by avoiding a per-instance `__dict__`:\n```python\nclass Point:\n    __slots__ = ('x', 'y')\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n```"),
    ex("what is a metaclass", "A metaclass is the class of a class — it controls how classes are created:\n```python\nclass SingletonMeta(type):\n    _instances = {}\n\n    def __call__(cls, *args, **kwargs):\n        if cls not in cls._instances:\n            cls._instances[cls] = super().__call__(*args, **kwargs)\n        return cls._instances[cls]\n\nclass Config(metaclass=SingletonMeta):\n    pass\n```"),
    ex("what is __getitem__", "`__getitem__` makes your class subscriptable with `[]`:\n```python\nclass Grid:\n    def __init__(self, data):\n        self._data = data\n\n    def __getitem__(self, key):\n        return self._data[key]\n\ng = Grid([[1,2],[3,4]])\nprint(g[0])  # [1, 2]\n```"),
    ex("how do i make a class callable", "Implement `__call__`:\n```python\nclass Adder:\n    def __init__(self, n):\n        self.n = n\n\n    def __call__(self, x):\n        return x + self.n\n\nadd5 = Adder(5)\nprint(add5(10))  # 15\n```"),
    ex("what is __enter__ and __exit__", "These implement the context manager protocol for `with` statements:\n```python\nclass ManagedFile:\n    def __init__(self, path):\n        self.path = path\n\n    def __enter__(self):\n        self.file = open(self.path)\n        return self.file\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.file.close()\n        return False  # don't suppress exceptions\n\nwith ManagedFile('data.txt') as f:\n    print(f.read())\n```"),
    ex("what is lru_cache", "`@lru_cache` memoizes function results — great for recursive or expensive pure functions:\n```python\nfrom functools import lru_cache\n\n@lru_cache(maxsize=128)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n-1) + fib(n-2)\n\nfib(100)  # fast\n```"),
    ex("what is functools.partial", "`partial` pre-fills some arguments of a function:\n```python\nfrom functools import partial\n\ndef power(base, exp):\n    return base ** exp\n\nsquare = partial(power, exp=2)\ncube   = partial(power, exp=3)\n\nprint(square(4))  # 16\nprint(cube(3))    # 27\n```"),
    ex("what is operator module", "`operator` provides function versions of Python operators — useful with `map`, `sorted`, `functools.reduce`:\n```python\nimport operator\n\noperator.add(1, 2)       # 3\noperator.itemgetter(1)([10, 20, 30])  # 20\n\nsorted(users, key=operator.attrgetter('name'))\n```"),
    ex("what is __all__ in python", "`__all__` lists public names exported when someone does `from module import *`:\n```python\n# mymodule.py\n__all__ = ['PublicClass', 'public_func']\n\nclass PublicClass: ...\ndef public_func(): ...\ndef _private_func(): ...\n```"),
    ex("what is monkey patching", "Monkey patching replaces or extends code at runtime — often used in tests:\n```python\nimport mymodule\n\ndef fake_send(msg):\n    print(f'[mock] {msg}')\n\nmymodule.send = fake_send  # patch\n```"),
]

# ── Multi-turn conversations ───────────────────────────────────────────────────
multi_turn = [
    {"messages": [
        {"role": "user", "content": "how do i read a file line by line"},
        {"role": "silicat", "content": "```python\nwith open('file.txt', encoding='utf-8') as f:\n    for line in f:\n        print(line.rstrip())\n```"},
        {"role": "user", "content": "how do i skip blank lines"},
        {"role": "silicat", "content": "```python\nwith open('file.txt', encoding='utf-8') as f:\n    for line in f:\n        line = line.strip()\n        if not line:\n            continue\n        print(line)\n```"},
        {"role": "user", "content": "how do i count the non-blank lines"},
        {"role": "silicat", "content": "```python\nwith open('file.txt', encoding='utf-8') as f:\n    count = sum(1 for line in f if line.strip())\nprint(count)\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "write a function to validate an email"},
        {"role": "silicat", "content": "```python\nimport re\n\ndef is_valid_email(email):\n    pattern = r'^[\\w.+-]+@[\\w-]+\\.[\\w.]{2,}$'\n    return bool(re.match(pattern, email))\n```"},
        {"role": "user", "content": "what about phone numbers"},
        {"role": "silicat", "content": "```python\ndef is_valid_phone(phone):\n    import re\n    # Matches formats: 123-456-7890, (123) 456-7890, +1 123 456 7890\n    pattern = r'^[+]?[\\d\\s\\-().]{7,15}$'\n    return bool(re.match(pattern, phone.strip()))\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "how do i make a simple api with fastapi"},
        {"role": "silicat", "content": "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\nitems = {}\n\n@app.get('/items/{item_id}')\ndef get_item(item_id: int):\n    return items.get(item_id, {'error': 'not found'})\n\n@app.post('/items/{item_id}')\ndef create_item(item_id: int, name: str):\n    items[item_id] = name\n    return {'id': item_id, 'name': name}\n```\nRun with: `uvicorn main:app --reload`"},
        {"role": "user", "content": "how do i add a database to it"},
        {"role": "silicat", "content": "```python\nfrom fastapi import FastAPI\nfrom sqlalchemy import create_engine, Column, Integer, String\nfrom sqlalchemy.orm import DeclarativeBase, Session\n\nengine = create_engine('sqlite:///./db.sqlite')\n\nclass Base(DeclarativeBase):\n    pass\n\nclass Item(Base):\n    __tablename__ = 'items'\n    id = Column(Integer, primary_key=True)\n    name = Column(String)\n\nBase.metadata.create_all(engine)\napp = FastAPI()\n\n@app.post('/items')\ndef create(name: str):\n    with Session(engine) as s:\n        item = Item(name=name)\n        s.add(item)\n        s.commit()\n        s.refresh(item)\n        return {'id': item.id, 'name': item.name}\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "write a class for a shopping cart"},
        {"role": "silicat", "content": "```python\nclass ShoppingCart:\n    def __init__(self):\n        self.items = {}\n\n    def add(self, name, price, qty=1):\n        if name in self.items:\n            self.items[name]['qty'] += qty\n        else:\n            self.items[name] = {'price': price, 'qty': qty}\n\n    def remove(self, name):\n        self.items.pop(name, None)\n\n    def total(self):\n        return sum(i['price'] * i['qty'] for i in self.items.values())\n\n    def __str__(self):\n        lines = [f\"{n}: {i['qty']} x ${i['price']:.2f}\" for n, i in self.items.items()]\n        return '\\n'.join(lines) + f'\\nTotal: ${self.total():.2f}'\n```"},
        {"role": "user", "content": "add a discount method"},
        {"role": "silicat", "content": "```python\ndef apply_discount(self, percent):\n    \"\"\"Apply a percentage discount (0-100) to the total.\"\"\"\n    if not 0 <= percent <= 100:\n        raise ValueError('percent must be 0-100')\n    self._discount = percent / 100\n\ndef total(self):\n    subtotal = sum(i['price'] * i['qty'] for i in self.items.values())\n    return subtotal * (1 - getattr(self, '_discount', 0))\n```\nAdd these methods to the class."},
    ]},
    {"messages": [
        {"role": "user", "content": "how do i sort a list of people by age"},
        {"role": "silicat", "content": "```python\npeople = [\n    {'name': 'Alice', 'age': 30},\n    {'name': 'Bob', 'age': 25},\n    {'name': 'Carol', 'age': 35},\n]\npeople.sort(key=lambda p: p['age'])\n```"},
        {"role": "user", "content": "then by name if age is the same"},
        {"role": "silicat", "content": "```python\npeople.sort(key=lambda p: (p['age'], p['name']))\n```\nTuples compare left to right — sort by age first, then by name if ages are equal."},
        {"role": "user", "content": "how do i sort descending"},
        {"role": "silicat", "content": "```python\npeople.sort(key=lambda p: (-p['age'], p['name']))\n# or:\npeople.sort(key=lambda p: p['age'], reverse=True)\n```\nNegate numeric keys to reverse just that field while keeping others ascending."},
    ]},
    {"messages": [
        {"role": "user", "content": "what is a context manager"},
        {"role": "silicat", "content": "A context manager handles setup and teardown automatically using `with`. The most common example is file handling:\n```python\nwith open('file.txt') as f:\n    data = f.read()\n# file is closed here automatically\n```\nYou can write your own using `@contextmanager` or by implementing `__enter__` and `__exit__`."},
        {"role": "user", "content": "can i write my own"},
        {"role": "silicat", "content": "Yes — two ways:\n\n**1. Using @contextmanager:**\n```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef timer():\n    import time\n    start = time.perf_counter()\n    yield\n    print(f'elapsed: {time.perf_counter()-start:.3f}s')\n\nwith timer():\n    sum(range(1_000_000))\n```\n\n**2. Using a class:**\n```python\nclass Timer:\n    def __enter__(self):\n        import time\n        self._start = time.perf_counter()\n        return self\n\n    def __exit__(self, *_):\n        import time\n        print(f'elapsed: {time.perf_counter()-self._start:.3f}s')\n```"},
    ]},
    {"messages": [
        {"role": "user", "content": "i keep getting a RecursionError"},
        {"role": "silicat", "content": "A `RecursionError` means your recursive function has no base case or is going too deep (Python's default limit is 1000 calls).\n\nCheck that your base case is reachable:\n```python\n# Wrong — no base case:\ndef count(n):\n    return 1 + count(n - 1)\n\n# Fixed:\ndef count(n):\n    if n <= 0:\n        return 0\n    return 1 + count(n - 1)\n```"},
        {"role": "user", "content": "how do i increase the recursion limit"},
        {"role": "silicat", "content": "```python\nimport sys\nsys.setrecursionlimit(5000)\n```\nBut this is usually a band-aid. Better to convert to an iterative approach or use a stack explicitly — recursion in Python isn't tail-call optimized, so deep recursion can hit memory limits too."},
    ]},
    {"messages": [
        {"role": "user", "content": "i want to store data between runs of my script"},
        {"role": "silicat", "content": "Simplest options:\n\n**JSON file:**\n```python\nimport json\nfrom pathlib import Path\n\nSTATE_FILE = Path('state.json')\n\ndef load():\n    if STATE_FILE.exists():\n        return json.loads(STATE_FILE.read_text())\n    return {}\n\ndef save(data):\n    STATE_FILE.write_text(json.dumps(data, indent=2))\n```\n\nFor bigger data: use SQLite (`sqlite3`) or a key-value store like `shelve`."},
        {"role": "user", "content": "show me the shelve version"},
        {"role": "silicat", "content": "```python\nimport shelve\n\n# Write:\nwith shelve.open('mydata') as db:\n    db['user'] = {'name': 'Alice', 'score': 100}\n\n# Read:\nwith shelve.open('mydata') as db:\n    user = db['user']\n    print(user['name'])\n```\n`shelve` stores Python objects directly — no serialization needed. Creates a few files with your chosen name."},
    ]},
]

with JSONL.open("a", encoding="utf-8") as f:
    for item in examples:
        f.write(json.dumps(item) + "\n")
    for item in multi_turn:
        f.write(json.dumps(item) + "\n")

print(f"Added {len(examples)} single-turn + {len(multi_turn)} multi-turn examples.")
print(f"Total lines now: {sum(1 for _ in JSONL.open())}")
