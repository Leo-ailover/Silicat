import json

E = []

def add(user, silicat):
    E.append({"messages": [
        {"role": "user", "content": user},
        {"role": "silicat", "content": silicat},
    ]})

def addmt(turns):
    msgs = []
    roles = ["user", "silicat", "user", "silicat"]
    for r, c in zip(roles, turns):
        msgs.append({"role": r, "content": c})
    E.append({"messages": msgs})


# ---------------- Variables & basics ----------------
add("How do I create a variable in Python?",
    "You just assign a value with `=`. No type declaration needed:\n\n```python\nname = \"Alice\"\nage = 30\nheight = 1.75\n```")

add("what's the difference between = and == in python",
    "`=` assigns a value to a variable, while `==` compares two values for equality and returns a bool.\n\n```python\nx = 5      # assignment\nx == 5     # comparison -> True\n```")

add("how to swap two variables in python",
    "Use tuple unpacking, no temp variable needed:\n\n```python\na, b = 1, 2\na, b = b, a\nprint(a, b)  # 2 1\n```")

add("assign the same value to multiple variables",
    "Chain the assignment:\n\n```python\nx = y = z = 0\n```")

add("can I assign multiple variables on one line",
    "Yes, with comma-separated targets and values:\n\n```python\na, b, c = 1, 2, 3\n```")

add("how do I check the type of a variable",
    "Use the `type()` function, or `isinstance()` for type checks:\n\n```python\ntype(42)            # <class 'int'>\nisinstance(42, int) # True\n```")

add("what does None mean in python",
    "`None` is a special object representing the absence of a value. It's Python's version of \"null\". A function with no `return` statement returns `None`.\n\n```python\nx = None\nprint(x is None)  # True\n```")

add("how to check if a variable is None",
    "Use `is None` rather than `== None`:\n\n```python\nif x is None:\n    print(\"no value\")\n```")

add("delete a variable python",
    "Use the `del` statement:\n\n```python\nx = 5\ndel x\n# referencing x now raises NameError\n```")

# ---------------- Numbers ----------------
add("how do I do integer division in python",
    "Use the `//` operator, which floors the result:\n\n```python\n7 // 2   # 3\n-7 // 2  # -4\n```")

add("what does the modulo operator do",
    "`%` returns the remainder of division:\n\n```python\n17 % 5  # 2\n10 % 2  # 0 (even)\n```")

add("how to raise a number to a power",
    "Use `**`:\n\n```python\n2 ** 10  # 1024\n9 ** 0.5 # 3.0 (square root)\n```")

add("python round a number",
    "Use `round()`. The second argument sets decimal places:\n\n```python\nround(3.14159, 2)  # 3.14\nround(2.5)         # 2 (banker's rounding)\n```")

add("how to get the absolute value",
    "Use `abs()`:\n\n```python\nabs(-7)    # 7\nabs(-2.5)  # 2.5\n```")

add("convert float to int python",
    "Use `int()`, which truncates toward zero:\n\n```python\nint(3.9)   # 3\nint(-3.9)  # -3\n```")

add("how do I convert a string to a number",
    "Use `int()` for whole numbers and `float()` for decimals:\n\n```python\nint(\"42\")     # 42\nfloat(\"3.14\") # 3.14\n```")

add("round up python",
    "Use `math.ceil()`:\n\n```python\nimport math\nmath.ceil(4.1)  # 5\n```")

add("round down python",
    "Use `math.floor()` or integer division:\n\n```python\nimport math\nmath.floor(4.9)  # 4\n```")

add("how to check if a number is even",
    "Check the remainder when divided by 2:\n\n```python\nn = 10\nif n % 2 == 0:\n    print(\"even\")\n```")

add("get quotient and remainder at once python",
    "Use `divmod()`, which returns both:\n\n```python\nq, r = divmod(17, 5)\nprint(q, r)  # 3 2\n```")

add("what's the max int in python",
    "Python ints have arbitrary precision, so there's no fixed maximum. They grow as large as your memory allows:\n\n```python\n2 ** 200  # works fine\n```")

add("how do I format a number with commas as thousands separators",
    "Use an f-string with the `,` format spec:\n\n```python\nn = 1234567\nprint(f\"{n:,}\")  # 1,234,567\n```")

add("show a float with 2 decimal places",
    "Use `.2f` in an f-string:\n\n```python\nx = 3.14159\nprint(f\"{x:.2f}\")  # 3.14\n```")

add("convert int to binary string python",
    "Use `bin()`, or format with `b`:\n\n```python\nbin(10)        # '0b1010'\nf\"{10:b}\"      # '1010'\n```")

add("hex of a number python",
    "Use `hex()`:\n\n```python\nhex(255)  # '0xff'\n```")

# ---------------- Strings ----------------
add("reverse a string python",
    "Use slicing with a step of -1:\n\n```python\ns = \"hello\"\nprint(s[::-1])  # 'olleh'\n```")

add("how do I make a string uppercase",
    "Use `.upper()`:\n\n```python\n\"hello\".upper()  # 'HELLO'\n```")

add("lowercase a string",
    "Use `.lower()`:\n\n```python\n\"HELLO\".lower()  # 'hello'\n```")

add("how to capitalize the first letter of a string",
    "Use `.capitalize()` for the whole string, or `.title()` for each word:\n\n```python\n\"hello world\".capitalize()  # 'Hello world'\n\"hello world\".title()       # 'Hello World'\n```")

add("remove whitespace from a string python",
    "Use `.strip()` to trim both ends, `.lstrip()` / `.rstrip()` for one side:\n\n```python\n\"  hi  \".strip()  # 'hi'\n```")

add("how do I check if a string contains a substring",
    "Use the `in` operator:\n\n```python\nif \"cat\" in \"category\":\n    print(\"found\")\n```")

add("split a string by comma",
    "Use `.split(',')`:\n\n```python\n\"a,b,c\".split(\",\")  # ['a', 'b', 'c']\n```")

add("how to split a string into words",
    "Call `.split()` with no arguments to split on any whitespace:\n\n```python\n\"the quick fox\".split()  # ['the', 'quick', 'fox']\n```")

add("join a list of strings python",
    "Use `.join()` on the separator string:\n\n```python\nwords = [\"a\", \"b\", \"c\"]\n\"-\".join(words)  # 'a-b-c'\n```")

add("replace part of a string python",
    "Use `.replace(old, new)`:\n\n```python\n\"hello\".replace(\"l\", \"L\")  # 'heLLo'\n```")

add("how do I count occurrences of a character in a string",
    "Use `.count()`:\n\n```python\n\"banana\".count(\"a\")  # 3\n```")

add("check if a string starts with something",
    "Use `.startswith()`:\n\n```python\n\"hello.py\".startswith(\"hello\")  # True\n```")

add("check if string ends with .txt",
    "Use `.endswith()`:\n\n```python\nfilename.endswith(\".txt\")\n```")

add("how to find the index of a substring",
    "`.find()` returns the index or -1 if not found; `.index()` raises if not found:\n\n```python\n\"hello\".find(\"l\")   # 2\n\"hello\".find(\"z\")   # -1\n```")

add("how do I check if a string is all digits",
    "Use `.isdigit()`:\n\n```python\n\"12345\".isdigit()  # True\n\"12a\".isdigit()    # False\n```")

add("string is alphabetic python",
    "Use `.isalpha()`:\n\n```python\n\"abc\".isalpha()  # True\n\"ab1\".isalpha()  # False\n```")

add("how long is a string python",
    "Use `len()`:\n\n```python\nlen(\"hello\")  # 5\n```")

add("get the first character of a string",
    "Index with `[0]`:\n\n```python\n\"hello\"[0]  # 'h'\n```")

add("get the last character of a string",
    "Use negative indexing with `[-1]`:\n\n```python\n\"hello\"[-1]  # 'o'\n```")

add("repeat a string n times python",
    "Multiply the string by an int:\n\n```python\n\"ab\" * 3  # 'ababab'\n```")

add("how to pad a string with zeros",
    "Use `.zfill()` or an f-string format spec:\n\n```python\n\"42\".zfill(5)   # '00042'\nf\"{42:05d}\"     # '00042'\n```")

add("center a string in a field python",
    "Use `.center(width)`:\n\n```python\n\"hi\".center(10, \"-\")  # '----hi----'\n```")

add("how to remove a specific character from a string",
    "Replace it with an empty string:\n\n```python\n\"a-b-c\".replace(\"-\", \"\")  # 'abc'\n```")

add("check if a string is a palindrome python",
    "Compare the string to its reverse:\n\n```python\ndef is_palindrome(s):\n    return s == s[::-1]\n\nis_palindrome(\"racecar\")  # True\n```")

add("count vowels in a string",
    "```python\ndef count_vowels(s):\n    return sum(1 for c in s.lower() if c in \"aeiou\")\n\ncount_vowels(\"Hello\")  # 2\n```")

add("how do I title case only the first word and keep the rest",
    "Use `.capitalize()`, which lowercases everything else:\n\n```python\n\"hELLO wORLD\".capitalize()  # 'Hello world'\n```")

add("swap case of a string python",
    "Use `.swapcase()`:\n\n```python\n\"Hello\".swapcase()  # 'hELLO'\n```")

# ---------------- f-strings ----------------
add("what is an f-string",
    "An f-string is a string literal prefixed with `f` that lets you embed expressions inside `{}`. They're the cleanest way to format strings.\n\n```python\nname = \"Sam\"\nprint(f\"Hi {name}, you are {2025 - 1990} years old\")\n```")

add("how do I put a variable inside a string python",
    "Use an f-string:\n\n```python\nx = 42\nprint(f\"the value is {x}\")\n```")

add("can I do math inside an f-string",
    "Yes, any expression works inside the braces:\n\n```python\na, b = 3, 4\nprint(f\"sum is {a + b}\")  # sum is 7\n```")

add("show variable name and value with f-string",
    "Use the `=` specifier (Python 3.8+):\n\n```python\nx = 10\nprint(f\"{x=}\")  # x=10\n```")

add("f-string percentage format",
    "Use `.1%`:\n\n```python\nratio = 0.256\nprint(f\"{ratio:.1%}\")  # 25.6%\n```")

add("how to align text with f-strings",
    "Use `<`, `>`, or `^` for left, right, center alignment with a width:\n\n```python\nf\"{'hi':>10}\"  # '        hi'\nf\"{'hi':<10}\"  # 'hi        '\nf\"{'hi':^10}\"  # '    hi    '\n```")

add("f-string with curly braces literal",
    "Double the braces to show a literal brace:\n\n```python\nf\"{{literal}}\"  # '{literal}'\n```")

# ---------------- Lists ----------------
add("how do I create a list in python",
    "Use square brackets:\n\n```python\nnums = [1, 2, 3]\nempty = []\n```")

add("add an item to a list python",
    "Use `.append()` for one item, `.extend()` for several:\n\n```python\nnums = [1, 2]\nnums.append(3)        # [1, 2, 3]\nnums.extend([4, 5])   # [1, 2, 3, 4, 5]\n```")

add("how to remove an item from a list",
    "`.remove(value)` removes by value, `.pop(index)` removes by position:\n\n```python\nlst = [1, 2, 3]\nlst.remove(2)  # [1, 3]\nlst.pop(0)     # returns 1, list is now [3]\n```")

add("insert into a list at a position python",
    "Use `.insert(index, value)`:\n\n```python\nlst = [1, 3]\nlst.insert(1, 2)  # [1, 2, 3]\n```")

add("how do I sort a list",
    "`.sort()` sorts in place; `sorted()` returns a new list:\n\n```python\nlst = [3, 1, 2]\nlst.sort()           # lst is now [1, 2, 3]\nsorted([3, 1, 2])    # [1, 2, 3]\n```")

add("sort a list in descending order python",
    "Pass `reverse=True`:\n\n```python\nsorted([1, 3, 2], reverse=True)  # [3, 2, 1]\n```")

add("how to reverse a list",
    "Use `.reverse()` in place, `[::-1]` for a copy, or `reversed()` for an iterator:\n\n```python\nlst = [1, 2, 3]\nlst[::-1]  # [3, 2, 1]\n```")

add("get the length of a list",
    "Use `len()`:\n\n```python\nlen([1, 2, 3])  # 3\n```")

add("how do I check if a list contains a value",
    "Use `in`:\n\n```python\nif 3 in [1, 2, 3]:\n    print(\"yes\")\n```")

add("find the index of an item in a list",
    "Use `.index()`:\n\n```python\n[\"a\", \"b\", \"c\"].index(\"b\")  # 1\n```")

add("how to count items in a list python",
    "Use `.count()` for a specific value:\n\n```python\n[1, 1, 2, 1].count(1)  # 3\n```")

add("sum a list of numbers python",
    "Use `sum()`:\n\n```python\nsum([1, 2, 3, 4])  # 10\n```")

add("max and min of a list",
    "Use `max()` and `min()`:\n\n```python\nmax([3, 1, 9, 2])  # 9\nmin([3, 1, 9, 2])  # 1\n```")

add("how do I remove duplicates from a list",
    "Convert to a set and back. Use `dict.fromkeys` if you must keep order:\n\n```python\nlst = [1, 2, 2, 3, 1]\nlist(set(lst))            # order not guaranteed\nlist(dict.fromkeys(lst))  # [1, 2, 3] order preserved\n```")

add("how to copy a list python",
    "Use `.copy()`, slicing, or `list()`. Plain assignment just creates another reference:\n\n```python\na = [1, 2, 3]\nb = a.copy()   # independent copy\nc = a[:]       # also a copy\n```")

add("clear all items from a list",
    "Use `.clear()`:\n\n```python\nlst = [1, 2, 3]\nlst.clear()  # []\n```")

add("how do I get every other element of a list",
    "Use a slice step of 2:\n\n```python\nlst = [0, 1, 2, 3, 4, 5]\nlst[::2]  # [0, 2, 4]\n```")

add("flatten a list of lists python",
    "Use a nested comprehension:\n\n```python\nnested = [[1, 2], [3, 4], [5]]\nflat = [x for row in nested for x in row]\n# [1, 2, 3, 4, 5]\n```")

add("how to find the second largest number in a list",
    "Sort the unique values and take the second from the end:\n\n```python\ndef second_largest(nums):\n    return sorted(set(nums))[-2]\n\nsecond_largest([5, 1, 9, 9, 3])  # 5\n```")

add("how do I check if a list is empty",
    "An empty list is falsy, so just test it directly:\n\n```python\nif not lst:\n    print(\"empty\")\n```")

add("multiply every element in a list by 2",
    "Use a list comprehension:\n\n```python\nnums = [1, 2, 3]\ndoubled = [n * 2 for n in nums]  # [2, 4, 6]\n```")

add("how to concatenate two lists",
    "Use `+` or `.extend()`:\n\n```python\n[1, 2] + [3, 4]  # [1, 2, 3, 4]\n```")

add("average of a list python",
    "Divide the sum by the length:\n\n```python\nnums = [2, 4, 6]\navg = sum(nums) / len(nums)  # 4.0\n```")

add("sort a list of strings by length",
    "Pass `key=len`:\n\n```python\nwords = [\"ccc\", \"a\", \"bb\"]\nsorted(words, key=len)  # ['a', 'bb', 'ccc']\n```")

add("how to create a list of numbers from 1 to 10",
    "Wrap `range` in `list()`:\n\n```python\nlist(range(1, 11))  # [1, 2, ..., 10]\n```")

add("repeat a list element python",
    "Multiply the list by an int:\n\n```python\n[0] * 5  # [0, 0, 0, 0, 0]\n```")

# ---------------- Slicing ----------------
add("explain list slicing in python",
    "Slicing uses `seq[start:stop:step]`. `start` is inclusive, `stop` is exclusive, `step` is the stride. Any can be omitted.\n\n```python\nlst = [0, 1, 2, 3, 4]\nlst[1:4]   # [1, 2, 3]\nlst[:3]    # [0, 1, 2]\nlst[2:]    # [2, 3, 4]\nlst[::-1]  # [4, 3, 2, 1, 0]\n```")

add("get the first 3 elements of a list",
    "Slice from the start:\n\n```python\nlst[:3]\n```")

add("get the last 3 elements of a list",
    "Use a negative start:\n\n```python\nlst[-3:]\n```")

add("how to get everything except the last element",
    "```python\nlst[:-1]\n```")

add("slice a string python",
    "Strings slice just like lists:\n\n```python\ns = \"python\"\ns[0:3]   # 'pyt'\ns[-3:]   # 'hon'\n```")

add("what does s[::-1] do",
    "It reverses a sequence by slicing with a step of -1, producing a new reversed copy:\n\n```python\n\"abc\"[::-1]  # 'cba'\n```")

# ---------------- Dicts ----------------
add("how do I create a dictionary in python",
    "Use curly braces with key-value pairs:\n\n```python\nperson = {\"name\": \"Sam\", \"age\": 30}\nempty = {}\n```")

add("add a key to a dictionary",
    "Assign to a new key:\n\n```python\nd = {}\nd[\"color\"] = \"blue\"\n```")

add("how to get a value from a dict safely",
    "Use `.get()` to avoid a KeyError when the key is missing:\n\n```python\nd = {\"a\": 1}\nd.get(\"b\")          # None\nd.get(\"b\", 0)       # 0 (default)\n```")

add("loop through a dictionary python",
    "Use `.items()` to get keys and values together:\n\n```python\nfor key, value in d.items():\n    print(key, value)\n```")

add("how do I get all keys of a dictionary",
    "Use `.keys()`:\n\n```python\nlist(d.keys())\n```")

add("get all values from a dict",
    "Use `.values()`:\n\n```python\nlist(d.values())\n```")

add("check if a key exists in a dictionary",
    "Use `in`:\n\n```python\nif \"name\" in d:\n    print(\"present\")\n```")

add("how to delete a key from a dictionary",
    "Use `del` or `.pop()`:\n\n```python\ndel d[\"age\"]\nd.pop(\"name\", None)  # safe, returns default if missing\n```")

add("merge two dictionaries python",
    "In Python 3.9+ use the `|` operator, or `**` unpacking:\n\n```python\na = {\"x\": 1}\nb = {\"y\": 2}\na | b              # {'x': 1, 'y': 2}\n{**a, **b}         # same result\n```")

add("how do I count word frequencies in python",
    "Use `collections.Counter` or a plain dict:\n\n```python\nfrom collections import Counter\nwords = \"a b a c a b\".split()\nCounter(words)  # Counter({'a': 3, 'b': 2, 'c': 1})\n```")

add("dictionary default value if key missing",
    "Use `.get(key, default)` or `collections.defaultdict`:\n\n```python\nfrom collections import defaultdict\nd = defaultdict(int)\nd[\"x\"] += 1  # no KeyError, starts at 0\n```")

add("how to iterate dict keys and values",
    "```python\nfor k, v in d.items():\n    print(f\"{k} -> {v}\")\n```")

add("sort a dictionary by value python",
    "Use `sorted()` with a key on the items:\n\n```python\nd = {\"a\": 3, \"b\": 1, \"c\": 2}\ndict(sorted(d.items(), key=lambda kv: kv[1]))\n# {'b': 1, 'c': 2, 'a': 3}\n```")

add("sort dict by key",
    "```python\ndict(sorted(d.items()))\n```")

add("invert a dictionary swap keys and values",
    "Use a dict comprehension:\n\n```python\nd = {\"a\": 1, \"b\": 2}\n{v: k for k, v in d.items()}  # {1: 'a', 2: 'b'}\n```")

add("get the key with the max value in a dict",
    "Use `max()` with `key=d.get`:\n\n```python\nd = {\"a\": 3, \"b\": 9, \"c\": 1}\nmax(d, key=d.get)  # 'b'\n```")

add("how to update a dict with another dict",
    "Use `.update()`:\n\n```python\nd = {\"a\": 1}\nd.update({\"b\": 2})  # {'a': 1, 'b': 2}\n```")

add("create a dict from two lists python",
    "Zip them and pass to `dict()`:\n\n```python\nkeys = [\"a\", \"b\"]\nvals = [1, 2]\ndict(zip(keys, vals))  # {'a': 1, 'b': 2}\n```")

# ---------------- Tuples ----------------
add("what is a tuple in python",
    "A tuple is an ordered, immutable sequence. You create it with parentheses (or just commas). Once created you can't change its contents.\n\n```python\npoint = (3, 4)\nsingle = (5,)  # note the trailing comma\n```")

add("difference between list and tuple",
    "Lists are mutable (you can change them) and use `[]`; tuples are immutable and use `()`. Use tuples for fixed collections and as dict keys.\n\n```python\n[1, 2]  # mutable list\n(1, 2)  # immutable tuple\n```")

add("how to make a tuple with one element",
    "Add a trailing comma, otherwise it's just parentheses:\n\n```python\nt = (5,)   # tuple\nx = (5)    # just the int 5\n```")

add("unpack a tuple python",
    "Assign it to multiple variables:\n\n```python\npoint = (3, 4)\nx, y = point\n```")

add("convert tuple to list python",
    "Use `list()`:\n\n```python\nlist((1, 2, 3))  # [1, 2, 3]\n```")

add("can I use a tuple as a dictionary key",
    "Yes, because tuples are hashable (as long as their contents are):\n\n```python\nlocations = {(0, 0): \"origin\", (1, 2): \"point A\"}\n```")

# ---------------- Sets ----------------
add("what is a set in python",
    "A set is an unordered collection of unique elements. Great for membership tests and removing duplicates.\n\n```python\ns = {1, 2, 3}\ns.add(2)  # still {1, 2, 3}\n```")

add("how to create an empty set",
    "Use `set()` — `{}` makes an empty dict, not a set:\n\n```python\nempty = set()\n```")

add("union of two sets python",
    "Use `|` or `.union()`:\n\n```python\n{1, 2} | {2, 3}  # {1, 2, 3}\n```")

add("intersection of two sets",
    "Use `&` or `.intersection()`:\n\n```python\n{1, 2, 3} & {2, 3, 4}  # {2, 3}\n```")

add("difference of sets python",
    "Use `-`:\n\n```python\n{1, 2, 3} - {2}  # {1, 3}\n```")

add("how do I find common elements between two lists",
    "Convert to sets and intersect:\n\n```python\na = [1, 2, 3]\nb = [2, 3, 4]\nlist(set(a) & set(b))  # [2, 3]\n```")

add("add to a set python",
    "Use `.add()`:\n\n```python\ns = {1, 2}\ns.add(3)\n```")

add("symmetric difference of two sets",
    "Use `^` for elements in either set but not both:\n\n```python\n{1, 2, 3} ^ {2, 3, 4}  # {1, 4}\n```")

add("check if one set is a subset of another",
    "Use `<=` or `.issubset()`:\n\n```python\n{1, 2} <= {1, 2, 3}  # True\n```")

# ---------------- Booleans & truthiness ----------------
add("what is truthiness in python",
    "Every value can be evaluated as True or False in a boolean context. Empty collections, `0`, `\"\"`, and `None` are falsy; almost everything else is truthy.\n\n```python\nbool(0)     # False\nbool(\"\")    # False\nbool([])    # False\nbool([0])   # True\n```")

add("what values are falsy in python",
    "The falsy values are: `False`, `None`, `0`, `0.0`, `\"\"` (empty string), `[]`, `{}`, `()`, `set()`, and `range(0)`. Everything else is truthy.")

add("how do I convert something to a boolean",
    "Use `bool()`:\n\n```python\nbool(1)    # True\nbool(0)    # False\nbool(\"x\")  # True\n```")

add("and or not in python",
    "These are the logical operators. `and`/`or` short-circuit and return one of the operands, not strictly True/False:\n\n```python\nTrue and False  # False\nTrue or False   # True\nnot True        # False\n```")

add("what does the or operator return for default values",
    "`or` returns the first truthy operand, which is handy for defaults:\n\n```python\nname = user_input or \"Anonymous\"\n```")

# ---------------- Operators ----------------
add("what are comparison operators in python",
    "They compare two values and return a bool: `==` equal, `!=` not equal, `<`, `>`, `<=`, `>=`.\n\n```python\n5 > 3   # True\n5 != 3  # True\n```")

add("can I chain comparisons in python",
    "Yes, Python lets you chain them naturally:\n\n```python\nx = 5\nif 0 < x < 10:\n    print(\"in range\")\n```")

add("difference between is and ==",
    "`==` checks value equality; `is` checks identity (same object in memory). Use `is` only for `None`, `True`, `False`.\n\n```python\na = [1, 2]\nb = [1, 2]\na == b  # True (same values)\na is b  # False (different objects)\n```")

add("what does += do in python",
    "It's an augmented assignment: `x += 1` is shorthand for `x = x + 1`. Similar operators exist for `-=`, `*=`, `/=`, etc.\n\n```python\nx = 5\nx += 3  # x is now 8\n```")

add("bitwise operators python",
    "Python has `&` (and), `|` (or), `^` (xor), `~` (not), `<<` (left shift), `>>` (right shift):\n\n```python\n5 & 3   # 1\n5 | 2   # 7\n1 << 4  # 16\n```")

# ---------------- Control flow ----------------
add("how do I write an if statement in python",
    "```python\nif x > 0:\n    print(\"positive\")\nelif x == 0:\n    print(\"zero\")\nelse:\n    print(\"negative\")\n```")

add("how to write a for loop python",
    "Iterate directly over a sequence:\n\n```python\nfor item in [1, 2, 3]:\n    print(item)\n```")

add("loop a certain number of times python",
    "Use `range()`:\n\n```python\nfor i in range(5):\n    print(i)  # 0 1 2 3 4\n```")

add("while loop example python",
    "```python\ncount = 0\nwhile count < 3:\n    print(count)\n    count += 1\n```")

add("what does break do in a loop",
    "`break` immediately exits the innermost loop:\n\n```python\nfor n in range(10):\n    if n == 5:\n        break\n    print(n)  # prints 0..4\n```")

add("what does continue do",
    "`continue` skips the rest of the current iteration and moves to the next:\n\n```python\nfor n in range(5):\n    if n % 2 == 0:\n        continue\n    print(n)  # prints 1, 3\n```")

add("how to write an infinite loop python",
    "Use `while True` and break out when needed:\n\n```python\nwhile True:\n    cmd = input(\"> \")\n    if cmd == \"quit\":\n        break\n```")

add("for else loop python what does it mean",
    "The `else` after a `for` runs only if the loop completed without hitting `break`. Useful for search loops:\n\n```python\nfor x in items:\n    if x == target:\n        print(\"found\")\n        break\nelse:\n    print(\"not found\")\n```")

add("how to loop with index python",
    "Use `enumerate()`:\n\n```python\nfor i, value in enumerate([\"a\", \"b\", \"c\"]):\n    print(i, value)\n```")

add("loop two lists at the same time python",
    "Use `zip()`:\n\n```python\nnames = [\"a\", \"b\"]\nages = [30, 25]\nfor name, age in zip(names, ages):\n    print(name, age)\n```")

add("how do I do a nested loop in python",
    "Put one loop inside another:\n\n```python\nfor i in range(3):\n    for j in range(3):\n        print(i, j)\n```")

add("countdown loop python",
    "Use `range` with a negative step:\n\n```python\nfor i in range(5, 0, -1):\n    print(i)  # 5 4 3 2 1\n```")

add("fizzbuzz in python",
    "```python\nfor n in range(1, 16):\n    if n % 15 == 0:\n        print(\"FizzBuzz\")\n    elif n % 3 == 0:\n        print(\"Fizz\")\n    elif n % 5 == 0:\n        print(\"Buzz\")\n    else:\n        print(n)\n```")

add("how do I check multiple conditions in an if",
    "Combine them with `and` / `or`:\n\n```python\nif age >= 18 and has_id:\n    print(\"allowed\")\n```")

add("match statement python example",
    "Python 3.10+ has structural pattern matching with `match`/`case`:\n\n```python\ndef describe(x):\n    match x:\n        case 0:\n            return \"zero\"\n        case 1 | 2:\n            return \"small\"\n        case _:\n            return \"other\"\n```")

# ---------------- Ternary ----------------
add("ternary operator python",
    "Python's conditional expression reads `A if condition else B`:\n\n```python\nstatus = \"adult\" if age >= 18 else \"minor\"\n```")

add("one line if else python",
    "Use a conditional expression:\n\n```python\nx = 10\nsign = \"pos\" if x > 0 else \"non-pos\"\n```")

add("how to assign a value based on a condition in one line",
    "Use the ternary form `value_if_true if cond else value_if_false`:\n\n```python\nmax_val = a if a > b else b\n```")

# ---------------- Comprehensions ----------------
add("what is a list comprehension",
    "A concise way to build a list from an iterable. The form is `[expr for item in iterable if condition]`.\n\n```python\nsquares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]\n```")

add("list comprehension with condition python",
    "Add an `if` clause at the end:\n\n```python\nevens = [x for x in range(10) if x % 2 == 0]\n# [0, 2, 4, 6, 8]\n```")

add("how do I write a dict comprehension",
    "Use `{key: value for ...}`:\n\n```python\nsquares = {x: x**2 for x in range(4)}\n# {0: 0, 1: 1, 2: 4, 3: 9}\n```")

add("set comprehension python",
    "Use `{expr for ...}`:\n\n```python\nunique_lengths = {len(w) for w in [\"a\", \"bb\", \"cc\"]}\n# {1, 2}\n```")

add("convert a for loop to a list comprehension",
    "A loop that appends becomes a comprehension. For example:\n\n```python\n# loop\nresult = []\nfor x in range(5):\n    result.append(x * 2)\n\n# comprehension\nresult = [x * 2 for x in range(5)]\n```")

add("comprehension with if else python",
    "Put the conditional expression before the `for`:\n\n```python\n[x if x > 0 else 0 for x in nums]\n```")

add("nested list comprehension python",
    "Stack the `for` clauses left to right:\n\n```python\nmatrix = [[1, 2], [3, 4]]\nflat = [x for row in matrix for x in row]  # [1, 2, 3, 4]\n```")

add("how to filter a list with a comprehension",
    "Add an `if` at the end to keep only matching items:\n\n```python\nwords = [\"apple\", \"\", \"pear\", \"\"]\nnon_empty = [w for w in words if w]\n```")

add("create a dict from a list with comprehension",
    "```python\nwords = [\"a\", \"bb\", \"ccc\"]\nlengths = {w: len(w) for w in words}\n# {'a': 1, 'bb': 2, 'ccc': 3}\n```")

add("generator expression vs list comprehension",
    "A generator expression uses `()` and is lazy — it computes values one at a time, saving memory. A list comprehension builds the whole list at once.\n\n```python\nsum(x**2 for x in range(1000000))  # memory-efficient\n```")

# ---------------- Functions ----------------
add("how do I define a function in python",
    "Use the `def` keyword:\n\n```python\ndef greet(name):\n    return f\"Hello, {name}\"\n\ngreet(\"Sam\")  # 'Hello, Sam'\n```")

add("function with default argument python",
    "Give the parameter a value in the signature:\n\n```python\ndef greet(name, greeting=\"Hi\"):\n    return f\"{greeting}, {name}\"\n\ngreet(\"Sam\")              # 'Hi, Sam'\ngreet(\"Sam\", \"Hello\")     # 'Hello, Sam'\n```")

add("what does *args mean in python",
    "`*args` collects extra positional arguments into a tuple, letting a function accept any number of them.\n\n```python\ndef total(*args):\n    return sum(args)\n\ntotal(1, 2, 3)  # 6\n```")

add("what does **kwargs do",
    "`**kwargs` collects extra keyword arguments into a dict.\n\n```python\ndef show(**kwargs):\n    for k, v in kwargs.items():\n        print(k, v)\n\nshow(a=1, b=2)\n```")

add("how to return multiple values from a function",
    "Return a tuple; the caller can unpack it:\n\n```python\ndef min_max(nums):\n    return min(nums), max(nums)\n\nlo, hi = min_max([3, 1, 9])\n```")

add("what is a lambda function",
    "A lambda is a small anonymous function written inline. The form is `lambda args: expression`.\n\n```python\nsquare = lambda x: x ** 2\nsquare(5)  # 25\n```")

add("when should I use a lambda",
    "Use lambdas for short throwaway functions, typically as arguments to `sorted`, `map`, or `filter`:\n\n```python\npairs = [(1, \"b\"), (2, \"a\")]\nsorted(pairs, key=lambda p: p[1])  # sort by second element\n```")

add("default argument mutable bug python",
    "Never use a mutable default like `[]` — it's shared across calls. Use `None` and create it inside:\n\n```python\ndef add_item(item, items=None):\n    if items is None:\n        items = []\n    items.append(item)\n    return items\n```")

add("how do keyword arguments work in python",
    "You can pass arguments by name, in any order:\n\n```python\ndef rect(width, height):\n    return width * height\n\nrect(height=4, width=3)  # 12\n```")

add("force keyword only arguments python",
    "Put a bare `*` in the signature; parameters after it must be passed by name:\n\n```python\ndef connect(host, *, port=80):\n    ...\n\nconnect(\"example.com\", port=443)  # port must be named\n```")

add("positional only parameters python",
    "Use `/` in the signature; parameters before it can't be passed by keyword:\n\n```python\ndef f(x, y, /):\n    return x + y\n\nf(1, 2)  # ok; f(x=1, y=2) is an error\n```")

add("how to document a function in python",
    "Add a docstring as the first statement:\n\n```python\ndef area(r):\n    \"\"\"Return the area of a circle with radius r.\"\"\"\n    return 3.14159 * r ** 2\n```")

add("what is a closure in python",
    "A closure is a nested function that remembers variables from the enclosing scope even after the outer function has finished.\n\n```python\ndef multiplier(n):\n    def mul(x):\n        return x * n\n    return mul\n\ntimes3 = multiplier(3)\ntimes3(5)  # 15\n```")

add("how do I modify a global variable inside a function",
    "Declare it with `global`:\n\n```python\ncount = 0\ndef increment():\n    global count\n    count += 1\n```")

add("nonlocal keyword python",
    "`nonlocal` lets a nested function rebind a variable from the enclosing (non-global) scope:\n\n```python\ndef counter():\n    n = 0\n    def inc():\n        nonlocal n\n        n += 1\n        return n\n    return inc\n```")

add("explain scope in python",
    "Python resolves names using the LEGB rule: Local, Enclosing, Global, Built-in, in that order. Assigning inside a function creates a local name unless you use `global`/`nonlocal`.")

add("pass a function as an argument python",
    "Functions are objects, so just pass the name without calling it:\n\n```python\ndef apply(fn, x):\n    return fn(x)\n\napply(abs, -5)  # 5\n```")

add("how to give a function variable number of arguments",
    "Use `*args` for positional and `**kwargs` for keyword:\n\n```python\ndef log(*args, **kwargs):\n    print(args, kwargs)\n\nlog(1, 2, level=\"info\")\n```")

add("recursive function python example",
    "```python\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nfactorial(5)  # 120\n```")

add("unpack a list into function arguments",
    "Use `*` to spread a list and `**` to spread a dict:\n\n```python\ndef add(a, b, c):\n    return a + b + c\n\nargs = [1, 2, 3]\nadd(*args)  # 6\n```")

# ---------------- enumerate / zip / range ----------------
add("what does enumerate do",
    "`enumerate()` yields `(index, value)` pairs while iterating, so you get a counter for free.\n\n```python\nfor i, c in enumerate(\"abc\"):\n    print(i, c)  # 0 a / 1 b / 2 c\n```")

add("enumerate starting at 1",
    "Pass the `start` argument:\n\n```python\nfor i, item in enumerate(items, start=1):\n    print(i, item)\n```")

add("what does zip do in python",
    "`zip()` pairs up elements from multiple iterables, stopping at the shortest one.\n\n```python\nlist(zip([1, 2, 3], [\"a\", \"b\", \"c\"]))\n# [(1, 'a'), (2, 'b'), (3, 'c')]\n```")

add("how to unzip a list of pairs python",
    "Use `zip(*pairs)`:\n\n```python\npairs = [(1, \"a\"), (2, \"b\")]\nnums, letters = zip(*pairs)\n# nums = (1, 2), letters = ('a', 'b')\n```")

add("what does range do",
    "`range(start, stop, step)` produces a sequence of integers from `start` up to but not including `stop`.\n\n```python\nlist(range(2, 10, 2))  # [2, 4, 6, 8]\n```")

add("range backwards python",
    "Use a negative step:\n\n```python\nlist(range(10, 0, -1))  # [10, 9, ..., 1]\n```")

add("range with one argument",
    "A single argument is the stop value, starting from 0:\n\n```python\nlist(range(4))  # [0, 1, 2, 3]\n```")

# ---------------- map / filter ----------------
add("what does map do in python",
    "`map()` applies a function to every item of an iterable, returning a lazy iterator:\n\n```python\nlist(map(str, [1, 2, 3]))  # ['1', '2', '3']\n```")

add("what does filter do",
    "`filter()` keeps only items for which a function returns True:\n\n```python\nlist(filter(lambda x: x > 0, [-1, 2, -3, 4]))  # [2, 4]\n```")

add("map vs list comprehension",
    "Both transform iterables. Comprehensions are usually more readable; `map` can be slightly faster with an existing function:\n\n```python\nlist(map(str.upper, words))\n[w.upper() for w in words]\n```")

# ---------------- Unpacking ----------------
add("how do I unpack a list in python",
    "Assign it to matching variables:\n\n```python\na, b, c = [1, 2, 3]\n```")

add("star unpacking python",
    "A starred target captures the remaining items as a list:\n\n```python\nfirst, *rest = [1, 2, 3, 4]\n# first = 1, rest = [2, 3, 4]\n```")

add("get first and last element with unpacking",
    "Use a starred middle:\n\n```python\nfirst, *middle, last = [1, 2, 3, 4, 5]\n# first=1, middle=[2,3,4], last=5\n```")

add("unpack nested tuples python",
    "Mirror the structure on the left side:\n\n```python\n(a, (b, c)) = (1, (2, 3))\n# a=1, b=2, c=3\n```")

add("ignore a value when unpacking python",
    "Use `_` as a throwaway name:\n\n```python\nx, _, z = (1, 2, 3)\n```")

# ---------------- Walrus ----------------
add("what is the walrus operator",
    "`:=` assigns a value as part of an expression. It's handy to avoid computing something twice:\n\n```python\nif (n := len(data)) > 10:\n    print(f\"too long: {n} items\")\n```")

add("walrus operator in a while loop",
    "It lets you read and test in one line:\n\n```python\nwhile (line := input()) != \"quit\":\n    print(line)\n```")

add("use walrus operator in list comprehension",
    "It avoids recomputing a value:\n\n```python\n[y for x in data if (y := f(x)) > 0]\n```")

# ---------------- Type conversion ----------------
add("convert list to string python",
    "Use `.join()` if items are strings, else map them first:\n\n```python\n\"\".join([\"a\", \"b\", \"c\"])         # 'abc'\n\",\".join(map(str, [1, 2, 3]))     # '1,2,3'\n```")

add("string to list of characters python",
    "Pass the string to `list()`:\n\n```python\nlist(\"abc\")  # ['a', 'b', 'c']\n```")

add("convert list to set python",
    "```python\nset([1, 2, 2, 3])  # {1, 2, 3}\n```")

add("how to convert bool to int python",
    "Pass it to `int()`; True is 1 and False is 0:\n\n```python\nint(True)   # 1\nint(False)  # 0\n```")

add("convert string to list python",
    "If it's comma-separated use `.split()`; for individual characters use `list()`:\n\n```python\n\"a,b,c\".split(\",\")  # ['a', 'b', 'c']\nlist(\"abc\")         # ['a', 'b', 'c']\n```")

add("how do I turn a number into a string",
    "Use `str()`:\n\n```python\nstr(42)  # '42'\n```")

# ---------------- Identity examples ----------------
add("who are you", "I'm Silicat, a Python coding assistant.")
add("what are you", "I'm Silicat, an assistant that helps you write and understand Python code.")
add("what's your name?", "My name is Silicat. I help with Python programming.")
add("are you chatgpt", "No, I'm Silicat, a Python coding assistant.")
add("what can you do", "I'm Silicat. I can help you write, debug, and understand Python code across topics like data types, functions, loops, comprehensions, and more.")
add("introduce yourself", "Hi, I'm Silicat, a coding assistant focused on Python. Ask me anything about Python and I'll help.")

# ---------------- More string variety ----------------
add("how to remove vowels from a string",
    "```python\ndef remove_vowels(s):\n    return \"\".join(c for c in s if c not in \"aeiouAEIOU\")\n\nremove_vowels(\"hello\")  # 'hll'\n```")

add("how do I check if two strings are anagrams",
    "Sort both and compare, or compare character counts:\n\n```python\ndef is_anagram(a, b):\n    return sorted(a) == sorted(b)\n\nis_anagram(\"listen\", \"silent\")  # True\n```")

add("how to find the longest word in a sentence",
    "```python\nsentence = \"the quick brown fox\"\nlongest = max(sentence.split(), key=len)  # 'quick'\n```")

add("how do I check if a string is empty",
    "Empty strings are falsy, so test directly:\n\n```python\nif not s:\n    print(\"empty\")\n```")

add("count words in a string python",
    "Split and take the length:\n\n```python\nlen(\"one two three\".split())  # 3\n```")

add("how to replace only the first occurrence in a string",
    "Pass a count of 1 to `.replace()`:\n\n```python\n\"a-b-c\".replace(\"-\", \"_\", 1)  # 'a_b-c'\n```")

add("multiline string python",
    "Use triple quotes:\n\n```python\ntext = \"\"\"line one\nline two\nline three\"\"\"\n```")

add("how to escape quotes in a string python",
    "Use a backslash or the other quote style:\n\n```python\n'It\\'s here'\n\"It's here\"\n```")

add("raw string python what is it",
    "An `r` prefix makes backslashes literal, which is great for regex and Windows paths:\n\n```python\nr\"C:\\new\\folder\"  # backslashes not treated as escapes\n```")

add("how do I split a string on multiple delimiters",
    "Use `re.split` with a character class:\n\n```python\nimport re\nre.split(r\"[,;]\", \"a,b;c\")  # ['a', 'b', 'c']\n```")

add("strip a specific character from a string",
    "Pass the characters to `.strip()`:\n\n```python\n\"***hi***\".strip(\"*\")  # 'hi'\n```")

# ---------------- Misc useful patterns ----------------
add("how to read user input in python",
    "Use `input()`, which always returns a string:\n\n```python\nname = input(\"Your name: \")\nage = int(input(\"Your age: \"))  # convert if you need a number\n```")

add("how do I print without a newline python",
    "Pass `end=\"\"` to `print`:\n\n```python\nprint(\"a\", end=\"\")\nprint(\"b\")  # prints 'ab'\n```")

add("print multiple things with a separator",
    "Use the `sep` argument:\n\n```python\nprint(\"2025\", \"01\", \"15\", sep=\"-\")  # 2025-01-15\n```")

add("how to check if all elements meet a condition",
    "Use `all()`:\n\n```python\nall(x > 0 for x in [1, 2, 3])  # True\n```")

add("check if any element meets a condition python",
    "Use `any()`:\n\n```python\nany(x < 0 for x in [1, -2, 3])  # True\n```")

add("how do I sort a list of tuples by second element",
    "Use a key on index 1:\n\n```python\npairs = [(1, 3), (2, 1), (3, 2)]\nsorted(pairs, key=lambda p: p[1])  # [(2, 1), (3, 2), (1, 3)]\n```")

add("how to swap keys and values keeping it sorted",
    "```python\nd = {\"a\": 3, \"b\": 1}\nsorted(d.items(), key=lambda kv: kv[1])\n# [('b', 1), ('a', 3)]\n```")

add("how do I find duplicates in a list",
    "Compare counts, or use a Counter:\n\n```python\nfrom collections import Counter\nnums = [1, 2, 2, 3, 3, 3]\ndups = [k for k, v in Counter(nums).items() if v > 1]\n# [2, 3]\n```")

add("how to chunk a list into groups of n",
    "Slice in steps of n:\n\n```python\ndef chunk(lst, n):\n    return [lst[i:i+n] for i in range(0, len(lst), n)]\n\nchunk([1, 2, 3, 4, 5], 2)  # [[1, 2], [3, 4], [5]]\n```")

add("how do I generate a list of squares",
    "```python\n[x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]\n```")

add("how to create a multiplication table python",
    "```python\nfor i in range(1, 4):\n    for j in range(1, 4):\n        print(f\"{i}x{j}={i*j}\", end=\"  \")\n    print()\n```")

add("how do I sum only even numbers in a list",
    "```python\nnums = [1, 2, 3, 4, 5, 6]\ntotal = sum(n for n in nums if n % 2 == 0)  # 12\n```")

add("how to find the most common element in a list",
    "Use `Counter.most_common`:\n\n```python\nfrom collections import Counter\nCounter([1, 1, 2, 3, 1]).most_common(1)  # [(1, 3)]\n```")

add("how do I reverse the words in a sentence",
    "Split, reverse, and join:\n\n```python\nsentence = \"hello world foo\"\n\" \".join(sentence.split()[::-1])  # 'foo world hello'\n```")

add("how to check if a year is a leap year",
    "```python\ndef is_leap(year):\n    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)\n\nis_leap(2024)  # True\n```")

add("convert celsius to fahrenheit python",
    "```python\ndef c_to_f(c):\n    return c * 9 / 5 + 32\n\nc_to_f(100)  # 212.0\n```")

add("how do I check if a number is prime",
    "```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n```")

add("fibonacci sequence python",
    "```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\n[fib(i) for i in range(8)]  # [0, 1, 1, 2, 3, 5, 8, 13]\n```")

add("how to find the gcd of two numbers",
    "Use `math.gcd`:\n\n```python\nimport math\nmath.gcd(48, 36)  # 12\n```")

add("how do I generate random numbers python",
    "Use the `random` module:\n\n```python\nimport random\nrandom.randint(1, 6)        # inclusive both ends\nrandom.choice([\"a\", \"b\"])   # random element\n```")

add("shuffle a list python",
    "Use `random.shuffle`, which shuffles in place:\n\n```python\nimport random\nlst = [1, 2, 3, 4]\nrandom.shuffle(lst)\n```")

# ---------------- Conceptual ----------------
add("is python statically or dynamically typed",
    "Python is dynamically typed: variables don't have fixed types and you don't declare them. The type is associated with the value, not the name, and can change at runtime.")

add("what is the difference between mutable and immutable",
    "Mutable objects (lists, dicts, sets) can be changed in place. Immutable objects (int, float, str, tuple, frozenset) cannot — operations on them create new objects instead.")

add("why is my list changing unexpectedly python",
    "Most likely two variables reference the same list. Assignment doesn't copy; use `.copy()` or `list()` for an independent copy:\n\n```python\nb = a.copy()\n```")

add("what's the difference between append and extend",
    "`.append(x)` adds `x` as a single element; `.extend(iterable)` adds each element of the iterable:\n\n```python\nlst = [1]\nlst.append([2, 3])  # [1, [2, 3]]\nlst = [1]\nlst.extend([2, 3])  # [1, 2, 3]\n```")

add("difference between sort and sorted",
    "`list.sort()` sorts the list in place and returns `None`. `sorted()` works on any iterable and returns a new sorted list, leaving the original unchanged.")

add("what is a docstring",
    "A docstring is a string literal placed as the first statement of a module, function, or class. It documents what the object does and is accessible via `__doc__` or `help()`.")

add("what does pass do in python",
    "`pass` is a no-op placeholder; it does nothing but is syntactically required where a statement is expected:\n\n```python\ndef todo():\n    pass\n```")

add("what is the difference between return and print",
    "`print` displays output to the console; `return` sends a value back to the caller so it can be used. A function without `return` returns `None`.")

# ---------------- MULTI-TURN conversations ----------------
addmt([
    "write a function to add two numbers",
    "```python\ndef add(a, b):\n    return a + b\n\nadd(2, 3)  # 5\n```",
    "now make it handle any number of arguments",
    "Use `*args` to accept any count and sum them:\n\n```python\ndef add(*args):\n    return sum(args)\n\nadd(2, 3)        # 5\nadd(1, 2, 3, 4)  # 10\n```",
])

addmt([
    "how do I reverse a string",
    "Slice with a step of -1:\n\n```python\ns = \"hello\"\ns[::-1]  # 'olleh'\n```",
    "what if I want to reverse only the letters and ignore spaces",
    "Keep the spaces in place and reverse just the letters:\n\n```python\ndef reverse_letters(s):\n    letters = [c for c in s if c != \" \"][::-1]\n    it = iter(letters)\n    return \"\".join(next(it) if c != \" \" else \" \" for c in s)\n\nreverse_letters(\"ab cd\")  # 'dc ba'\n```",
])

addmt([
    "write a list comprehension that squares numbers 1 to 5",
    "```python\n[x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]\n```",
    "now only keep the even squares",
    "Add a filter that checks the square is even:\n\n```python\n[x**2 for x in range(1, 6) if x**2 % 2 == 0]  # [4, 16]\n```",
])

addmt([
    "how do I find the max value in a list",
    "Use the built-in `max()`:\n\n```python\nmax([3, 7, 2, 9, 4])  # 9\n```",
    "what if the list is empty",
    "`max([])` raises ValueError. Pass a `default` to handle it:\n\n```python\nmax([], default=None)  # None\n```",
])

addmt([
    "how to count how many times each letter appears in a string",
    "Use `collections.Counter`:\n\n```python\nfrom collections import Counter\nCounter(\"banana\")  # Counter({'a': 3, 'n': 2, 'b': 1})\n```",
    "how do I get just the most common one",
    "Use `.most_common(1)`:\n\n```python\nCounter(\"banana\").most_common(1)  # [('a', 3)]\n```",
])

addmt([
    "write a function that returns whether a number is even",
    "```python\ndef is_even(n):\n    return n % 2 == 0\n```",
    "make it work for negative numbers too",
    "It already does — `%` handles negatives correctly for evenness:\n\n```python\nis_even(-4)  # True\nis_even(-3)  # False\n```\nNo change needed.",
])

addmt([
    "how do I merge two dictionaries",
    "In Python 3.9+ use `|`:\n\n```python\na = {\"x\": 1}\nb = {\"y\": 2}\na | b  # {'x': 1, 'y': 2}\n```",
    "what happens if they share a key",
    "The right-hand dict wins for shared keys:\n\n```python\n{\"x\": 1} | {\"x\": 9}  # {'x': 9}\n```",
])

addmt([
    "loop over a list and print each item",
    "```python\nfor item in [\"a\", \"b\", \"c\"]:\n    print(item)\n```",
    "now print the index too",
    "Use `enumerate()`:\n\n```python\nfor i, item in enumerate([\"a\", \"b\", \"c\"]):\n    print(i, item)\n```",
])

addmt([
    "how do I remove duplicates from a list",
    "Convert to a set:\n\n```python\nlist(set([1, 2, 2, 3]))  # order not guaranteed\n```",
    "I need to keep the original order though",
    "Use `dict.fromkeys`, which preserves insertion order:\n\n```python\nlist(dict.fromkeys([3, 1, 2, 1, 3]))  # [3, 1, 2]\n```",
])

addmt([
    "write a function to calculate the average of a list",
    "```python\ndef average(nums):\n    return sum(nums) / len(nums)\n\naverage([2, 4, 6])  # 4.0\n```",
    "guard against division by zero for an empty list",
    "Return 0 (or None) when the list is empty:\n\n```python\ndef average(nums):\n    return sum(nums) / len(nums) if nums else 0\n```",
])

addmt([
    "how do I sort a dictionary by its values",
    "```python\nd = {\"a\": 3, \"b\": 1, \"c\": 2}\ndict(sorted(d.items(), key=lambda kv: kv[1]))\n# {'b': 1, 'c': 2, 'a': 3}\n```",
    "can I sort it descending instead",
    "Add `reverse=True`:\n\n```python\ndict(sorted(d.items(), key=lambda kv: kv[1], reverse=True))\n# {'a': 3, 'c': 2, 'b': 1}\n```",
])

addmt([
    "write a function that greets a person",
    "```python\ndef greet(name):\n    return f\"Hello, {name}!\"\n```",
    "add an optional greeting word with a default",
    "```python\ndef greet(name, greeting=\"Hello\"):\n    return f\"{greeting}, {name}!\"\n\ngreet(\"Sam\")            # 'Hello, Sam!'\ngreet(\"Sam\", \"Hi\")      # 'Hi, Sam!'\n```",
])

addmt([
    "how do I check if a key is in a dict",
    "Use `in`:\n\n```python\nif \"name\" in d:\n    ...\n```",
    "and get its value with a fallback if it's missing",
    "Use `.get()` with a default:\n\n```python\nd.get(\"name\", \"unknown\")\n```",
])

addmt([
    "how to zip two lists together",
    "```python\nlist(zip([1, 2], [\"a\", \"b\"]))  # [(1, 'a'), (2, 'b')]\n```",
    "what if the lists are different lengths",
    "`zip` stops at the shorter one. Use `itertools.zip_longest` to pad instead:\n\n```python\nfrom itertools import zip_longest\nlist(zip_longest([1, 2, 3], [\"a\"], fillvalue=\"-\"))\n# [(1, 'a'), (2, '-'), (3, '-')]\n```",
])

addmt([
    "make a counter that increments each call",
    "Use a closure with `nonlocal`:\n\n```python\ndef make_counter():\n    n = 0\n    def count():\n        nonlocal n\n        n += 1\n        return n\n    return count\n\nc = make_counter()\nc()  # 1\nc()  # 2\n```",
    "can I make it start from a custom number",
    "Add a parameter to the outer function:\n\n```python\ndef make_counter(start=0):\n    n = start\n    def count():\n        nonlocal n\n        n += 1\n        return n\n    return count\n```",
])

addmt([
    "how do I filter a list to keep only positive numbers",
    "```python\nnums = [-2, 3, -1, 5]\n[n for n in nums if n > 0]  # [3, 5]\n```",
    "now also square them",
    "Apply the transform in the same comprehension:\n\n```python\n[n**2 for n in nums if n > 0]  # [9, 25]\n```",
])

addmt([
    "write a function to count vowels in a word",
    "```python\ndef count_vowels(s):\n    return sum(1 for c in s.lower() if c in \"aeiou\")\n```",
    "now return which vowels appeared",
    "Collect them into a set:\n\n```python\ndef vowels_used(s):\n    return {c for c in s.lower() if c in \"aeiou\"}\n\nvowels_used(\"Hello\")  # {'e', 'o'}\n```",
])

addmt([
    "how do I split a full name into first and last",
    "Split on whitespace and unpack:\n\n```python\nfirst, last = \"Jane Doe\".split()\n```",
    "what about middle names",
    "Use star unpacking to absorb the middle parts:\n\n```python\nfirst, *middle, last = \"Jane Anne Doe\".split()\n# first='Jane', middle=['Anne'], last='Doe'\n```",
])

addmt([
    "how to build a dict mapping numbers to their squares",
    "Use a dict comprehension:\n\n```python\n{x: x**2 for x in range(5)}\n# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}\n```",
    "only include odd numbers",
    "Add a condition:\n\n```python\n{x: x**2 for x in range(5) if x % 2 == 1}\n# {1: 1, 3: 9}\n```",
])

addmt([
    "write a loop that stops when it finds a negative number",
    "Use `break`:\n\n```python\nfor n in nums:\n    if n < 0:\n        break\n    print(n)\n```",
    "how do I know whether it found one",
    "Use a `for/else`; the `else` runs only if no `break` happened:\n\n```python\nfor n in nums:\n    if n < 0:\n        print(\"found negative\")\n        break\nelse:\n    print(\"all non-negative\")\n```",
])

addmt([
    "how do I convert a string of numbers to a list of ints",
    "Split and map to int:\n\n```python\nlist(map(int, \"1 2 3\".split()))  # [1, 2, 3]\n```",
    "what if they're comma separated",
    "Split on the comma instead:\n\n```python\nlist(map(int, \"1,2,3\".split(\",\")))  # [1, 2, 3]\n```",
])

addmt([
    "write a function returning the largest of two numbers",
    "```python\ndef larger(a, b):\n    return a if a > b else b\n```",
    "extend it to any number of arguments",
    "Use `*args` and the built-in `max`:\n\n```python\ndef larger(*args):\n    return max(args)\n\nlarger(3, 7, 2)  # 7\n```",
])

addmt([
    "how to read a number from the user",
    "Convert the input string with `int()`:\n\n```python\nn = int(input(\"Enter a number: \"))\n```",
    "how do I handle the case where they type letters",
    "Wrap it in try/except:\n\n```python\ntry:\n    n = int(input(\"Enter a number: \"))\nexcept ValueError:\n    print(\"That's not a number\")\n```",
])

addmt([
    "make a list of the first 10 even numbers",
    "```python\n[x for x in range(20) if x % 2 == 0]  # [0, 2, ..., 18]\n```",
    "I'd rather start at 2 and not include 0",
    "Iterate over even numbers directly:\n\n```python\nlist(range(2, 22, 2))  # [2, 4, ..., 20]\n```",
])

addmt([
    "how do I join a list of words with spaces",
    "```python\n\" \".join([\"hello\", \"world\"])  # 'hello world'\n```",
    "what if some items are numbers",
    "Convert each to a string first with `map`:\n\n```python\n\" \".join(map(str, [\"x\", 1, 2.5]))  # 'x 1 2.5'\n```",
])

addmt([
    "what does the walrus operator do",
    "`:=` assigns within an expression. Example:\n\n```python\nif (n := len(items)) > 3:\n    print(f\"{n} items\")\n```",
    "show it inside a comprehension",
    "It can store an intermediate result to reuse:\n\n```python\nresults = [y for x in data if (y := x * 2) > 10]\n```",
])

addmt([
    "how do I check if all items in a list are strings",
    "Use `all()` with `isinstance`:\n\n```python\nall(isinstance(x, str) for x in items)\n```",
    "now check if at least one is an int",
    "Use `any()`:\n\n```python\nany(isinstance(x, int) for x in items)\n```",
])

addmt([
    "write a function to repeat a string n times",
    "```python\ndef repeat(s, n):\n    return s * n\n\nrepeat(\"ab\", 3)  # 'ababab'\n```",
    "add a separator between repetitions",
    "Join a list of copies:\n\n```python\ndef repeat(s, n, sep=\"\"):\n    return sep.join([s] * n)\n\nrepeat(\"ab\", 3, \"-\")  # 'ab-ab-ab'\n```",
])

addmt([
    "how do I get the unique characters in a string",
    "Convert to a set:\n\n```python\nset(\"banana\")  # {'a', 'b', 'n'}\n```",
    "I want them sorted as a string",
    "Sort the set and join:\n\n```python\n\"\".join(sorted(set(\"banana\")))  # 'abn'\n```",
])

addmt([
    "create a function that checks for a palindrome",
    "```python\ndef is_palindrome(s):\n    return s == s[::-1]\n```",
    "make it ignore case and spaces",
    "Normalize first:\n\n```python\ndef is_palindrome(s):\n    cleaned = \"\".join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]\n\nis_palindrome(\"A man a plan a canal Panama\")  # True\n```",
])

# ---------------- Extra single-turn to reach count ----------------
add("how to use map with multiple lists",
    "Pass several iterables; the function receives one item from each:\n\n```python\nlist(map(lambda x, y: x + y, [1, 2], [10, 20]))  # [11, 22]\n```")

add("how do I reverse a dictionary's iteration order",
    "Use `reversed()` on the dict (3.8+) which iterates keys in reverse insertion order:\n\n```python\nfor k in reversed(d):\n    print(k)\n```")

add("how to make all keys lowercase in a dict",
    "Use a dict comprehension:\n\n```python\n{k.lower(): v for k, v in d.items()}\n```")

add("how do I get both index and value while modifying nothing",
    "`enumerate` is the idiomatic way:\n\n```python\nfor i, v in enumerate(seq):\n    ...\n```")

add("how to create a range as a list quickly",
    "```python\nlist(range(5))  # [0, 1, 2, 3, 4]\n```")

add("what is the difference between a tuple and a list for keys",
    "Only immutable, hashable objects can be dict keys. Tuples qualify, lists don't:\n\n```python\n{(1, 2): \"ok\"}   # works\n{[1, 2]: \"bad\"}  # TypeError\n```")

add("how do I round a list of floats",
    "Use a comprehension:\n\n```python\n[round(x, 2) for x in [1.111, 2.222]]  # [1.11, 2.22]\n```")

add("how do I get the ascii code of a character",
    "Use `ord()`; reverse with `chr()`:\n\n```python\nord(\"A\")  # 65\nchr(97)   # 'a'\n```")

add("how to build a string from a range of letters",
    "```python\n\"\".join(chr(c) for c in range(ord(\"a\"), ord(\"f\")+1))  # 'abcdef'\n```")

add("how do I check if a string contains only whitespace",
    "Use `.isspace()`:\n\n```python\n\"   \".isspace()  # True\n```")

add("convert a dict to a list of tuples",
    "Use `.items()` wrapped in `list()`:\n\n```python\nlist({\"a\": 1, \"b\": 2}.items())  # [('a', 1), ('b', 2)]\n```")

add("how to find min and max in one pass",
    "Use the built-ins (they each scan once):\n\n```python\nnums = [3, 1, 9, 4]\nlow, high = min(nums), max(nums)\n```")

add("how do I make a frozenset",
    "Use `frozenset()`; it's an immutable, hashable set:\n\n```python\nfs = frozenset([1, 2, 3])\n```")

add("how to repeat code a fixed number of times without using the counter",
    "Use `_` as the loop variable:\n\n```python\nfor _ in range(3):\n    print(\"hi\")\n```")

add("what does the in operator do",
    "It tests membership in a sequence, set, or dict (keys), returning a bool:\n\n```python\n3 in [1, 2, 3]      # True\n\"a\" in \"cat\"        # True\n\"k\" in {\"k\": 1}     # True\n```")

add("how do I negate a condition with not",
    "Prefix it with `not`:\n\n```python\nif not is_ready:\n    print(\"wait\")\n```")

add("how to convert a list of ints to a list of strings",
    "```python\nlist(map(str, [1, 2, 3]))  # ['1', '2', '3']\n```")

add("how do I get the keys sorted from a dict",
    "```python\nsorted(d.keys())\n```")

add("how to use a default dict for grouping",
    "```python\nfrom collections import defaultdict\ngroups = defaultdict(list)\nfor word in [\"apple\", \"ant\", \"bee\"]:\n    groups[word[0]].append(word)\n# {'a': ['apple', 'ant'], 'b': ['bee']}\n```")

add("how do I check if a value is a list",
    "```python\nisinstance(x, list)\n```")

add("how do I make a shallow copy of a dict",
    "Use `.copy()` or `dict()`:\n\n```python\nd2 = d.copy()\n```")

add("how to combine list elements with their index into tuples",
    "```python\nlist(enumerate([\"a\", \"b\"]))  # [(0, 'a'), (1, 'b')]\n```")

add("how do I check if a number is within a range",
    "Chain comparisons:\n\n```python\nif 1 <= x <= 100:\n    print(\"valid\")\n```")

add("how to convert seconds to minutes and seconds",
    "Use `divmod`:\n\n```python\nmins, secs = divmod(135, 60)  # 2, 15\n```")

add("how do I get the type name as a string",
    "Use `type(x).__name__`:\n\n```python\ntype(42).__name__  # 'int'\n```")

add("how to check if two lists are equal",
    "Use `==`, which compares element by element in order:\n\n```python\n[1, 2, 3] == [1, 2, 3]  # True\n```")

add("how to check if two lists have the same elements ignoring order",
    "Compare sorted versions or sets (if no duplicates matter):\n\n```python\nsorted(a) == sorted(b)\n```")

add("how do I create a string of n spaces",
    "```python\n\" \" * 4  # '    '\n```")

add("how to title-case a sentence properly",
    "Use `.title()`:\n\n```python\n\"the great gatsby\".title()  # 'The Great Gatsby'\n```")

add("how do I remove the last item from a list and use it",
    "Use `.pop()` with no argument:\n\n```python\nlast = lst.pop()\n```")

add("how to check if a string represents a float",
    "Try converting it:\n\n```python\ndef is_float(s):\n    try:\n        float(s)\n        return True\n    except ValueError:\n        return False\n```")

add("how do I make a number negative regardless of sign",
    "Negate its absolute value:\n\n```python\n-abs(x)\n```")

add("how to get the integer and fractional parts of a float",
    "Use `math.modf`:\n\n```python\nimport math\nmath.modf(3.75)  # (0.75, 3.0)\n```")

add("how do I clamp a number between min and max",
    "Nest `min` and `max`:\n\n```python\ndef clamp(x, lo, hi):\n    return max(lo, min(x, hi))\n\nclamp(15, 0, 10)  # 10\n```")

add("how to count how many items satisfy a condition",
    "Sum a generator of booleans:\n\n```python\nsum(1 for x in nums if x > 0)\n```")

add("how do I make a dict from enumerate",
    "```python\ndict(enumerate([\"a\", \"b\", \"c\"]))  # {0: 'a', 1: 'b', 2: 'c'}\n```")

add("how to safely index a list with a default",
    "Check the length, or use try/except:\n\n```python\nval = lst[i] if i < len(lst) else None\n```")

add("how do I reverse a number's digits",
    "Convert to string, reverse, convert back:\n\n```python\nint(str(1234)[::-1])  # 4321\n```")

add("how to sum the digits of a number",
    "```python\nsum(int(d) for d in str(12345))  # 15\n```")

add("how do I check if all characters in a string are unique",
    "Compare the length to the set length:\n\n```python\ndef all_unique(s):\n    return len(s) == len(set(s))\n```")

add("how to convert a list of pairs into a dict",
    "```python\ndict([(\"a\", 1), (\"b\", 2)])  # {'a': 1, 'b': 2}\n```")

add("how do I get the index of the largest element",
    "Use `max` with a key over the indices:\n\n```python\nnums = [3, 9, 2]\nmax(range(len(nums)), key=nums.__getitem__)  # 1\n```")

add("how to interleave two lists",
    "Zip and flatten:\n\n```python\na, b = [1, 2], [\"x\", \"y\"]\n[v for pair in zip(a, b) for v in pair]  # [1, 'x', 2, 'y']\n```")

add("how do I make a string from a list of numbers separated by commas",
    "```python\n\",\".join(str(n) for n in [1, 2, 3])  # '1,2,3'\n```")

add("how to check if a list is sorted",
    "Compare neighbors:\n\n```python\ndef is_sorted(lst):\n    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))\n```")

add("how do I find elements in list a but not in list b",
    "Use set difference:\n\n```python\nlist(set(a) - set(b))\n```")

add("how to make every word in a list uppercase",
    "```python\n[w.upper() for w in words]\n```")

add("how do I check if a string is a valid integer",
    "For non-negative use `.isdigit()`; otherwise try `int()`:\n\n```python\ndef is_int(s):\n    try:\n        int(s)\n        return True\n    except ValueError:\n        return False\n```")

add("how to get the nth fibonacci number with recursion",
    "```python\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n-1) + fib(n-2)\n```\nNote: the iterative version is far faster for large n.")

add("how do I build a comma separated string with a trailing newline",
    "```python\nline = \",\".join(parts) + \"\\n\"\n```")

add("how to lowercase dict keys and values",
    "```python\n{k.lower(): v.lower() for k, v in d.items()}\n```")

add("how do I check if a number is positive negative or zero",
    "```python\ndef sign(n):\n    if n > 0:\n        return \"positive\"\n    elif n < 0:\n        return \"negative\"\n    return \"zero\"\n```")

add("how to repeat each element of a list",
    "```python\n[x for x in [1, 2, 3] for _ in range(2)]  # [1, 1, 2, 2, 3, 3]\n```")

add("how do I make a set from a string",
    "```python\nset(\"hello\")  # {'h', 'e', 'l', 'o'}\n```")

add("how to find the difference between consecutive elements",
    "```python\nnums = [1, 4, 9, 16]\n[b - a for a, b in zip(nums, nums[1:])]  # [3, 5, 7]\n```")

add("how do I conditionally build a list",
    "Use a comprehension with an `if`:\n\n```python\n[x for x in data if keep(x)]\n```")

add("how to turn 'true'/'false' strings into booleans",
    "Compare to the string explicitly (don't use `bool()`, since any non-empty string is truthy):\n\n```python\ndef to_bool(s):\n    return s.strip().lower() == \"true\"\n```")

add("how do I get the first n items of any iterable",
    "Use `itertools.islice`:\n\n```python\nfrom itertools import islice\nlist(islice(gen, 3))\n```")

add("how to find the longest string in a list",
    "```python\nmax([\"a\", \"abc\", \"ab\"], key=len)  # 'abc'\n```")

add("how do I sum a list of lists element-wise",
    "Zip them and sum each position:\n\n```python\nrows = [[1, 2], [3, 4], [5, 6]]\n[sum(col) for col in zip(*rows)]  # [9, 12]\n```")

add("how to make a histogram dict from a list",
    "```python\nfrom collections import Counter\ndict(Counter([1, 1, 2, 3, 3, 3]))  # {1: 2, 2: 1, 3: 3}\n```")

add("how do I check if a dict is empty",
    "Empty dicts are falsy:\n\n```python\nif not d:\n    print(\"empty\")\n```")

add("how to get a value deep in nested dicts safely",
    "Chain `.get()` calls:\n\n```python\ndata.get(\"user\", {}).get(\"name\", \"unknown\")\n```")

add("how do I create an empty dict, list, set, tuple",
    "```python\n{}        # empty dict\n[]        # empty list\nset()     # empty set\n()        # empty tuple\n```")

add("how to print a list without brackets",
    "Join its string items:\n\n```python\nprint(\", \".join(map(str, [1, 2, 3])))  # 1, 2, 3\n```")

add("how do I check the boolean of an empty vs non-empty container",
    "Containers are truthy when non-empty:\n\n```python\nbool([])   # False\nbool([0])  # True\n```")

add("how to make a function that optionally takes extra config",
    "Use `**kwargs`:\n\n```python\ndef configure(name, **options):\n    print(name, options)\n\nconfigure(\"server\", port=80, debug=True)\n```")

add("how do I get even-indexed elements of a list",
    "Slice with step 2:\n\n```python\nlst[::2]\n```")

add("how to combine two dicts summing shared values",
    "Use a Counter:\n\n```python\nfrom collections import Counter\nCounter({\"a\": 1}) + Counter({\"a\": 2, \"b\": 1})\n# Counter({'a': 3, 'b': 1})\n```")

add("how do I write a guard clause to exit a function early",
    "Return at the top when a precondition fails:\n\n```python\ndef process(data):\n    if not data:\n        return None\n    ...\n```")

add("how to format a percentage from a fraction",
    "```python\nf\"{3/8:.1%}\"  # '37.5%'\n```")

add("how do I count down from 10 to 1 inclusive",
    "```python\nfor i in range(10, 0, -1):\n    print(i)\n```")

add("how to make pairs of consecutive elements",
    "Zip the list with itself shifted by one:\n\n```python\nlst = [1, 2, 3, 4]\nlist(zip(lst, lst[1:]))  # [(1, 2), (2, 3), (3, 4)]\n```")

add("how do I check whether a string is uppercase",
    "Use `.isupper()`:\n\n```python\n\"HELLO\".isupper()  # True\n```")

add("how to convert a number to a list of its digits",
    "```python\n[int(d) for d in str(12345)]  # [1, 2, 3, 4, 5]\n```")

add("how do I default a function argument to the current list",
    "Avoid mutable defaults; use None and build inside:\n\n```python\ndef f(items=None):\n    items = items or []\n    ...\n```")

add("how to find the position of the smallest element",
    "```python\nnums = [4, 2, 7, 1]\nnums.index(min(nums))  # 3\n```")

add("how do I uppercase the first letter of each word but keep the rest as-is",
    "Capitalize each word manually to avoid `.title()` lowercasing the rest:\n\n```python\n\" \".join(w[:1].upper() + w[1:] for w in s.split())\n```")

add("how to check if a string is numeric including decimals",
    "`.isdigit()` only handles integers. Try `float()` for decimals:\n\n```python\ndef is_number(s):\n    try:\n        float(s)\n        return True\n    except ValueError:\n        return False\n```")

add("how do I build a list of tuples (index, squared value)",
    "```python\n[(i, i**2) for i in range(4)]  # [(0, 0), (1, 1), (2, 4), (3, 9)]\n```")

add("how to safely divide two numbers avoiding zero division",
    "```python\ndef safe_div(a, b):\n    return a / b if b != 0 else 0\n```")

add("how do I convert temperature fahrenheit to celsius",
    "```python\ndef f_to_c(f):\n    return (f - 32) * 5 / 9\n\nf_to_c(212)  # 100.0\n```")

add("how to get distinct words from a sentence",
    "```python\nset(\"a b a c b\".split())  # {'a', 'b', 'c'}\n```")

add("how do I make a number always two digits as a string",
    "```python\nf\"{7:02d}\"  # '07'\n```")

add("how to use ternary inside a list comprehension to label numbers",
    "```python\n[\"even\" if n % 2 == 0 else \"odd\" for n in range(4)]\n# ['even', 'odd', 'even', 'odd']\n```")

add("how do I check if two variables point to the same object",
    "Use `is`:\n\n```python\na = b = []\na is b  # True\n```")

add("how to get a slice that skips the first and last element",
    "```python\nlst[1:-1]\n```")

add("how do I concatenate strings in a loop efficiently",
    "Collect parts in a list and join once, instead of `+=` in the loop:\n\n```python\nparts = []\nfor x in items:\n    parts.append(str(x))\nresult = \"\".join(parts)\n```")

add("how to check membership in multiple values cleanly",
    "Test against a set or tuple:\n\n```python\nif x in {\"a\", \"b\", \"c\"}:\n    ...\n```")

add("how do I sort strings case-insensitively",
    "Pass `key=str.lower`:\n\n```python\nsorted([\"banana\", \"Apple\"], key=str.lower)  # ['Apple', 'banana']\n```")

add("how to get min by a custom key",
    "```python\nwords = [\"ccc\", \"a\", \"bb\"]\nmin(words, key=len)  # 'a'\n```")

add("how do I check if a list contains any duplicates",
    "Compare length to set length:\n\n```python\nlen(lst) != len(set(lst))\n```")

add("how to build a comma list but with 'and' before the last item",
    "```python\ndef oxford(items):\n    if len(items) < 2:\n        return \"\".join(items)\n    return \", \".join(items[:-1]) + \" and \" + items[-1]\n\noxford([\"a\", \"b\", \"c\"])  # 'a, b and c'\n```")

add("how do I make a list where each value is its index times 10",
    "```python\n[i * 10 for i in range(5)]  # [0, 10, 20, 30, 40]\n```")

add("how to test if a string contains a digit",
    "```python\nany(c.isdigit() for c in s)\n```")

add("how do I assign default values from a dict",
    "Use `.get()` per field, or unpack with defaults:\n\n```python\nconfig = {\"host\": \"localhost\"}\nhost = config.get(\"host\", \"0.0.0.0\")\nport = config.get(\"port\", 8000)\n```")

add("how to loop over a dict's values only",
    "```python\nfor v in d.values():\n    print(v)\n```")

add("how do I make a tuple of a single computed value",
    "Add a trailing comma:\n\n```python\nt = (compute(),)\n```")

add("how to find common keys between two dicts",
    "Intersect their key views:\n\n```python\na.keys() & b.keys()\n```")

add("how do I get the absolute difference between two numbers",
    "```python\nabs(a - b)\n```")

add("how to make a dict counting list element lengths",
    "```python\nwords = [\"a\", \"bb\", \"ccc\"]\n{w: len(w) for w in words}\n```")

add("how do I check that a function received the right number of items",
    "Compare `len(args)`:\n\n```python\ndef f(*args):\n    if len(args) != 2:\n        raise ValueError(\"need exactly 2\")\n```")

add("how to round to the nearest 10",
    "```python\nround(x / 10) * 10\n```")

add("how do I get a reversed enumerate",
    "Reverse the sequence and pair with descending indices manually:\n\n```python\nlst = [\"a\", \"b\", \"c\"]\nlist(zip(range(len(lst)-1, -1, -1), reversed(lst)))\n# [(2, 'c'), (1, 'b'), (0, 'a')]\n```")

add("how to check if string has balanced parentheses",
    "Track a counter:\n\n```python\ndef balanced(s):\n    depth = 0\n    for c in s:\n        if c == \"(\":\n            depth += 1\n        elif c == \")\":\n            depth -= 1\n            if depth < 0:\n                return False\n    return depth == 0\n```")

add("how do I convert a comprehension result back into a dict and filter",
    "Filter inside the comprehension:\n\n```python\n{k: v for k, v in d.items() if v > 0}\n```")

add("how to make all values in a list absolute",
    "```python\n[abs(x) for x in [-1, 2, -3]]  # [1, 2, 3]\n```")

add("how do I check if a character is a letter",
    "```python\nc.isalpha()\n```")

add("how to produce a running total of a list",
    "Use `itertools.accumulate`:\n\n```python\nfrom itertools import accumulate\nlist(accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10]\n```")

add("how do I default to zero when summing an empty list",
    "`sum([])` already returns 0, so no special handling is needed:\n\n```python\nsum([])  # 0\n```")

add("how to make a function accept either a list or single value",
    "Normalize to a list at the top:\n\n```python\ndef process(x):\n    if not isinstance(x, list):\n        x = [x]\n    return [i * 2 for i in x]\n```")

add("how do I get keys whose values exceed a threshold",
    "```python\n[k for k, v in d.items() if v > 5]\n```")

add("how to find index of first element matching a condition",
    "```python\nnext((i for i, x in enumerate(lst) if x > 10), -1)\n```")

add("how do I split text into lines",
    "Use `.splitlines()`:\n\n```python\n\"a\\nb\\nc\".splitlines()  # ['a', 'b', 'c']\n```")

add("how to convert all dict values to int",
    "```python\n{k: int(v) for k, v in d.items()}\n```")

add("how do I get the middle element of a list",
    "```python\nlst[len(lst) // 2]\n```")

add("how to test if every word starts with a capital",
    "```python\nall(w[0].isupper() for w in words if w)\n```")

add("how do I create a list of None values",
    "```python\n[None] * 5\n```")

add("how to swap two elements in a list by index",
    "```python\nlst[i], lst[j] = lst[j], lst[i]\n```")

add("how do I remove all occurrences of a value from a list",
    "Filter it out into a new list:\n\n```python\nlst = [x for x in lst if x != target]\n```")

add("how to convert minutes to a HH:MM string",
    "```python\ndef fmt(minutes):\n    h, m = divmod(minutes, 60)\n    return f\"{h:02d}:{m:02d}\"\n\nfmt(135)  # '02:15'\n```")

add("how do I check if a number is a perfect square",
    "```python\nimport math\ndef is_square(n):\n    r = math.isqrt(n)\n    return r * r == n\n```")

add("how to apply a function to every dict value",
    "```python\n{k: f(v) for k, v in d.items()}\n```")

add("how do I get a list of bools whether each number is positive",
    "```python\n[n > 0 for n in [-1, 2, 0, 3]]  # [False, True, False, True]\n```")

add("how to convert a dict to query string style",
    "```python\nd = {\"a\": 1, \"b\": 2}\n\"&\".join(f\"{k}={v}\" for k, v in d.items())  # 'a=1&b=2'\n```")

add("how do I make sure a value is at least 1",
    "```python\nmax(1, x)\n```")

add("how to capitalize every word and strip extra spaces",
    "```python\n\" \".join(w.capitalize() for w in s.split())\n```")

add("how do I check if list elements are all the same",
    "```python\nlen(set(lst)) <= 1\n```")

add("how to make a list of cumulative sums manually",
    "```python\ntotal = 0\nresult = []\nfor x in [1, 2, 3]:\n    total += x\n    result.append(total)\n# [1, 3, 6]\n```")

add("how do I get the last word of a sentence",
    "```python\nsentence.split()[-1]\n```")

add("how to format a float as currency",
    "```python\nf\"${1234.5:,.2f}\"  # '$1,234.50'\n```")

add("how do I check if an object is iterable",
    "Try getting an iterator, or check for `__iter__`:\n\n```python\nhasattr(x, \"__iter__\")\n```")

add("how to make a frequency dict without Counter",
    "```python\nfreq = {}\nfor c in \"banana\":\n    freq[c] = freq.get(c, 0) + 1\n# {'b': 1, 'a': 3, 'n': 2}\n```")

add("how do I keep only alphanumeric characters in a string",
    "```python\n\"\".join(c for c in s if c.isalnum())\n```")

add("how to chain default with walrus to avoid recompute",
    "```python\nif (val := lookup(key)) is not None:\n    use(val)\n```")

add("how do I check if a list of strings are all non-empty",
    "```python\nall(items)\n```")

add("how to format an integer with a leading plus sign",
    "```python\nf\"{5:+d}\"   # '+5'\nf\"{-5:+d}\"  # '-5'\n```")

add("how do I count truthy values in a list",
    "Sum the list (booleans count as 1):\n\n```python\nsum(bool(x) for x in items)\n```")

add("how to make a dict with all values set to zero from keys",
    "```python\ndict.fromkeys([\"a\", \"b\", \"c\"], 0)  # {'a': 0, 'b': 0, 'c': 0}\n```")

add("how do I get a substring between two characters",
    "```python\ns = \"a[hello]b\"\ns[s.index(\"[\")+1 : s.index(\"]\")]  # 'hello'\n```")

add("how to make a numbered list output",
    "```python\nfor i, item in enumerate(items, 1):\n    print(f\"{i}. {item}\")\n```")

add("how do I check whether a string contains only letters and spaces",
    "```python\nall(c.isalpha() or c == \" \" for c in s)\n```")

add("how to find which keys two dicts disagree on",
    "```python\n[k for k in a.keys() & b.keys() if a[k] != b[k]]\n```")

add("how do I make a default value with the ternary operator",
    "```python\nname = raw if raw else \"default\"\n```")

add("how to split a list into evens and odds",
    "```python\nnums = [1, 2, 3, 4, 5]\nevens = [n for n in nums if n % 2 == 0]\nodds = [n for n in nums if n % 2 == 1]\n```")

add("how do I get every key-value pair where the value is a string",
    "```python\n{k: v for k, v in d.items() if isinstance(v, str)}\n```")

add("how to convert a list to a tuple",
    "```python\ntuple([1, 2, 3])  # (1, 2, 3)\n```")

add("how do I make a comma string only from positive numbers",
    "```python\n\",\".join(str(n) for n in nums if n > 0)\n```")

add("how to count how many words are longer than 4 letters",
    "```python\nsum(1 for w in words if len(w) > 4)\n```")

add("how do I check if a value is None or empty",
    "Both cases are falsy, so test directly:\n\n```python\nif not value:\n    ...\n```")

add("how to repeat a function n times collecting results",
    "```python\n[roll() for _ in range(5)]\n```")

add("how do I find the average word length in a sentence",
    "```python\nwords = sentence.split()\navg = sum(len(w) for w in words) / len(words)\n```")

add("how to make a boolean from comparing two strings ignoring case",
    "```python\na.lower() == b.lower()\n```")

add("how do I turn a flat list into pairs",
    "Zip the even and odd slices:\n\n```python\nflat = [1, 2, 3, 4]\nlist(zip(flat[::2], flat[1::2]))  # [(1, 2), (3, 4)]\n```")

add("how to default an entire dict if missing keys",
    "Merge defaults under the actual config:\n\n```python\ndefaults = {\"port\": 80, \"host\": \"localhost\"}\nfinal = {**defaults, **user_config}\n```")

add("how do I check if a string has no spaces",
    "```python\n\" \" not in s\n```")

add("how to compute the product of a list",
    "Use `math.prod`:\n\n```python\nimport math\nmath.prod([1, 2, 3, 4])  # 24\n```")

add("how do I create a list comprehension over a dict",
    "Iterate `.items()`:\n\n```python\n[f\"{k}={v}\" for k, v in d.items()]\n```")

add("how to get unique values preserving order from any iterable",
    "```python\ndef unique(seq):\n    seen = set()\n    out = []\n    for x in seq:\n        if x not in seen:\n            seen.add(x)\n            out.append(x)\n    return out\n```")

add("how do I make a string of stars for a bar chart",
    "```python\n\"*\" * value\n```")

add("how to check if a number is in a list of ranges",
    "```python\nany(lo <= x <= hi for lo, hi in ranges)\n```")

add("how do I capitalize a string only if it isn't already",
    "```python\ns if s[:1].isupper() else s.capitalize()\n```")

add("how to flatten and dedupe a list of lists",
    "```python\nnested = [[1, 2], [2, 3]]\nsorted({x for row in nested for x in row})  # [1, 2, 3]\n```")

add("how do I get a dictionary's first key",
    "```python\nnext(iter(d))\n```")

add("how to filter dict to top n by value",
    "```python\ndict(sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:n])\n```")

add("how do I build a string repeating a pattern to a length",
    "```python\ndef fill(pattern, length):\n    return (pattern * (length // len(pattern) + 1))[:length]\n\nfill(\"ab\", 5)  # 'ababa'\n```")

add("how to test if a list contains only numbers",
    "```python\nall(isinstance(x, (int, float)) for x in lst)\n```")

add("how do I create a grid of zeros",
    "Use a nested comprehension (not list multiplication, which shares rows):\n\n```python\ngrid = [[0] * 3 for _ in range(2)]\n# [[0, 0, 0], [0, 0, 0]]\n```")

add("why does [[0]*3]*2 cause a bug",
    "Because the outer multiplication copies the same inner list reference, so all rows are the same object. Editing one edits all. Use a comprehension instead:\n\n```python\ngrid = [[0] * 3 for _ in range(2)]\n```")

add("how do I get the keys and values as parallel lists",
    "```python\nkeys = list(d.keys())\nvals = list(d.values())\n```")

add("how to convert a string number with commas to int",
    "Remove the commas first:\n\n```python\nint(\"1,234\".replace(\",\", \"\"))  # 1234\n```")

add("how do I make a function with no arguments that returns a constant",
    "```python\ndef pi():\n    return 3.14159\n```")

add("how to filter out None values from a list",
    "```python\n[x for x in lst if x is not None]\n```")

add("how do I check if a string is a substring ignoring case",
    "```python\n\"cat\" in \"CATEGORY\".lower()\n```")

add("how to compute factorial with math module",
    "```python\nimport math\nmath.factorial(5)  # 120\n```")

add("how do I make every other character uppercase",
    "```python\n\"\".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s))\n```")

add("how to get a value's index or None",
    "```python\nlst.index(x) if x in lst else None\n```")

add("how do I quickly test truthiness of many conditions",
    "Use `all` for AND-of-many, `any` for OR-of-many:\n\n```python\nall([cond1, cond2, cond3])\n```")

add("how to make a dict comprehension that swaps and filters",
    "```python\n{v: k for k, v in d.items() if v is not None}\n```")

add("how do I pad a list to a fixed length",
    "```python\ndef pad(lst, n, fill=0):\n    return lst + [fill] * (n - len(lst))\n\npad([1, 2], 5)  # [1, 2, 0, 0, 0]\n```")

add("how to convert a boolean to yes/no string",
    "```python\n\"yes\" if flag else \"no\"\n```")

add("how do I count items grouped by a key function",
    "```python\nfrom collections import Counter\nCounter(len(w) for w in words)\n```")

add("how to safely get a nested list element",
    "```python\nval = matrix[r][c] if r < len(matrix) and c < len(matrix[r]) else None\n```")

add("how do I make a comma-separated string of key=value pairs",
    "```python\n\", \".join(f\"{k}={v}\" for k, v in d.items())\n```")

add("how to detect if all elements are unique using a set",
    "```python\nlen(set(lst)) == len(lst)\n```")

add("how do I find the shortest string in a list",
    "```python\nmin(words, key=len)\n```")

add("how to compute average ignoring None values",
    "```python\nvals = [x for x in data if x is not None]\navg = sum(vals) / len(vals) if vals else 0\n```")

add("how do I check if a number is between two others exclusively",
    "```python\nlo < x < hi\n```")

add("how to convert each word to its length",
    "```python\n[len(w) for w in words]\n```")

add("how do I make a set difference both ways",
    "```python\nonly_a = set(a) - set(b)\nonly_b = set(b) - set(a)\n```")

add("how to format a list as a bulleted string",
    "```python\n\"\\n\".join(f\"- {item}\" for item in items)\n```")

add("how do I check if a string equals any of several options",
    "```python\nif s in (\"yes\", \"y\", \"true\"):\n    ...\n```")

add("how to make all keys uppercase and values lowercase",
    "```python\n{k.upper(): v.lower() for k, v in d.items()}\n```")

add("how do I find the index of the maximum value cleanly",
    "```python\nmax(range(len(nums)), key=lambda i: nums[i])\n```")

add("how to repeat a list of items cyclically",
    "Use `itertools.cycle` with islice:\n\n```python\nfrom itertools import cycle, islice\nlist(islice(cycle([1, 2, 3]), 7))  # [1, 2, 3, 1, 2, 3, 1]\n```")

add("how do I default a missing function arg to a computed value",
    "Use None sentinel and compute inside:\n\n```python\ndef f(x=None):\n    if x is None:\n        x = expensive_default()\n    return x\n```")

add("how to count how many keys a dict has",
    "```python\nlen(d)\n```")

add("how do I get a slice from the end of a string",
    "```python\ns[-4:]  # last 4 characters\n```")

add("how to make a list of running maximums",
    "```python\nfrom itertools import accumulate\nlist(accumulate([3, 1, 4, 1, 5], max))  # [3, 3, 4, 4, 5]\n```")

add("how do I check if all dict values are equal",
    "```python\nlen(set(d.values())) <= 1\n```")

add("how to count uppercase letters in a string",
    "```python\nsum(1 for c in s if c.isupper())\n```")

add("how do I make a copy of a nested list safely",
    "Use `copy.deepcopy`, since a shallow copy shares the inner lists:\n\n```python\nimport copy\ncopy.deepcopy(nested)\n```")

add("how to format a ratio as 'x out of y'",
    "```python\nf\"{got} out of {total}\"\n```")

add("how do I convert a string to title case but keep acronyms",
    "`.title()` mangles acronyms, so capitalize each word's first letter manually:\n\n```python\n\" \".join(w[:1].upper() + w[1:] for w in s.split())\n```")

add("how to map each item to a (value, is_even) tuple",
    "```python\n[(n, n % 2 == 0) for n in nums]\n```")

print(len(E))
with open("/home/user/Silicat/data/synth/core_python.jsonl", "w") as f:
    for ex in E:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")
