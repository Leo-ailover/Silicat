"""Generate OOP / Pythonic-patterns instruction-response training data for Silicat."""
import json

examples = []


def add(user, silicat):
    examples.append({"messages": [
        {"role": "user", "content": user},
        {"role": "silicat", "content": silicat},
    ]})


def add_multi(turns):
    """turns: list of (user, silicat) tuples -> one conversation."""
    msgs = []
    for u, s in turns:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "silicat", "content": s})
    examples.append({"messages": msgs})


# ---------------------------------------------------------------------------
# 1. Basic classes / __init__ / instance vs class attributes
# ---------------------------------------------------------------------------

add(
    "Create a simple Python class called Dog with a name and a bark method.",
    "```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def bark(self):\n        return f\"{self.name} says woof!\"\n```",
)

add(
    "How do I define a class with an __init__ constructor that takes x and y?",
    "```python\nclass Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n```\n\n`__init__` runs automatically when you create an instance, e.g. `Point(1, 2)`.",
)

add(
    "Write a Car class storing make, model and year.",
    "```python\nclass Car:\n    def __init__(self, make, model, year):\n        self.make = make\n        self.model = model\n        self.year = year\n\n    def description(self):\n        return f\"{self.year} {self.make} {self.model}\"\n```",
)

add(
    "What's the difference between a class attribute and an instance attribute? Show an example.",
    "Class attributes are shared by all instances; instance attributes belong to a single object.\n\n```python\nclass Counter:\n    total = 0  # class attribute, shared\n\n    def __init__(self):\n        self.count = 0  # instance attribute, per object\n        Counter.total += 1\n\na = Counter()\nb = Counter()\nprint(Counter.total)  # 2\nprint(a.count, b.count)  # 0 0\n```",
)

add(
    "Make a BankAccount class with deposit and withdraw methods.",
    "```python\nclass BankAccount:\n    def __init__(self, balance=0):\n        self.balance = balance\n\n    def deposit(self, amount):\n        self.balance += amount\n        return self.balance\n\n    def withdraw(self, amount):\n        if amount > self.balance:\n            raise ValueError(\"Insufficient funds\")\n        self.balance -= amount\n        return self.balance\n```",
)

add(
    "Why is using a mutable default argument like a list in __init__ dangerous?",
    "Because the default is created once and shared across all instances, so mutations leak between objects. Use `None` as a sentinel instead.\n\n```python\nclass Basket:\n    def __init__(self, items=None):\n        self.items = items if items is not None else []\n```",
)

add(
    "Give me a class Temperature that stores celsius and can convert to fahrenheit.",
    "```python\nclass Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    def to_fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n```",
)

add(
    "How do I create an instance of a class and call its method?",
    "```python\nclass Greeter:\n    def __init__(self, name):\n        self.name = name\n\n    def greet(self):\n        return f\"Hello, {self.name}!\"\n\ng = Greeter(\"Ada\")\nprint(g.greet())  # Hello, Ada!\n```",
)

# ---------------------------------------------------------------------------
# 2. @property
# ---------------------------------------------------------------------------

add(
    "How do I use @property to make a read-only attribute?",
    "Decorate a method with `@property` and it becomes accessible like an attribute without parentheses.\n\n```python\nclass Circle:\n    def __init__(self, radius):\n        self._radius = radius\n\n    @property\n    def area(self):\n        return 3.14159 * self._radius ** 2\n\nc = Circle(2)\nprint(c.area)  # 12.56636\n```",
)

add(
    "Add a getter and setter for a private _name field using property.",
    "```python\nclass Person:\n    def __init__(self, name):\n        self._name = name\n\n    @property\n    def name(self):\n        return self._name\n\n    @name.setter\n    def name(self, value):\n        if not value:\n            raise ValueError(\"name cannot be empty\")\n        self._name = value\n```",
)

add(
    "Use a property to validate that age is non-negative.",
    "```python\nclass Person:\n    def __init__(self, age):\n        self.age = age  # goes through the setter\n\n    @property\n    def age(self):\n        return self._age\n\n    @age.setter\n    def age(self, value):\n        if value < 0:\n            raise ValueError(\"age must be non-negative\")\n        self._age = value\n```",
)

add(
    "How can I make a computed property for full_name from first and last name?",
    "```python\nclass User:\n    def __init__(self, first, last):\n        self.first = first\n        self.last = last\n\n    @property\n    def full_name(self):\n        return f\"{self.first} {self.last}\"\n```",
)

add(
    "Show me a property with a deleter.",
    "```python\nclass Resource:\n    def __init__(self, data):\n        self._data = data\n\n    @property\n    def data(self):\n        return self._data\n\n    @data.deleter\n    def data(self):\n        print(\"releasing data\")\n        del self._data\n```",
)

add(
    "Make Temperature with a fahrenheit property that reads and writes the underlying celsius.",
    "```python\nclass Temperature:\n    def __init__(self, celsius=0):\n        self.celsius = celsius\n\n    @property\n    def fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n\n    @fahrenheit.setter\n    def fahrenheit(self, value):\n        self.celsius = (value - 32) * 5 / 9\n```",
)

# ---------------------------------------------------------------------------
# 3. @staticmethod / @classmethod
# ---------------------------------------------------------------------------

add(
    "What's the difference between @staticmethod and @classmethod?",
    "A `@classmethod` receives the class as its first argument (`cls`) and can access/modify class state or build instances; a `@staticmethod` receives neither `self` nor `cls` and is just a function namespaced in the class.\n\n```python\nclass Demo:\n    @classmethod\n    def from_class(cls):\n        return cls()\n\n    @staticmethod\n    def helper(x):\n        return x * 2\n```",
)

add(
    "Add a classmethod factory that builds a Date from a string 'YYYY-MM-DD'.",
    "```python\nclass Date:\n    def __init__(self, year, month, day):\n        self.year = year\n        self.month = month\n        self.day = day\n\n    @classmethod\n    def from_string(cls, s):\n        year, month, day = map(int, s.split(\"-\"))\n        return cls(year, month, day)\n```",
)

add(
    "Write a staticmethod that checks if a year is a leap year.",
    "```python\nclass Calendar:\n    @staticmethod\n    def is_leap_year(year):\n        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n```",
)

add(
    "Use a classmethod to count how many instances of a class were created.",
    "```python\nclass Widget:\n    _count = 0\n\n    def __init__(self):\n        Widget._count += 1\n\n    @classmethod\n    def instance_count(cls):\n        return cls._count\n```",
)

add(
    "Give me an alternative constructor using classmethod that creates a square from a side length.",
    "```python\nclass Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    @classmethod\n    def square(cls, side):\n        return cls(side, side)\n```",
)

# ---------------------------------------------------------------------------
# 4. Inheritance / super / overriding
# ---------------------------------------------------------------------------

add(
    "How do I make a class inherit from another and call the parent's __init__?",
    "```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n\nclass Dog(Animal):\n    def __init__(self, name, breed):\n        super().__init__(name)\n        self.breed = breed\n```\n\n`super().__init__(...)` runs the parent constructor so you don't duplicate its logic.",
)

add(
    "Override a method in a subclass but still call the parent version.",
    "```python\nclass Base:\n    def greet(self):\n        return \"Hello\"\n\nclass Loud(Base):\n    def greet(self):\n        return super().greet().upper() + \"!!!\"\n```",
)

add(
    "Create an Employee base class and a Manager subclass that adds a team list.",
    "```python\nclass Employee:\n    def __init__(self, name, salary):\n        self.name = name\n        self.salary = salary\n\nclass Manager(Employee):\n    def __init__(self, name, salary, team=None):\n        super().__init__(name, salary)\n        self.team = team or []\n\n    def add_report(self, employee):\n        self.team.append(employee)\n```",
)

add(
    "What is method resolution order (MRO) and how do I see it?",
    "MRO is the order Python searches base classes for attributes/methods, computed with the C3 linearization. View it with `ClassName.__mro__` or `ClassName.mro()`.\n\n```python\nclass A: pass\nclass B(A): pass\nclass C(A): pass\nclass D(B, C): pass\n\nprint([c.__name__ for c in D.__mro__])\n# ['D', 'B', 'C', 'A', 'object']\n```",
)

add(
    "Show diamond inheritance and how super() cooperates.",
    "```python\nclass A:\n    def __init__(self):\n        print(\"A\")\n        super().__init__()\n\nclass B(A):\n    def __init__(self):\n        print(\"B\")\n        super().__init__()\n\nclass C(A):\n    def __init__(self):\n        print(\"C\")\n        super().__init__()\n\nclass D(B, C):\n    def __init__(self):\n        print(\"D\")\n        super().__init__()\n\nD()  # prints D, B, C, A — each runs once thanks to the MRO\n```",
)

add(
    "Demonstrate a mixin class in Python.",
    "A mixin provides reusable behavior to be combined with other classes via multiple inheritance.\n\n```python\nclass JSONSerializableMixin:\n    def to_json(self):\n        import json\n        return json.dumps(self.__dict__)\n\nclass User(JSONSerializableMixin):\n    def __init__(self, name):\n        self.name = name\n\nprint(User(\"Ada\").to_json())  # {\"name\": \"Ada\"}\n```",
)

add(
    "How do I check if an object is an instance of a class or its subclass?",
    "```python\nisinstance(obj, MyClass)      # True for instances and subclass instances\nissubclass(SubClass, MyClass) # True if SubClass derives from MyClass\n```",
)

# ---------------------------------------------------------------------------
# 5. Dunder methods
# ---------------------------------------------------------------------------

add(
    "Add __str__ and __repr__ to a Point class. What's the difference?",
    "`__str__` is the readable/user-facing string; `__repr__` is the unambiguous developer/debug string (ideally valid Python). `print()` uses `__str__`, the REPL and containers use `__repr__`.\n\n```python\nclass Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __str__(self):\n        return f\"({self.x}, {self.y})\"\n\n    def __repr__(self):\n        return f\"Point({self.x!r}, {self.y!r})\"\n```",
)

add(
    "Implement __eq__ so two Money objects compare equal by amount.",
    "```python\nclass Money:\n    def __init__(self, amount):\n        self.amount = amount\n\n    def __eq__(self, other):\n        if not isinstance(other, Money):\n            return NotImplemented\n        return self.amount == other.amount\n```\n\nWhen you define `__eq__` you should usually also define `__hash__` if instances need to be hashable.",
)

add(
    "Make a Vector class support + with __add__.",
    "```python\nclass Vector:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\n    def __repr__(self):\n        return f\"Vector({self.x}, {self.y})\"\n```",
)

add(
    "Implement __len__ so len() works on my Playlist class.",
    "```python\nclass Playlist:\n    def __init__(self):\n        self.songs = []\n\n    def __len__(self):\n        return len(self.songs)\n```",
)

add(
    "Add __getitem__ and __setitem__ so I can index into my Grid class.",
    "```python\nclass Grid:\n    def __init__(self, rows, cols):\n        self._cells = [[0] * cols for _ in range(rows)]\n\n    def __getitem__(self, pos):\n        r, c = pos\n        return self._cells[r][c]\n\n    def __setitem__(self, pos, value):\n        r, c = pos\n        self._cells[r][c] = value\n\ng = Grid(2, 2)\ng[0, 1] = 5\nprint(g[0, 1])  # 5\n```",
)

add(
    "Make my class iterable with __iter__ and __next__.",
    "```python\nclass Countdown:\n    def __init__(self, start):\n        self.current = start\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.current <= 0:\n            raise StopIteration\n        self.current -= 1\n        return self.current + 1\n\nfor n in Countdown(3):\n    print(n)  # 3, 2, 1\n```",
)

add(
    "How do I make an object callable like a function with __call__?",
    "```python\nclass Multiplier:\n    def __init__(self, factor):\n        self.factor = factor\n\n    def __call__(self, x):\n        return x * self.factor\n\ndouble = Multiplier(2)\nprint(double(10))  # 20\n```",
)

add(
    "Implement __lt__ so I can sort a list of Person by age.",
    "```python\nfrom functools import total_ordering\n\n@total_ordering\nclass Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n    def __eq__(self, other):\n        return self.age == other.age\n\n    def __lt__(self, other):\n        return self.age < other.age\n```\n\n`@total_ordering` fills in `>`, `>=`, `<=` from `__eq__` and `__lt__`.",
)

add(
    "Add __contains__ so the `in` operator works on my custom collection.",
    "```python\nclass Inventory:\n    def __init__(self):\n        self.items = set()\n\n    def __contains__(self, item):\n        return item in self.items\n\ninv = Inventory()\ninv.items.add(\"sword\")\nprint(\"sword\" in inv)  # True\n```",
)

add(
    "Define __hash__ and __eq__ together so my objects work as dict keys.",
    "```python\nclass Coord:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __eq__(self, other):\n        return (self.x, self.y) == (other.x, other.y)\n\n    def __hash__(self):\n        return hash((self.x, self.y))\n```\n\nObjects that compare equal must have equal hashes, so base both on the same fields.",
)

add(
    "Implement __enter__ and __exit__ to make a class usable with `with`.",
    "```python\nclass Timer:\n    def __enter__(self):\n        import time\n        self.start = time.perf_counter()\n        return self\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        import time\n        self.elapsed = time.perf_counter() - self.start\n        print(f\"Elapsed: {self.elapsed:.4f}s\")\n        return False  # don't suppress exceptions\n```",
)

add(
    "Add __bool__ so an empty cart is falsy.",
    "```python\nclass Cart:\n    def __init__(self):\n        self.items = []\n\n    def __bool__(self):\n        return bool(self.items)\n\nc = Cart()\nprint(bool(c))  # False\n```",
)

add(
    "Make __getattr__ return a default for missing attributes.",
    "`__getattr__` is only called when normal lookup fails.\n\n```python\nclass DefaultDict:\n    def __init__(self):\n        self._data = {}\n\n    def __getattr__(self, name):\n        return self._data.get(name, None)\n```",
)

add(
    "Implement __add__, __radd__ so sum() works on Money.",
    "```python\nclass Money:\n    def __init__(self, amount):\n        self.amount = amount\n\n    def __add__(self, other):\n        other_amt = other.amount if isinstance(other, Money) else other\n        return Money(self.amount + other_amt)\n\n    def __radd__(self, other):  # supports sum() which starts at 0\n        return self.__add__(other)\n\n    def __repr__(self):\n        return f\"Money({self.amount})\"\n\nprint(sum([Money(1), Money(2)]))  # Money(3)\n```",
)

# ---------------------------------------------------------------------------
# 6. dataclasses
# ---------------------------------------------------------------------------

add(
    "Convert a Point class to a dataclass.",
    "```python\nfrom dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n```\n\n`@dataclass` auto-generates `__init__`, `__repr__`, and `__eq__`.",
)

add(
    "Make a frozen dataclass that is immutable and hashable.",
    "```python\nfrom dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Color:\n    r: int\n    g: int\n    b: int\n```\n\n`frozen=True` blocks attribute assignment and makes instances hashable so they can be set/dict keys.",
)

add(
    "Use dataclass field with a default_factory for a list.",
    "```python\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass Team:\n    name: str\n    members: list = field(default_factory=list)\n```\n\nUse `default_factory` for mutable defaults so each instance gets its own list.",
)

add(
    "How do I add a derived field in a dataclass using __post_init__?",
    "```python\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass Rectangle:\n    width: float\n    height: float\n    area: float = field(init=False)\n\n    def __post_init__(self):\n        self.area = self.width * self.height\n```",
)

add(
    "Make a dataclass orderable so I can sort instances.",
    "```python\nfrom dataclasses import dataclass\n\n@dataclass(order=True)\nclass Version:\n    major: int\n    minor: int\n    patch: int\n```\n\n`order=True` generates `__lt__`, `__le__`, `__gt__`, `__ge__` comparing fields as a tuple.",
)

add(
    "Exclude a field from the dataclass repr.",
    "```python\nfrom dataclasses import dataclass, field\n\n@dataclass\nclass User:\n    name: str\n    password: str = field(repr=False)\n```",
)

add(
    "Give a dataclass a default value for one field.",
    "```python\nfrom dataclasses import dataclass\n\n@dataclass\nclass Config:\n    host: str\n    port: int = 8080\n    debug: bool = False\n```",
)

add(
    "Convert a dataclass instance to a dictionary.",
    "```python\nfrom dataclasses import dataclass, asdict\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n\nprint(asdict(Point(1, 2)))  # {'x': 1, 'y': 2}\n```",
)

# ---------------------------------------------------------------------------
# 7. namedtuple / enum
# ---------------------------------------------------------------------------

add(
    "Create a namedtuple for a 2D point.",
    "```python\nfrom collections import namedtuple\n\nPoint = namedtuple(\"Point\", [\"x\", \"y\"])\np = Point(1, 2)\nprint(p.x, p.y)  # 1 2\n```",
)

add(
    "Show the typing.NamedTuple class syntax.",
    "```python\nfrom typing import NamedTuple\n\nclass Point(NamedTuple):\n    x: int\n    y: int\n    label: str = \"origin\"\n```",
)

add(
    "Create an Enum for the days of the week.",
    "```python\nfrom enum import Enum\n\nclass Weekday(Enum):\n    MONDAY = 1\n    TUESDAY = 2\n    WEDNESDAY = 3\n    THURSDAY = 4\n    FRIDAY = 5\n    SATURDAY = 6\n    SUNDAY = 7\n```",
)

add(
    "Use enum.auto() so I don't have to assign values manually.",
    "```python\nfrom enum import Enum, auto\n\nclass Color(Enum):\n    RED = auto()\n    GREEN = auto()\n    BLUE = auto()\n```",
)

add(
    "Make an enum where members are also strings (StrEnum).",
    "```python\nfrom enum import StrEnum\n\nclass Status(StrEnum):\n    ACTIVE = \"active\"\n    INACTIVE = \"inactive\"\n\nprint(Status.ACTIVE == \"active\")  # True\n```",
)

add(
    "How do I iterate over enum members and look one up by value?",
    "```python\nfrom enum import Enum\n\nclass Color(Enum):\n    RED = 1\n    GREEN = 2\n\nfor c in Color:\n    print(c.name, c.value)\n\nprint(Color(1))        # Color.RED  (lookup by value)\nprint(Color[\"GREEN\"])  # Color.GREEN (lookup by name)\n```",
)

add(
    "Create a Flag enum for combinable permissions.",
    "```python\nfrom enum import Flag, auto\n\nclass Permission(Flag):\n    READ = auto()\n    WRITE = auto()\n    EXECUTE = auto()\n\np = Permission.READ | Permission.WRITE\nprint(Permission.READ in p)  # True\n```",
)

# ---------------------------------------------------------------------------
# 8. ABC / abstractmethod
# ---------------------------------------------------------------------------

add(
    "How do I create an abstract base class with an abstract method?",
    "```python\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        ...\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        return self.side ** 2\n```\n\nYou cannot instantiate `Shape` directly; subclasses must implement every abstract method.",
)

add(
    "Combine abstractmethod with property.",
    "```python\nfrom abc import ABC, abstractmethod\n\nclass Animal(ABC):\n    @property\n    @abstractmethod\n    def sound(self):\n        ...\n\nclass Cat(Animal):\n    @property\n    def sound(self):\n        return \"meow\"\n```",
)

add(
    "Why can't I instantiate my abstract class? Show the error scenario.",
    "An ABC with unimplemented abstract methods raises `TypeError` on instantiation.\n\n```python\nfrom abc import ABC, abstractmethod\n\nclass Base(ABC):\n    @abstractmethod\n    def run(self): ...\n\nBase()  # TypeError: Can't instantiate abstract class Base with abstract method run\n```",
)

add(
    "Define an interface-like ABC for a repository with save and get.",
    "```python\nfrom abc import ABC, abstractmethod\n\nclass Repository(ABC):\n    @abstractmethod\n    def save(self, entity): ...\n\n    @abstractmethod\n    def get(self, id): ...\n```",
)

# ---------------------------------------------------------------------------
# 9. __slots__
# ---------------------------------------------------------------------------

add(
    "What does __slots__ do and how do I use it?",
    "`__slots__` declares a fixed set of attributes, saving memory by avoiding a per-instance `__dict__` and preventing new attributes.\n\n```python\nclass Point:\n    __slots__ = (\"x\", \"y\")\n\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n```",
)

add(
    "Add __slots__ to a class with many instances to save memory.",
    "```python\nclass Particle:\n    __slots__ = (\"x\", \"y\", \"vx\", \"vy\")\n\n    def __init__(self, x, y, vx, vy):\n        self.x, self.y = x, y\n        self.vx, self.vy = vx, vy\n```",
)

add(
    "Use __slots__ with a dataclass.",
    "In Python 3.10+ you can pass `slots=True` to the decorator.\n\n```python\nfrom dataclasses import dataclass\n\n@dataclass(slots=True)\nclass Point:\n    x: int\n    y: int\n```",
)

# ---------------------------------------------------------------------------
# 10. descriptors
# ---------------------------------------------------------------------------

add(
    "Show me a simple descriptor that validates a positive number.",
    "A descriptor is a class implementing `__get__`/`__set__` used as a class attribute to control access.\n\n```python\nclass Positive:\n    def __set_name__(self, owner, name):\n        self.name = \"_\" + name\n\n    def __get__(self, obj, objtype=None):\n        return getattr(obj, self.name)\n\n    def __set__(self, obj, value):\n        if value <= 0:\n            raise ValueError(\"must be positive\")\n        setattr(obj, self.name, value)\n\nclass Account:\n    balance = Positive()\n\n    def __init__(self, balance):\n        self.balance = balance\n```",
)

add(
    "Write a descriptor that logs every access to an attribute.",
    "```python\nclass LoggedAccess:\n    def __set_name__(self, owner, name):\n        self.public_name = name\n        self.private_name = \"_\" + name\n\n    def __get__(self, obj, objtype=None):\n        value = getattr(obj, self.private_name)\n        print(f\"get {self.public_name} -> {value}\")\n        return value\n\n    def __set__(self, obj, value):\n        print(f\"set {self.public_name} = {value}\")\n        setattr(obj, self.private_name, value)\n```",
)

# ---------------------------------------------------------------------------
# 11. context managers (class-based and @contextmanager) - 8+ variations
# ---------------------------------------------------------------------------

add(
    "Write a context manager using contextlib.contextmanager.",
    "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef managed_resource(name):\n    print(f\"acquire {name}\")\n    try:\n        yield name\n    finally:\n        print(f\"release {name}\")\n```",
)

add(
    "Create a class-based context manager that opens and closes a file-like resource.",
    "```python\nclass FileManager:\n    def __init__(self, path, mode):\n        self.path = path\n        self.mode = mode\n\n    def __enter__(self):\n        self.file = open(self.path, self.mode)\n        return self.file\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.file.close()\n        return False\n```",
)

add(
    "Make a context manager that times a block of code.",
    "```python\nimport time\nfrom contextlib import contextmanager\n\n@contextmanager\ndef timer(label):\n    start = time.perf_counter()\n    try:\n        yield\n    finally:\n        print(f\"{label}: {time.perf_counter() - start:.4f}s\")\n```",
)

add(
    "Context manager that temporarily changes the working directory and restores it.",
    "```python\nimport os\nfrom contextlib import contextmanager\n\n@contextmanager\ndef chdir(path):\n    old = os.getcwd()\n    os.chdir(path)\n    try:\n        yield\n    finally:\n        os.chdir(old)\n```",
)

add(
    "How do I suppress a specific exception with a context manager?",
    "```python\nfrom contextlib import suppress\n\nwith suppress(FileNotFoundError):\n    open(\"missing.txt\")\n# no error raised\n```",
)

add(
    "Write a context manager that suppresses exceptions by returning True from __exit__.",
    "Returning a truthy value from `__exit__` swallows the exception raised inside the `with` block.\n\n```python\nclass IgnoreErrors:\n    def __enter__(self):\n        return self\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        return exc_type is not None  # suppress any exception\n```",
)

add(
    "Make a reentrant context manager for a database transaction with commit/rollback.",
    "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef transaction(conn):\n    try:\n        yield conn\n        conn.commit()\n    except Exception:\n        conn.rollback()\n        raise\n```",
)

add(
    "Use contextlib.ExitStack to manage a dynamic number of context managers.",
    "```python\nfrom contextlib import ExitStack\n\ndef open_all(paths):\n    with ExitStack() as stack:\n        files = [stack.enter_context(open(p)) for p in paths]\n        # all files are open here\n        return [f.read() for f in files]\n    # all files closed on exit\n```",
)

add(
    "Create a context manager that acquires and releases a threading lock.",
    "```python\nfrom contextlib import contextmanager\nimport threading\n\n@contextmanager\ndef locked(lock: threading.Lock):\n    lock.acquire()\n    try:\n        yield\n    finally:\n        lock.release()\n```",
)

add(
    "Make a context manager class that redirects something on enter and resets on exit.",
    "```python\nclass Indent:\n    level = 0\n\n    def __enter__(self):\n        Indent.level += 1\n        return self\n\n    def __exit__(self, *exc):\n        Indent.level -= 1\n        return False\n\n    def print(self, msg):\n        print(\"  \" * Indent.level + msg)\n```",
)

# ---------------------------------------------------------------------------
# 12. decorators - 10+ variations
# ---------------------------------------------------------------------------

add(
    "Write a basic function decorator that logs calls.",
    "```python\nimport functools\n\ndef log_calls(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f\"calling {func.__name__}\")\n        return func(*args, **kwargs)\n    return wrapper\n```\n\n`functools.wraps` copies the original function's name and docstring onto the wrapper.",
)

add(
    "Create a decorator that times how long a function takes.",
    "```python\nimport time, functools\n\ndef timed(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        start = time.perf_counter()\n        result = func(*args, **kwargs)\n        print(f\"{func.__name__} took {time.perf_counter() - start:.4f}s\")\n        return result\n    return wrapper\n```",
)

add(
    "Write a decorator that takes an argument: repeat the function N times.",
    "```python\nimport functools\n\ndef repeat(n):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for _ in range(n):\n                result = func(*args, **kwargs)\n            return result\n        return wrapper\n    return decorator\n\n@repeat(3)\ndef greet():\n    print(\"hi\")\n```\n\nA parametrized decorator is a function returning a decorator (three nested levels).",
)

add(
    "Make a decorator that caches results (a memoize decorator).",
    "```python\nimport functools\n\ndef memoize(func):\n    cache = {}\n    @functools.wraps(func)\n    def wrapper(*args):\n        if args not in cache:\n            cache[args] = func(*args)\n        return cache[args]\n    return wrapper\n```\n\nFor production prefer the built-in `functools.lru_cache`.",
)

add(
    "How do I use functools.lru_cache?",
    "```python\nimport functools\n\n@functools.lru_cache(maxsize=128)\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n```",
)

add(
    "Write a decorator that retries a function on exception.",
    "```python\nimport functools, time\n\ndef retry(times=3, delay=1):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for attempt in range(times):\n                try:\n                    return func(*args, **kwargs)\n                except Exception:\n                    if attempt == times - 1:\n                        raise\n                    time.sleep(delay)\n        return wrapper\n    return decorator\n```",
)

add(
    "Create a class-based decorator that counts how many times a function is called.",
    "```python\nimport functools\n\nclass CountCalls:\n    def __init__(self, func):\n        functools.update_wrapper(self, func)\n        self.func = func\n        self.count = 0\n\n    def __call__(self, *args, **kwargs):\n        self.count += 1\n        return self.func(*args, **kwargs)\n```",
)

add(
    "Write a decorator that validates the first argument is positive.",
    "```python\nimport functools\n\ndef require_positive(func):\n    @functools.wraps(func)\n    def wrapper(x, *args, **kwargs):\n        if x <= 0:\n            raise ValueError(\"first argument must be positive\")\n        return func(x, *args, **kwargs)\n    return wrapper\n```",
)

add(
    "Why should I always use functools.wraps in my decorators?",
    "Without it, the wrapper replaces the original function's `__name__`, `__doc__`, and signature metadata, breaking introspection, help(), and debuggers. `functools.wraps` copies those over.\n\n```python\nimport functools\n\ndef deco(func):\n    @functools.wraps(func)\n    def wrapper(*a, **k):\n        return func(*a, **k)\n    return wrapper\n```",
)

add(
    "Make a class decorator that adds a 'created_at' timestamp to instances.",
    "A class decorator receives and returns a class.\n\n```python\nimport time\n\ndef track_creation(cls):\n    orig_init = cls.__init__\n    def new_init(self, *args, **kwargs):\n        orig_init(self, *args, **kwargs)\n        self.created_at = time.time()\n    cls.__init__ = new_init\n    return cls\n\n@track_creation\nclass Widget:\n    def __init__(self, name):\n        self.name = name\n```",
)

add(
    "Write a decorator that registers functions into a registry dict.",
    "```python\nregistry = {}\n\ndef register(name):\n    def decorator(func):\n        registry[name] = func\n        return func\n    return decorator\n\n@register(\"greet\")\ndef greet():\n    return \"hi\"\n```",
)

add(
    "Stack two decorators on one function — show the order they apply.",
    "Decorators apply bottom-up: the one closest to the function wraps first.\n\n```python\ndef bold(f):\n    return lambda: \"<b>\" + f() + \"</b>\"\n\ndef italic(f):\n    return lambda: \"<i>\" + f() + \"</i>\"\n\n@bold\n@italic\ndef text():\n    return \"hi\"\n\nprint(text())  # <b><i>hi</i></b>\n```",
)

add(
    "Create a decorator that only runs a function once and caches the result.",
    "```python\nimport functools\n\ndef run_once(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        if not wrapper.has_run:\n            wrapper.result = func(*args, **kwargs)\n            wrapper.has_run = True\n        return wrapper.result\n    wrapper.has_run = False\n    return wrapper\n```",
)

# ---------------------------------------------------------------------------
# 13. design patterns
# ---------------------------------------------------------------------------

add(
    "Implement the Singleton pattern in Python.",
    "```python\nclass Singleton:\n    _instance = None\n\n    def __new__(cls, *args, **kwargs):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n```\n\nA more Pythonic alternative is to use a module-level object, since modules are singletons.",
)

add(
    "Make a singleton using a decorator.",
    "```python\nimport functools\n\ndef singleton(cls):\n    instances = {}\n    @functools.wraps(cls)\n    def get_instance(*args, **kwargs):\n        if cls not in instances:\n            instances[cls] = cls(*args, **kwargs)\n        return instances[cls]\n    return get_instance\n\n@singleton\nclass Config:\n    pass\n```",
)

add(
    "Show me a simple factory pattern.",
    "```python\nclass Dog:\n    def speak(self): return \"woof\"\n\nclass Cat:\n    def speak(self): return \"meow\"\n\ndef animal_factory(kind):\n    animals = {\"dog\": Dog, \"cat\": Cat}\n    cls = animals.get(kind)\n    if cls is None:\n        raise ValueError(f\"unknown animal: {kind}\")\n    return cls()\n```",
)

add(
    "Implement the observer pattern.",
    "```python\nclass Subject:\n    def __init__(self):\n        self._observers = []\n\n    def subscribe(self, observer):\n        self._observers.append(observer)\n\n    def notify(self, event):\n        for obs in self._observers:\n            obs.update(event)\n\nclass Logger:\n    def update(self, event):\n        print(f\"got event: {event}\")\n```",
)

add(
    "Implement the strategy pattern for different sorting strategies.",
    "```python\nclass Sorter:\n    def __init__(self, strategy):\n        self.strategy = strategy\n\n    def sort(self, data):\n        return self.strategy(data)\n\nasc = lambda d: sorted(d)\ndesc = lambda d: sorted(d, reverse=True)\n\ns = Sorter(desc)\nprint(s.sort([3, 1, 2]))  # [3, 2, 1]\n```\n\nIn Python the strategy is often just a callable passed in, no class hierarchy needed.",
)

add(
    "Show the builder pattern with a fluent interface.",
    "```python\nclass PizzaBuilder:\n    def __init__(self):\n        self.toppings = []\n\n    def add(self, topping):\n        self.toppings.append(topping)\n        return self  # enables chaining\n\n    def build(self):\n        return f\"Pizza with {', '.join(self.toppings)}\"\n\npizza = PizzaBuilder().add(\"cheese\").add(\"basil\").build()\n```",
)

add(
    "Implement a simple decorator design pattern (wrapping objects).",
    "```python\nclass Coffee:\n    def cost(self): return 2.0\n\nclass MilkDecorator:\n    def __init__(self, coffee):\n        self._coffee = coffee\n\n    def cost(self):\n        return self._coffee.cost() + 0.5\n\ndrink = MilkDecorator(Coffee())\nprint(drink.cost())  # 2.5\n```",
)

# ---------------------------------------------------------------------------
# 14. composition vs inheritance / encapsulation
# ---------------------------------------------------------------------------

add(
    "Show composition instead of inheritance for a Car that has an Engine.",
    "Composition models a 'has-a' relationship and is often more flexible than inheritance.\n\n```python\nclass Engine:\n    def start(self):\n        return \"engine started\"\n\nclass Car:\n    def __init__(self):\n        self.engine = Engine()  # has-a\n\n    def start(self):\n        return self.engine.start()\n```",
)

add(
    "How do I make an attribute 'private' in Python?",
    "Python has no true private, but a leading underscore signals 'internal', and a double underscore triggers name mangling.\n\n```python\nclass Account:\n    def __init__(self):\n        self._balance = 0      # convention: protected\n        self.__secret = \"abc\"  # name-mangled to _Account__secret\n```",
)

add(
    "Explain name mangling with double underscore attributes.",
    "A name with two leading underscores (and at most one trailing) is rewritten to `_ClassName__name`, avoiding accidental clashes in subclasses.\n\n```python\nclass A:\n    def __init__(self):\n        self.__x = 1\n\na = A()\nprint(a._A__x)  # 1  (accessible via the mangled name)\n```",
)

# ---------------------------------------------------------------------------
# Generated/systematic variations to reach volume
# ---------------------------------------------------------------------------

# Many simple "create a class X with Y" prompts
simple_classes = [
    ("Stack", "push and pop", "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        return self._items.pop()\n\n    def is_empty(self):\n        return not self._items\n```"),
    ("Queue", "enqueue and dequeue", "```python\nfrom collections import deque\n\nclass Queue:\n    def __init__(self):\n        self._items = deque()\n\n    def enqueue(self, item):\n        self._items.append(item)\n\n    def dequeue(self):\n        return self._items.popleft()\n```"),
    ("LinkedList", "append and __iter__", "```python\nclass Node:\n    def __init__(self, value, next=None):\n        self.value = value\n        self.next = next\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n\n    def append(self, value):\n        node = Node(value)\n        if self.head is None:\n            self.head = node\n            return\n        cur = self.head\n        while cur.next:\n            cur = cur.next\n        cur.next = node\n\n    def __iter__(self):\n        cur = self.head\n        while cur:\n            yield cur.value\n            cur = cur.next\n```"),
    ("Rectangle", "area and perimeter methods", "```python\nclass Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def area(self):\n        return self.width * self.height\n\n    def perimeter(self):\n        return 2 * (self.width + self.height)\n```"),
    ("Circle", "an area property", "```python\nimport math\n\nclass Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    @property\n    def area(self):\n        return math.pi * self.radius ** 2\n```"),
    ("Matrix", "addition via __add__", "```python\nclass Matrix:\n    def __init__(self, rows):\n        self.rows = rows\n\n    def __add__(self, other):\n        return Matrix([\n            [a + b for a, b in zip(r1, r2)]\n            for r1, r2 in zip(self.rows, other.rows)\n        ])\n```"),
    ("ShoppingCart", "add_item and total", "```python\nclass ShoppingCart:\n    def __init__(self):\n        self.items = {}\n\n    def add_item(self, name, price, qty=1):\n        self.items[name] = self.items.get(name, 0) + price * qty\n\n    def total(self):\n        return sum(self.items.values())\n```"),
    ("Stopwatch", "start, stop and elapsed", "```python\nimport time\n\nclass Stopwatch:\n    def __init__(self):\n        self._start = None\n        self._elapsed = 0.0\n\n    def start(self):\n        self._start = time.perf_counter()\n\n    def stop(self):\n        self._elapsed += time.perf_counter() - self._start\n        self._start = None\n\n    @property\n    def elapsed(self):\n        return self._elapsed\n```"),
    ("EventEmitter", "on and emit", "```python\nclass EventEmitter:\n    def __init__(self):\n        self._handlers = {}\n\n    def on(self, event, handler):\n        self._handlers.setdefault(event, []).append(handler)\n\n    def emit(self, event, *args):\n        for handler in self._handlers.get(event, []):\n            handler(*args)\n```"),
    ("Stack", "push, pop and __len__", "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, x):\n        self._items.append(x)\n\n    def pop(self):\n        return self._items.pop()\n\n    def __len__(self):\n        return len(self._items)\n```"),
    ("Fraction", "addition and __repr__", "```python\nfrom math import gcd\n\nclass Fraction:\n    def __init__(self, num, den):\n        g = gcd(num, den)\n        self.num = num // g\n        self.den = den // g\n\n    def __add__(self, other):\n        return Fraction(self.num * other.den + other.num * self.den,\n                        self.den * other.den)\n\n    def __repr__(self):\n        return f\"{self.num}/{self.den}\"\n```"),
    ("RingBuffer", "append with fixed capacity", "```python\nfrom collections import deque\n\nclass RingBuffer:\n    def __init__(self, capacity):\n        self._buf = deque(maxlen=capacity)\n\n    def append(self, item):\n        self._buf.append(item)\n\n    def items(self):\n        return list(self._buf)\n```"),
]

phrasings = [
    "Write a {name} class with {feat}.",
    "Create a Python {name} class that supports {feat}.",
    "I need a {name} class with {feat}.",
    "Give me a {name} implementation with {feat}.",
    "How do I implement a {name} class with {feat}?",
]

for i, (name, feat, code) in enumerate(simple_classes):
    p = phrasings[i % len(phrasings)]
    add(p.format(name=name, feat=feat), code)

# dunder method one-liner variations
dunders = [
    ("__str__", "return a human-readable string", "Book", "title", "```python\nclass Book:\n    def __init__(self, title):\n        self.title = title\n\n    def __str__(self):\n        return f\"Book: {self.title}\"\n```"),
    ("__repr__", "return an unambiguous representation", "Book", "title", "```python\nclass Book:\n    def __init__(self, title):\n        self.title = title\n\n    def __repr__(self):\n        return f\"Book(title={self.title!r})\"\n```"),
    ("__eq__", "compare by value", "Tag", "label", "```python\nclass Tag:\n    def __init__(self, label):\n        self.label = label\n\n    def __eq__(self, other):\n        return isinstance(other, Tag) and self.label == other.label\n```"),
    ("__len__", "report the number of stored items", "Box", "contents", "```python\nclass Box:\n    def __init__(self):\n        self.contents = []\n\n    def __len__(self):\n        return len(self.contents)\n```"),
    ("__getitem__", "support indexing", "Deck", "cards", "```python\nclass Deck:\n    def __init__(self, cards):\n        self.cards = cards\n\n    def __getitem__(self, index):\n        return self.cards[index]\n```"),
    ("__iter__", "be iterable with yield", "Tree", "values", "```python\nclass Tree:\n    def __init__(self, values):\n        self.values = values\n\n    def __iter__(self):\n        yield from self.values\n```"),
    ("__call__", "be callable", "Adder", "n", "```python\nclass Adder:\n    def __init__(self, n):\n        self.n = n\n\n    def __call__(self, x):\n        return x + self.n\n```"),
    ("__contains__", "support the in operator", "Bag", "elements", "```python\nclass Bag:\n    def __init__(self):\n        self.elements = []\n\n    def __contains__(self, item):\n        return item in self.elements\n```"),
    ("__hash__", "be hashable based on an id", "Entity", "id", "```python\nclass Entity:\n    def __init__(self, id):\n        self.id = id\n\n    def __hash__(self):\n        return hash(self.id)\n\n    def __eq__(self, other):\n        return isinstance(other, Entity) and self.id == other.id\n```"),
    ("__mul__", "support multiplication by a scalar", "Vec", "data", "```python\nclass Vec:\n    def __init__(self, data):\n        self.data = data\n\n    def __mul__(self, scalar):\n        return Vec([x * scalar for x in self.data])\n```"),
    ("__sub__", "support subtraction", "Money", "cents", "```python\nclass Money:\n    def __init__(self, cents):\n        self.cents = cents\n\n    def __sub__(self, other):\n        return Money(self.cents - other.cents)\n```"),
    ("__neg__", "support unary negation", "Temp", "value", "```python\nclass Temp:\n    def __init__(self, value):\n        self.value = value\n\n    def __neg__(self):\n        return Temp(-self.value)\n```"),
    ("__getitem__ and __len__", "act like a sequence", "Sentence", "words", "```python\nclass Sentence:\n    def __init__(self, text):\n        self.words = text.split()\n\n    def __getitem__(self, i):\n        return self.words[i]\n\n    def __len__(self):\n        return len(self.words)\n```"),
    ("__format__", "support custom format specs", "Money", "amount", "```python\nclass Money:\n    def __init__(self, amount):\n        self.amount = amount\n\n    def __format__(self, spec):\n        return format(self.amount, spec)\n```"),
]

dphrasings = [
    "Implement {d} on a {cls} class so it can {feat}.",
    "Add {d} to {cls} to {feat}.",
    "How do I make {cls} {feat} using {d}?",
    "Give me a {cls} class that uses {d} to {feat}.",
    "Show {d} on a {cls} so instances {feat}.",
]
for i, (d, feat, cls, attr, code) in enumerate(dunders):
    p = dphrasings[i % len(dphrasings)]
    add(p.format(d=d, cls=cls, feat=feat), code)

# property variations
prop_specs = [
    ("speed", "must be non-negative", "Vehicle", "value < 0", '"speed cannot be negative"'),
    ("email", "must contain @", "User", '"@" not in value', '"invalid email"'),
    ("percentage", "must be between 0 and 100", "Grade", "not 0 <= value <= 100", '"out of range"'),
    ("price", "must be positive", "Product", "value <= 0", '"price must be positive"'),
    ("username", "must not be empty", "Profile", "not value", '"username required"'),
    ("quantity", "must be an int", "Order", "not isinstance(value, int)", '"quantity must be int"'),
]
for i, (field, rule, cls, cond, msg) in enumerate(prop_specs):
    code = (
        "```python\n"
        f"class {cls}:\n"
        f"    def __init__(self, {field}):\n"
        f"        self.{field} = {field}\n\n"
        f"    @property\n"
        f"    def {field}(self):\n"
        f"        return self._{field}\n\n"
        f"    @{field}.setter\n"
        f"    def {field}(self, value):\n"
        f"        if {cond}:\n"
        f"            raise ValueError({msg})\n"
        f"        self._{field} = value\n"
        "```"
    )
    pp = [
        f"Add a validated property for {field} on {cls} that {rule}.",
        f"Use @property so {cls}.{field} {rule}.",
        f"Make {field} on {cls} a property that validates it {rule}.",
    ]
    add(pp[i % len(pp)], code)

# dataclass variations
dc_specs = [
    ("Point3D", [("x", "float"), ("y", "float"), ("z", "float")], "@dataclass", ""),
    ("Employee", [("name", "str"), ("salary", "float"), ("active", "bool = True")], "@dataclass", ""),
    ("RGB", [("r", "int"), ("g", "int"), ("b", "int")], "@dataclass(frozen=True)", "an immutable"),
    ("SemVer", [("major", "int"), ("minor", "int"), ("patch", "int")], "@dataclass(order=True)", "an orderable"),
    ("Settings", [("debug", "bool = False"), ("level", "int = 1")], "@dataclass", ""),
    ("Card", [("rank", "str"), ("suit", "str")], "@dataclass(frozen=True)", "a frozen"),
]
for i, (cls, fields, deco, adj) in enumerate(dc_specs):
    fieldlines = "\n".join(f"    {n}: {t}" for n, t in fields)
    code = f"```python\nfrom dataclasses import dataclass\n\n{deco}\nclass {cls}:\n{fieldlines}\n```"
    pp = [
        f"Make {adj or 'a'} dataclass {cls} with fields {', '.join(n for n, _ in fields)}.",
        f"Create {adj or 'a'} {cls} dataclass.",
        f"Define {cls} as {adj or 'a'} dataclass with these fields: {', '.join(n for n, _ in fields)}.",
    ]
    add(pp[i % len(pp)], code)

# enum variations
enum_specs = [
    ("Direction", ["NORTH", "SOUTH", "EAST", "WEST"], "auto"),
    ("HttpStatus", [("OK", 200), ("NOT_FOUND", 404), ("SERVER_ERROR", 500)], "int"),
    ("Suit", ["HEARTS", "DIAMONDS", "CLUBS", "SPADES"], "auto"),
    ("LogLevel", [("DEBUG", 10), ("INFO", 20), ("WARNING", 30), ("ERROR", 40)], "int"),
    ("Size", ["SMALL", "MEDIUM", "LARGE"], "auto"),
]
for i, (cls, members, kind) in enumerate(enum_specs):
    if kind == "auto":
        body = "\n".join(f"    {m} = auto()" for m in members)
        code = f"```python\nfrom enum import Enum, auto\n\nclass {cls}(Enum):\n{body}\n```"
        names = ", ".join(members)
    else:
        body = "\n".join(f"    {m} = {v}" for m, v in members)
        code = f"```python\nfrom enum import Enum\n\nclass {cls}(Enum):\n{body}\n```"
        names = ", ".join(m for m, _ in members)
    pp = [
        f"Create an enum {cls} with members {names}.",
        f"Define a {cls} enumeration.",
        f"Make an Enum called {cls}.",
    ]
    add(pp[i % len(pp)], code)

# inheritance variations
inh_specs = [
    ("Shape", "area", "Triangle", [("base", "height")], "0.5 * self.base * self.height"),
    ("Account", "interest", "Savings", [("balance", "rate")], "self.balance * self.rate"),
    ("Animal", "legs", "Spider", [], "8"),
    ("Payment", "fee", "CreditCard", [("amount",)], "self.amount * 0.03"),
]
for i, (base, method, sub, ctor, expr) in enumerate(inh_specs):
    params = ctor[0] if ctor else ()
    init_params = ", ".join(params)
    assigns = "\n".join(f"        self.{p} = {p}" for p in params) or "        pass"
    code = (
        "```python\n"
        f"class {base}:\n"
        f"    def {method}(self):\n"
        f"        raise NotImplementedError\n\n"
        f"class {sub}({base}):\n"
        + (f"    def __init__(self, {init_params}):\n{assigns}\n\n" if params else "")
        + f"    def {method}(self):\n"
        f"        return {expr}\n"
        "```"
    )
    pp = [
        f"Create a base class {base} and subclass {sub} that overrides {method}().",
        f"Make {sub} inherit from {base} and implement {method}().",
        f"Subclass {base} into {sub} with a real {method} method.",
    ]
    add(pp[i % len(pp)], code)

# abc variations
abc_specs = [
    ("Serializer", ["serialize", "deserialize"]),
    ("Storage", ["read", "write"]),
    ("Validator", ["validate"]),
    ("Plugin", ["activate", "deactivate"]),
]
for i, (cls, methods) in enumerate(abc_specs):
    body = "\n\n".join(f"    @abstractmethod\n    def {m}(self):\n        ..." for m in methods)
    code = f"```python\nfrom abc import ABC, abstractmethod\n\nclass {cls}(ABC):\n{body}\n```"
    pp = [
        f"Define an abstract base class {cls} with abstract methods {', '.join(methods)}.",
        f"Create an ABC named {cls} requiring {', '.join(methods)}.",
        f"Make an interface {cls} using ABC with {', '.join(methods)}.",
    ]
    add(pp[i % len(pp)], code)

# decorator variations (more)
deco_specs = [
    ("debug", "print arguments and return value",
     "```python\nimport functools\n\ndef debug(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        print(f\"{func.__name__}({args}, {kwargs})\")\n        result = func(*args, **kwargs)\n        print(f\"-> {result}\")\n        return result\n    return wrapper\n```"),
    ("deprecated", "warn that a function is deprecated",
     "```python\nimport functools, warnings\n\ndef deprecated(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        warnings.warn(f\"{func.__name__} is deprecated\", DeprecationWarning)\n        return func(*args, **kwargs)\n    return wrapper\n```"),
    ("synchronized", "guard a function with a lock",
     "```python\nimport functools, threading\n\ndef synchronized(func):\n    lock = threading.Lock()\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        with lock:\n            return func(*args, **kwargs)\n    return wrapper\n```"),
    ("suppress_errors", "catch and ignore exceptions",
     "```python\nimport functools\n\ndef suppress_errors(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        try:\n            return func(*args, **kwargs)\n        except Exception as e:\n            print(f\"suppressed: {e}\")\n            return None\n    return wrapper\n```"),
    ("uppercase_result", "uppercase a string return value",
     "```python\nimport functools\n\ndef uppercase_result(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs).upper()\n    return wrapper\n```"),
]
dvar = [
    "Write a decorator called {n} that will {desc}.",
    "Create a {n} decorator to {desc}.",
    "I need a decorator named {n} that can {desc}.",
    "Show me how to build a {n} decorator that {desc}.",
]
for i, (n, desc, code) in enumerate(deco_specs):
    add(dvar[i % len(dvar)].format(n=n, desc=desc), code)

# context manager variations (more)
cm_specs = [
    ("open_db", "open and close a database connection",
     "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef open_db(dsn):\n    conn = connect(dsn)\n    try:\n        yield conn\n    finally:\n        conn.close()\n```"),
    ("temp_attr", "temporarily set an attribute and restore it",
     "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef temp_attr(obj, name, value):\n    old = getattr(obj, name)\n    setattr(obj, name, value)\n    try:\n        yield\n    finally:\n        setattr(obj, name, old)\n```"),
    ("ignore_keyboard_interrupt", "swallow KeyboardInterrupt in a block",
     "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef ignore_keyboard_interrupt():\n    try:\n        yield\n    except KeyboardInterrupt:\n        pass\n```"),
    ("tag", "print an opening and closing HTML tag",
     "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef tag(name):\n    print(f\"<{name}>\")\n    yield\n    print(f\"</{name}>\")\n```"),
]
cmvar = [
    "Write a context manager {n} that will {desc}.",
    "Create a context manager named {n} to {desc}.",
    "Make a `with`-statement helper {n} that can {desc}.",
    "Show me a contextmanager {n} that will {desc}.",
]
for i, (n, desc, code) in enumerate(cm_specs):
    add(cmvar[i % len(cmvar)].format(n=n, desc=desc), code)

# classmethod/staticmethod variations
cm_factory = [
    ("Color", "from_hex", "hex_str", "return cls(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))", ["r", "g", "b"]),
    ("Duration", "from_seconds", "seconds", "return cls(seconds // 3600, (seconds % 3600) // 60, seconds % 60)", ["h", "m", "s"]),
    ("Money", "from_dollars", "dollars", "return cls(int(dollars * 100))", ["cents"]),
]
for i, (cls, mname, arg, body, params) in enumerate(cm_factory):
    init_params = ", ".join(params)
    assigns = "\n".join(f"        self.{p} = {p}" for p in params)
    code = (
        "```python\n"
        f"class {cls}:\n"
        f"    def __init__(self, {init_params}):\n"
        f"{assigns}\n\n"
        f"    @classmethod\n"
        f"    def {mname}(cls, {arg}):\n"
        f"        {body}\n"
        "```"
    )
    pp = [
        f"Add a classmethod {mname} to {cls} as an alternative constructor.",
        f"Give {cls} a {mname} factory classmethod.",
        f"Create {cls}.{mname} using @classmethod.",
    ]
    add(pp[i % len(pp)], code)

# namedtuple variations
nt_specs = [
    ("Color", ["red", "green", "blue"]),
    ("Employee", ["name", "title", "salary"]),
    ("Coordinate", ["lat", "lon"]),
    ("RGBA", ["r", "g", "b", "a"]),
]
for i, (name, fields) in enumerate(nt_specs):
    code = f"```python\nfrom collections import namedtuple\n\n{name} = namedtuple(\"{name}\", {fields!r})\n```"
    pp = [
        f"Make a namedtuple {name} with fields {', '.join(fields)}.",
        f"Create a namedtuple called {name}.",
        f"Define a {name} namedtuple holding {', '.join(fields)}.",
    ]
    add(pp[i % len(pp)], code)

# __slots__ variations
slot_specs = [
    ("Pixel", ["x", "y", "color"]),
    ("Token", ["type", "value", "line"]),
    ("Vector3", ["x", "y", "z"]),
]
for i, (cls, slots) in enumerate(slot_specs):
    assigns = "\n".join(f"        self.{s} = {s}" for s in slots)
    code = (
        f"```python\nclass {cls}:\n    __slots__ = {tuple(slots)!r}\n\n"
        f"    def __init__(self, {', '.join(slots)}):\n{assigns}\n```"
    )
    pp = [
        f"Add __slots__ to a {cls} class with {', '.join(slots)}.",
        f"Make a memory-efficient {cls} class using __slots__.",
        f"Use __slots__ on {cls}.",
    ]
    add(pp[i % len(pp)], code)

# ---------------------------------------------------------------------------
# Multi-turn conversations (~30)
# ---------------------------------------------------------------------------

add_multi([
    ("Make a Stack class.",
     "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        return self._items.pop()\n```"),
    ("Now add a peek method.",
     "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        return self._items.pop()\n\n    def peek(self):\n        return self._items[-1]\n```"),
    ("Make pop and peek raise a clear error when the stack is empty.",
     "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        if not self._items:\n            raise IndexError(\"pop from empty stack\")\n        return self._items.pop()\n\n    def peek(self):\n        if not self._items:\n            raise IndexError(\"peek from empty stack\")\n        return self._items[-1]\n```"),
    ("Add __len__ too.",
     "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n\n    def push(self, item):\n        self._items.append(item)\n\n    def pop(self):\n        if not self._items:\n            raise IndexError(\"pop from empty stack\")\n        return self._items.pop()\n\n    def peek(self):\n        if not self._items:\n            raise IndexError(\"peek from empty stack\")\n        return self._items[-1]\n\n    def __len__(self):\n        return len(self._items)\n```"),
])

add_multi([
    ("Create a Point dataclass.",
     "```python\nfrom dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: float\n    y: float\n```"),
    ("Make it frozen.",
     "```python\nfrom dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Point:\n    x: float\n    y: float\n```"),
    ("Add a method to compute distance to another point.",
     "```python\nimport math\nfrom dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Point:\n    x: float\n    y: float\n\n    def distance_to(self, other):\n        return math.hypot(self.x - other.x, self.y - other.y)\n```"),
])

add_multi([
    ("Write a decorator that times a function.",
     "```python\nimport time, functools\n\ndef timed(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        start = time.perf_counter()\n        result = func(*args, **kwargs)\n        print(f\"{func.__name__}: {time.perf_counter() - start:.4f}s\")\n        return result\n    return wrapper\n```"),
    ("Change it so it logs to a logger instead of printing.",
     "```python\nimport time, functools, logging\n\nlogger = logging.getLogger(__name__)\n\ndef timed(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        start = time.perf_counter()\n        result = func(*args, **kwargs)\n        logger.info(\"%s: %.4fs\", func.__name__, time.perf_counter() - start)\n        return result\n    return wrapper\n```"),
    ("Now let me pass a custom label as a decorator argument.",
     "```python\nimport time, functools, logging\n\nlogger = logging.getLogger(__name__)\n\ndef timed(label=None):\n    def decorator(func):\n        name = label or func.__name__\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            start = time.perf_counter()\n            result = func(*args, **kwargs)\n            logger.info(\"%s: %.4fs\", name, time.perf_counter() - start)\n            return result\n        return wrapper\n    return decorator\n```"),
])

add_multi([
    ("Make an Animal base class.",
     "```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        raise NotImplementedError\n```"),
    ("Add Dog and Cat subclasses.",
     "```python\nclass Dog(Animal):\n    def speak(self):\n        return \"woof\"\n\nclass Cat(Animal):\n    def speak(self):\n        return \"meow\"\n```"),
    ("Turn Animal into an abstract base class so speak must be implemented.",
     "```python\nfrom abc import ABC, abstractmethod\n\nclass Animal(ABC):\n    def __init__(self, name):\n        self.name = name\n\n    @abstractmethod\n    def speak(self):\n        ...\n```"),
])

add_multi([
    ("Build a context manager class that opens a file.",
     "```python\nclass FileOpener:\n    def __init__(self, path, mode=\"r\"):\n        self.path = path\n        self.mode = mode\n\n    def __enter__(self):\n        self.file = open(self.path, self.mode)\n        return self.file\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        self.file.close()\n```"),
    ("Rewrite it using contextlib.contextmanager.",
     "```python\nfrom contextlib import contextmanager\n\n@contextmanager\ndef file_opener(path, mode=\"r\"):\n    f = open(path, mode)\n    try:\n        yield f\n    finally:\n        f.close()\n```"),
])

add_multi([
    ("Create a Money class storing cents.",
     "```python\nclass Money:\n    def __init__(self, cents):\n        self.cents = cents\n```"),
    ("Add __repr__ that shows dollars.",
     "```python\nclass Money:\n    def __init__(self, cents):\n        self.cents = cents\n\n    def __repr__(self):\n        return f\"Money(${self.cents / 100:.2f})\"\n```"),
    ("Support addition with __add__.",
     "```python\nclass Money:\n    def __init__(self, cents):\n        self.cents = cents\n\n    def __repr__(self):\n        return f\"Money(${self.cents / 100:.2f})\"\n\n    def __add__(self, other):\n        return Money(self.cents + other.cents)\n```"),
    ("Make instances comparable and hashable.",
     "```python\nfrom functools import total_ordering\n\n@total_ordering\nclass Money:\n    def __init__(self, cents):\n        self.cents = cents\n\n    def __repr__(self):\n        return f\"Money(${self.cents / 100:.2f})\"\n\n    def __add__(self, other):\n        return Money(self.cents + other.cents)\n\n    def __eq__(self, other):\n        return isinstance(other, Money) and self.cents == other.cents\n\n    def __lt__(self, other):\n        return self.cents < other.cents\n\n    def __hash__(self):\n        return hash(self.cents)\n```"),
])

add_multi([
    ("Make a Config singleton.",
     "```python\nclass Config:\n    _instance = None\n\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n```"),
    ("Add settings initialized only once.",
     "```python\nclass Config:\n    _instance = None\n\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n            cls._instance.settings = {}\n        return cls._instance\n```"),
])

add_multi([
    ("Define an Enum for traffic light colors.",
     "```python\nfrom enum import Enum, auto\n\nclass Light(Enum):\n    RED = auto()\n    YELLOW = auto()\n    GREEN = auto()\n```"),
    ("Add a method that returns the next light.",
     "```python\nfrom enum import Enum, auto\n\nclass Light(Enum):\n    RED = auto()\n    YELLOW = auto()\n    GREEN = auto()\n\n    def next(self):\n        order = [Light.GREEN, Light.YELLOW, Light.RED]\n        return order[(order.index(self) + 1) % len(order)]\n```"),
])

add_multi([
    ("Create a Vector2D class.",
     "```python\nclass Vector2D:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n```"),
    ("Add __add__ and __sub__.",
     "```python\nclass Vector2D:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __add__(self, other):\n        return Vector2D(self.x + other.x, self.y + other.y)\n\n    def __sub__(self, other):\n        return Vector2D(self.x - other.x, self.y - other.y)\n```"),
    ("Add scalar multiplication and a magnitude property.",
     "```python\nimport math\n\nclass Vector2D:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __add__(self, other):\n        return Vector2D(self.x + other.x, self.y + other.y)\n\n    def __sub__(self, other):\n        return Vector2D(self.x - other.x, self.y - other.y)\n\n    def __mul__(self, scalar):\n        return Vector2D(self.x * scalar, self.y * scalar)\n\n    @property\n    def magnitude(self):\n        return math.hypot(self.x, self.y)\n```"),
    ("Make it nicely printable.",
     "```python\nimport math\n\nclass Vector2D:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __add__(self, other):\n        return Vector2D(self.x + other.x, self.y + other.y)\n\n    def __sub__(self, other):\n        return Vector2D(self.x - other.x, self.y - other.y)\n\n    def __mul__(self, scalar):\n        return Vector2D(self.x * scalar, self.y * scalar)\n\n    @property\n    def magnitude(self):\n        return math.hypot(self.x, self.y)\n\n    def __repr__(self):\n        return f\"Vector2D({self.x}, {self.y})\"\n```"),
])

add_multi([
    ("Write a simple observer pattern.",
     "```python\nclass Subject:\n    def __init__(self):\n        self._observers = []\n\n    def subscribe(self, obs):\n        self._observers.append(obs)\n\n    def notify(self, data):\n        for obs in self._observers:\n            obs(data)\n```"),
    ("Add the ability to unsubscribe.",
     "```python\nclass Subject:\n    def __init__(self):\n        self._observers = []\n\n    def subscribe(self, obs):\n        self._observers.append(obs)\n\n    def unsubscribe(self, obs):\n        self._observers.remove(obs)\n\n    def notify(self, data):\n        for obs in self._observers:\n            obs(data)\n```"),
])

add_multi([
    ("Create a Temperature class storing celsius.",
     "```python\nclass Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n```"),
    ("Add a fahrenheit property.",
     "```python\nclass Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    @property\n    def fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n```"),
    ("Let me set fahrenheit too and have it update celsius.",
     "```python\nclass Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    @property\n    def fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n\n    @fahrenheit.setter\n    def fahrenheit(self, value):\n        self.celsius = (value - 32) * 5 / 9\n```"),
    ("Prevent celsius from going below absolute zero.",
     "```python\nclass Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    @property\n    def celsius(self):\n        return self._celsius\n\n    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError(\"below absolute zero\")\n        self._celsius = value\n\n    @property\n    def fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n\n    @fahrenheit.setter\n    def fahrenheit(self, value):\n        self.celsius = (value - 32) * 5 / 9\n```"),
])

add_multi([
    ("Make a Counter class that starts at zero.",
     "```python\nclass Counter:\n    def __init__(self):\n        self.value = 0\n\n    def increment(self):\n        self.value += 1\n```"),
    ("Add support for using it as a callable to increment.",
     "```python\nclass Counter:\n    def __init__(self):\n        self.value = 0\n\n    def increment(self):\n        self.value += 1\n\n    def __call__(self):\n        self.increment()\n        return self.value\n```"),
])

add_multi([
    ("Create an LRU-style cache decorator manually.",
     "```python\nimport functools\nfrom collections import OrderedDict\n\ndef lru(maxsize=128):\n    def decorator(func):\n        cache = OrderedDict()\n        @functools.wraps(func)\n        def wrapper(*args):\n            if args in cache:\n                cache.move_to_end(args)\n                return cache[args]\n            result = func(*args)\n            cache[args] = result\n            if len(cache) > maxsize:\n                cache.popitem(last=False)\n            return result\n        return wrapper\n    return decorator\n```"),
    ("Actually just use the standard library instead.",
     "```python\nimport functools\n\n@functools.lru_cache(maxsize=128)\ndef compute(x):\n    ...\n```\n\n`functools.lru_cache` is battle-tested and handles thread safety and statistics (`compute.cache_info()`) for you."),
])

add_multi([
    ("Define a Shape ABC with an area method.",
     "```python\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        ...\n```"),
    ("Add Circle and Square implementations.",
     "```python\nimport math\n\nclass Circle(Shape):\n    def __init__(self, r):\n        self.r = r\n\n    def area(self):\n        return math.pi * self.r ** 2\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        return self.side ** 2\n```"),
    ("Add a perimeter abstractmethod too.",
     "```python\nimport math\nfrom abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        ...\n\n    @abstractmethod\n    def perimeter(self):\n        ...\n\nclass Circle(Shape):\n    def __init__(self, r):\n        self.r = r\n\n    def area(self):\n        return math.pi * self.r ** 2\n\n    def perimeter(self):\n        return 2 * math.pi * self.r\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        return self.side ** 2\n\n    def perimeter(self):\n        return 4 * self.side\n```"),
])

add_multi([
    ("Make a class-based context manager for a database transaction.",
     "```python\nclass Transaction:\n    def __init__(self, conn):\n        self.conn = conn\n\n    def __enter__(self):\n        return self.conn\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        if exc_type is None:\n            self.conn.commit()\n        else:\n            self.conn.rollback()\n        return False\n```"),
    ("Make sure it never suppresses the exception.",
     "It already returns `False` from `__exit__`, which means exceptions propagate. The `return False` (or simply not returning anything) is what guarantees the exception is re-raised after rollback:\n\n```python\nclass Transaction:\n    def __init__(self, conn):\n        self.conn = conn\n\n    def __enter__(self):\n        return self.conn\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        if exc_type is None:\n            self.conn.commit()\n        else:\n            self.conn.rollback()\n        return False  # propagate any exception\n```"),
])

add_multi([
    ("Create a Person class with name and age.",
     "```python\nclass Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n```"),
    ("Make it a dataclass instead.",
     "```python\nfrom dataclasses import dataclass\n\n@dataclass\nclass Person:\n    name: str\n    age: int\n```"),
    ("Sort a list of people by age.",
     "```python\npeople.sort(key=lambda p: p.age)\n```\n\nOr make the dataclass orderable with `@dataclass(order=True)` and put `age` first so comparisons use it."),
])

add_multi([
    ("Write a retry decorator.",
     "```python\nimport functools, time\n\ndef retry(times=3):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for attempt in range(times):\n                try:\n                    return func(*args, **kwargs)\n                except Exception:\n                    if attempt == times - 1:\n                        raise\n        return wrapper\n    return decorator\n```"),
    ("Add exponential backoff between attempts.",
     "```python\nimport functools, time\n\ndef retry(times=3, base_delay=0.5):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for attempt in range(times):\n                try:\n                    return func(*args, **kwargs)\n                except Exception:\n                    if attempt == times - 1:\n                        raise\n                    time.sleep(base_delay * 2 ** attempt)\n        return wrapper\n    return decorator\n```"),
    ("Let me restrict which exceptions trigger a retry.",
     "```python\nimport functools, time\n\ndef retry(times=3, base_delay=0.5, exceptions=(Exception,)):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            for attempt in range(times):\n                try:\n                    return func(*args, **kwargs)\n                except exceptions:\n                    if attempt == times - 1:\n                        raise\n                    time.sleep(base_delay * 2 ** attempt)\n        return wrapper\n    return decorator\n```"),
])

add_multi([
    ("Make a simple Queue using a list.",
     "```python\nclass Queue:\n    def __init__(self):\n        self._items = []\n\n    def enqueue(self, x):\n        self._items.append(x)\n\n    def dequeue(self):\n        return self._items.pop(0)\n```"),
    ("That pop(0) is slow. Use something more efficient.",
     "`list.pop(0)` is O(n). Use `collections.deque` for O(1) operations at both ends:\n\n```python\nfrom collections import deque\n\nclass Queue:\n    def __init__(self):\n        self._items = deque()\n\n    def enqueue(self, x):\n        self._items.append(x)\n\n    def dequeue(self):\n        return self._items.popleft()\n```"),
])

add_multi([
    ("Create a class with a private balance attribute.",
     "```python\nclass Account:\n    def __init__(self, balance=0):\n        self._balance = balance\n```"),
    ("Expose it as a read-only property.",
     "```python\nclass Account:\n    def __init__(self, balance=0):\n        self._balance = balance\n\n    @property\n    def balance(self):\n        return self._balance\n```"),
    ("Add deposit and withdraw that go through validation.",
     "```python\nclass Account:\n    def __init__(self, balance=0):\n        self._balance = balance\n\n    @property\n    def balance(self):\n        return self._balance\n\n    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError(\"amount must be positive\")\n        self._balance += amount\n\n    def withdraw(self, amount):\n        if amount > self._balance:\n            raise ValueError(\"insufficient funds\")\n        self._balance -= amount\n```"),
])

add_multi([
    ("Make a frozen dataclass for a 2D point.",
     "```python\nfrom dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass Point:\n    x: int\n    y: int\n```"),
    ("Can I use it as a dictionary key now?",
     "Yes. `frozen=True` makes the dataclass immutable and auto-generates `__hash__`, so instances are hashable and usable as dict keys or set members:\n\n```python\nd = {Point(0, 0): \"origin\"}\nprint(d[Point(0, 0)])  # origin\n```"),
])

add_multi([
    ("Implement a factory function for shapes.",
     "```python\ndef make_shape(kind, **kwargs):\n    if kind == \"circle\":\n        return Circle(kwargs[\"radius\"])\n    if kind == \"square\":\n        return Square(kwargs[\"side\"])\n    raise ValueError(f\"unknown shape: {kind}\")\n```"),
    ("Refactor it to use a registry dict instead of if/elif.",
     "```python\n_SHAPES = {}\n\ndef register_shape(name):\n    def deco(cls):\n        _SHAPES[name] = cls\n        return cls\n    return deco\n\ndef make_shape(kind, **kwargs):\n    try:\n        return _SHAPES[kind](**kwargs)\n    except KeyError:\n        raise ValueError(f\"unknown shape: {kind}\")\n\n@register_shape(\"circle\")\nclass Circle:\n    def __init__(self, radius):\n        self.radius = radius\n```"),
])

add_multi([
    ("Build a Matrix class wrapping a list of lists.",
     "```python\nclass Matrix:\n    def __init__(self, rows):\n        self.rows = rows\n```"),
    ("Add indexing with __getitem__ for (row, col) tuples.",
     "```python\nclass Matrix:\n    def __init__(self, rows):\n        self.rows = rows\n\n    def __getitem__(self, pos):\n        r, c = pos\n        return self.rows[r][c]\n```"),
    ("Add __setitem__ too.",
     "```python\nclass Matrix:\n    def __init__(self, rows):\n        self.rows = rows\n\n    def __getitem__(self, pos):\n        r, c = pos\n        return self.rows[r][c]\n\n    def __setitem__(self, pos, value):\n        r, c = pos\n        self.rows[r][c] = value\n```"),
])

add_multi([
    ("Make a class iterable over its internal list.",
     "```python\nclass Collection:\n    def __init__(self, items):\n        self._items = items\n\n    def __iter__(self):\n        return iter(self._items)\n```"),
    ("Add __len__ and __getitem__ so it's a full sequence.",
     "```python\nclass Collection:\n    def __init__(self, items):\n        self._items = items\n\n    def __iter__(self):\n        return iter(self._items)\n\n    def __len__(self):\n        return len(self._items)\n\n    def __getitem__(self, index):\n        return self._items[index]\n```"),
    ("Could I just inherit from collections.abc.Sequence instead?",
     "Yes. Subclass `Sequence` and implement only `__getitem__` and `__len__`; the ABC provides `__iter__`, `__contains__`, `__reversed__`, `index`, and `count` for free:\n\n```python\nfrom collections.abc import Sequence\n\nclass Collection(Sequence):\n    def __init__(self, items):\n        self._items = list(items)\n\n    def __getitem__(self, index):\n        return self._items[index]\n\n    def __len__(self):\n        return len(self._items)\n```"),
])

add_multi([
    ("Write a property-based getter/setter for a name field.",
     "```python\nclass Person:\n    def __init__(self, name):\n        self.name = name\n\n    @property\n    def name(self):\n        return self._name\n\n    @name.setter\n    def name(self, value):\n        self._name = value\n```"),
    ("Strip whitespace and reject empty names in the setter.",
     "```python\nclass Person:\n    def __init__(self, name):\n        self.name = name\n\n    @property\n    def name(self):\n        return self._name\n\n    @name.setter\n    def name(self, value):\n        value = value.strip()\n        if not value:\n            raise ValueError(\"name cannot be empty\")\n        self._name = value\n```"),
])

add_multi([
    ("Create a class decorator that adds a __repr__ automatically.",
     "```python\ndef auto_repr(cls):\n    def __repr__(self):\n        attrs = ', '.join(f\"{k}={v!r}\" for k, v in self.__dict__.items())\n        return f\"{cls.__name__}({attrs})\"\n    cls.__repr__ = __repr__\n    return cls\n\n@auto_repr\nclass Item:\n    def __init__(self, name, price):\n        self.name = name\n        self.price = price\n```"),
    ("Isn't this just what @dataclass does?",
     "Largely, yes. `@dataclass` generates `__init__`, `__repr__`, and `__eq__` for you based on annotated fields, so prefer it unless you specifically need to add a repr to existing non-dataclass classes:\n\n```python\nfrom dataclasses import dataclass\n\n@dataclass\nclass Item:\n    name: str\n    price: float\n```"),
])

add_multi([
    ("Make a Singleton base class others can inherit from.",
     "```python\nclass Singleton:\n    _instances = {}\n\n    def __new__(cls, *args, **kwargs):\n        if cls not in cls._instances:\n            cls._instances[cls] = super().__new__(cls)\n        return cls._instances[cls]\n```"),
    ("Implement it as a metaclass instead.",
     "```python\nclass SingletonMeta(type):\n    _instances = {}\n\n    def __call__(cls, *args, **kwargs):\n        if cls not in cls._instances:\n            cls._instances[cls] = super().__call__(*args, **kwargs)\n        return cls._instances[cls]\n\nclass Config(metaclass=SingletonMeta):\n    pass\n```"),
])

add_multi([
    ("Define a strategy pattern with classes.",
     "```python\nfrom abc import ABC, abstractmethod\n\nclass Strategy(ABC):\n    @abstractmethod\n    def execute(self, data):\n        ...\n\nclass Reverse(Strategy):\n    def execute(self, data):\n        return data[::-1]\n\nclass Context:\n    def __init__(self, strategy):\n        self.strategy = strategy\n\n    def run(self, data):\n        return self.strategy.execute(data)\n```"),
    ("Simplify it the Pythonic way with plain functions.",
     "In Python a strategy can just be a callable, so the class hierarchy is often unnecessary:\n\n```python\nclass Context:\n    def __init__(self, strategy):\n        self.strategy = strategy  # any callable\n\n    def run(self, data):\n        return self.strategy(data)\n\nctx = Context(lambda d: d[::-1])\nprint(ctx.run([1, 2, 3]))  # [3, 2, 1]\n```"),
])

add_multi([
    ("Create an enum of order statuses.",
     "```python\nfrom enum import Enum, auto\n\nclass OrderStatus(Enum):\n    PENDING = auto()\n    SHIPPED = auto()\n    DELIVERED = auto()\n    CANCELLED = auto()\n```"),
    ("Make it a StrEnum so it serializes to its name nicely.",
     "```python\nfrom enum import StrEnum\n\nclass OrderStatus(StrEnum):\n    PENDING = \"pending\"\n    SHIPPED = \"shipped\"\n    DELIVERED = \"delivered\"\n    CANCELLED = \"cancelled\"\n\nprint(OrderStatus.SHIPPED == \"shipped\")  # True\n```"),
])

add_multi([
    ("Write a descriptor for a typed attribute.",
     "```python\nclass Typed:\n    def __init__(self, type_):\n        self.type_ = type_\n\n    def __set_name__(self, owner, name):\n        self.name = \"_\" + name\n\n    def __get__(self, obj, objtype=None):\n        return getattr(obj, self.name)\n\n    def __set__(self, obj, value):\n        if not isinstance(value, self.type_):\n            raise TypeError(f\"expected {self.type_.__name__}\")\n        setattr(obj, self.name, value)\n```"),
    ("Use it on a class.",
     "```python\nclass Account:\n    owner = Typed(str)\n    balance = Typed(int)\n\n    def __init__(self, owner, balance):\n        self.owner = owner\n        self.balance = balance\n\nAccount(\"Ada\", 100)       # ok\nAccount(\"Ada\", \"oops\")    # TypeError: expected int\n```"),
])

add_multi([
    ("Make a context manager that opens multiple files.",
     "```python\nfrom contextlib import ExitStack\n\nclass MultiOpen:\n    def __init__(self, *paths):\n        self.paths = paths\n\n    def __enter__(self):\n        self._stack = ExitStack()\n        return [self._stack.enter_context(open(p)) for p in self.paths]\n\n    def __exit__(self, *exc):\n        self._stack.close()\n        return False\n```"),
    ("Simplify by just using ExitStack directly at the call site.",
     "```python\nfrom contextlib import ExitStack\n\nwith ExitStack() as stack:\n    files = [stack.enter_context(open(p)) for p in (\"a.txt\", \"b.txt\")]\n    # use files; all closed automatically on exit\n```"),
])

# ---------------------------------------------------------------------------
# A few more standalone, conceptual Q&A to round out and add variety
# ---------------------------------------------------------------------------

add(
    "What is the difference between __new__ and __init__?",
    "`__new__` creates and returns the instance (it's a static method receiving the class); `__init__` initializes the already-created instance. You override `__new__` only when you need to control instance creation, e.g. for immutable types or singletons.\n\n```python\nclass Foo:\n    def __new__(cls, *args):\n        print(\"creating\")\n        return super().__new__(cls)\n\n    def __init__(self, x):\n        print(\"initializing\")\n        self.x = x\n```",
)

add(
    "How do I call a parent method from a grandchild class with multiple inheritance?",
    "Use `super()`, which follows the MRO rather than hard-coding a parent. To target a specific class, use the explicit form `Parent.method(self, ...)`, but cooperative `super()` is usually correct.\n\n```python\nclass A:\n    def run(self): return \"A\"\n\nclass B(A):\n    def run(self): return \"B->\" + super().run()\n\nclass C(B):\n    def run(self): return \"C->\" + super().run()\n```",
)

add(
    "When should I prefer composition over inheritance?",
    "Prefer composition when the relationship is 'has-a' rather than 'is-a', when you want to swap behavior at runtime, or when inheritance would couple you to a base class's implementation. Inheritance is best for genuine subtype/is-a relationships where the subclass is substitutable for the base.",
)

add(
    "How do I make a class JSON serializable?",
    "Provide a method that returns a dict, or implement a custom `JSONEncoder`.\n\n```python\nimport json\nfrom dataclasses import dataclass, asdict\n\n@dataclass\nclass User:\n    name: str\n    age: int\n\nprint(json.dumps(asdict(User(\"Ada\", 36))))\n```",
)

add(
    "Explain duck typing with an example.",
    "Duck typing means Python cares about whether an object supports the needed behavior, not its type: 'if it walks like a duck and quacks like a duck, it's a duck.'\n\n```python\ndef make_it_speak(thing):\n    return thing.speak()  # works for anything with a speak() method\n\nclass Dog:\n    def speak(self): return \"woof\"\n\nclass Robot:\n    def speak(self): return \"beep\"\n\nprint(make_it_speak(Dog()), make_it_speak(Robot()))\n```",
)

add(
    "How do I implement __iadd__ for in-place addition?",
    "`__iadd__` handles `+=` and should usually mutate and return `self`.\n\n```python\nclass Accumulator:\n    def __init__(self, total=0):\n        self.total = total\n\n    def __iadd__(self, value):\n        self.total += value\n        return self\n```",
)

add(
    "Make a class that supports the with-statement and returns something useful from __enter__.",
    "```python\nclass Connection:\n    def __enter__(self):\n        print(\"connecting\")\n        self.session = {\"open\": True}\n        return self.session  # bound to the `as` variable\n\n    def __exit__(self, *exc):\n        print(\"closing\")\n        self.session[\"open\"] = False\n        return False\n\nwith Connection() as session:\n    print(session)\n```",
)

add(
    "How do I define class-level constants?",
    "```python\nclass Circle:\n    PI = 3.14159  # class constant, shared by all instances\n\n    def __init__(self, r):\n        self.r = r\n\n    def area(self):\n        return Circle.PI * self.r ** 2\n```",
)

add(
    "What does @cached_property do?",
    "`functools.cached_property` computes a value once on first access and caches it on the instance, so later accesses are free. The instance needs a `__dict__` (no `__slots__` without `__dict__`).\n\n```python\nimport functools\n\nclass DataSet:\n    def __init__(self, values):\n        self.values = values\n\n    @functools.cached_property\n    def mean(self):\n        return sum(self.values) / len(self.values)\n```",
)

add(
    "How do I make an immutable class without dataclasses?",
    "Override `__setattr__` to block changes after init, or use `__slots__` plus property-only access. A common approach:\n\n```python\nclass Immutable:\n    __slots__ = (\"_x\",)\n\n    def __init__(self, x):\n        object.__setattr__(self, \"_x\", x)\n\n    @property\n    def x(self):\n        return self._x\n\n    def __setattr__(self, name, value):\n        raise AttributeError(\"immutable\")\n```",
)

add(
    "Show me how to implement __reversed__.",
    "```python\nclass MyList:\n    def __init__(self, items):\n        self.items = items\n\n    def __reversed__(self):\n        return reversed(self.items)\n\nprint(list(reversed(MyList([1, 2, 3]))))  # [3, 2, 1]\n```",
)

add(
    "How can a method return a new instance of its own class generically?",
    "Use `type(self)` (or `self.__class__`) so subclasses get instances of themselves.\n\n```python\nclass Vector:\n    def __init__(self, data):\n        self.data = data\n\n    def scaled(self, k):\n        return type(self)([x * k for x in self.data])\n```",
)

add(
    "What is a metaclass in one example?",
    "A metaclass is the class of a class; it customizes class creation. Most code never needs one.\n\n```python\nclass UpperAttrMeta(type):\n    def __new__(mcs, name, bases, namespace):\n        namespace[\"created_by\"] = \"meta\"\n        return super().__new__(mcs, name, bases, namespace)\n\nclass Thing(metaclass=UpperAttrMeta):\n    pass\n\nprint(Thing.created_by)  # meta\n```",
)

add(
    "How do I override __eq__ and keep the object hashable?",
    "Define `__hash__` alongside `__eq__` based on the same immutable fields, because defining `__eq__` alone sets `__hash__` to None.\n\n```python\nclass Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __eq__(self, other):\n        return (self.x, self.y) == (other.x, other.y)\n\n    def __hash__(self):\n        return hash((self.x, self.y))\n```",
)

add(
    "Show a class that acts as both an iterator and iterable.",
    "```python\nclass Range:\n    def __init__(self, n):\n        self.n = n\n\n    def __iter__(self):\n        self.i = 0\n        return self\n\n    def __next__(self):\n        if self.i >= self.n:\n            raise StopIteration\n        self.i += 1\n        return self.i - 1\n```",
)

# Write out
out_path = "/home/user/Silicat/data/synth/oop.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print(f"wrote {len(examples)} examples to {out_path}")
