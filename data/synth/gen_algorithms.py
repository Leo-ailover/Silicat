"""Generate instruction/response training data for Silicat: algorithms & data structures."""
import json

examples = []


def add(user, silicat):
    examples.append({"messages": [
        {"role": "user", "content": user},
        {"role": "silicat", "content": silicat},
    ]})


def add_multi(turns):
    # turns: list of (role, content)
    msgs = [{"role": r, "content": c} for r, c in turns]
    examples.append({"messages": msgs})


# ---------------------------------------------------------------------------
# FIBONACCI (many variations)
# ---------------------------------------------------------------------------
add("write fibonacci in python",
    "Here's a simple iterative fibonacci:\n\n```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```")

add("fibonacci sequence python",
    "This prints the first `n` numbers of the Fibonacci sequence:\n\n```python\ndef fib_sequence(n):\n    a, b = 0, 1\n    result = []\n    for _ in range(n):\n        result.append(a)\n        a, b = b, a + b\n    return result\n\nprint(fib_sequence(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\n```")

add("how do I compute the nth fibonacci number?",
    "The cleanest way is iterative, which runs in O(n) time:\n\n```python\ndef nth_fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```")

add("recursive fibonacci",
    "Here's the classic recursive version. It's elegant but O(2^n), so it's slow for large n:\n\n```python\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n```")

add("iterative fibonacci function",
    "```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```")

add("fibonacci with memoization",
    "Memoization caches results so each value is computed once, giving O(n):\n\n```python\nfrom functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n```")

add("fib function please",
    "```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```")

add("memoized fibonacci with a dict",
    "```python\ndef fib(n, memo=None):\n    if memo is None:\n        memo = {}\n    if n < 2:\n        return n\n    if n not in memo:\n        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)\n    return memo[n]\n```")

add("generate fibonacci numbers up to n with a generator",
    "A generator is memory-friendly since it yields one value at a time:\n\n```python\ndef fib_gen(count):\n    a, b = 0, 1\n    for _ in range(count):\n        yield a\n        a, b = b, a + b\n\nprint(list(fib_gen(8)))  # [0, 1, 1, 2, 3, 5, 8, 13]\n```")

add("fibonacci one liner",
    "Using reduce for a compact iterative version:\n\n```python\nfrom functools import reduce\n\ndef fib(n):\n    return reduce(lambda x, _: (x[1], x[0] + x[1]), range(n), (0, 1))[0]\n```")

add("can you give me a fast fibonacci for big n?",
    "Fast doubling computes fib(n) in O(log n):\n\n```python\ndef fib(n):\n    def fd(k):\n        if k == 0:\n            return (0, 1)\n        a, b = fd(k >> 1)\n        c = a * (2 * b - a)\n        d = a * a + b * b\n        if k & 1:\n            return (d, c + d)\n        return (c, d)\n    return fd(n)[0]\n```")

add("print first 10 fibonacci numbers",
    "```python\na, b = 0, 1\nfor _ in range(10):\n    print(a, end=' ')\n    a, b = b, a + b\n# 0 1 1 2 3 5 8 13 21 34\n```")

# ---------------------------------------------------------------------------
# FACTORIAL
# ---------------------------------------------------------------------------
add("factorial in python",
    "```python\ndef factorial(n):\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n```")

add("recursive factorial function",
    "```python\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n```")

add("how to calculate factorial",
    "The standard library already has one:\n\n```python\nimport math\nprint(math.factorial(5))  # 120\n```\n\nOr write it yourself iteratively:\n\n```python\ndef factorial(n):\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n```")

add("factorial without recursion",
    "```python\ndef factorial(n):\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n```")

add("compute n!",
    "```python\nimport math\nprint(math.factorial(6))  # 720\n```")

add("factorial using math module",
    "```python\nimport math\nprint(math.factorial(10))  # 3628800\n```")

# ---------------------------------------------------------------------------
# PRIME CHECKING
# ---------------------------------------------------------------------------
add("check if a number is prime in python",
    "Only check divisors up to sqrt(n) for efficiency:\n\n```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n```")

add("prime number function",
    "```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n```")

add("how do I test for primality?",
    "```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    if n % 2 == 0:\n        return n == 2\n    for i in range(3, int(n ** 0.5) + 1, 2):\n        if n % i == 0:\n            return False\n    return True\n```")

add("generate all primes up to n",
    "The Sieve of Eratosthenes is the efficient way:\n\n```python\ndef sieve(n):\n    is_p = [True] * (n + 1)\n    is_p[0] = is_p[1] = False\n    for i in range(2, int(n ** 0.5) + 1):\n        if is_p[i]:\n            for j in range(i * i, n + 1, i):\n                is_p[j] = False\n    return [i for i, p in enumerate(is_p) if p]\n```")

add("list primes below 100",
    "```python\ndef sieve(n):\n    is_p = [True] * (n + 1)\n    is_p[0] = is_p[1] = False\n    for i in range(2, int(n ** 0.5) + 1):\n        if is_p[i]:\n            for j in range(i * i, n + 1, i):\n                is_p[j] = False\n    return [i for i, p in enumerate(is_p) if p]\n\nprint(sieve(100))\n```")

add("is_prime function python",
    "```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n```")

add("first n prime numbers",
    "```python\ndef first_n_primes(count):\n    primes = []\n    num = 2\n    while len(primes) < count:\n        if all(num % p for p in primes if p * p <= num):\n            primes.append(num)\n        num += 1\n    return primes\n\nprint(first_n_primes(5))  # [2, 3, 5, 7, 11]\n```")

# ---------------------------------------------------------------------------
# GCD / LCM
# ---------------------------------------------------------------------------
add("gcd of two numbers python",
    "Euclid's algorithm:\n\n```python\ndef gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n```")

add("greatest common divisor",
    "```python\nimport math\nprint(math.gcd(48, 36))  # 12\n```")

add("lcm in python",
    "LCM is derived from GCD:\n\n```python\nimport math\n\ndef lcm(a, b):\n    return a * b // math.gcd(a, b)\n\nprint(lcm(4, 6))  # 12\n```")

add("recursive gcd",
    "```python\ndef gcd(a, b):\n    if b == 0:\n        return a\n    return gcd(b, a % b)\n```")

add("least common multiple of two integers",
    "```python\nimport math\nprint(math.lcm(4, 6))  # 12  (math.lcm added in Python 3.9)\n```")

add("euclidean algorithm",
    "```python\ndef gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n```")

# ---------------------------------------------------------------------------
# SORTING - bubble, merge, quick, insertion, selection, sorted()
# ---------------------------------------------------------------------------
add("bubble sort python",
    "```python\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n```")

add("implement bubble sort with early exit",
    "Stop early if a pass makes no swaps (already sorted):\n\n```python\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break\n    return arr\n```")

add("merge sort",
    "Classic divide-and-conquer, O(n log n):\n\n```python\ndef merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i]); i += 1\n        else:\n            result.append(right[j]); j += 1\n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result\n```")

add("quicksort in python",
    "```python\ndef quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    mid = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + mid + quicksort(right)\n```")

add("insertion sort",
    "```python\ndef insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j] > key:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr\n```")

add("selection sort python",
    "```python\ndef selection_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i + 1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr\n```")

add("how do I sort a list in python",
    "Use the built-in `sorted()` (returns a new list) or `.sort()` (in place):\n\n```python\nnums = [3, 1, 4, 1, 5]\nprint(sorted(nums))   # [1, 1, 3, 4, 5]\nnums.sort()           # sorts in place\n```")

add("sort a list in descending order",
    "```python\nnums = [3, 1, 4, 1, 5]\nprint(sorted(nums, reverse=True))  # [5, 4, 3, 1, 1]\n```")

add("sort list of strings by length",
    "```python\nwords = ['pear', 'fig', 'banana']\nprint(sorted(words, key=len))  # ['fig', 'pear', 'banana']\n```")

add("sort a list of tuples by second element",
    "```python\npairs = [(1, 'b'), (2, 'a'), (3, 'c')]\nprint(sorted(pairs, key=lambda x: x[1]))  # [(2, 'a'), (1, 'b'), (3, 'c')]\n```")

add("quick sort with lomuto partition",
    "In-place quicksort using the Lomuto partition scheme:\n\n```python\ndef quicksort(arr, lo=0, hi=None):\n    if hi is None:\n        hi = len(arr) - 1\n    if lo < hi:\n        p = partition(arr, lo, hi)\n        quicksort(arr, lo, p - 1)\n        quicksort(arr, p + 1, hi)\n    return arr\n\ndef partition(arr, lo, hi):\n    pivot = arr[hi]\n    i = lo - 1\n    for j in range(lo, hi):\n        if arr[j] <= pivot:\n            i += 1\n            arr[i], arr[j] = arr[j], arr[i]\n    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]\n    return i + 1\n```")

add("counting sort",
    "Counting sort works for non-negative integers in O(n + k):\n\n```python\ndef counting_sort(arr):\n    if not arr:\n        return arr\n    m = max(arr)\n    counts = [0] * (m + 1)\n    for x in arr:\n        counts[x] += 1\n    result = []\n    for value, c in enumerate(counts):\n        result.extend([value] * c)\n    return result\n```")

add("heap sort python",
    "```python\nimport heapq\n\ndef heap_sort(arr):\n    heapq.heapify(arr)\n    return [heapq.heappop(arr) for _ in range(len(arr))]\n```")

# ---------------------------------------------------------------------------
# BINARY SEARCH / LINEAR SEARCH
# ---------------------------------------------------------------------------
add("binary search python",
    "Requires a sorted list. Returns the index or -1:\n\n```python\ndef binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n```")

add("recursive binary search",
    "```python\ndef binary_search(arr, target, lo=0, hi=None):\n    if hi is None:\n        hi = len(arr) - 1\n    if lo > hi:\n        return -1\n    mid = (lo + hi) // 2\n    if arr[mid] == target:\n        return mid\n    if arr[mid] < target:\n        return binary_search(arr, target, mid + 1, hi)\n    return binary_search(arr, target, lo, mid - 1)\n```")

add("how to search a sorted list efficiently",
    "Use Python's `bisect` module for binary search:\n\n```python\nimport bisect\n\narr = [1, 3, 5, 7, 9]\ni = bisect.bisect_left(arr, 5)\nfound = i < len(arr) and arr[i] == 5\nprint(i, found)  # 2 True\n```")

add("linear search",
    "```python\ndef linear_search(arr, target):\n    for i, x in enumerate(arr):\n        if x == target:\n            return i\n    return -1\n```")

add("find index of element in list",
    "If you just need the index and the value exists, use `.index()`:\n\n```python\nnums = [10, 20, 30]\nprint(nums.index(20))  # 1\n```")

add("binary search but return insertion point",
    "```python\nimport bisect\n\narr = [1, 3, 5, 7]\nprint(bisect.bisect_left(arr, 4))  # 2 -> where 4 would be inserted\n```")

# ---------------------------------------------------------------------------
# REVERSING
# ---------------------------------------------------------------------------
add("reverse a string in python",
    "Slicing is the idiomatic way:\n\n```python\ns = 'hello'\nprint(s[::-1])  # 'olleh'\n```")

add("reverse a list",
    "```python\nnums = [1, 2, 3]\nprint(nums[::-1])     # [3, 2, 1]\nnums.reverse()        # in place\n```")

add("reverse a string without slicing",
    "```python\ndef reverse(s):\n    result = ''\n    for ch in s:\n        result = ch + result\n    return result\n```")

add("how do I reverse words in a sentence",
    "```python\nsentence = 'the quick brown fox'\nprint(' '.join(sentence.split()[::-1]))  # 'fox brown quick the'\n```")

add("reverse an integer python",
    "```python\ndef reverse_int(n):\n    sign = -1 if n < 0 else 1\n    return sign * int(str(abs(n))[::-1])\n\nprint(reverse_int(-123))  # -321\n```")

# ---------------------------------------------------------------------------
# PALINDROME
# ---------------------------------------------------------------------------
add("check if a string is a palindrome",
    "```python\ndef is_palindrome(s):\n    return s == s[::-1]\n```")

add("palindrome check ignoring case and spaces",
    "```python\ndef is_palindrome(s):\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]\n\nprint(is_palindrome('A man, a plan, a canal: Panama'))  # True\n```")

add("how to detect a palindrome number",
    "```python\ndef is_palindrome(n):\n    return str(n) == str(n)[::-1]\n\nprint(is_palindrome(12321))  # True\n```")

add("palindrome function two pointer",
    "Two-pointer avoids building a reversed copy:\n\n```python\ndef is_palindrome(s):\n    i, j = 0, len(s) - 1\n    while i < j:\n        if s[i] != s[j]:\n            return False\n        i += 1\n        j -= 1\n    return True\n```")

add("is this word a palindrome python",
    "```python\ndef is_palindrome(word):\n    return word == word[::-1]\n```")

# ---------------------------------------------------------------------------
# ANAGRAM
# ---------------------------------------------------------------------------
add("check if two strings are anagrams",
    "Sort both and compare, or compare character counts:\n\n```python\ndef is_anagram(a, b):\n    return sorted(a) == sorted(b)\n```")

add("anagram check using Counter",
    "```python\nfrom collections import Counter\n\ndef is_anagram(a, b):\n    return Counter(a) == Counter(b)\n```")

add("anagram function ignoring spaces and case",
    "```python\ndef is_anagram(a, b):\n    norm = lambda s: sorted(c.lower() for c in s if c.isalnum())\n    return norm(a) == norm(b)\n```")

# ---------------------------------------------------------------------------
# FIZZBUZZ
# ---------------------------------------------------------------------------
add("fizzbuzz python",
    "```python\nfor i in range(1, 101):\n    if i % 15 == 0:\n        print('FizzBuzz')\n    elif i % 3 == 0:\n        print('Fizz')\n    elif i % 5 == 0:\n        print('Buzz')\n    else:\n        print(i)\n```")

add("write fizzbuzz as a function",
    "```python\ndef fizzbuzz(n):\n    out = []\n    for i in range(1, n + 1):\n        if i % 15 == 0:\n            out.append('FizzBuzz')\n        elif i % 3 == 0:\n            out.append('Fizz')\n        elif i % 5 == 0:\n            out.append('Buzz')\n        else:\n            out.append(str(i))\n    return out\n```")

add("fizzbuzz without modulo for 15",
    "You can build the string by concatenation:\n\n```python\nfor i in range(1, 101):\n    s = ''\n    if i % 3 == 0:\n        s += 'Fizz'\n    if i % 5 == 0:\n        s += 'Buzz'\n    print(s or i)\n```")

# ---------------------------------------------------------------------------
# TWO SUM
# ---------------------------------------------------------------------------
add("two sum problem python",
    "Use a hash map for O(n):\n\n```python\ndef two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []\n```")

add("find two numbers that add up to a target",
    "```python\ndef two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        complement = target - n\n        if complement in seen:\n            return [seen[complement], i]\n        seen[n] = i\n    return []\n```")

add("two sum brute force",
    "The brute-force O(n^2) approach:\n\n```python\ndef two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []\n```")

# ---------------------------------------------------------------------------
# SLIDING WINDOW
# ---------------------------------------------------------------------------
add("max sum subarray of size k sliding window",
    "```python\ndef max_subarray_sum(arr, k):\n    window = sum(arr[:k])\n    best = window\n    for i in range(k, len(arr)):\n        window += arr[i] - arr[i - k]\n        best = max(best, window)\n    return best\n```")

add("longest substring without repeating characters",
    "Sliding window with a set:\n\n```python\ndef length_of_longest_substring(s):\n    seen = set()\n    left = 0\n    best = 0\n    for right, ch in enumerate(s):\n        while ch in seen:\n            seen.remove(s[left])\n            left += 1\n        seen.add(ch)\n        best = max(best, right - left + 1)\n    return best\n```")

add("smallest subarray with sum at least target",
    "```python\ndef min_subarray_len(target, nums):\n    left = 0\n    total = 0\n    best = float('inf')\n    for right in range(len(nums)):\n        total += nums[right]\n        while total >= target:\n            best = min(best, right - left + 1)\n            total -= nums[left]\n            left += 1\n    return best if best != float('inf') else 0\n```")

# ---------------------------------------------------------------------------
# STACK / QUEUE / DEQUE
# ---------------------------------------------------------------------------
add("implement a stack in python",
    "A list works as a stack with append/pop:\n\n```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n    def push(self, x):\n        self._items.append(x)\n    def pop(self):\n        return self._items.pop()\n    def peek(self):\n        return self._items[-1]\n    def is_empty(self):\n        return not self._items\n```")

add("queue in python",
    "Use `collections.deque` for O(1) pops from the front:\n\n```python\nfrom collections import deque\n\nq = deque()\nq.append(1)      # enqueue\nq.append(2)\nfront = q.popleft()  # dequeue -> 1\n```")

add("deque example python",
    "```python\nfrom collections import deque\n\nd = deque([1, 2, 3])\nd.appendleft(0)   # deque([0, 1, 2, 3])\nd.append(4)       # deque([0, 1, 2, 3, 4])\nd.pop()           # 4\nd.popleft()       # 0\n```")

add("check balanced parentheses with a stack",
    "```python\ndef is_balanced(s):\n    pairs = {')': '(', ']': '[', '}': '{'}\n    stack = []\n    for ch in s:\n        if ch in '([{':\n            stack.append(ch)\n        elif ch in pairs:\n            if not stack or stack.pop() != pairs[ch]:\n                return False\n    return not stack\n```")

add("implement a queue using two stacks",
    "```python\nclass Queue:\n    def __init__(self):\n        self.in_stack = []\n        self.out_stack = []\n    def enqueue(self, x):\n        self.in_stack.append(x)\n    def dequeue(self):\n        if not self.out_stack:\n            while self.in_stack:\n                self.out_stack.append(self.in_stack.pop())\n        return self.out_stack.pop()\n```")

# ---------------------------------------------------------------------------
# LINKED LIST
# ---------------------------------------------------------------------------
add("singly linked list in python",
    "```python\nclass Node:\n    def __init__(self, value, next=None):\n        self.value = value\n        self.next = next\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n    def push_front(self, value):\n        self.head = Node(value, self.head)\n    def to_list(self):\n        out, node = [], self.head\n        while node:\n            out.append(node.value)\n            node = node.next\n        return out\n```")

add("reverse a linked list",
    "Iterate while flipping the `next` pointers:\n\n```python\ndef reverse_list(head):\n    prev = None\n    while head:\n        nxt = head.next\n        head.next = prev\n        prev = head\n        head = nxt\n    return prev\n```")

add("detect a cycle in a linked list",
    "Floyd's tortoise and hare:\n\n```python\ndef has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            return True\n    return False\n```")

add("find the middle of a linked list",
    "```python\ndef middle_node(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n    return slow\n```")

# ---------------------------------------------------------------------------
# BINARY TREES
# ---------------------------------------------------------------------------
add("binary tree node class python",
    "```python\nclass TreeNode:\n    def __init__(self, value, left=None, right=None):\n        self.value = value\n        self.left = left\n        self.right = right\n```")

add("inorder traversal of a binary tree",
    "```python\ndef inorder(root):\n    result = []\n    def visit(node):\n        if node:\n            visit(node.left)\n            result.append(node.value)\n            visit(node.right)\n    visit(root)\n    return result\n```")

add("preorder traversal binary tree",
    "```python\ndef preorder(root):\n    result = []\n    def visit(node):\n        if node:\n            result.append(node.value)\n            visit(node.left)\n            visit(node.right)\n    visit(root)\n    return result\n```")

add("postorder traversal",
    "```python\ndef postorder(root):\n    result = []\n    def visit(node):\n        if node:\n            visit(node.left)\n            visit(node.right)\n            result.append(node.value)\n    visit(root)\n    return result\n```")

add("level order traversal bfs of a tree",
    "BFS with a queue:\n\n```python\nfrom collections import deque\n\ndef level_order(root):\n    if not root:\n        return []\n    result, q = [], deque([root])\n    while q:\n        node = q.popleft()\n        result.append(node.value)\n        if node.left:\n            q.append(node.left)\n        if node.right:\n            q.append(node.right)\n    return result\n```")

add("height of a binary tree",
    "```python\ndef height(root):\n    if not root:\n        return 0\n    return 1 + max(height(root.left), height(root.right))\n```")

add("iterative inorder traversal with a stack",
    "```python\ndef inorder(root):\n    result, stack = [], []\n    node = root\n    while node or stack:\n        while node:\n            stack.append(node)\n            node = node.left\n        node = stack.pop()\n        result.append(node.value)\n        node = node.right\n    return result\n```")

add("dfs on a binary tree",
    "```python\ndef dfs(root):\n    result, stack = [], [root] if root else []\n    while stack:\n        node = stack.pop()\n        result.append(node.value)\n        if node.right:\n            stack.append(node.right)\n        if node.left:\n            stack.append(node.left)\n    return result\n```")

add("insert into a binary search tree",
    "```python\ndef insert(root, value):\n    if root is None:\n        return TreeNode(value)\n    if value < root.value:\n        root.left = insert(root.left, value)\n    else:\n        root.right = insert(root.right, value)\n    return root\n```")

# ---------------------------------------------------------------------------
# GRAPHS
# ---------------------------------------------------------------------------
add("build a graph adjacency list in python",
    "```python\nfrom collections import defaultdict\n\ngraph = defaultdict(list)\nedges = [(0, 1), (0, 2), (1, 2)]\nfor u, v in edges:\n    graph[u].append(v)\n    graph[v].append(u)  # undirected\n```")

add("bfs on a graph",
    "```python\nfrom collections import deque\n\ndef bfs(graph, start):\n    visited = {start}\n    order = []\n    q = deque([start])\n    while q:\n        node = q.popleft()\n        order.append(node)\n        for nbr in graph[node]:\n            if nbr not in visited:\n                visited.add(nbr)\n                q.append(nbr)\n    return order\n```")

add("dfs on a graph recursive",
    "```python\ndef dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    order = [start]\n    for nbr in graph[start]:\n        if nbr not in visited:\n            order.extend(dfs(graph, nbr, visited))\n    return order\n```")

add("dfs iterative with a stack",
    "```python\ndef dfs(graph, start):\n    visited = set()\n    order = []\n    stack = [start]\n    while stack:\n        node = stack.pop()\n        if node not in visited:\n            visited.add(node)\n            order.append(node)\n            stack.extend(graph[node])\n    return order\n```")

add("shortest path in an unweighted graph",
    "BFS gives shortest paths when edges are unweighted:\n\n```python\nfrom collections import deque\n\ndef shortest_path(graph, start, goal):\n    q = deque([[start]])\n    visited = {start}\n    while q:\n        path = q.popleft()\n        node = path[-1]\n        if node == goal:\n            return path\n        for nbr in graph[node]:\n            if nbr not in visited:\n                visited.add(nbr)\n                q.append(path + [nbr])\n    return None\n```")

add("detect a cycle in a directed graph",
    "Track nodes on the current DFS path:\n\n```python\ndef has_cycle(graph):\n    WHITE, GRAY, BLACK = 0, 1, 2\n    color = {node: WHITE for node in graph}\n    def dfs(u):\n        color[u] = GRAY\n        for v in graph[u]:\n            if color[v] == GRAY:\n                return True\n            if color[v] == WHITE and dfs(v):\n                return True\n        color[u] = BLACK\n        return False\n    return any(dfs(n) for n in graph if color[n] == WHITE)\n```")

add("topological sort python",
    "Kahn's algorithm using in-degrees:\n\n```python\nfrom collections import deque, defaultdict\n\ndef topo_sort(graph):\n    indeg = defaultdict(int)\n    for u in graph:\n        for v in graph[u]:\n            indeg[v] += 1\n    q = deque([u for u in graph if indeg[u] == 0])\n    order = []\n    while q:\n        u = q.popleft()\n        order.append(u)\n        for v in graph[u]:\n            indeg[v] -= 1\n            if indeg[v] == 0:\n                q.append(v)\n    return order\n```")

add("dijkstra shortest path",
    "```python\nimport heapq\n\ndef dijkstra(graph, start):\n    dist = {start: 0}\n    pq = [(0, start)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist.get(u, float('inf')):\n            continue\n        for v, w in graph[u]:\n            nd = d + w\n            if nd < dist.get(v, float('inf')):\n                dist[v] = nd\n                heapq.heappush(pq, (nd, v))\n    return dist\n```")

# ---------------------------------------------------------------------------
# DYNAMIC PROGRAMMING
# ---------------------------------------------------------------------------
add("climbing stairs dp",
    "It's just Fibonacci in disguise:\n\n```python\ndef climb_stairs(n):\n    a, b = 1, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```")

add("coin change minimum coins dp",
    "```python\ndef coin_change(coins, amount):\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for c in coins:\n        for x in range(c, amount + 1):\n            dp[x] = min(dp[x], dp[x - c] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1\n```")

add("longest common subsequence",
    "```python\ndef lcs(a, b):\n    m, n = len(a), len(b)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if a[i - 1] == b[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1] + 1\n            else:\n                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n    return dp[m][n]\n```")

add("0/1 knapsack python dp",
    "```python\ndef knapsack(weights, values, capacity):\n    n = len(weights)\n    dp = [[0] * (capacity + 1) for _ in range(n + 1)]\n    for i in range(1, n + 1):\n        for w in range(capacity + 1):\n            dp[i][w] = dp[i - 1][w]\n            if weights[i - 1] <= w:\n                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])\n    return dp[n][capacity]\n```")

add("longest increasing subsequence",
    "O(n^2) DP version:\n\n```python\ndef lis(nums):\n    if not nums:\n        return 0\n    dp = [1] * len(nums)\n    for i in range(len(nums)):\n        for j in range(i):\n            if nums[j] < nums[i]:\n                dp[i] = max(dp[i], dp[j] + 1)\n    return max(dp)\n```")

add("edit distance dp",
    "Levenshtein distance:\n\n```python\ndef edit_distance(a, b):\n    m, n = len(a), len(b)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(m + 1):\n        dp[i][0] = i\n    for j in range(n + 1):\n        dp[0][j] = j\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            cost = 0 if a[i - 1] == b[j - 1] else 1\n            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)\n    return dp[m][n]\n```")

add("maximum subarray sum kadane",
    "Kadane's algorithm, O(n):\n\n```python\ndef max_subarray(nums):\n    best = cur = nums[0]\n    for x in nums[1:]:\n        cur = max(x, cur + x)\n        best = max(best, cur)\n    return best\n```")

add("house robber dp",
    "```python\ndef rob(nums):\n    prev = cur = 0\n    for n in nums:\n        prev, cur = cur, max(cur, prev + n)\n    return cur\n```")

add("number of ways to make change dp",
    "```python\ndef change(amount, coins):\n    dp = [0] * (amount + 1)\n    dp[0] = 1\n    for c in coins:\n        for x in range(c, amount + 1):\n            dp[x] += dp[x - c]\n    return dp[amount]\n```")

# ---------------------------------------------------------------------------
# HASH MAPS / COUNTING
# ---------------------------------------------------------------------------
add("count occurrences of each element in a list",
    "```python\nfrom collections import Counter\n\nnums = [1, 1, 2, 3, 3, 3]\nprint(Counter(nums))  # Counter({3: 3, 1: 2, 2: 1})\n```")

add("count word frequency in a string",
    "```python\nfrom collections import Counter\n\ntext = 'the cat sat on the mat'\nprint(Counter(text.split()))\n```")

add("find the most common element",
    "```python\nfrom collections import Counter\n\nnums = [1, 2, 2, 3, 3, 3]\nprint(Counter(nums).most_common(1)[0][0])  # 3\n```")

add("count characters without Counter",
    "```python\ndef char_count(s):\n    counts = {}\n    for ch in s:\n        counts[ch] = counts.get(ch, 0) + 1\n    return counts\n```")

add("find first non-repeating character",
    "```python\nfrom collections import Counter\n\ndef first_unique(s):\n    counts = Counter(s)\n    for ch in s:\n        if counts[ch] == 1:\n            return ch\n    return None\n```")

add("group anagrams together",
    "Key each word by its sorted letters:\n\n```python\nfrom collections import defaultdict\n\ndef group_anagrams(words):\n    groups = defaultdict(list)\n    for w in words:\n        groups[''.join(sorted(w))].append(w)\n    return list(groups.values())\n```")

# ---------------------------------------------------------------------------
# SETS / DEDUP
# ---------------------------------------------------------------------------
add("remove duplicates from a list",
    "If order doesn't matter, use a set:\n\n```python\nnums = [1, 2, 2, 3, 3]\nprint(list(set(nums)))\n```")

add("remove duplicates keeping order",
    "`dict.fromkeys` preserves insertion order:\n\n```python\nnums = [3, 1, 3, 2, 1]\nprint(list(dict.fromkeys(nums)))  # [3, 1, 2]\n```")

add("find common elements between two lists",
    "```python\na = [1, 2, 3, 4]\nb = [3, 4, 5, 6]\nprint(list(set(a) & set(b)))  # [3, 4]\n```")

add("find elements in one list but not the other",
    "```python\na = [1, 2, 3, 4]\nb = [3, 4]\nprint(list(set(a) - set(b)))  # [1, 2]\n```")

add("check if a list has duplicates",
    "```python\ndef has_duplicates(lst):\n    return len(lst) != len(set(lst))\n```")

# ---------------------------------------------------------------------------
# HEAPS / PRIORITY QUEUE
# ---------------------------------------------------------------------------
add("min heap in python",
    "`heapq` implements a min-heap on a list:\n\n```python\nimport heapq\n\nheap = []\nheapq.heappush(heap, 3)\nheapq.heappush(heap, 1)\nheapq.heappush(heap, 2)\nprint(heapq.heappop(heap))  # 1\n```")

add("max heap in python",
    "Negate the values to simulate a max-heap:\n\n```python\nimport heapq\n\nheap = []\nfor x in [3, 1, 2]:\n    heapq.heappush(heap, -x)\nprint(-heapq.heappop(heap))  # 3\n```")

add("k largest elements",
    "```python\nimport heapq\n\nnums = [5, 1, 8, 3, 9, 2]\nprint(heapq.nlargest(3, nums))  # [9, 8, 5]\n```")

add("k smallest elements",
    "```python\nimport heapq\n\nnums = [5, 1, 8, 3, 9, 2]\nprint(heapq.nsmallest(3, nums))  # [1, 2, 3]\n```")

add("priority queue with tuples",
    "Push `(priority, item)` tuples; the heap orders by priority:\n\n```python\nimport heapq\n\npq = []\nheapq.heappush(pq, (2, 'task b'))\nheapq.heappush(pq, (1, 'task a'))\nprint(heapq.heappop(pq))  # (1, 'task a')\n```")

add("kth largest element in an array",
    "```python\nimport heapq\n\ndef kth_largest(nums, k):\n    return heapq.nlargest(k, nums)[-1]\n```")

add("merge k sorted lists with a heap",
    "```python\nimport heapq\n\ndef merge_k(lists):\n    return list(heapq.merge(*lists))\n```")

# ---------------------------------------------------------------------------
# SORTING DICTS
# ---------------------------------------------------------------------------
add("sort a dictionary by value",
    "```python\nd = {'a': 3, 'b': 1, 'c': 2}\nordered = dict(sorted(d.items(), key=lambda kv: kv[1]))\nprint(ordered)  # {'b': 1, 'c': 2, 'a': 3}\n```")

add("sort a dict by key",
    "```python\nd = {'c': 1, 'a': 2, 'b': 3}\nprint(dict(sorted(d.items())))  # {'a': 2, 'b': 3, 'c': 1}\n```")

add("sort dictionary by value descending",
    "```python\nd = {'a': 1, 'b': 3, 'c': 2}\nprint(dict(sorted(d.items(), key=lambda kv: kv[1], reverse=True)))\n```")

add("get top 3 keys by value from a dict",
    "```python\nfrom heapq import nlargest\n\nd = {'a': 5, 'b': 2, 'c': 9, 'd': 1}\nprint(nlargest(3, d, key=d.get))  # ['c', 'a', 'b']\n```")

# ---------------------------------------------------------------------------
# RECURSION misc
# ---------------------------------------------------------------------------
add("sum of a list recursively",
    "```python\ndef rec_sum(lst):\n    if not lst:\n        return 0\n    return lst[0] + rec_sum(lst[1:])\n```")

add("power function recursive",
    "Fast exponentiation in O(log n):\n\n```python\ndef power(base, exp):\n    if exp == 0:\n        return 1\n    half = power(base, exp // 2)\n    if exp % 2:\n        return half * half * base\n    return half * half\n```")

add("tower of hanoi",
    "```python\ndef hanoi(n, source, target, aux):\n    if n == 1:\n        print(f'Move disk 1 from {source} to {target}')\n        return\n    hanoi(n - 1, source, aux, target)\n    print(f'Move disk {n} from {source} to {target}')\n    hanoi(n - 1, aux, target, source)\n```")

add("flatten a nested list recursively",
    "```python\ndef flatten(lst):\n    result = []\n    for item in lst:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result\n```")

add("permutations of a list",
    "```python\nfrom itertools import permutations\n\nprint(list(permutations([1, 2, 3])))\n```")

add("all subsets of a set powerset",
    "```python\nfrom itertools import combinations\n\ndef powerset(items):\n    result = []\n    for r in range(len(items) + 1):\n        result.extend(combinations(items, r))\n    return result\n```")

# ---------------------------------------------------------------------------
# MISC well-known
# ---------------------------------------------------------------------------
add("check if two strings are rotations of each other",
    "A rotation is a substring of the doubled string:\n\n```python\ndef is_rotation(a, b):\n    return len(a) == len(b) and b in a + a\n```")

add("find missing number in 0..n",
    "```python\ndef missing_number(nums):\n    n = len(nums)\n    return n * (n + 1) // 2 - sum(nums)\n```")

add("find the duplicate number",
    "```python\ndef find_duplicate(nums):\n    seen = set()\n    for n in nums:\n        if n in seen:\n            return n\n        seen.add(n)\n    return -1\n```")

add("majority element boyer moore",
    "Boyer-Moore voting, O(n) time O(1) space:\n\n```python\ndef majority(nums):\n    count = 0\n    candidate = None\n    for n in nums:\n        if count == 0:\n            candidate = n\n        count += 1 if n == candidate else -1\n    return candidate\n```")

add("move all zeros to the end of a list",
    "```python\ndef move_zeros(nums):\n    pos = 0\n    for i in range(len(nums)):\n        if nums[i] != 0:\n            nums[pos], nums[i] = nums[i], nums[pos]\n            pos += 1\n    return nums\n```")

add("rotate an array by k",
    "```python\ndef rotate(nums, k):\n    k %= len(nums)\n    return nums[-k:] + nums[:-k]\n```")

add("intersection of two sorted arrays",
    "```python\ndef intersect(a, b):\n    i = j = 0\n    result = []\n    while i < len(a) and j < len(b):\n        if a[i] == b[j]:\n            result.append(a[i])\n            i += 1; j += 1\n        elif a[i] < b[j]:\n            i += 1\n        else:\n            j += 1\n    return result\n```")

add("count vowels in a string",
    "```python\ndef count_vowels(s):\n    return sum(1 for ch in s.lower() if ch in 'aeiou')\n```")

add("title case a string",
    "```python\ns = 'hello world'\nprint(s.title())  # 'Hello World'\n```")

add("caesar cipher python",
    "```python\ndef caesar(text, shift):\n    result = []\n    for ch in text:\n        if ch.isalpha():\n            base = ord('A') if ch.isupper() else ord('a')\n            result.append(chr((ord(ch) - base + shift) % 26 + base))\n        else:\n            result.append(ch)\n    return ''.join(result)\n```")

add("run length encoding",
    "```python\nfrom itertools import groupby\n\ndef rle(s):\n    return ''.join(f'{ch}{len(list(g))}' for ch, g in groupby(s))\n\nprint(rle('aaabbc'))  # 'a3b2c1'\n```")

add("binary representation of a number",
    "```python\nn = 10\nprint(bin(n)[2:])  # '1010'\n```")

add("count set bits in an integer",
    "```python\ndef count_bits(n):\n    return bin(n).count('1')\n```")

add("check if a number is a power of two",
    "Bit trick: a power of two has exactly one set bit:\n\n```python\ndef is_power_of_two(n):\n    return n > 0 and (n & (n - 1)) == 0\n```")

add("sum of digits of a number",
    "```python\ndef digit_sum(n):\n    return sum(int(d) for d in str(abs(n)))\n```")

add("find max and min of a list",
    "```python\nnums = [3, 7, 1, 9, 4]\nprint(max(nums), min(nums))  # 9 1\n```")

add("second largest element in a list",
    "```python\ndef second_largest(nums):\n    return sorted(set(nums))[-2]\n```")

add("merge two sorted lists",
    "```python\ndef merge(a, b):\n    i = j = 0\n    result = []\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            result.append(a[i]); i += 1\n        else:\n            result.append(b[j]); j += 1\n    result.extend(a[i:])\n    result.extend(b[j:])\n    return result\n```")

add("matrix transpose python",
    "```python\nmatrix = [[1, 2, 3], [4, 5, 6]]\nprint([list(row) for row in zip(*matrix)])  # [[1, 4], [2, 5], [3, 6]]\n```")

add("rotate a matrix 90 degrees",
    "```python\ndef rotate90(matrix):\n    return [list(row) for row in zip(*matrix[::-1])]\n```")

add("spiral order of a matrix",
    "```python\ndef spiral(matrix):\n    result = []\n    while matrix:\n        result += matrix.pop(0)\n        matrix = [list(row) for row in zip(*matrix)][::-1]\n    return result\n```")

add("gcd of a list of numbers",
    "```python\nimport math\nfrom functools import reduce\n\ndef gcd_list(nums):\n    return reduce(math.gcd, nums)\n```")

add("chunk a list into groups of n",
    "```python\ndef chunk(lst, n):\n    return [lst[i:i + n] for i in range(0, len(lst), n)]\n```")

add("find all pairs that sum to target",
    "```python\ndef pair_sums(nums, target):\n    seen = set()\n    pairs = []\n    for n in nums:\n        if target - n in seen:\n            pairs.append((target - n, n))\n        seen.add(n)\n    return pairs\n```")

add("binary search for first occurrence",
    "```python\ndef first_occurrence(arr, target):\n    lo, hi = 0, len(arr) - 1\n    result = -1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            result = mid\n            hi = mid - 1\n        elif arr[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return result\n```")

add("valid parentheses leetcode",
    "```python\ndef is_valid(s):\n    pairs = {')': '(', ']': '[', '}': '{'}\n    stack = []\n    for ch in s:\n        if ch in '([{':\n            stack.append(ch)\n        elif not stack or stack.pop() != pairs[ch]:\n            return False\n    return not stack\n```")

add("fibonacci using matrix exponentiation",
    "Matrix power gives O(log n):\n\n```python\ndef fib(n):\n    def mat_mult(a, b):\n        return [[a[0][0]*b[0][0]+a[0][1]*b[1][0], a[0][0]*b[0][1]+a[0][1]*b[1][1]],\n                [a[1][0]*b[0][0]+a[1][1]*b[1][0], a[1][0]*b[0][1]+a[1][1]*b[1][1]]]\n    result = [[1, 0], [0, 1]]\n    base = [[1, 1], [1, 0]]\n    while n:\n        if n & 1:\n            result = mat_mult(result, base)\n        base = mat_mult(base, base)\n        n >>= 1\n    return result[0][1]\n```")

add("merge intervals",
    "```python\ndef merge_intervals(intervals):\n    intervals.sort()\n    merged = []\n    for start, end in intervals:\n        if merged and start <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], end)\n        else:\n            merged.append([start, end])\n    return merged\n```")

add("count islands in a grid dfs",
    "```python\ndef num_islands(grid):\n    if not grid:\n        return 0\n    rows, cols = len(grid), len(grid[0])\n    def dfs(r, c):\n        if 0 <= r < rows and 0 <= c < cols and grid[r][c] == '1':\n            grid[r][c] = '0'\n            dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)\n    count = 0\n    for r in range(rows):\n        for c in range(cols):\n            if grid[r][c] == '1':\n                count += 1\n                dfs(r, c)\n    return count\n```")

add("sieve of eratosthenes",
    "```python\ndef sieve(n):\n    primes = [True] * (n + 1)\n    primes[0:2] = [False, False]\n    for i in range(2, int(n ** 0.5) + 1):\n        if primes[i]:\n            for j in range(i * i, n + 1, i):\n                primes[j] = False\n    return [i for i in range(n + 1) if primes[i]]\n```")

add("trapping rain water",
    "Two-pointer approach, O(n):\n\n```python\ndef trap(height):\n    left, right = 0, len(height) - 1\n    left_max = right_max = 0\n    water = 0\n    while left < right:\n        if height[left] < height[right]:\n            left_max = max(left_max, height[left])\n            water += left_max - height[left]\n            left += 1\n        else:\n            right_max = max(right_max, height[right])\n            water += right_max - height[right]\n            right -= 1\n    return water\n```")

add("product of array except self",
    "```python\ndef product_except_self(nums):\n    n = len(nums)\n    result = [1] * n\n    prefix = 1\n    for i in range(n):\n        result[i] = prefix\n        prefix *= nums[i]\n    suffix = 1\n    for i in range(n - 1, -1, -1):\n        result[i] *= suffix\n        suffix *= nums[i]\n    return result\n```")

add("group elements by a key function",
    "```python\nfrom collections import defaultdict\n\ndef group_by(items, key):\n    groups = defaultdict(list)\n    for item in items:\n        groups[key(item)].append(item)\n    return dict(groups)\n```")

add("binary tree is balanced",
    "```python\ndef is_balanced(root):\n    def height(node):\n        if not node:\n            return 0\n        lh = height(node.left)\n        rh = height(node.right)\n        if lh == -1 or rh == -1 or abs(lh - rh) > 1:\n            return -1\n        return 1 + max(lh, rh)\n    return height(root) != -1\n```")

add("lowest common ancestor in a BST",
    "```python\ndef lca(root, p, q):\n    while root:\n        if p < root.value and q < root.value:\n            root = root.left\n        elif p > root.value and q > root.value:\n            root = root.right\n        else:\n            return root\n    return None\n```")

add("invert a binary tree",
    "```python\ndef invert(root):\n    if root:\n        root.left, root.right = invert(root.right), invert(root.left)\n    return root\n```")

add("count nodes in a binary tree",
    "```python\ndef count_nodes(root):\n    if not root:\n        return 0\n    return 1 + count_nodes(root.left) + count_nodes(root.right)\n```")

add("min stack supporting getMin in O(1)",
    "```python\nclass MinStack:\n    def __init__(self):\n        self.stack = []\n        self.mins = []\n    def push(self, x):\n        self.stack.append(x)\n        self.mins.append(min(x, self.mins[-1]) if self.mins else x)\n    def pop(self):\n        self.mins.pop()\n        return self.stack.pop()\n    def get_min(self):\n        return self.mins[-1]\n```")

add("LRU cache python",
    "`OrderedDict` makes this easy:\n\n```python\nfrom collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cache = OrderedDict()\n        self.capacity = capacity\n    def get(self, key):\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n    def put(self, key, value):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity:\n            self.cache.popitem(last=False)\n```")

add("binary search rightmost insertion",
    "```python\nimport bisect\n\narr = [1, 2, 2, 2, 3]\nprint(bisect.bisect_right(arr, 2))  # 4\n```")

add("dot product of two vectors",
    "```python\ndef dot(a, b):\n    return sum(x * y for x, y in zip(a, b))\n```")

add("fibonacci modulo m pisano",
    "Compute fib(n) mod m without overflow:\n\n```python\ndef fib_mod(n, m):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, (a + b) % m\n    return a\n```")

add("longest palindromic substring",
    "Expand around center:\n\n```python\ndef longest_palindrome(s):\n    def expand(l, r):\n        while l >= 0 and r < len(s) and s[l] == s[r]:\n            l -= 1; r += 1\n        return s[l + 1:r]\n    best = ''\n    for i in range(len(s)):\n        for cand in (expand(i, i), expand(i, i + 1)):\n            if len(cand) > len(best):\n                best = cand\n    return best\n```")

add("count distinct elements in a list",
    "```python\nnums = [1, 2, 2, 3, 3, 3]\nprint(len(set(nums)))  # 3\n```")

add("zip two lists into a dict",
    "```python\nkeys = ['a', 'b', 'c']\nvalues = [1, 2, 3]\nprint(dict(zip(keys, values)))  # {'a': 1, 'b': 2, 'c': 3}\n```")

add("find peak element",
    "Binary search works since we only need any peak:\n\n```python\ndef find_peak(nums):\n    lo, hi = 0, len(nums) - 1\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if nums[mid] < nums[mid + 1]:\n            lo = mid + 1\n        else:\n            hi = mid\n    return lo\n```")

add("subsets / combinations of size k",
    "```python\nfrom itertools import combinations\n\nprint(list(combinations([1, 2, 3, 4], 2)))\n```")

add("generate all binary strings of length n",
    "```python\nfrom itertools import product\n\ndef binary_strings(n):\n    return [''.join(bits) for bits in product('01', repeat=n)]\n```")

add("compute average of a list",
    "```python\ndef average(nums):\n    return sum(nums) / len(nums) if nums else 0\n```")

add("find mode of a list",
    "```python\nfrom collections import Counter\n\ndef mode(nums):\n    return Counter(nums).most_common(1)[0][0]\n```")

add("median of a list",
    "```python\nimport statistics\nprint(statistics.median([3, 1, 2]))  # 2\n```")

add("dedupe and sort a list",
    "```python\nnums = [3, 1, 2, 3, 1]\nprint(sorted(set(nums)))  # [1, 2, 3]\n```")

add("convert roman numeral to integer",
    "```python\ndef roman_to_int(s):\n    vals = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}\n    total = 0\n    for i in range(len(s)):\n        if i + 1 < len(s) and vals[s[i]] < vals[s[i + 1]]:\n            total -= vals[s[i]]\n        else:\n            total += vals[s[i]]\n    return total\n```")

add("integer to roman numeral",
    "```python\ndef int_to_roman(n):\n    table = [(1000,'M'),(900,'CM'),(500,'D'),(400,'CD'),(100,'C'),\n             (90,'XC'),(50,'L'),(40,'XL'),(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]\n    result = []\n    for value, symbol in table:\n        while n >= value:\n            result.append(symbol)\n            n -= value\n    return ''.join(result)\n```")

add("is a string a valid number",
    "```python\ndef is_number(s):\n    try:\n        float(s)\n        return True\n    except ValueError:\n        return False\n```")

add("count pairs with given difference",
    "```python\ndef count_pairs_diff(nums, k):\n    s = set(nums)\n    return sum(1 for n in s if n + k in s)\n```")

add("sort characters in a string",
    "```python\ns = 'dcba'\nprint(''.join(sorted(s)))  # 'abcd'\n```")

add("frequency sort a string by count",
    "```python\nfrom collections import Counter\n\ndef freq_sort(s):\n    counts = Counter(s)\n    return ''.join(ch * c for ch, c in counts.most_common())\n```")

# ---------------------------------------------------------------------------
# MULTI-TURN CONVERSATIONS (~30)
# ---------------------------------------------------------------------------
add_multi([
    ("user", "write a recursive fibonacci"),
    ("silicat", "```python\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n```"),
    ("user", "now make it iterative"),
    ("silicat", "Iterative runs in O(n) instead of O(2^n):\n\n```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```"),
])

add_multi([
    ("user", "iterative fibonacci"),
    ("silicat", "```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```"),
    ("user", "what's the time complexity?"),
    ("silicat", "O(n) time and O(1) space, since it loops once and keeps only two variables. The recursive version without memoization is O(2^n)."),
])

add_multi([
    ("user", "give me a bubble sort"),
    ("silicat", "```python\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n```"),
    ("user", "add early termination if it's already sorted"),
    ("silicat", "Track whether any swap happened in a pass:\n\n```python\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break\n    return arr\n```"),
])

add_multi([
    ("user", "binary search please"),
    ("silicat", "```python\ndef binary_search(arr, target):\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n```"),
    ("user", "make it recursive"),
    ("silicat", "```python\ndef binary_search(arr, target, lo=0, hi=None):\n    if hi is None:\n        hi = len(arr) - 1\n    if lo > hi:\n        return -1\n    mid = (lo + hi) // 2\n    if arr[mid] == target:\n        return mid\n    if arr[mid] < target:\n        return binary_search(arr, target, mid + 1, hi)\n    return binary_search(arr, target, lo, mid - 1)\n```"),
])

add_multi([
    ("user", "is_prime function"),
    ("silicat", "```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n ** 0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n```"),
    ("user", "can you speed it up by skipping even numbers?"),
    ("silicat", "Yes, handle 2 separately and only test odd divisors:\n\n```python\ndef is_prime(n):\n    if n < 2:\n        return False\n    if n == 2:\n        return True\n    if n % 2 == 0:\n        return False\n    for i in range(3, int(n ** 0.5) + 1, 2):\n        if n % i == 0:\n            return False\n    return True\n```"),
])

add_multi([
    ("user", "linear search function"),
    ("silicat", "```python\ndef linear_search(arr, target):\n    for i, x in enumerate(arr):\n        if x == target:\n            return i\n    return -1\n```"),
    ("user", "return all matching indices instead"),
    ("silicat", "```python\ndef find_all(arr, target):\n    return [i for i, x in enumerate(arr) if x == target]\n```"),
])

add_multi([
    ("user", "check if a string is a palindrome"),
    ("silicat", "```python\ndef is_palindrome(s):\n    return s == s[::-1]\n```"),
    ("user", "ignore case, spaces, and punctuation"),
    ("silicat", "```python\ndef is_palindrome(s):\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]\n```"),
])

add_multi([
    ("user", "factorial function"),
    ("silicat", "```python\ndef factorial(n):\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n```"),
    ("user", "raise an error for negative input"),
    ("silicat", "```python\ndef factorial(n):\n    if n < 0:\n        raise ValueError('n must be non-negative')\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n```"),
])

add_multi([
    ("user", "quicksort"),
    ("silicat", "```python\ndef quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    mid = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + mid + quicksort(right)\n```"),
    ("user", "what's the worst case complexity?"),
    ("silicat", "O(n^2), which happens when the pivot is consistently the smallest or largest element (e.g. an already-sorted list with a poor pivot choice). The average case is O(n log n). Choosing a random or median-of-three pivot makes the worst case unlikely."),
])

add_multi([
    ("user", "two sum"),
    ("silicat", "```python\ndef two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target - n], i]\n        seen[n] = i\n    return []\n```"),
    ("user", "return the values instead of the indices"),
    ("silicat", "```python\ndef two_sum(nums, target):\n    seen = set()\n    for n in nums:\n        if target - n in seen:\n            return [target - n, n]\n        seen.add(n)\n    return []\n```"),
])

add_multi([
    ("user", "merge sort implementation"),
    ("silicat", "```python\ndef merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    out, i, j = [], 0, 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            out.append(left[i]); i += 1\n        else:\n            out.append(right[j]); j += 1\n    out.extend(left[i:]); out.extend(right[j:])\n    return out\n```"),
    ("user", "is it stable?"),
    ("silicat", "Yes. Because the merge uses `left[i] <= right[j]`, equal elements keep their original relative order, so merge sort is stable."),
])

add_multi([
    ("user", "implement a stack"),
    ("silicat", "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n    def push(self, x):\n        self._items.append(x)\n    def pop(self):\n        return self._items.pop()\n    def is_empty(self):\n        return not self._items\n```"),
    ("user", "add a peek method and a size method"),
    ("silicat", "```python\nclass Stack:\n    def __init__(self):\n        self._items = []\n    def push(self, x):\n        self._items.append(x)\n    def pop(self):\n        return self._items.pop()\n    def peek(self):\n        return self._items[-1]\n    def size(self):\n        return len(self._items)\n    def is_empty(self):\n        return not self._items\n```"),
])

add_multi([
    ("user", "bfs on a graph"),
    ("silicat", "```python\nfrom collections import deque\n\ndef bfs(graph, start):\n    visited = {start}\n    order = []\n    q = deque([start])\n    while q:\n        node = q.popleft()\n        order.append(node)\n        for nbr in graph[node]:\n            if nbr not in visited:\n                visited.add(nbr)\n                q.append(nbr)\n    return order\n```"),
    ("user", "now give me the DFS version"),
    ("silicat", "Swap the queue for a stack (or recurse):\n\n```python\ndef dfs(graph, start):\n    visited = set()\n    order = []\n    stack = [start]\n    while stack:\n        node = stack.pop()\n        if node not in visited:\n            visited.add(node)\n            order.append(node)\n            stack.extend(graph[node])\n    return order\n```"),
])

add_multi([
    ("user", "count occurrences of items in a list"),
    ("silicat", "```python\nfrom collections import Counter\n\nnums = [1, 1, 2, 3]\nprint(Counter(nums))\n```"),
    ("user", "now only show items that appear more than once"),
    ("silicat", "```python\nfrom collections import Counter\n\ndef duplicates(nums):\n    return [item for item, c in Counter(nums).items() if c > 1]\n```"),
])

add_multi([
    ("user", "sort a dictionary by value"),
    ("silicat", "```python\nd = {'a': 3, 'b': 1, 'c': 2}\nprint(dict(sorted(d.items(), key=lambda kv: kv[1])))\n```"),
    ("user", "descending please"),
    ("silicat", "```python\nd = {'a': 3, 'b': 1, 'c': 2}\nprint(dict(sorted(d.items(), key=lambda kv: kv[1], reverse=True)))\n```"),
])

add_multi([
    ("user", "reverse a linked list"),
    ("silicat", "```python\ndef reverse_list(head):\n    prev = None\n    while head:\n        nxt = head.next\n        head.next = prev\n        prev = head\n        head = nxt\n    return prev\n```"),
    ("user", "can you do it recursively?"),
    ("silicat", "```python\ndef reverse_list(head, prev=None):\n    if head is None:\n        return prev\n    nxt = head.next\n    head.next = prev\n    return reverse_list(nxt, head)\n```"),
])

add_multi([
    ("user", "inorder traversal of a binary tree"),
    ("silicat", "```python\ndef inorder(root):\n    result = []\n    def visit(node):\n        if node:\n            visit(node.left)\n            result.append(node.value)\n            visit(node.right)\n    visit(root)\n    return result\n```"),
    ("user", "make it iterative"),
    ("silicat", "```python\ndef inorder(root):\n    result, stack = [], []\n    node = root\n    while node or stack:\n        while node:\n            stack.append(node)\n            node = node.left\n        node = stack.pop()\n        result.append(node.value)\n        node = node.right\n    return result\n```"),
])

add_multi([
    ("user", "coin change minimum coins"),
    ("silicat", "```python\ndef coin_change(coins, amount):\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for c in coins:\n        for x in range(c, amount + 1):\n            dp[x] = min(dp[x], dp[x - c] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1\n```"),
    ("user", "what does it return if amount can't be made?"),
    ("silicat", "It returns -1. If `dp[amount]` is still `float('inf')` after filling the table, no combination of coins sums to the amount, so the function returns -1."),
])

add_multi([
    ("user", "remove duplicates from a list"),
    ("silicat", "```python\nnums = [1, 2, 2, 3]\nprint(list(set(nums)))\n```"),
    ("user", "but I need to preserve the original order"),
    ("silicat", "Use `dict.fromkeys`, which keeps insertion order:\n\n```python\nnums = [3, 1, 3, 2, 1]\nprint(list(dict.fromkeys(nums)))  # [3, 1, 2]\n```"),
])

add_multi([
    ("user", "find the max element in a list"),
    ("silicat", "```python\nnums = [3, 9, 2, 7]\nprint(max(nums))  # 9\n```"),
    ("user", "handle the empty list case"),
    ("silicat", "`max` raises ValueError on an empty list, so pass a default:\n\n```python\ndef safe_max(nums):\n    return max(nums, default=None)\n```"),
])

add_multi([
    ("user", "anagram check"),
    ("silicat", "```python\ndef is_anagram(a, b):\n    return sorted(a) == sorted(b)\n```"),
    ("user", "make it more efficient than sorting"),
    ("silicat", "Counting characters is O(n) instead of O(n log n):\n\n```python\nfrom collections import Counter\n\ndef is_anagram(a, b):\n    return Counter(a) == Counter(b)\n```"),
])

add_multi([
    ("user", "gcd of two numbers"),
    ("silicat", "```python\ndef gcd(a, b):\n    while b:\n        a, b = b, a % b\n    return a\n```"),
    ("user", "now give me lcm using that"),
    ("silicat", "```python\ndef lcm(a, b):\n    return a * b // gcd(a, b)\n```"),
])

add_multi([
    ("user", "climbing stairs problem"),
    ("silicat", "```python\ndef climb_stairs(n):\n    a, b = 1, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```"),
    ("user", "what if you can take 1, 2, or 3 steps?"),
    ("silicat", "Sum the last three states instead of two:\n\n```python\ndef climb_stairs(n):\n    a, b, c = 1, 1, 2\n    if n == 0:\n        return 1\n    if n == 1:\n        return 1\n    for _ in range(n - 2):\n        a, b, c = b, c, a + b + c\n    return c\n```"),
])

add_multi([
    ("user", "implement a queue"),
    ("silicat", "```python\nfrom collections import deque\n\nclass Queue:\n    def __init__(self):\n        self._items = deque()\n    def enqueue(self, x):\n        self._items.append(x)\n    def dequeue(self):\n        return self._items.popleft()\n    def is_empty(self):\n        return not self._items\n```"),
    ("user", "why deque instead of a list?"),
    ("silicat", "A list's `pop(0)` is O(n) because every remaining element shifts left. `deque.popleft()` is O(1), so it's the right structure for a queue."),
])

add_multi([
    ("user", "find kth largest element"),
    ("silicat", "```python\nimport heapq\n\ndef kth_largest(nums, k):\n    return heapq.nlargest(k, nums)[-1]\n```"),
    ("user", "do it without sorting the whole list"),
    ("silicat", "Keep a min-heap of size k, so it's O(n log k):\n\n```python\nimport heapq\n\ndef kth_largest(nums, k):\n    heap = nums[:k]\n    heapq.heapify(heap)\n    for n in nums[k:]:\n        if n > heap[0]:\n            heapq.heapreplace(heap, n)\n    return heap[0]\n```"),
])

add_multi([
    ("user", "fizzbuzz"),
    ("silicat", "```python\nfor i in range(1, 101):\n    if i % 15 == 0:\n        print('FizzBuzz')\n    elif i % 3 == 0:\n        print('Fizz')\n    elif i % 5 == 0:\n        print('Buzz')\n    else:\n        print(i)\n```"),
    ("user", "make it configurable with custom rules"),
    ("silicat", "Pass a list of (divisor, word) rules:\n\n```python\ndef fizzbuzz(n, rules=((3, 'Fizz'), (5, 'Buzz'))):\n    out = []\n    for i in range(1, n + 1):\n        s = ''.join(word for d, word in rules if i % d == 0)\n        out.append(s or str(i))\n    return out\n```"),
])

add_multi([
    ("user", "reverse a string"),
    ("silicat", "```python\ns = 'hello'\nprint(s[::-1])\n```"),
    ("user", "do it without slicing or reversed()"),
    ("silicat", "```python\ndef reverse(s):\n    chars = list(s)\n    i, j = 0, len(chars) - 1\n    while i < j:\n        chars[i], chars[j] = chars[j], chars[i]\n        i += 1; j -= 1\n    return ''.join(chars)\n```"),
])

add_multi([
    ("user", "memoized fibonacci"),
    ("silicat", "```python\nfrom functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n```"),
    ("user", "do it without lru_cache"),
    ("silicat", "Pass a dict as the cache:\n\n```python\ndef fib(n, memo=None):\n    if memo is None:\n        memo = {}\n    if n < 2:\n        return n\n    if n not in memo:\n        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)\n    return memo[n]\n```"),
])

add_multi([
    ("user", "longest common subsequence"),
    ("silicat", "```python\ndef lcs(a, b):\n    m, n = len(a), len(b)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if a[i - 1] == b[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1] + 1\n            else:\n                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n    return dp[m][n]\n```"),
    ("user", "now reconstruct the actual subsequence, not just its length"),
    ("silicat", "Walk back through the DP table:\n\n```python\ndef lcs(a, b):\n    m, n = len(a), len(b)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if a[i - 1] == b[j - 1]:\n                dp[i][j] = dp[i - 1][j - 1] + 1\n            else:\n                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])\n    seq = []\n    i, j = m, n\n    while i > 0 and j > 0:\n        if a[i - 1] == b[j - 1]:\n            seq.append(a[i - 1]); i -= 1; j -= 1\n        elif dp[i - 1][j] >= dp[i][j - 1]:\n            i -= 1\n        else:\n            j -= 1\n    return ''.join(reversed(seq))\n```"),
])

add_multi([
    ("user", "selection sort"),
    ("silicat", "```python\ndef selection_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        min_idx = i\n        for j in range(i + 1, n):\n            if arr[j] < arr[min_idx]:\n                min_idx = j\n        arr[i], arr[min_idx] = arr[min_idx], arr[i]\n    return arr\n```"),
    ("user", "what's its time complexity?"),
    ("silicat", "O(n^2) in all cases (best, average, and worst), because it always scans the unsorted portion to find the minimum. It uses O(1) extra space and does at most n-1 swaps."),
])

add_multi([
    ("user", "insertion sort"),
    ("silicat", "```python\ndef insertion_sort(arr):\n    for i in range(1, len(arr)):\n        key = arr[i]\n        j = i - 1\n        while j >= 0 and arr[j] > key:\n            arr[j + 1] = arr[j]\n            j -= 1\n        arr[j + 1] = key\n    return arr\n```"),
    ("user", "when is insertion sort a good choice?"),
    ("silicat", "It's great for small or nearly-sorted lists: it's O(n) on already-sorted input, stable, in-place, and has low overhead. That's why hybrid sorts like Timsort use insertion sort for small runs."),
])

add_multi([
    ("user", "detect a cycle in a linked list"),
    ("silicat", "```python\ndef has_cycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            return True\n    return False\n```"),
    ("user", "now return the node where the cycle starts"),
    ("silicat", "After they meet, move one pointer to the head and advance both one step at a time:\n\n```python\ndef cycle_start(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow is fast:\n            slow = head\n            while slow is not fast:\n                slow = slow.next\n                fast = fast.next\n            return slow\n    return None\n```"),
])

add_multi([
    ("user", "level order traversal of a tree"),
    ("silicat", "```python\nfrom collections import deque\n\ndef level_order(root):\n    if not root:\n        return []\n    result, q = [], deque([root])\n    while q:\n        node = q.popleft()\n        result.append(node.value)\n        if node.left:\n            q.append(node.left)\n        if node.right:\n            q.append(node.right)\n    return result\n```"),
    ("user", "group the values by level instead of flattening"),
    ("silicat", "Process the queue one full level at a time:\n\n```python\nfrom collections import deque\n\ndef level_order(root):\n    if not root:\n        return []\n    result, q = [], deque([root])\n    while q:\n        level = []\n        for _ in range(len(q)):\n            node = q.popleft()\n            level.append(node.value)\n            if node.left:\n                q.append(node.left)\n            if node.right:\n                q.append(node.right)\n        result.append(level)\n    return result\n```"),
])

add_multi([
    ("user", "max sum subarray of size k"),
    ("silicat", "```python\ndef max_subarray_sum(arr, k):\n    window = sum(arr[:k])\n    best = window\n    for i in range(k, len(arr)):\n        window += arr[i] - arr[i - k]\n        best = max(best, window)\n    return best\n```"),
    ("user", "also return the starting index of that window"),
    ("silicat", "```python\ndef max_subarray_sum(arr, k):\n    window = sum(arr[:k])\n    best, best_start = window, 0\n    for i in range(k, len(arr)):\n        window += arr[i] - arr[i - k]\n        if window > best:\n            best, best_start = window, i - k + 1\n    return best, best_start\n```"),
])

add_multi([
    ("user", "knapsack problem"),
    ("silicat", "```python\ndef knapsack(weights, values, capacity):\n    n = len(weights)\n    dp = [[0] * (capacity + 1) for _ in range(n + 1)]\n    for i in range(1, n + 1):\n        for w in range(capacity + 1):\n            dp[i][w] = dp[i - 1][w]\n            if weights[i - 1] <= w:\n                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])\n    return dp[n][capacity]\n```"),
    ("user", "can you reduce it to a 1D array?"),
    ("silicat", "Yes, iterate the capacity in reverse so each item is used at most once:\n\n```python\ndef knapsack(weights, values, capacity):\n    dp = [0] * (capacity + 1)\n    for i in range(len(weights)):\n        for w in range(capacity, weights[i] - 1, -1):\n            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])\n    return dp[capacity]\n```"),
])

# ---------------------------------------------------------------------------
# BATCH 2 — more variations to reach 350+
# ---------------------------------------------------------------------------
add("nth fibonacci number recursively",
    "```python\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n```")
add("fibonacci with a loop",
    "```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```")
add("fibonacci series up to n terms",
    "```python\ndef fib_series(n):\n    a, b, out = 0, 1, []\n    for _ in range(n):\n        out.append(a)\n        a, b = b, a + b\n    return out\n```")
add("how to write fib in python efficiently",
    "The iterative form is O(n) time and O(1) space:\n\n```python\ndef fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n```")
add("compute factorial iteratively in python",
    "```python\ndef factorial(n):\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n```")
add("factorial with reduce",
    "```python\nfrom functools import reduce\nfrom operator import mul\n\ndef factorial(n):\n    return reduce(mul, range(1, n + 1), 1)\n```")
add("how do I check primality of a big number quickly",
    "For very large numbers, use a probabilistic Miller-Rabin test:\n\n```python\ndef is_prime(n, k=20):\n    if n < 2:\n        return False\n    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):\n        if n % p == 0:\n            return n == p\n    d, r = n - 1, 0\n    while d % 2 == 0:\n        d //= 2; r += 1\n    import random\n    for _ in range(k):\n        a = random.randrange(2, n - 1)\n        x = pow(a, d, n)\n        if x in (1, n - 1):\n            continue\n        for _ in range(r - 1):\n            x = x * x % n\n            if x == n - 1:\n                break\n        else:\n            return False\n    return True\n```")
add("prime factorization in python",
    "```python\ndef prime_factors(n):\n    factors = []\n    d = 2\n    while d * d <= n:\n        while n % d == 0:\n            factors.append(d)\n            n //= d\n        d += 1\n    if n > 1:\n        factors.append(n)\n    return factors\n```")
add("check if a number is prime simple version",
    "```python\ndef is_prime(n):\n    return n > 1 and all(n % i for i in range(2, int(n ** 0.5) + 1))\n```")
add("count primes below n",
    "```python\ndef count_primes(n):\n    if n < 3:\n        return 0\n    sieve = [True] * n\n    sieve[0] = sieve[1] = False\n    for i in range(2, int(n ** 0.5) + 1):\n        if sieve[i]:\n            for j in range(i * i, n, i):\n                sieve[j] = False\n    return sum(sieve)\n```")
add("gcd recursive python",
    "```python\ndef gcd(a, b):\n    return a if b == 0 else gcd(b, a % b)\n```")
add("lcm of a list of numbers",
    "```python\nimport math\nfrom functools import reduce\n\ndef lcm_list(nums):\n    return reduce(lambda a, b: a * b // math.gcd(a, b), nums)\n```")
add("how to sort a list of dictionaries by a field",
    "```python\npeople = [{'name': 'Al', 'age': 30}, {'name': 'Bo', 'age': 25}]\nprint(sorted(people, key=lambda p: p['age']))\n```")
add("sort numbers in place",
    "```python\nnums = [3, 1, 2]\nnums.sort()\nprint(nums)  # [1, 2, 3]\n```")
add("sort a list and keep original indices",
    "```python\nnums = [40, 10, 30]\norder = sorted(range(len(nums)), key=lambda i: nums[i])\nprint(order)  # [1, 2, 0]\n```")
add("stable sort by two keys",
    "Sort by the secondary key first, then the primary, or use a tuple key:\n\n```python\nrecords = [('b', 2), ('a', 2), ('a', 1)]\nprint(sorted(records, key=lambda r: (r[1], r[0])))\n```")
add("shell sort python",
    "```python\ndef shell_sort(arr):\n    gap = len(arr) // 2\n    while gap > 0:\n        for i in range(gap, len(arr)):\n            temp = arr[i]\n            j = i\n            while j >= gap and arr[j - gap] > temp:\n                arr[j] = arr[j - gap]\n                j -= gap\n            arr[j] = temp\n        gap //= 2\n    return arr\n```")
add("binary search leftmost target",
    "```python\nimport bisect\n\ndef search_left(arr, target):\n    i = bisect.bisect_left(arr, target)\n    return i if i < len(arr) and arr[i] == target else -1\n```")
add("search in a rotated sorted array",
    "```python\ndef search(nums, target):\n    lo, hi = 0, len(nums) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if nums[mid] == target:\n            return mid\n        if nums[lo] <= nums[mid]:\n            if nums[lo] <= target < nums[mid]:\n                hi = mid - 1\n            else:\n                lo = mid + 1\n        else:\n            if nums[mid] < target <= nums[hi]:\n                lo = mid + 1\n            else:\n                hi = mid - 1\n    return -1\n```")
add("how to reverse a list in place",
    "```python\nnums = [1, 2, 3, 4]\nnums.reverse()\nprint(nums)  # [4, 3, 2, 1]\n```")
add("reverse only part of a list",
    "```python\nnums = [1, 2, 3, 4, 5]\nnums[1:4] = nums[1:4][::-1]\nprint(nums)  # [1, 4, 3, 2, 5]\n```")
add("check palindrome recursively",
    "```python\ndef is_palindrome(s):\n    if len(s) <= 1:\n        return True\n    return s[0] == s[-1] and is_palindrome(s[1:-1])\n```")
add("longest palindrome length in a string",
    "```python\nfrom collections import Counter\n\ndef longest_palindrome(s):\n    counts = Counter(s)\n    length = sum(c // 2 * 2 for c in counts.values())\n    if any(c % 2 for c in counts.values()):\n        length += 1\n    return length\n```")
add("are these two phrases anagrams",
    "```python\nfrom collections import Counter\n\ndef is_anagram(a, b):\n    clean = lambda s: Counter(c.lower() for c in s if c.isalpha())\n    return clean(a) == clean(b)\n```")
add("fizzbuzz with list comprehension",
    "```python\nprint(['FizzBuzz' if i % 15 == 0 else 'Fizz' if i % 3 == 0 else 'Buzz' if i % 5 == 0 else i for i in range(1, 16)])\n```")
add("three sum problem",
    "```python\ndef three_sum(nums):\n    nums.sort()\n    res = []\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i - 1]:\n            continue\n        lo, hi = i + 1, len(nums) - 1\n        while lo < hi:\n            total = nums[i] + nums[lo] + nums[hi]\n            if total < 0:\n                lo += 1\n            elif total > 0:\n                hi -= 1\n            else:\n                res.append([nums[i], nums[lo], nums[hi]])\n                while lo < hi and nums[lo] == nums[lo + 1]:\n                    lo += 1\n                while lo < hi and nums[hi] == nums[hi - 1]:\n                    hi -= 1\n                lo += 1; hi -= 1\n    return res\n```")
add("count distinct substrings using a set",
    "```python\ndef distinct_substrings(s):\n    subs = set()\n    for i in range(len(s)):\n        for j in range(i + 1, len(s) + 1):\n            subs.add(s[i:j])\n    return len(subs)\n```")
add("fixed size sliding window average",
    "```python\ndef window_averages(arr, k):\n    window = sum(arr[:k])\n    result = [window / k]\n    for i in range(k, len(arr)):\n        window += arr[i] - arr[i - k]\n        result.append(window / k)\n    return result\n```")
add("evaluate reverse polish notation with a stack",
    "```python\ndef eval_rpn(tokens):\n    stack = []\n    ops = {'+': lambda a, b: a + b, '-': lambda a, b: a - b,\n           '*': lambda a, b: a * b, '/': lambda a, b: int(a / b)}\n    for t in tokens:\n        if t in ops:\n            b = stack.pop(); a = stack.pop()\n            stack.append(ops[t](a, b))\n        else:\n            stack.append(int(t))\n    return stack[0]\n```")
add("implement a circular queue",
    "```python\nclass CircularQueue:\n    def __init__(self, k):\n        self.q = [None] * k\n        self.size = k\n        self.head = self.count = 0\n    def enqueue(self, x):\n        if self.count == self.size:\n            return False\n        self.q[(self.head + self.count) % self.size] = x\n        self.count += 1\n        return True\n    def dequeue(self):\n        if self.count == 0:\n            return None\n        x = self.q[self.head]\n        self.head = (self.head + 1) % self.size\n        self.count -= 1\n        return x\n```")
add("doubly linked list node",
    "```python\nclass Node:\n    def __init__(self, value):\n        self.value = value\n        self.prev = None\n        self.next = None\n```")
add("merge two sorted linked lists",
    "```python\ndef merge_two_lists(a, b):\n    dummy = tail = Node(0)\n    while a and b:\n        if a.value <= b.value:\n            tail.next = a; a = a.next\n        else:\n            tail.next = b; b = b.next\n        tail = tail.next\n    tail.next = a or b\n    return dummy.next\n```")
add("remove nth node from end of list",
    "```python\ndef remove_nth_from_end(head, n):\n    dummy = Node(0)\n    dummy.next = head\n    fast = slow = dummy\n    for _ in range(n):\n        fast = fast.next\n    while fast.next:\n        fast = fast.next\n        slow = slow.next\n    slow.next = slow.next.next\n    return dummy.next\n```")
add("validate a binary search tree",
    "```python\ndef is_valid_bst(root, low=float('-inf'), high=float('inf')):\n    if not root:\n        return True\n    if not (low < root.value < high):\n        return False\n    return (is_valid_bst(root.left, low, root.value) and\n            is_valid_bst(root.right, root.value, high))\n```")
add("diameter of a binary tree",
    "```python\ndef diameter(root):\n    best = 0\n    def depth(node):\n        nonlocal best\n        if not node:\n            return 0\n        l = depth(node.left)\n        r = depth(node.right)\n        best = max(best, l + r)\n        return 1 + max(l, r)\n    depth(root)\n    return best\n```")
add("sum of all nodes in a binary tree",
    "```python\ndef tree_sum(root):\n    if not root:\n        return 0\n    return root.value + tree_sum(root.left) + tree_sum(root.right)\n```")
add("maximum depth of binary tree",
    "```python\ndef max_depth(root):\n    if not root:\n        return 0\n    return 1 + max(max_depth(root.left), max_depth(root.right))\n```")
add("path sum in a binary tree",
    "```python\ndef has_path_sum(root, target):\n    if not root:\n        return False\n    if not root.left and not root.right:\n        return target == root.value\n    rem = target - root.value\n    return has_path_sum(root.left, rem) or has_path_sum(root.right, rem)\n```")
add("connected components in an undirected graph",
    "```python\ndef count_components(graph):\n    visited = set()\n    def dfs(node):\n        visited.add(node)\n        for nbr in graph[node]:\n            if nbr not in visited:\n                dfs(nbr)\n    count = 0\n    for node in graph:\n        if node not in visited:\n            count += 1\n            dfs(node)\n    return count\n```")
add("check if path exists between two nodes",
    "```python\ndef path_exists(graph, start, end):\n    stack = [start]\n    visited = set()\n    while stack:\n        node = stack.pop()\n        if node == end:\n            return True\n        if node not in visited:\n            visited.add(node)\n            stack.extend(graph[node])\n    return False\n```")
add("bipartite graph check",
    "```python\nfrom collections import deque\n\ndef is_bipartite(graph):\n    color = {}\n    for start in graph:\n        if start in color:\n            continue\n        color[start] = 0\n        q = deque([start])\n        while q:\n            node = q.popleft()\n            for nbr in graph[node]:\n                if nbr not in color:\n                    color[nbr] = color[node] ^ 1\n                    q.append(nbr)\n                elif color[nbr] == color[node]:\n                    return False\n    return True\n```")
add("number of ways to climb stairs memoized",
    "```python\nfrom functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef climb(n):\n    if n <= 2:\n        return n\n    return climb(n - 1) + climb(n - 2)\n```")
add("minimum path sum in a grid dp",
    "```python\ndef min_path_sum(grid):\n    rows, cols = len(grid), len(grid[0])\n    for r in range(rows):\n        for c in range(cols):\n            if r == 0 and c == 0:\n                continue\n            up = grid[r - 1][c] if r > 0 else float('inf')\n            left = grid[r][c - 1] if c > 0 else float('inf')\n            grid[r][c] += min(up, left)\n    return grid[-1][-1]\n```")
add("unique paths in a grid dp",
    "```python\ndef unique_paths(m, n):\n    dp = [[1] * n for _ in range(m)]\n    for r in range(1, m):\n        for c in range(1, n):\n            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]\n    return dp[m - 1][n - 1]\n```")
add("partition equal subset sum dp",
    "```python\ndef can_partition(nums):\n    total = sum(nums)\n    if total % 2:\n        return False\n    target = total // 2\n    dp = {0}\n    for n in nums:\n        dp |= {s + n for s in dp if s + n <= target}\n    return target in dp\n```")
add("word break dp",
    "```python\ndef word_break(s, words):\n    word_set = set(words)\n    dp = [False] * (len(s) + 1)\n    dp[0] = True\n    for i in range(1, len(s) + 1):\n        for j in range(i):\n            if dp[j] and s[j:i] in word_set:\n                dp[i] = True\n                break\n    return dp[len(s)]\n```")
add("count frequency of words from a file",
    "```python\nfrom collections import Counter\n\ndef word_freq(path):\n    with open(path) as f:\n        return Counter(f.read().split())\n```")
add("invert a dictionary",
    "```python\nd = {'a': 1, 'b': 2}\nprint({v: k for k, v in d.items()})  # {1: 'a', 2: 'b'}\n```")
add("merge two dictionaries",
    "```python\na = {'x': 1}\nb = {'y': 2}\nprint({**a, **b})  # {'x': 1, 'y': 2}\n```")
add("count anagram groups",
    "```python\nfrom collections import defaultdict\n\ndef anagram_groups(words):\n    groups = defaultdict(list)\n    for w in words:\n        groups[''.join(sorted(w))].append(w)\n    return len(groups)\n```")
add("symmetric difference of two sets",
    "```python\na = {1, 2, 3}\nb = {2, 3, 4}\nprint(a ^ b)  # {1, 4}\n```")
add("check if one set is a subset of another",
    "```python\na = {1, 2}\nb = {1, 2, 3}\nprint(a.issubset(b))  # True\n```")
add("union of multiple lists into a set",
    "```python\nlists = [[1, 2], [2, 3], [3, 4]]\nprint(set().union(*lists))  # {1, 2, 3, 4}\n```")
add("top k frequent elements",
    "```python\nfrom collections import Counter\n\ndef top_k_frequent(nums, k):\n    return [item for item, _ in Counter(nums).most_common(k)]\n```")
add("heapify a list",
    "```python\nimport heapq\n\nnums = [5, 3, 8, 1]\nheapq.heapify(nums)\nprint(nums[0])  # smallest element\n```")
add("running median with two heaps",
    "```python\nimport heapq\n\nclass MedianFinder:\n    def __init__(self):\n        self.lo = []  # max-heap (negated)\n        self.hi = []  # min-heap\n    def add(self, num):\n        heapq.heappush(self.lo, -num)\n        heapq.heappush(self.hi, -heapq.heappop(self.lo))\n        if len(self.hi) > len(self.lo):\n            heapq.heappush(self.lo, -heapq.heappop(self.hi))\n    def median(self):\n        if len(self.lo) > len(self.hi):\n            return -self.lo[0]\n        return (-self.lo[0] + self.hi[0]) / 2\n```")
add("sort dict items by value then key",
    "```python\nd = {'b': 2, 'a': 2, 'c': 1}\nprint(sorted(d.items(), key=lambda kv: (kv[1], kv[0])))\n```")
add("get the key with the maximum value in a dict",
    "```python\nd = {'a': 3, 'b': 7, 'c': 5}\nprint(max(d, key=d.get))  # 'b'\n```")
add("sum values of a dictionary",
    "```python\nd = {'a': 1, 'b': 2, 'c': 3}\nprint(sum(d.values()))  # 6\n```")
add("recursion to count down",
    "```python\ndef countdown(n):\n    if n <= 0:\n        print('done')\n        return\n    print(n)\n    countdown(n - 1)\n```")
add("recursive string length",
    "```python\ndef length(s):\n    if not s:\n        return 0\n    return 1 + length(s[1:])\n```")
add("ackermann function",
    "```python\ndef ackermann(m, n):\n    if m == 0:\n        return n + 1\n    if n == 0:\n        return ackermann(m - 1, 1)\n    return ackermann(m - 1, ackermann(m, n - 1))\n```")
add("generate combinations with replacement",
    "```python\nfrom itertools import combinations_with_replacement\n\nprint(list(combinations_with_replacement([1, 2], 2)))\n```")
add("n queens count solutions",
    "```python\ndef total_n_queens(n):\n    def solve(row, cols, diag1, diag2):\n        if row == n:\n            return 1\n        count = 0\n        for col in range(n):\n            if col in cols or (row - col) in diag1 or (row + col) in diag2:\n                continue\n            count += solve(row + 1, cols | {col}, diag1 | {row - col}, diag2 | {row + col})\n        return count\n    return solve(0, set(), set(), set())\n```")
add("binary to decimal conversion",
    "```python\nprint(int('1010', 2))  # 10\n```")
add("decimal to binary conversion",
    "```python\nprint(format(10, 'b'))  # '1010'\n```")
add("hamming distance between two integers",
    "```python\ndef hamming_distance(a, b):\n    return bin(a ^ b).count('1')\n```")
add("single number that appears once using xor",
    "```python\nfrom functools import reduce\nfrom operator import xor\n\ndef single_number(nums):\n    return reduce(xor, nums)\n```")
add("reverse bits of a 32-bit integer",
    "```python\ndef reverse_bits(n):\n    result = 0\n    for _ in range(32):\n        result = (result << 1) | (n & 1)\n        n >>= 1\n    return result\n```")
add("gray code sequence",
    "```python\ndef gray_code(n):\n    return [i ^ (i >> 1) for i in range(2 ** n)]\n```")
add("check armstrong number",
    "```python\ndef is_armstrong(n):\n    digits = str(n)\n    p = len(digits)\n    return n == sum(int(d) ** p for d in digits)\n```")
add("collatz sequence length",
    "```python\ndef collatz_length(n):\n    steps = 0\n    while n != 1:\n        n = n // 2 if n % 2 == 0 else 3 * n + 1\n        steps += 1\n    return steps\n```")
add("greatest product of three numbers",
    "```python\ndef max_product_three(nums):\n    nums.sort()\n    return max(nums[-1] * nums[-2] * nums[-3], nums[0] * nums[1] * nums[-1])\n```")
add("find pair with smallest difference",
    "```python\ndef min_diff_pair(nums):\n    nums.sort()\n    return min((nums[i + 1] - nums[i], (nums[i], nums[i + 1])) for i in range(len(nums) - 1))[1]\n```")
add("two pointer remove duplicates from sorted array",
    "```python\ndef remove_duplicates(nums):\n    if not nums:\n        return 0\n    k = 1\n    for i in range(1, len(nums)):\n        if nums[i] != nums[k - 1]:\n            nums[k] = nums[i]\n            k += 1\n    return k\n```")
add("container with most water",
    "```python\ndef max_area(height):\n    left, right = 0, len(height) - 1\n    best = 0\n    while left < right:\n        best = max(best, min(height[left], height[right]) * (right - left))\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return best\n```")
add("group consecutive numbers into ranges",
    "```python\ndef summary_ranges(nums):\n    ranges, i = [], 0\n    while i < len(nums):\n        start = nums[i]\n        while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:\n            i += 1\n        ranges.append(f'{start}->{nums[i]}' if start != nums[i] else str(start))\n        i += 1\n    return ranges\n```")
add("count inversions in an array",
    "```python\ndef count_inversions(arr):\n    def sort_count(a):\n        if len(a) <= 1:\n            return a, 0\n        mid = len(a) // 2\n        left, x = sort_count(a[:mid])\n        right, y = sort_count(a[mid:])\n        merged, z, i, j = [], 0, 0, 0\n        while i < len(left) and j < len(right):\n            if left[i] <= right[j]:\n                merged.append(left[i]); i += 1\n            else:\n                merged.append(right[j]); j += 1\n                z += len(left) - i\n        merged += left[i:] + right[j:]\n        return merged, x + y + z\n    return sort_count(arr)[1]\n```")
add("first missing positive integer",
    "```python\ndef first_missing_positive(nums):\n    s = set(nums)\n    i = 1\n    while i in s:\n        i += 1\n    return i\n```")
add("longest consecutive sequence",
    "```python\ndef longest_consecutive(nums):\n    s = set(nums)\n    best = 0\n    for n in s:\n        if n - 1 not in s:\n            length = 1\n            while n + length in s:\n                length += 1\n            best = max(best, length)\n    return best\n```")
add("subarray sum equals k count",
    "```python\nfrom collections import defaultdict\n\ndef subarray_sum(nums, k):\n    prefix = defaultdict(int)\n    prefix[0] = 1\n    total = count = 0\n    for n in nums:\n        total += n\n        count += prefix[total - k]\n        prefix[total] += 1\n    return count\n```")
add("flatten a dictionary",
    "```python\ndef flatten(d, parent='', sep='.'):\n    items = {}\n    for k, v in d.items():\n        key = f'{parent}{sep}{k}' if parent else k\n        if isinstance(v, dict):\n            items.update(flatten(v, key, sep))\n        else:\n            items[key] = v\n    return items\n```")
add("binary search to find square root",
    "```python\ndef int_sqrt(n):\n    lo, hi = 0, n\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if mid * mid <= n:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return hi\n```")
add("longest word in a sentence",
    "```python\ndef longest_word(sentence):\n    return max(sentence.split(), key=len)\n```")
add("capitalize first letter of each word manually",
    "```python\ndef capitalize_words(s):\n    return ' '.join(w[:1].upper() + w[1:] for w in s.split())\n```")
add("check if two trees are identical",
    "```python\ndef is_same_tree(p, q):\n    if not p and not q:\n        return True\n    if not p or not q or p.value != q.value:\n        return False\n    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)\n```")
add("serialize a binary tree to a list",
    "```python\nfrom collections import deque\n\ndef serialize(root):\n    out, q = [], deque([root])\n    while q:\n        node = q.popleft()\n        if node:\n            out.append(node.value)\n            q.append(node.left)\n            q.append(node.right)\n        else:\n            out.append(None)\n    return out\n```")
add("count leaf nodes in a tree",
    "```python\ndef count_leaves(root):\n    if not root:\n        return 0\n    if not root.left and not root.right:\n        return 1\n    return count_leaves(root.left) + count_leaves(root.right)\n```")
add("dijkstra return path",
    "```python\nimport heapq\n\ndef dijkstra_path(graph, start, end):\n    pq = [(0, start, [start])]\n    seen = set()\n    while pq:\n        cost, node, path = heapq.heappop(pq)\n        if node == end:\n            return path, cost\n        if node in seen:\n            continue\n        seen.add(node)\n        for nbr, w in graph[node]:\n            if nbr not in seen:\n                heapq.heappush(pq, (cost + w, nbr, path + [nbr]))\n    return None, float('inf')\n```")
add("number of provinces union find",
    "```python\ndef find_circle_num(is_connected):\n    n = len(is_connected)\n    parent = list(range(n))\n    def find(x):\n        while parent[x] != x:\n            parent[x] = parent[parent[x]]\n            x = parent[x]\n        return x\n    for i in range(n):\n        for j in range(i + 1, n):\n            if is_connected[i][j]:\n                parent[find(i)] = find(j)\n    return len({find(i) for i in range(n)})\n```")
add("union find data structure",
    "```python\nclass UnionFind:\n    def __init__(self, n):\n        self.parent = list(range(n))\n        self.rank = [0] * n\n    def find(self, x):\n        if self.parent[x] != x:\n            self.parent[x] = self.find(self.parent[x])\n        return self.parent[x]\n    def union(self, a, b):\n        ra, rb = self.find(a), self.find(b)\n        if ra == rb:\n            return False\n        if self.rank[ra] < self.rank[rb]:\n            ra, rb = rb, ra\n        self.parent[rb] = ra\n        if self.rank[ra] == self.rank[rb]:\n            self.rank[ra] += 1\n        return True\n```")
add("trie data structure python",
    "```python\nclass Trie:\n    def __init__(self):\n        self.root = {}\n    def insert(self, word):\n        node = self.root\n        for ch in word:\n            node = node.setdefault(ch, {})\n        node['#'] = True\n    def search(self, word):\n        node = self.root\n        for ch in word:\n            if ch not in node:\n                return False\n            node = node[ch]\n        return '#' in node\n```")
add("count ways to decode a digit string dp",
    "```python\ndef num_decodings(s):\n    if not s or s[0] == '0':\n        return 0\n    prev, cur = 1, 1\n    for i in range(1, len(s)):\n        tmp = 0\n        if s[i] != '0':\n            tmp += cur\n        if 10 <= int(s[i - 1:i + 1]) <= 26:\n            tmp += prev\n        prev, cur = cur, tmp\n    return cur\n```")
add("maximum product subarray",
    "```python\ndef max_product(nums):\n    best = cur_max = cur_min = nums[0]\n    for n in nums[1:]:\n        candidates = (n, cur_max * n, cur_min * n)\n        cur_max = max(candidates)\n        cur_min = min(candidates)\n        best = max(best, cur_max)\n    return best\n```")
add("rotate list right by k recursion-free",
    "```python\nfrom collections import deque\n\ndef rotate(nums, k):\n    d = deque(nums)\n    d.rotate(k)\n    return list(d)\n```")
add("interleave two lists",
    "```python\ndef interleave(a, b):\n    result = []\n    for x, y in zip(a, b):\n        result.append(x)\n        result.append(y)\n    return result\n```")
add("frequency of each digit in a number",
    "```python\nfrom collections import Counter\n\ndef digit_freq(n):\n    return Counter(str(abs(n)))\n```")
add("check if a string has all unique characters",
    "```python\ndef all_unique(s):\n    return len(set(s)) == len(s)\n```")
add("find duplicates in a list with a set",
    "```python\ndef find_duplicates(nums):\n    seen, dups = set(), set()\n    for n in nums:\n        if n in seen:\n            dups.add(n)\n        seen.add(n)\n    return list(dups)\n```")

# A few more multi-turns
add_multi([
    ("user", "topological sort"),
    ("silicat", "```python\nfrom collections import deque, defaultdict\n\ndef topo_sort(graph):\n    indeg = defaultdict(int)\n    for u in graph:\n        for v in graph[u]:\n            indeg[v] += 1\n    q = deque([u for u in graph if indeg[u] == 0])\n    order = []\n    while q:\n        u = q.popleft()\n        order.append(u)\n        for v in graph[u]:\n            indeg[v] -= 1\n            if indeg[v] == 0:\n                q.append(v)\n    return order\n```"),
    ("user", "how do I detect if there's a cycle so sorting fails?"),
    ("silicat", "If the result doesn't include every node, there was a cycle:\n\n```python\nif len(order) != len(graph):\n    raise ValueError('graph has a cycle')\n```"),
])
add_multi([
    ("user", "heap sort"),
    ("silicat", "```python\nimport heapq\n\ndef heap_sort(arr):\n    heapq.heapify(arr)\n    return [heapq.heappop(arr) for _ in range(len(arr))]\n```"),
    ("user", "is heap sort stable?"),
    ("silicat", "No. Heap sort is not stable because sift operations can reorder equal elements relative to each other. If you need stability, use merge sort or Python's built-in `sorted`, which is Timsort and stable."),
])
add_multi([
    ("user", "count vowels in a string"),
    ("silicat", "```python\ndef count_vowels(s):\n    return sum(1 for ch in s.lower() if ch in 'aeiou')\n```"),
    ("user", "return a breakdown of each vowel's count"),
    ("silicat", "```python\nfrom collections import Counter\n\ndef vowel_breakdown(s):\n    return {v: c for v, c in Counter(s.lower()).items() if v in 'aeiou'}\n```"),
])
add_multi([
    ("user", "dijkstra"),
    ("silicat", "```python\nimport heapq\n\ndef dijkstra(graph, start):\n    dist = {start: 0}\n    pq = [(0, start)]\n    while pq:\n        d, u = heapq.heappop(pq)\n        if d > dist.get(u, float('inf')):\n            continue\n        for v, w in graph[u]:\n            nd = d + w\n            if nd < dist.get(v, float('inf')):\n                dist[v] = nd\n                heapq.heappush(pq, (nd, v))\n    return dist\n```"),
    ("user", "does it work with negative edge weights?"),
    ("silicat", "No. Dijkstra assumes non-negative weights; with negative edges it can finalize a node's distance too early and give wrong answers. Use Bellman-Ford for graphs with negative edges (it also detects negative cycles)."),
])
add_multi([
    ("user", "kadane's algorithm for max subarray"),
    ("silicat", "```python\ndef max_subarray(nums):\n    best = cur = nums[0]\n    for x in nums[1:]:\n        cur = max(x, cur + x)\n        best = max(best, cur)\n    return best\n```"),
    ("user", "also return the actual subarray"),
    ("silicat", "Track the start and end indices as you go:\n\n```python\ndef max_subarray(nums):\n    best = cur = nums[0]\n    start = end = temp = 0\n    for i in range(1, len(nums)):\n        if nums[i] > cur + nums[i]:\n            cur = nums[i]\n            temp = i\n        else:\n            cur += nums[i]\n        if cur > best:\n            best = cur\n            start, end = temp, i\n    return best, nums[start:end + 1]\n```"),
])
add_multi([
    ("user", "remove nth node from end of a linked list"),
    ("silicat", "```python\ndef remove_nth_from_end(head, n):\n    dummy = Node(0)\n    dummy.next = head\n    fast = slow = dummy\n    for _ in range(n):\n        fast = fast.next\n    while fast.next:\n        fast = fast.next\n        slow = slow.next\n    slow.next = slow.next.next\n    return dummy.next\n```"),
    ("user", "why use a dummy node?"),
    ("silicat", "The dummy node handles the edge case where you need to remove the head itself. Without it, `slow` could never sit before the head, so you'd need special-case logic. The dummy gives a uniform node-before-target to splice from."),
])

# Write out
out_path = "/home/user/Silicat/data/synth/algorithms.jsonl"
with open(out_path, "w") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print(f"Wrote {len(examples)} examples to {out_path}")
