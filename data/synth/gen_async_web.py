import json

examples = []

def add(user, silicat):
    examples.append({"messages": [
        {"role": "user", "content": user},
        {"role": "silicat", "content": silicat},
    ]})

def addmulti(turns):
    # turns: list of (user, silicat)
    msgs = []
    for u, s in turns:
        msgs.append({"role": "user", "content": u})
        msgs.append({"role": "silicat", "content": s})
    examples.append({"messages": msgs})


# ---------------------------------------------------------------------------
# ASYNCIO BASICS (many phrasing variations)
# ---------------------------------------------------------------------------

add(
    "How do I run a basic async function in Python?",
    "Use `asyncio.run()` to start the event loop and run a coroutine:\n\n```python\nimport asyncio\n\nasync def main():\n    print(\"hello\")\n    await asyncio.sleep(1)\n    print(\"world\")\n\nasyncio.run(main())\n```\n\n`asyncio.run()` creates a new event loop, runs the coroutine until it finishes, and closes the loop."
)

add(
    "Show me a minimal asyncio example.",
    "```python\nimport asyncio\n\nasync def greet():\n    await asyncio.sleep(0.5)\n    return \"done\"\n\nresult = asyncio.run(greet())\nprint(result)\n```"
)

add(
    "What does async/await actually do?",
    "`async def` defines a coroutine, and `await` suspends the coroutine until the awaited operation completes, letting the event loop run other tasks meanwhile:\n\n```python\nimport asyncio\n\nasync def fetch_data():\n    print(\"start\")\n    await asyncio.sleep(2)  # yields control back to the loop\n    print(\"done\")\n    return 42\n\nasyncio.run(fetch_data())\n```\n\nawait doesn't block the whole program; it only pauses that coroutine."
)

add(
    "How can I sleep without blocking in asyncio?",
    "Use `asyncio.sleep()` instead of `time.sleep()`:\n\n```python\nimport asyncio\n\nasync def worker():\n    print(\"working\")\n    await asyncio.sleep(3)  # non-blocking\n    print(\"finished\")\n\nasyncio.run(worker())\n```\n\n`time.sleep()` blocks the entire event loop; `asyncio.sleep()` lets other coroutines run."
)

add(
    "Run two coroutines at the same time in asyncio.",
    "Use `asyncio.gather()` to run them concurrently:\n\n```python\nimport asyncio\n\nasync def task(name, delay):\n    await asyncio.sleep(delay)\n    return f\"{name} after {delay}s\"\n\nasync def main():\n    results = await asyncio.gather(\n        task(\"A\", 1),\n        task(\"B\", 2),\n    )\n    print(results)\n\nasyncio.run(main())\n```"
)

add(
    "How do I use asyncio.gather to collect results?",
    "```python\nimport asyncio\n\nasync def square(n):\n    await asyncio.sleep(0.1)\n    return n * n\n\nasync def main():\n    results = await asyncio.gather(*(square(i) for i in range(5)))\n    print(results)  # [0, 1, 4, 9, 16]\n\nasyncio.run(main())\n```\n\n`gather` returns results in the same order as the input coroutines."
)

add(
    "What's the difference between create_task and gather?",
    "`asyncio.create_task()` schedules a coroutine to run in the background and returns a Task you can await later; `gather()` runs several awaitables concurrently and waits for all of them at once.\n\n```python\nimport asyncio\n\nasync def work(n):\n    await asyncio.sleep(n)\n    return n\n\nasync def main():\n    # create_task: schedule now, await later\n    t1 = asyncio.create_task(work(1))\n    t2 = asyncio.create_task(work(2))\n    print(await t1, await t2)\n\n    # gather: run and wait together\n    print(await asyncio.gather(work(1), work(2)))\n\nasyncio.run(main())\n```"
)

add(
    "How do I schedule a coroutine to run in the background?",
    "Use `asyncio.create_task()`:\n\n```python\nimport asyncio\n\nasync def background():\n    await asyncio.sleep(1)\n    print(\"background done\")\n\nasync def main():\n    task = asyncio.create_task(background())\n    print(\"doing other work\")\n    await task  # wait for it to finish\n\nasyncio.run(main())\n```"
)

add(
    "Can you explain coroutines vs tasks in asyncio?",
    "A coroutine is what you get from calling an `async def` function; it doesn't run until awaited. A Task wraps a coroutine and schedules it on the event loop so it starts running immediately in the background.\n\n```python\nimport asyncio\n\nasync def job():\n    await asyncio.sleep(1)\n    return \"ok\"\n\nasync def main():\n    coro = job()                     # not running yet\n    task = asyncio.create_task(coro) # now scheduled and running\n    return await task\n\nasyncio.run(main())\n```"
)

add(
    "I want to fire off many async tasks and wait for them all.",
    "```python\nimport asyncio\n\nasync def process(item):\n    await asyncio.sleep(0.2)\n    return item * 2\n\nasync def main():\n    items = list(range(10))\n    tasks = [asyncio.create_task(process(i)) for i in items]\n    results = await asyncio.gather(*tasks)\n    print(results)\n\nasyncio.run(main())\n```"
)

add(
    "How do I add a timeout to an async operation?",
    "Use `asyncio.wait_for()`:\n\n```python\nimport asyncio\n\nasync def slow():\n    await asyncio.sleep(10)\n    return \"done\"\n\nasync def main():\n    try:\n        result = await asyncio.wait_for(slow(), timeout=2.0)\n    except asyncio.TimeoutError:\n        print(\"timed out\")\n\nasyncio.run(main())\n```"
)

add(
    "Use asyncio.timeout context manager.",
    "Python 3.11+ has `asyncio.timeout()` as a context manager:\n\n```python\nimport asyncio\n\nasync def slow():\n    await asyncio.sleep(10)\n\nasync def main():\n    try:\n        async with asyncio.timeout(2):\n            await slow()\n    except asyncio.TimeoutError:\n        print(\"operation timed out\")\n\nasyncio.run(main())\n```"
)

add(
    "How do I limit concurrency with a semaphore in asyncio?",
    "```python\nimport asyncio\n\nasync def fetch(sem, n):\n    async with sem:\n        print(f\"start {n}\")\n        await asyncio.sleep(1)\n        print(f\"end {n}\")\n        return n\n\nasync def main():\n    sem = asyncio.Semaphore(3)  # at most 3 at once\n    await asyncio.gather(*(fetch(sem, i) for i in range(10)))\n\nasyncio.run(main())\n```\n\nThe semaphore caps how many coroutines run inside the `async with` block simultaneously."
)

add(
    "Explain asyncio.Lock with an example.",
    "An `asyncio.Lock` ensures only one coroutine enters a critical section at a time:\n\n```python\nimport asyncio\n\ncounter = 0\nlock = asyncio.Lock()\n\nasync def increment():\n    global counter\n    async with lock:\n        tmp = counter\n        await asyncio.sleep(0.01)\n        counter = tmp + 1\n\nasync def main():\n    await asyncio.gather(*(increment() for _ in range(100)))\n    print(counter)  # 100\n\nasyncio.run(main())\n```"
)

add(
    "How do I use an asyncio.Event?",
    "An Event lets coroutines wait until something signals them:\n\n```python\nimport asyncio\n\nasync def waiter(event):\n    print(\"waiting\")\n    await event.wait()\n    print(\"go!\")\n\nasync def main():\n    event = asyncio.Event()\n    task = asyncio.create_task(waiter(event))\n    await asyncio.sleep(1)\n    event.set()  # wake up the waiter\n    await task\n\nasyncio.run(main())\n```"
)

add(
    "Producer/consumer with asyncio.Queue please.",
    "```python\nimport asyncio\n\nasync def producer(queue):\n    for i in range(5):\n        await asyncio.sleep(0.1)\n        await queue.put(i)\n    await queue.put(None)  # sentinel\n\nasync def consumer(queue):\n    while True:\n        item = await queue.get()\n        if item is None:\n            break\n        print(\"consumed\", item)\n\nasync def main():\n    queue = asyncio.Queue()\n    await asyncio.gather(producer(queue), consumer(queue))\n\nasyncio.run(main())\n```"
)

add(
    "How can I run a blocking function inside async code?",
    "Offload it to a thread with `asyncio.to_thread()` so it doesn't block the event loop:\n\n```python\nimport asyncio\nimport time\n\ndef blocking_io():\n    time.sleep(2)  # blocking\n    return \"done\"\n\nasync def main():\n    result = await asyncio.to_thread(blocking_io)\n    print(result)\n\nasyncio.run(main())\n```"
)

add(
    "What is asyncio.as_completed used for?",
    "It yields awaitables as they finish, so you can process results in completion order rather than input order:\n\n```python\nimport asyncio\n\nasync def work(n):\n    await asyncio.sleep(n)\n    return n\n\nasync def main():\n    coros = [work(3), work(1), work(2)]\n    for fut in asyncio.as_completed(coros):\n        result = await fut\n        print(\"finished\", result)\n\nasyncio.run(main())\n```"
)

add(
    "How do I cancel an asyncio task?",
    "```python\nimport asyncio\n\nasync def long_task():\n    try:\n        await asyncio.sleep(100)\n    except asyncio.CancelledError:\n        print(\"cancelled, cleaning up\")\n        raise\n\nasync def main():\n    task = asyncio.create_task(long_task())\n    await asyncio.sleep(1)\n    task.cancel()\n    try:\n        await task\n    except asyncio.CancelledError:\n        print(\"task was cancelled\")\n\nasyncio.run(main())\n```"
)

add(
    "Show me asyncio.TaskGroup from Python 3.11.",
    "`TaskGroup` is the modern structured-concurrency way to run tasks; if any task fails, the rest are cancelled:\n\n```python\nimport asyncio\n\nasync def work(n):\n    await asyncio.sleep(n)\n    return n\n\nasync def main():\n    async with asyncio.TaskGroup() as tg:\n        t1 = tg.create_task(work(1))\n        t2 = tg.create_task(work(2))\n    print(t1.result(), t2.result())\n\nasyncio.run(main())\n```"
)

add(
    "How do I gather but not stop on the first error?",
    "Pass `return_exceptions=True` so exceptions come back as results instead of propagating:\n\n```python\nimport asyncio\n\nasync def maybe_fail(n):\n    if n == 2:\n        raise ValueError(\"boom\")\n    await asyncio.sleep(0.1)\n    return n\n\nasync def main():\n    results = await asyncio.gather(\n        *(maybe_fail(i) for i in range(4)),\n        return_exceptions=True,\n    )\n    print(results)  # [0, 1, ValueError('boom'), 3]\n\nasyncio.run(main())\n```"
)

add(
    "Run a coroutine periodically every few seconds.",
    "```python\nimport asyncio\n\nasync def tick():\n    print(\"tick\")\n\nasync def main():\n    for _ in range(5):\n        await tick()\n        await asyncio.sleep(2)\n\nasyncio.run(main())\n```"
)

# ---------------------------------------------------------------------------
# ASYNC GENERATORS / GENERATORS
# ---------------------------------------------------------------------------

add(
    "What's the difference between a generator and an async generator?",
    "A generator uses `yield` and is iterated with a normal `for`; an async generator uses `yield` inside an `async def` and is iterated with `async for`, allowing `await` between yields.\n\n```python\nimport asyncio\n\ndef sync_gen():\n    for i in range(3):\n        yield i\n\nasync def async_gen():\n    for i in range(3):\n        await asyncio.sleep(0.1)\n        yield i\n\nasync def main():\n    async for x in async_gen():\n        print(x)\n\nlist(sync_gen())\nasyncio.run(main())\n```"
)

add(
    "Write a simple generator function.",
    "```python\ndef countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nfor x in countdown(3):\n    print(x)  # 3, 2, 1\n```"
)

add(
    "How do I make an async generator?",
    "```python\nimport asyncio\n\nasync def stream_numbers(limit):\n    for i in range(limit):\n        await asyncio.sleep(0.2)\n        yield i\n\nasync def main():\n    async for n in stream_numbers(5):\n        print(n)\n\nasyncio.run(main())\n```"
)

add(
    "Explain yield in Python.",
    "`yield` turns a function into a generator: it produces a value and pauses, resuming where it left off on the next iteration. This makes generators lazy and memory-efficient.\n\n```python\ndef fib():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\ngen = fib()\nprint([next(gen) for _ in range(6)])  # [0, 1, 1, 2, 3, 5]\n```"
)

add(
    "How do I collect all items from an async generator into a list?",
    "```python\nimport asyncio\n\nasync def gen():\n    for i in range(5):\n        await asyncio.sleep(0.05)\n        yield i\n\nasync def main():\n    items = [x async for x in gen()]  # async comprehension\n    print(items)\n\nasyncio.run(main())\n```"
)

# ---------------------------------------------------------------------------
# REQUESTS (8+ variations)
# ---------------------------------------------------------------------------

add(
    "How do I make a GET request in Python?",
    "Use the `requests` library:\n\n```python\nimport requests\n\nresponse = requests.get(\"https://api.github.com\")\nprint(response.status_code)\nprint(response.json())\n```"
)

add(
    "Fetch a URL and print the response text.",
    "```python\nimport requests\n\nresp = requests.get(\"https://example.com\")\nprint(resp.text)\n```"
)

add(
    "How do I send query parameters with requests?",
    "Pass a dict to the `params` argument:\n\n```python\nimport requests\n\nresp = requests.get(\n    \"https://api.example.com/search\",\n    params={\"q\": \"python\", \"page\": 2},\n)\nprint(resp.url)  # ...?q=python&page=2\n```"
)

add(
    "Make a POST request with JSON body.",
    "```python\nimport requests\n\nresp = requests.post(\n    \"https://api.example.com/users\",\n    json={\"name\": \"Alice\", \"age\": 30},\n)\nprint(resp.status_code)\nprint(resp.json())\n```\n\nUsing `json=` automatically sets the `Content-Type: application/json` header and serializes the body."
)

add(
    "How do I add custom headers to a requests call?",
    "```python\nimport requests\n\nheaders = {\n    \"Authorization\": \"Bearer TOKEN\",\n    \"User-Agent\": \"my-app/1.0\",\n}\nresp = requests.get(\"https://api.example.com/data\", headers=headers)\nprint(resp.json())\n```"
)

add(
    "How do I set a timeout on a request?",
    "Always pass `timeout` so a request can't hang forever:\n\n```python\nimport requests\n\ntry:\n    resp = requests.get(\"https://api.example.com\", timeout=5)\n    resp.raise_for_status()\nexcept requests.exceptions.Timeout:\n    print(\"request timed out\")\nexcept requests.exceptions.RequestException as e:\n    print(\"error:\", e)\n```"
)

add(
    "How do I handle errors with requests?",
    "Use `raise_for_status()` and catch `RequestException`:\n\n```python\nimport requests\n\ntry:\n    resp = requests.get(\"https://api.example.com/data\", timeout=10)\n    resp.raise_for_status()  # raises on 4xx/5xx\n    data = resp.json()\nexcept requests.exceptions.HTTPError as e:\n    print(\"HTTP error:\", e)\nexcept requests.exceptions.ConnectionError:\n    print(\"connection failed\")\nexcept requests.exceptions.RequestException as e:\n    print(\"request failed:\", e)\n```"
)

add(
    "How do I use a requests Session?",
    "A Session reuses the underlying TCP connection and persists headers/cookies across requests:\n\n```python\nimport requests\n\nwith requests.Session() as session:\n    session.headers.update({\"Authorization\": \"Bearer TOKEN\"})\n    r1 = session.get(\"https://api.example.com/a\")\n    r2 = session.get(\"https://api.example.com/b\")\n    print(r1.status_code, r2.status_code)\n```"
)

add(
    "Download a file with requests.",
    "Stream it to avoid loading the whole file into memory:\n\n```python\nimport requests\n\nwith requests.get(\"https://example.com/big.zip\", stream=True) as r:\n    r.raise_for_status()\n    with open(\"big.zip\", \"wb\") as f:\n        for chunk in r.iter_content(chunk_size=8192):\n            f.write(chunk)\n```"
)

add(
    "How do I send form data with requests?",
    "Use the `data` argument with a dict (sends `application/x-www-form-urlencoded`):\n\n```python\nimport requests\n\nresp = requests.post(\n    \"https://example.com/login\",\n    data={\"username\": \"bob\", \"password\": \"secret\"},\n)\nprint(resp.status_code)\n```"
)

add(
    "Parse JSON from an API response.",
    "```python\nimport requests\n\nresp = requests.get(\"https://api.github.com/repos/python/cpython\")\ndata = resp.json()\nprint(data[\"stargazers_count\"])\n```"
)

add(
    "How do I upload a file with requests?",
    "```python\nimport requests\n\nwith open(\"photo.png\", \"rb\") as f:\n    resp = requests.post(\n        \"https://example.com/upload\",\n        files={\"file\": f},\n    )\nprint(resp.status_code)\n```"
)

add(
    "Check the status code and headers of a response.",
    "```python\nimport requests\n\nresp = requests.get(\"https://example.com\")\nprint(resp.status_code)        # 200\nprint(resp.headers[\"Content-Type\"])\nprint(resp.ok)                 # True if < 400\n```"
)

add(
    "How do I follow or disable redirects in requests?",
    "```python\nimport requests\n\n# Redirects are followed by default; disable with allow_redirects=False\nresp = requests.get(\"https://example.com\", allow_redirects=False)\nprint(resp.status_code)            # e.g. 301\nprint(resp.headers.get(\"Location\"))\n```"
)

add(
    "Send cookies with a request.",
    "```python\nimport requests\n\nresp = requests.get(\n    \"https://example.com\",\n    cookies={\"session_id\": \"abc123\"},\n)\nprint(resp.status_code)\n```"
)

# ---------------------------------------------------------------------------
# URLLIB
# ---------------------------------------------------------------------------

add(
    "How do I make an HTTP request with only the standard library?",
    "Use `urllib.request` (no external dependencies):\n\n```python\nimport urllib.request\nimport json\n\nwith urllib.request.urlopen(\"https://api.github.com\") as resp:\n    data = json.loads(resp.read().decode())\nprint(data)\n```"
)

add(
    "POST JSON with urllib.",
    "```python\nimport urllib.request\nimport json\n\npayload = json.dumps({\"name\": \"Alice\"}).encode()\nreq = urllib.request.Request(\n    \"https://api.example.com/users\",\n    data=payload,\n    headers={\"Content-Type\": \"application/json\"},\n    method=\"POST\",\n)\nwith urllib.request.urlopen(req) as resp:\n    print(resp.status)\n    print(resp.read().decode())\n```"
)

add(
    "How do I URL-encode query parameters with urllib?",
    "```python\nimport urllib.parse\nimport urllib.request\n\nparams = urllib.parse.urlencode({\"q\": \"python async\", \"page\": 2})\nurl = f\"https://example.com/search?{params}\"\nwith urllib.request.urlopen(url) as resp:\n    print(resp.read().decode())\n```"
)

# ---------------------------------------------------------------------------
# AIOHTTP (several)
# ---------------------------------------------------------------------------

add(
    "How do I make an async HTTP request with aiohttp?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as resp:\n            return await resp.text()\n\nhtml = asyncio.run(fetch(\"https://example.com\"))\nprint(html[:200])\n```"
)

add(
    "Fetch many URLs concurrently with aiohttp.",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, url):\n    async with session.get(url) as resp:\n        return await resp.text()\n\nasync def main(urls):\n    async with aiohttp.ClientSession() as session:\n        tasks = [fetch(session, u) for u in urls]\n        return await asyncio.gather(*tasks)\n\nurls = [\"https://example.com\"] * 5\nresults = asyncio.run(main(urls))\nprint(len(results))\n```\n\nReuse one `ClientSession` across all requests for connection pooling."
)

add(
    "Get JSON from an API with aiohttp.",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def get_json(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as resp:\n            resp.raise_for_status()\n            return await resp.json()\n\ndata = asyncio.run(get_json(\"https://api.github.com\"))\nprint(data)\n```"
)

add(
    "POST JSON with aiohttp.",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def post():\n    async with aiohttp.ClientSession() as session:\n        async with session.post(\n            \"https://api.example.com/items\",\n            json={\"name\": \"widget\"},\n        ) as resp:\n            return await resp.json()\n\nprint(asyncio.run(post()))\n```"
)

add(
    "Add a timeout to aiohttp requests.",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(url):\n    timeout = aiohttp.ClientTimeout(total=5)\n    async with aiohttp.ClientSession(timeout=timeout) as session:\n        async with session.get(url) as resp:\n            return await resp.text()\n\ntry:\n    asyncio.run(fetch(\"https://example.com\"))\nexcept asyncio.TimeoutError:\n    print(\"timed out\")\n```"
)

add(
    "Limit concurrent aiohttp requests with a semaphore.",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, sem, url):\n    async with sem:\n        async with session.get(url) as resp:\n            return await resp.text()\n\nasync def main(urls):\n    sem = asyncio.Semaphore(10)\n    async with aiohttp.ClientSession() as session:\n        tasks = [fetch(session, sem, u) for u in urls]\n        return await asyncio.gather(*tasks)\n\nurls = [\"https://example.com\"] * 50\nasyncio.run(main(urls))\n```"
)

# ---------------------------------------------------------------------------
# THREADING (several)
# ---------------------------------------------------------------------------

add(
    "How do I run a function in a separate thread?",
    "```python\nimport threading\n\ndef worker(name):\n    print(f\"hello from {name}\")\n\nt = threading.Thread(target=worker, args=(\"thread-1\",))\nt.start()\nt.join()\n```"
)

add(
    "Start multiple threads and wait for them.",
    "```python\nimport threading\n\ndef task(n):\n    print(f\"task {n}\")\n\nthreads = [threading.Thread(target=task, args=(i,)) for i in range(5)]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\n```"
)

add(
    "How do I use a threading.Lock?",
    "A Lock prevents race conditions on shared state:\n\n```python\nimport threading\n\ncounter = 0\nlock = threading.Lock()\n\ndef increment():\n    global counter\n    for _ in range(100000):\n        with lock:\n            counter += 1\n\nthreads = [threading.Thread(target=increment) for _ in range(2)]\nfor t in threads:\n    t.start()\nfor t in threads:\n    t.join()\nprint(counter)  # 200000\n```"
)

add(
    "Use ThreadPoolExecutor to run tasks.",
    "```python\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef square(n):\n    return n * n\n\nwith ThreadPoolExecutor(max_workers=4) as executor:\n    results = list(executor.map(square, range(10)))\nprint(results)\n```"
)

add(
    "How do I download multiple URLs with threads?",
    "Threads are great for I/O-bound work like HTTP:\n\n```python\nimport requests\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef fetch(url):\n    return requests.get(url, timeout=10).status_code\n\nurls = [\"https://example.com\"] * 10\nwith ThreadPoolExecutor(max_workers=5) as executor:\n    statuses = list(executor.map(fetch, urls))\nprint(statuses)\n```"
)

add(
    "Get return values from ThreadPoolExecutor using submit.",
    "```python\nfrom concurrent.futures import ThreadPoolExecutor, as_completed\n\ndef work(n):\n    return n * n\n\nwith ThreadPoolExecutor(max_workers=3) as executor:\n    futures = [executor.submit(work, i) for i in range(5)]\n    for future in as_completed(futures):\n        print(future.result())\n```"
)

add(
    "How do I pass data between threads safely?",
    "Use `queue.Queue`, which is thread-safe:\n\n```python\nimport threading\nimport queue\n\nq = queue.Queue()\n\ndef producer():\n    for i in range(5):\n        q.put(i)\n    q.put(None)\n\ndef consumer():\n    while True:\n        item = q.get()\n        if item is None:\n            break\n        print(\"got\", item)\n\nt1 = threading.Thread(target=producer)\nt2 = threading.Thread(target=consumer)\nt1.start(); t2.start()\nt1.join(); t2.join()\n```"
)

add(
    "Create a daemon thread.",
    "A daemon thread is killed automatically when the main program exits:\n\n```python\nimport threading\nimport time\n\ndef background():\n    while True:\n        time.sleep(1)\n        print(\"heartbeat\")\n\nt = threading.Thread(target=background, daemon=True)\nt.start()\ntime.sleep(3)  # daemon dies when main exits\n```"
)

# ---------------------------------------------------------------------------
# MULTIPROCESSING (several)
# ---------------------------------------------------------------------------

add(
    "How do I run code in a separate process?",
    "```python\nimport multiprocessing as mp\n\ndef worker(n):\n    print(f\"processing {n}\")\n\nif __name__ == \"__main__\":\n    p = mp.Process(target=worker, args=(5,))\n    p.start()\n    p.join()\n```\n\nGuard with `if __name__ == \"__main__\"` so child processes don't re-run the module."
)

add(
    "Use a multiprocessing Pool to parallelize CPU work.",
    "Multiprocessing sidesteps the GIL, so it's ideal for CPU-bound tasks:\n\n```python\nimport multiprocessing as mp\n\ndef heavy(n):\n    return sum(i * i for i in range(n))\n\nif __name__ == \"__main__\":\n    with mp.Pool(processes=4) as pool:\n        results = pool.map(heavy, [100000] * 8)\n    print(results)\n```"
)

add(
    "How do I use ProcessPoolExecutor?",
    "```python\nfrom concurrent.futures import ProcessPoolExecutor\n\ndef cube(n):\n    return n ** 3\n\nif __name__ == \"__main__\":\n    with ProcessPoolExecutor(max_workers=4) as executor:\n        results = list(executor.map(cube, range(10)))\n    print(results)\n```"
)

add(
    "Share data between processes.",
    "Use `multiprocessing.Queue` or shared values:\n\n```python\nimport multiprocessing as mp\n\ndef worker(q):\n    q.put(\"result from child\")\n\nif __name__ == \"__main__\":\n    q = mp.Queue()\n    p = mp.Process(target=worker, args=(q,))\n    p.start()\n    print(q.get())\n    p.join()\n```"
)

# ---------------------------------------------------------------------------
# GIL / CONCEPTUAL CONCURRENCY
# ---------------------------------------------------------------------------

add(
    "What is the GIL?",
    "The GIL (Global Interpreter Lock) is a mutex in CPython that allows only one thread to execute Python bytecode at a time. This means threads can't run Python code truly in parallel on multiple cores. It's fine for I/O-bound work (threads release the GIL while waiting on I/O) but limits CPU-bound work, where multiprocessing is the answer instead."
)

add(
    "When should I use asyncio vs threads?",
    "Use asyncio for high-concurrency I/O-bound work (thousands of network calls) where you control the code and can use async libraries. Use threads for I/O-bound work involving blocking libraries you can't make async (like `requests`). Both are limited by the GIL for CPU work, so for CPU-bound tasks use multiprocessing instead."
)

add(
    "asyncio vs threading vs multiprocessing — which do I pick?",
    "Rough guide:\n\n- asyncio: I/O-bound, very high concurrency, async-aware libraries, single thread cooperative scheduling.\n- threading: I/O-bound with blocking libraries; simpler than asyncio but limited by the GIL for CPU work.\n- multiprocessing: CPU-bound work that needs real parallelism across cores (bypasses the GIL).\n\nMnemonic: I/O-bound -> asyncio or threads; CPU-bound -> multiprocessing."
)

add(
    "Why don't threads speed up my CPU-heavy computation?",
    "Because of the GIL: only one thread runs Python bytecode at a time, so CPU-bound code doesn't get parallel speedup from threads. Use `multiprocessing` or `ProcessPoolExecutor` to use multiple cores:\n\n```python\nfrom concurrent.futures import ProcessPoolExecutor\n\ndef crunch(n):\n    return sum(i*i for i in range(n))\n\nif __name__ == \"__main__\":\n    with ProcessPoolExecutor() as ex:\n        print(list(ex.map(crunch, [10_000_000] * 4)))\n```"
)

add(
    "Is asyncio actually parallel?",
    "No. asyncio is concurrent but single-threaded; it interleaves tasks on one thread by switching at `await` points. It gives the illusion of parallelism for I/O-bound work but never runs two pieces of Python code at literally the same instant. For true parallelism use multiprocessing."
)

# ---------------------------------------------------------------------------
# FLASK (several)
# ---------------------------------------------------------------------------

add(
    "Create a minimal Flask app.",
    "```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route(\"/\")\ndef index():\n    return \"Hello, World!\"\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```"
)

add(
    "How do I add a route with a URL parameter in Flask?",
    "```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route(\"/user/<username>\")\ndef show_user(username):\n    return f\"User: {username}\"\n\n@app.route(\"/post/<int:post_id>\")\ndef show_post(post_id):\n    return f\"Post {post_id}\"\n```\n\nUse `<int:...>` to convert the parameter to an integer."
)

add(
    "How do I handle POST requests in Flask?",
    "```python\nfrom flask import Flask, request, jsonify\n\napp = Flask(__name__)\n\n@app.route(\"/submit\", methods=[\"POST\"])\ndef submit():\n    data = request.get_json()\n    name = data.get(\"name\")\n    return jsonify({\"message\": f\"Hello {name}\"})\n```"
)

add(
    "Return JSON from a Flask endpoint.",
    "```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route(\"/api/data\")\ndef data():\n    return jsonify({\"status\": \"ok\", \"items\": [1, 2, 3]})\n```"
)

add(
    "How do I read query parameters in Flask?",
    "```python\nfrom flask import Flask, request\n\napp = Flask(__name__)\n\n@app.route(\"/search\")\ndef search():\n    q = request.args.get(\"q\", \"\")\n    page = request.args.get(\"page\", 1, type=int)\n    return f\"searching '{q}' page {page}\"\n```"
)

add(
    "Support both GET and POST on one Flask route.",
    "```python\nfrom flask import Flask, request\n\napp = Flask(__name__)\n\n@app.route(\"/form\", methods=[\"GET\", \"POST\"])\ndef form():\n    if request.method == \"POST\":\n        return f\"received {request.form.get('name')}\"\n    return \"send a POST\"\n```"
)

add(
    "How do I use Flask blueprints?",
    "Blueprints let you split routes across modules:\n\n```python\n# users.py\nfrom flask import Blueprint, jsonify\n\nusers_bp = Blueprint(\"users\", __name__, url_prefix=\"/users\")\n\n@users_bp.route(\"/\")\ndef list_users():\n    return jsonify([\"alice\", \"bob\"])\n\n# app.py\nfrom flask import Flask\nfrom users import users_bp\n\napp = Flask(__name__)\napp.register_blueprint(users_bp)\n```"
)

add(
    "Return a custom status code in Flask.",
    "```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route(\"/create\", methods=[\"POST\"])\ndef create():\n    return jsonify({\"created\": True}), 201\n\n@app.route(\"/missing\")\ndef missing():\n    return jsonify({\"error\": \"not found\"}), 404\n```"
)

add(
    "How do I handle errors with a Flask error handler?",
    "```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.errorhandler(404)\ndef not_found(e):\n    return jsonify({\"error\": \"resource not found\"}), 404\n\n@app.errorhandler(500)\ndef server_error(e):\n    return jsonify({\"error\": \"internal error\"}), 500\n```"
)

# ---------------------------------------------------------------------------
# FASTAPI (several)
# ---------------------------------------------------------------------------

add(
    "Create a minimal FastAPI app.",
    "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/\")\ndef root():\n    return {\"message\": \"Hello World\"}\n```\n\nRun it with `uvicorn main:app --reload`."
)

add(
    "How do I add a path parameter in FastAPI?",
    "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/items/{item_id}\")\ndef read_item(item_id: int):\n    return {\"item_id\": item_id}\n```\n\nThe type hint `int` makes FastAPI validate and convert the parameter automatically."
)

add(
    "How do I use query parameters in FastAPI?",
    "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/search\")\ndef search(q: str, limit: int = 10):\n    return {\"q\": q, \"limit\": limit}\n```\n\nParameters not in the path become query parameters; those with defaults are optional."
)

add(
    "Use a Pydantic model for the request body in FastAPI.",
    "```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass Item(BaseModel):\n    name: str\n    price: float\n    in_stock: bool = True\n\n@app.post(\"/items\")\ndef create_item(item: Item):\n    return {\"received\": item.name, \"price\": item.price}\n```"
)

add(
    "Write an async endpoint in FastAPI.",
    "```python\nfrom fastapi import FastAPI\nimport aiohttp\n\napp = FastAPI()\n\n@app.get(\"/proxy\")\nasync def proxy():\n    async with aiohttp.ClientSession() as session:\n        async with session.get(\"https://api.github.com\") as resp:\n            return await resp.json()\n```"
)

add(
    "How do I return a specific status code in FastAPI?",
    "```python\nfrom fastapi import FastAPI, status\n\napp = FastAPI()\n\n@app.post(\"/items\", status_code=status.HTTP_201_CREATED)\ndef create():\n    return {\"created\": True}\n```"
)

add(
    "Raise an HTTP error in FastAPI.",
    "```python\nfrom fastapi import FastAPI, HTTPException\n\napp = FastAPI()\n\nitems = {1: \"apple\"}\n\n@app.get(\"/items/{item_id}\")\ndef get_item(item_id: int):\n    if item_id not in items:\n        raise HTTPException(status_code=404, detail=\"Item not found\")\n    return {\"item\": items[item_id]}\n```"
)

add(
    "How do I validate fields with Pydantic in FastAPI?",
    "```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel, Field, EmailStr\n\napp = FastAPI()\n\nclass User(BaseModel):\n    name: str = Field(min_length=1, max_length=50)\n    age: int = Field(ge=0, le=120)\n    email: EmailStr\n\n@app.post(\"/users\")\ndef create_user(user: User):\n    return user\n```"
)

# ---------------------------------------------------------------------------
# WEBSOCKETS
# ---------------------------------------------------------------------------

add(
    "How do I make a basic websocket server?",
    "Using the `websockets` library:\n\n```python\nimport asyncio\nimport websockets\n\nasync def handler(websocket):\n    async for message in websocket:\n        await websocket.send(f\"echo: {message}\")\n\nasync def main():\n    async with websockets.serve(handler, \"localhost\", 8765):\n        await asyncio.Future()  # run forever\n\nasyncio.run(main())\n```"
)

add(
    "Write a websocket client in Python.",
    "```python\nimport asyncio\nimport websockets\n\nasync def client():\n    async with websockets.connect(\"ws://localhost:8765\") as ws:\n        await ws.send(\"hello\")\n        reply = await ws.recv()\n        print(reply)\n\nasyncio.run(client())\n```"
)

add(
    "How do I add a websocket endpoint in FastAPI?",
    "```python\nfrom fastapi import FastAPI, WebSocket\n\napp = FastAPI()\n\n@app.websocket(\"/ws\")\nasync def websocket_endpoint(websocket: WebSocket):\n    await websocket.accept()\n    while True:\n        data = await websocket.receive_text()\n        await websocket.send_text(f\"echo: {data}\")\n```"
)

# ---------------------------------------------------------------------------
# MULTI-TURN CONVERSATIONS (~25)
# ---------------------------------------------------------------------------

addmulti([
    ("How do I fetch a URL with requests?",
     "```python\nimport requests\n\nresp = requests.get(\"https://api.github.com\")\nprint(resp.json())\n```"),
    ("Now fetch 10 URLs concurrently.",
     "Use a thread pool since `requests` is blocking:\n\n```python\nimport requests\nfrom concurrent.futures import ThreadPoolExecutor\n\nurls = [f\"https://api.github.com/users/user{i}\" for i in range(10)]\n\ndef fetch(url):\n    return requests.get(url).json()\n\nwith ThreadPoolExecutor(max_workers=10) as ex:\n    results = list(ex.map(fetch, urls))\nprint(len(results))\n```"),
    ("Add a timeout and error handling.",
     "```python\nimport requests\nfrom concurrent.futures import ThreadPoolExecutor\n\nurls = [f\"https://api.github.com/users/user{i}\" for i in range(10)]\n\ndef fetch(url):\n    try:\n        resp = requests.get(url, timeout=5)\n        resp.raise_for_status()\n        return resp.json()\n    except requests.exceptions.RequestException as e:\n        return {\"error\": str(e), \"url\": url}\n\nwith ThreadPoolExecutor(max_workers=10) as ex:\n    results = list(ex.map(fetch, urls))\nfor r in results:\n    print(r)\n```"),
])

addmulti([
    ("Write a simple async function that sleeps and returns a value.",
     "```python\nimport asyncio\n\nasync def work():\n    await asyncio.sleep(1)\n    return 42\n\nprint(asyncio.run(work()))\n```"),
    ("Run three of them concurrently.",
     "```python\nimport asyncio\n\nasync def work(n):\n    await asyncio.sleep(1)\n    return n\n\nasync def main():\n    return await asyncio.gather(work(1), work(2), work(3))\n\nprint(asyncio.run(main()))\n```"),
    ("Limit it so only two run at a time.",
     "```python\nimport asyncio\n\nasync def work(sem, n):\n    async with sem:\n        await asyncio.sleep(1)\n        return n\n\nasync def main():\n    sem = asyncio.Semaphore(2)\n    return await asyncio.gather(*(work(sem, i) for i in range(6)))\n\nprint(asyncio.run(main()))\n```"),
])

addmulti([
    ("Make a Flask hello world.",
     "```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route(\"/\")\ndef index():\n    return \"Hello!\"\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```"),
    ("Add a /greet/<name> route.",
     "```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route(\"/\")\ndef index():\n    return \"Hello!\"\n\n@app.route(\"/greet/<name>\")\ndef greet(name):\n    return f\"Hello, {name}!\"\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```"),
    ("Make it return JSON instead.",
     "```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route(\"/greet/<name>\")\ndef greet(name):\n    return jsonify({\"greeting\": f\"Hello, {name}!\"})\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```"),
])

addmulti([
    ("Create a FastAPI endpoint that returns a list of items.",
     "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/items\")\ndef list_items():\n    return [{\"id\": 1, \"name\": \"apple\"}, {\"id\": 2, \"name\": \"banana\"}]\n```"),
    ("Add an endpoint to create an item with a Pydantic model.",
     "```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass Item(BaseModel):\n    name: str\n    price: float\n\n@app.post(\"/items\")\ndef create_item(item: Item):\n    return {\"created\": item.name, \"price\": item.price}\n```"),
    ("Return a 404 if an item id isn't found.",
     "```python\nfrom fastapi import FastAPI, HTTPException\n\napp = FastAPI()\n\nitems = {1: \"apple\", 2: \"banana\"}\n\n@app.get(\"/items/{item_id}\")\ndef get_item(item_id: int):\n    if item_id not in items:\n        raise HTTPException(status_code=404, detail=\"Item not found\")\n    return {\"id\": item_id, \"name\": items[item_id]}\n```"),
])

addmulti([
    ("Show me a producer/consumer with asyncio.Queue.",
     "```python\nimport asyncio\n\nasync def producer(q):\n    for i in range(5):\n        await q.put(i)\n    await q.put(None)\n\nasync def consumer(q):\n    while True:\n        item = await q.get()\n        if item is None:\n            break\n        print(\"got\", item)\n\nasync def main():\n    q = asyncio.Queue()\n    await asyncio.gather(producer(q), consumer(q))\n\nasyncio.run(main())\n```"),
    ("Use multiple consumers.",
     "```python\nimport asyncio\n\nasync def producer(q, n):\n    for i in range(n):\n        await q.put(i)\n\nasync def consumer(q, name):\n    while True:\n        item = await q.get()\n        print(f\"{name} got {item}\")\n        q.task_done()\n\nasync def main():\n    q = asyncio.Queue()\n    consumers = [asyncio.create_task(consumer(q, f\"c{i}\")) for i in range(3)]\n    await producer(q, 10)\n    await q.join()          # wait until all items processed\n    for c in consumers:\n        c.cancel()\n\nasyncio.run(main())\n```"),
])

addmulti([
    ("How do I do a GET with aiohttp?",
     "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as resp:\n            return await resp.text()\n\nprint(asyncio.run(fetch(\"https://example.com\"))[:100])\n```"),
    ("Now fetch a list of URLs concurrently with one session.",
     "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, url):\n    async with session.get(url) as resp:\n        return await resp.text()\n\nasync def main(urls):\n    async with aiohttp.ClientSession() as session:\n        return await asyncio.gather(*(fetch(session, u) for u in urls))\n\nurls = [\"https://example.com\"] * 5\nresults = asyncio.run(main(urls))\nprint(len(results))\n```"),
    ("Cap it at 5 concurrent requests and handle errors.",
     "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, sem, url):\n    async with sem:\n        try:\n            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:\n                resp.raise_for_status()\n                return await resp.text()\n        except (aiohttp.ClientError, asyncio.TimeoutError) as e:\n            return f\"error: {e}\"\n\nasync def main(urls):\n    sem = asyncio.Semaphore(5)\n    async with aiohttp.ClientSession() as session:\n        return await asyncio.gather(*(fetch(session, sem, u) for u in urls))\n\nurls = [\"https://example.com\"] * 20\nasyncio.run(main(urls))\n```"),
])

addmulti([
    ("I have a CPU-heavy function. How do I speed it up with threads?",
     "Threads won't help CPU-bound work because of the GIL. Use multiprocessing instead:\n\n```python\nfrom concurrent.futures import ProcessPoolExecutor\n\ndef crunch(n):\n    return sum(i * i for i in range(n))\n\nif __name__ == \"__main__\":\n    with ProcessPoolExecutor() as ex:\n        results = list(ex.map(crunch, [5_000_000] * 4))\n    print(results)\n```"),
    ("Why exactly don't threads help here?",
     "The CPython GIL allows only one thread to execute Python bytecode at a time, so CPU-bound threads just take turns rather than running in parallel. Multiprocessing spawns separate processes, each with its own interpreter and GIL, so they genuinely run on different cores."),
])

addmulti([
    ("Make a requests call and check the status code.",
     "```python\nimport requests\n\nresp = requests.get(\"https://example.com\")\nprint(resp.status_code)\n```"),
    ("Raise an exception on a bad status.",
     "```python\nimport requests\n\nresp = requests.get(\"https://example.com\")\nresp.raise_for_status()  # raises HTTPError on 4xx/5xx\nprint(\"ok\")\n```"),
    ("Wrap it so it retries 3 times.",
     "```python\nimport requests\nimport time\n\ndef get_with_retry(url, retries=3, delay=1):\n    for attempt in range(retries):\n        try:\n            resp = requests.get(url, timeout=5)\n            resp.raise_for_status()\n            return resp\n        except requests.exceptions.RequestException as e:\n            if attempt == retries - 1:\n                raise\n            time.sleep(delay)\n\nresp = get_with_retry(\"https://example.com\")\nprint(resp.status_code)\n```"),
])

addmulti([
    ("Convert a blocking loop of requests into asyncio.",
     "Since `requests` is blocking, run it in threads via `asyncio.to_thread`:\n\n```python\nimport asyncio\nimport requests\n\ndef fetch(url):\n    return requests.get(url, timeout=5).status_code\n\nasync def main(urls):\n    tasks = [asyncio.to_thread(fetch, u) for u in urls]\n    return await asyncio.gather(*tasks)\n\nurls = [\"https://example.com\"] * 5\nprint(asyncio.run(main(urls)))\n```"),
    ("Can I do it natively async instead of using threads?",
     "Yes, switch to `aiohttp` which is natively async:\n\n```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, url):\n    async with session.get(url) as resp:\n        return resp.status\n\nasync def main(urls):\n    async with aiohttp.ClientSession() as session:\n        return await asyncio.gather(*(fetch(session, u) for u in urls))\n\nurls = [\"https://example.com\"] * 5\nprint(asyncio.run(main(urls)))\n```"),
])

addmulti([
    ("Write an asyncio task that runs in the background.",
     "```python\nimport asyncio\n\nasync def background():\n    await asyncio.sleep(2)\n    print(\"done\")\n\nasync def main():\n    task = asyncio.create_task(background())\n    print(\"main continues\")\n    await task\n\nasyncio.run(main())\n```"),
    ("How do I cancel it if it takes too long?",
     "```python\nimport asyncio\n\nasync def background():\n    await asyncio.sleep(100)\n\nasync def main():\n    task = asyncio.create_task(background())\n    await asyncio.sleep(2)\n    task.cancel()\n    try:\n        await task\n    except asyncio.CancelledError:\n        print(\"cancelled\")\n\nasyncio.run(main())\n```"),
])

addmulti([
    ("Set up a Flask API with a /users endpoint.",
     "```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\nusers = [{\"id\": 1, \"name\": \"alice\"}]\n\n@app.route(\"/users\")\ndef list_users():\n    return jsonify(users)\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```"),
    ("Add a POST to create a user.",
     "```python\nfrom flask import Flask, jsonify, request\n\napp = Flask(__name__)\nusers = [{\"id\": 1, \"name\": \"alice\"}]\n\n@app.route(\"/users\", methods=[\"GET\", \"POST\"])\ndef users_route():\n    if request.method == \"POST\":\n        data = request.get_json()\n        new_user = {\"id\": len(users) + 1, \"name\": data[\"name\"]}\n        users.append(new_user)\n        return jsonify(new_user), 201\n    return jsonify(users)\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n```"),
])

addmulti([
    ("How do I read JSON from a public API?",
     "```python\nimport requests\n\nresp = requests.get(\"https://jsonplaceholder.typicode.com/todos/1\")\ndata = resp.json()\nprint(data[\"title\"])\n```"),
    ("Now get the first 5 todos and print their titles.",
     "```python\nimport requests\n\nresp = requests.get(\"https://jsonplaceholder.typicode.com/todos\")\ntodos = resp.json()[:5]\nfor todo in todos:\n    print(todo[\"title\"])\n```"),
])

addmulti([
    ("Show me asyncio.gather with results.",
     "```python\nimport asyncio\n\nasync def fetch(n):\n    await asyncio.sleep(0.1)\n    return n * 10\n\nasync def main():\n    return await asyncio.gather(fetch(1), fetch(2), fetch(3))\n\nprint(asyncio.run(main()))  # [10, 20, 30]\n```"),
    ("What if one of them raises an exception?",
     "By default `gather` propagates the first exception and the rest keep running but their results are lost. Use `return_exceptions=True` to collect them instead:\n\n```python\nimport asyncio\n\nasync def fetch(n):\n    if n == 2:\n        raise ValueError(\"bad\")\n    return n\n\nasync def main():\n    return await asyncio.gather(fetch(1), fetch(2), fetch(3), return_exceptions=True)\n\nprint(asyncio.run(main()))  # [1, ValueError('bad'), 3]\n```"),
])

addmulti([
    ("Make a websocket echo server.",
     "```python\nimport asyncio\nimport websockets\n\nasync def echo(websocket):\n    async for msg in websocket:\n        await websocket.send(msg)\n\nasync def main():\n    async with websockets.serve(echo, \"localhost\", 8765):\n        await asyncio.Future()\n\nasyncio.run(main())\n```"),
    ("Write a client to test it.",
     "```python\nimport asyncio\nimport websockets\n\nasync def test():\n    async with websockets.connect(\"ws://localhost:8765\") as ws:\n        await ws.send(\"ping\")\n        print(await ws.recv())\n\nasyncio.run(test())\n```"),
])

addmulti([
    ("How do I use ThreadPoolExecutor.map?",
     "```python\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef double(n):\n    return n * 2\n\nwith ThreadPoolExecutor(max_workers=4) as ex:\n    print(list(ex.map(double, range(5))))\n```"),
    ("How do I get results as they complete instead?",
     "Use `submit` + `as_completed`:\n\n```python\nfrom concurrent.futures import ThreadPoolExecutor, as_completed\nimport time\n\ndef work(n):\n    time.sleep(n)\n    return n\n\nwith ThreadPoolExecutor(max_workers=3) as ex:\n    futures = [ex.submit(work, n) for n in [3, 1, 2]]\n    for fut in as_completed(futures):\n        print(\"done\", fut.result())\n```"),
])

addmulti([
    ("Send a POST request with requests.",
     "```python\nimport requests\n\nresp = requests.post(\"https://httpbin.org/post\", json={\"key\": \"value\"})\nprint(resp.json()[\"json\"])\n```"),
    ("Add an Authorization header.",
     "```python\nimport requests\n\nheaders = {\"Authorization\": \"Bearer my-token\"}\nresp = requests.post(\n    \"https://httpbin.org/post\",\n    json={\"key\": \"value\"},\n    headers=headers,\n)\nprint(resp.json()[\"headers\"][\"Authorization\"])\n```"),
    ("Use a session so the header persists across calls.",
     "```python\nimport requests\n\nwith requests.Session() as s:\n    s.headers.update({\"Authorization\": \"Bearer my-token\"})\n    r1 = s.post(\"https://httpbin.org/post\", json={\"a\": 1})\n    r2 = s.get(\"https://httpbin.org/get\")\n    print(r1.status_code, r2.status_code)\n```"),
])

addmulti([
    ("Write an async generator that yields numbers.",
     "```python\nimport asyncio\n\nasync def numbers(n):\n    for i in range(n):\n        await asyncio.sleep(0.1)\n        yield i\n\nasync def main():\n    async for x in numbers(5):\n        print(x)\n\nasyncio.run(main())\n```"),
    ("Collect them into a list.",
     "```python\nimport asyncio\n\nasync def numbers(n):\n    for i in range(n):\n        await asyncio.sleep(0.1)\n        yield i\n\nasync def main():\n    return [x async for x in numbers(5)]\n\nprint(asyncio.run(main()))  # [0, 1, 2, 3, 4]\n```"),
])

addmulti([
    ("Make a basic asyncio program with two tasks.",
     "```python\nimport asyncio\n\nasync def task(name):\n    await asyncio.sleep(1)\n    print(name)\n\nasync def main():\n    await asyncio.gather(task(\"a\"), task(\"b\"))\n\nasyncio.run(main())\n```"),
    ("Use a TaskGroup instead.",
     "```python\nimport asyncio\n\nasync def task(name):\n    await asyncio.sleep(1)\n    print(name)\n\nasync def main():\n    async with asyncio.TaskGroup() as tg:\n        tg.create_task(task(\"a\"))\n        tg.create_task(task(\"b\"))\n\nasyncio.run(main())\n```"),
])

addmulti([
    ("How do I call a REST API and handle the JSON?",
     "```python\nimport requests\n\nresp = requests.get(\"https://api.github.com/repos/python/cpython\")\nresp.raise_for_status()\ndata = resp.json()\nprint(data[\"full_name\"], data[\"stargazers_count\"])\n```"),
    ("What if the response isn't valid JSON?",
     "Catch `requests.exceptions.JSONDecodeError`:\n\n```python\nimport requests\n\nresp = requests.get(\"https://example.com\")\ntry:\n    data = resp.json()\nexcept requests.exceptions.JSONDecodeError:\n    print(\"not JSON, raw text:\", resp.text[:100])\n```"),
])

addmulti([
    ("Create a multiprocessing pool that squares numbers.",
     "```python\nimport multiprocessing as mp\n\ndef square(n):\n    return n * n\n\nif __name__ == \"__main__\":\n    with mp.Pool(4) as pool:\n        print(pool.map(square, range(10)))\n```"),
    ("Use ProcessPoolExecutor instead.",
     "```python\nfrom concurrent.futures import ProcessPoolExecutor\n\ndef square(n):\n    return n * n\n\nif __name__ == \"__main__\":\n    with ProcessPoolExecutor(max_workers=4) as ex:\n        print(list(ex.map(square, range(10))))\n```"),
])

addmulti([
    ("How do I rate-limit async requests to N per second?",
     "Combine a semaphore with timed releases, or simplest, gate with a semaphore and sleep:\n\n```python\nimport asyncio\nimport aiohttp\n\nasync def fetch(session, sem, url):\n    async with sem:\n        async with session.get(url) as resp:\n            await asyncio.sleep(1)  # crude pacing\n            return resp.status\n\nasync def main(urls):\n    sem = asyncio.Semaphore(5)\n    async with aiohttp.ClientSession() as session:\n        return await asyncio.gather(*(fetch(session, sem, u) for u in urls))\n\nasyncio.run(main([\"https://example.com\"] * 20))\n```"),
    ("That sleeps inside the lock. Can you pace it more cleanly?",
     "Yes, use a token-bucket style with a shared timestamp and lock so the rate is enforced without holding the semaphore during the sleep:\n\n```python\nimport asyncio\nimport time\nimport aiohttp\n\nclass RateLimiter:\n    def __init__(self, rate):\n        self.interval = 1 / rate\n        self.lock = asyncio.Lock()\n        self.next_time = time.monotonic()\n\n    async def wait(self):\n        async with self.lock:\n            now = time.monotonic()\n            if now < self.next_time:\n                await asyncio.sleep(self.next_time - now)\n            self.next_time = max(now, self.next_time) + self.interval\n\nasync def fetch(session, limiter, url):\n    await limiter.wait()\n    async with session.get(url) as resp:\n        return resp.status\n\nasync def main(urls):\n    limiter = RateLimiter(rate=5)  # 5/sec\n    async with aiohttp.ClientSession() as session:\n        return await asyncio.gather(*(fetch(session, limiter, u) for u in urls))\n\nasyncio.run(main([\"https://example.com\"] * 20))\n```"),
])

addmulti([
    ("Build a FastAPI app with a query parameter.",
     "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/search\")\ndef search(q: str):\n    return {\"query\": q}\n```"),
    ("Make the parameter optional with a default.",
     "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/search\")\ndef search(q: str = \"\", limit: int = 10):\n    return {\"query\": q, \"limit\": limit}\n```"),
    ("Add validation so limit is between 1 and 100.",
     "```python\nfrom fastapi import FastAPI, Query\n\napp = FastAPI()\n\n@app.get(\"/search\")\ndef search(q: str = \"\", limit: int = Query(10, ge=1, le=100)):\n    return {\"query\": q, \"limit\": limit}\n```"),
])

addmulti([
    ("How do I run blocking code without freezing my asyncio loop?",
     "Offload it with `asyncio.to_thread`:\n\n```python\nimport asyncio\nimport time\n\ndef blocking():\n    time.sleep(3)\n    return \"done\"\n\nasync def main():\n    result = await asyncio.to_thread(blocking)\n    print(result)\n\nasyncio.run(main())\n```"),
    ("What about a CPU-bound function instead of sleep?",
     "For CPU-bound work, a thread won't help due to the GIL; run it in a process pool via the loop's executor:\n\n```python\nimport asyncio\nfrom concurrent.futures import ProcessPoolExecutor\n\ndef crunch(n):\n    return sum(i * i for i in range(n))\n\nasync def main():\n    loop = asyncio.get_running_loop()\n    with ProcessPoolExecutor() as pool:\n        result = await loop.run_in_executor(pool, crunch, 10_000_000)\n    print(result)\n\nif __name__ == \"__main__\":\n    asyncio.run(main())\n```"),
])

addmulti([
    ("Make an asyncio.Lock example.",
     "```python\nimport asyncio\n\nlock = asyncio.Lock()\nbalance = 0\n\nasync def deposit(amount):\n    global balance\n    async with lock:\n        balance += amount\n\nasync def main():\n    await asyncio.gather(*(deposit(10) for _ in range(10)))\n    print(balance)  # 100\n\nasyncio.run(main())\n```"),
    ("Why do I even need the lock if asyncio is single-threaded?",
     "Single-threaded doesn't mean atomic: if a coroutine `await`s in the middle of a read-modify-write, another coroutine can interleave and corrupt the shared state. The lock guarantees the critical section runs without interruption from other coroutines."),
])

addmulti([
    ("How do I make concurrent requests but keep the GET order in results?",
     "`asyncio.gather` preserves input order in its results:\n\n```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, url):\n    async with session.get(url) as resp:\n        return resp.status\n\nasync def main(urls):\n    async with aiohttp.ClientSession() as session:\n        return await asyncio.gather(*(fetch(session, u) for u in urls))\n\nurls = [\"https://example.com/a\", \"https://example.com/b\"]\nprint(asyncio.run(main(urls)))  # order matches urls\n```"),
    ("What if I want them in completion order instead?",
     "Use `asyncio.as_completed`:\n\n```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, url):\n    async with session.get(url) as resp:\n        return url, resp.status\n\nasync def main(urls):\n    async with aiohttp.ClientSession() as session:\n        coros = [fetch(session, u) for u in urls]\n        for fut in asyncio.as_completed(coros):\n            url, status = await fut\n            print(url, status)\n\nasyncio.run(main([\"https://example.com\"] * 3))\n```"),
])

# ---------------------------------------------------------------------------
# MORE SINGLE-TURN to reach 320+: extra variety
# ---------------------------------------------------------------------------

add(
    "Difference between asyncio.sleep and time.sleep?",
    "`time.sleep()` blocks the entire thread (and event loop), while `asyncio.sleep()` yields control back to the loop so other coroutines can run. In async code always use `asyncio.sleep()`."
)

add(
    "How do I get the current running event loop?",
    "```python\nimport asyncio\n\nasync def main():\n    loop = asyncio.get_running_loop()\n    print(loop)\n\nasyncio.run(main())\n```"
)

add(
    "Run an executor from within asyncio.",
    "```python\nimport asyncio\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef blocking(x):\n    return x * 2\n\nasync def main():\n    loop = asyncio.get_running_loop()\n    with ThreadPoolExecutor() as pool:\n        result = await loop.run_in_executor(pool, blocking, 21)\n    print(result)\n\nasyncio.run(main())\n```"
)

add(
    "How do I make an HTTP HEAD request with requests?",
    "```python\nimport requests\n\nresp = requests.head(\"https://example.com\")\nprint(resp.status_code)\nprint(resp.headers[\"Content-Type\"])\n```"
)

add(
    "Send a PUT request.",
    "```python\nimport requests\n\nresp = requests.put(\n    \"https://httpbin.org/put\",\n    json={\"name\": \"updated\"},\n)\nprint(resp.status_code)\n```"
)

add(
    "Send a DELETE request.",
    "```python\nimport requests\n\nresp = requests.delete(\"https://httpbin.org/delete\")\nprint(resp.status_code)\n```"
)

add(
    "How do I access response content as bytes?",
    "```python\nimport requests\n\nresp = requests.get(\"https://example.com/image.png\")\ndata = resp.content  # bytes\nprint(len(data))\n```"
)

add(
    "Set the encoding of a requests response.",
    "```python\nimport requests\n\nresp = requests.get(\"https://example.com\")\nresp.encoding = \"utf-8\"\nprint(resp.text)\n```"
)

add(
    "How do I verify or disable SSL in requests?",
    "```python\nimport requests\n\n# verify is True by default; disable only for testing\nresp = requests.get(\"https://self-signed.example.com\", verify=False)\nprint(resp.status_code)\n```\n\nDisabling SSL verification is insecure; prefer providing a CA bundle via `verify=\"/path/ca.pem\"`."
)

add(
    "How do I make a Flask app return HTML?",
    "```python\nfrom flask import Flask, render_template_string\n\napp = Flask(__name__)\n\n@app.route(\"/\")\ndef home():\n    return render_template_string(\"<h1>Hello {{ name }}</h1>\", name=\"World\")\n```"
)

add(
    "How do I redirect in Flask?",
    "```python\nfrom flask import Flask, redirect, url_for\n\napp = Flask(__name__)\n\n@app.route(\"/old\")\ndef old():\n    return redirect(url_for(\"new\"))\n\n@app.route(\"/new\")\ndef new():\n    return \"new page\"\n```"
)

add(
    "How do I access request headers in Flask?",
    "```python\nfrom flask import Flask, request\n\napp = Flask(__name__)\n\n@app.route(\"/\")\ndef index():\n    token = request.headers.get(\"Authorization\")\n    return f\"token: {token}\"\n```"
)

add(
    "Enable CORS in FastAPI.",
    "```python\nfrom fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\n\napp = FastAPI()\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=[\"*\"],\n    allow_methods=[\"*\"],\n    allow_headers=[\"*\"],\n)\n```"
)

add(
    "How do I use dependency injection in FastAPI?",
    "```python\nfrom fastapi import FastAPI, Depends\n\napp = FastAPI()\n\ndef common_params(q: str = \"\", limit: int = 10):\n    return {\"q\": q, \"limit\": limit}\n\n@app.get(\"/items\")\ndef read_items(params: dict = Depends(common_params)):\n    return params\n```"
)

add(
    "Return a Pydantic model as the response in FastAPI.",
    "```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass Item(BaseModel):\n    name: str\n    price: float\n\n@app.get(\"/item\", response_model=Item)\ndef get_item():\n    return Item(name=\"book\", price=9.99)\n```"
)

add(
    "How do I run a FastAPI startup task?",
    "Use the lifespan context manager:\n\n```python\nfrom contextlib import asynccontextmanager\nfrom fastapi import FastAPI\n\n@asynccontextmanager\nasync def lifespan(app: FastAPI):\n    print(\"starting up\")\n    yield\n    print(\"shutting down\")\n\napp = FastAPI(lifespan=lifespan)\n```"
)

add(
    "What is a coroutine in Python?",
    "A coroutine is a function defined with `async def`; calling it returns a coroutine object that does nothing until it's awaited or scheduled on an event loop. It can suspend itself with `await` and resume later, enabling cooperative multitasking."
)

add(
    "How do I time how long an async operation takes?",
    "```python\nimport asyncio\nimport time\n\nasync def work():\n    await asyncio.sleep(1)\n\nasync def main():\n    start = time.perf_counter()\n    await work()\n    print(f\"took {time.perf_counter() - start:.2f}s\")\n\nasyncio.run(main())\n```"
)

add(
    "How do I run multiple independent asyncio coroutines that loop forever?",
    "```python\nimport asyncio\n\nasync def ticker(name, interval):\n    while True:\n        print(name)\n        await asyncio.sleep(interval)\n\nasync def main():\n    await asyncio.gather(\n        ticker(\"fast\", 1),\n        ticker(\"slow\", 3),\n    )\n\nasyncio.run(main())\n```"
)

add(
    "How do I send concurrent POST requests with aiohttp?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def post(session, payload):\n    async with session.post(\"https://httpbin.org/post\", json=payload) as resp:\n        return await resp.json()\n\nasync def main():\n    async with aiohttp.ClientSession() as session:\n        payloads = [{\"id\": i} for i in range(5)]\n        return await asyncio.gather(*(post(session, p) for p in payloads))\n\nresults = asyncio.run(main())\nprint(len(results))\n```"
)

add(
    "How do I handle an aiohttp request error?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        try:\n            async with session.get(url) as resp:\n                resp.raise_for_status()\n                return await resp.text()\n        except aiohttp.ClientResponseError as e:\n            return f\"HTTP {e.status}\"\n        except aiohttp.ClientError as e:\n            return f\"client error: {e}\"\n\nprint(asyncio.run(fetch(\"https://httpbin.org/status/404\")))\n```"
)

add(
    "How do I pass headers in aiohttp?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch():\n    headers = {\"Authorization\": \"Bearer token\"}\n    async with aiohttp.ClientSession(headers=headers) as session:\n        async with session.get(\"https://httpbin.org/headers\") as resp:\n            return await resp.json()\n\nprint(asyncio.run(fetch()))\n```"
)

add(
    "How do I pass query params in aiohttp?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch():\n    async with aiohttp.ClientSession() as session:\n        async with session.get(\n            \"https://httpbin.org/get\",\n            params={\"q\": \"python\", \"n\": 5},\n        ) as resp:\n            return await resp.json()\n\nprint(asyncio.run(fetch()))\n```"
)

add(
    "What's a thread-safe way to increment a counter?",
    "Guard it with a lock:\n\n```python\nimport threading\n\nlock = threading.Lock()\ncount = 0\n\ndef inc():\n    global count\n    with lock:\n        count += 1\n```\n\nWithout the lock, concurrent `count += 1` operations can interleave and lose updates."
)

add(
    "How do I use threading.Event to signal threads?",
    "```python\nimport threading\nimport time\n\nevent = threading.Event()\n\ndef worker():\n    print(\"waiting\")\n    event.wait()\n    print(\"go!\")\n\nt = threading.Thread(target=worker)\nt.start()\ntime.sleep(1)\nevent.set()\nt.join()\n```"
)

add(
    "How do I limit the number of concurrent threads?",
    "Set `max_workers` on the pool, or use a `threading.Semaphore`:\n\n```python\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef task(n):\n    return n\n\nwith ThreadPoolExecutor(max_workers=5) as ex:  # at most 5 at a time\n    results = list(ex.map(task, range(100)))\n```"
)

add(
    "How do I check how many CPUs are available for multiprocessing?",
    "```python\nimport os\nimport multiprocessing as mp\n\nprint(os.cpu_count())\nprint(mp.cpu_count())\n```"
)

add(
    "How do I use a multiprocessing shared counter?",
    "```python\nimport multiprocessing as mp\n\ndef worker(counter, lock):\n    with lock:\n        counter.value += 1\n\nif __name__ == \"__main__\":\n    counter = mp.Value(\"i\", 0)\n    lock = mp.Lock()\n    procs = [mp.Process(target=worker, args=(counter, lock)) for _ in range(10)]\n    for p in procs: p.start()\n    for p in procs: p.join()\n    print(counter.value)  # 10\n```"
)

add(
    "How do I parse a URL into components?",
    "```python\nfrom urllib.parse import urlparse\n\nparsed = urlparse(\"https://example.com:8080/path?q=1#frag\")\nprint(parsed.scheme)   # https\nprint(parsed.netloc)   # example.com:8080\nprint(parsed.path)     # /path\nprint(parsed.query)    # q=1\n```"
)

add(
    "How do I build a query string from a dict?",
    "```python\nfrom urllib.parse import urlencode\n\nprint(urlencode({\"q\": \"hello world\", \"page\": 2}))\n# q=hello+world&page=2\n```"
)

add(
    "How do I parse a query string into a dict?",
    "```python\nfrom urllib.parse import parse_qs\n\nprint(parse_qs(\"q=python&page=2&page=3\"))\n# {'q': ['python'], 'page': ['2', '3']}\n```"
)

add(
    "How do I make a synchronous endpoint vs async endpoint in FastAPI?",
    "FastAPI supports both; use `async def` when you `await` async I/O, and plain `def` for blocking/sync code (FastAPI runs `def` endpoints in a threadpool automatically):\n\n```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/sync\")\ndef sync_endpoint():\n    return {\"type\": \"sync\"}\n\n@app.get(\"/async\")\nasync def async_endpoint():\n    return {\"type\": \"async\"}\n```"
)

add(
    "How do I read the raw body in a FastAPI request?",
    "```python\nfrom fastapi import FastAPI, Request\n\napp = FastAPI()\n\n@app.post(\"/raw\")\nasync def raw(request: Request):\n    body = await request.body()\n    return {\"length\": len(body)}\n```"
)

add(
    "How do I post a JSON list of items to a REST API?",
    "```python\nimport requests\n\nitems = [{\"id\": 1}, {\"id\": 2}]\nresp = requests.post(\"https://httpbin.org/post\", json=items)\nprint(resp.json()[\"json\"])\n```"
)

add(
    "How do I retry a failed request with exponential backoff?",
    "```python\nimport time\nimport requests\n\ndef get_with_backoff(url, retries=4):\n    for attempt in range(retries):\n        try:\n            resp = requests.get(url, timeout=5)\n            resp.raise_for_status()\n            return resp\n        except requests.exceptions.RequestException:\n            if attempt == retries - 1:\n                raise\n            time.sleep(2 ** attempt)  # 1, 2, 4, ...\n\nprint(get_with_backoff(\"https://example.com\").status_code)\n```"
)

add(
    "Explain producer/consumer pattern.",
    "Producers create work items and put them on a shared queue; consumers take items off and process them. The queue decouples their speeds and provides backpressure. In asyncio you use `asyncio.Queue`; with threads you use `queue.Queue`; both are safe for concurrent access."
)

add(
    "How do I gracefully shut down an asyncio server on Ctrl+C?",
    "```python\nimport asyncio\n\nasync def main():\n    try:\n        while True:\n            await asyncio.sleep(1)\n            print(\"running\")\n    except asyncio.CancelledError:\n        print(\"cleaning up\")\n\ntry:\n    asyncio.run(main())\nexcept KeyboardInterrupt:\n    print(\"shutdown\")\n```"
)

add(
    "How do I run an async function from synchronous code?",
    "Use `asyncio.run()` at the top level (don't call it if a loop is already running):\n\n```python\nimport asyncio\n\nasync def fetch():\n    await asyncio.sleep(1)\n    return \"data\"\n\ndef sync_caller():\n    return asyncio.run(fetch())\n\nprint(sync_caller())\n```"
)

add(
    "What does await actually return?",
    "`await expr` suspends the coroutine until `expr` (an awaitable) completes, then evaluates to that awaitable's result. For example `result = await fetch()` gives you whatever `fetch()` returns once it finishes."
)

add(
    "How do I chain async functions?",
    "```python\nimport asyncio\n\nasync def step_one():\n    await asyncio.sleep(0.1)\n    return 10\n\nasync def step_two(x):\n    await asyncio.sleep(0.1)\n    return x * 2\n\nasync def main():\n    a = await step_one()\n    b = await step_two(a)\n    return b\n\nprint(asyncio.run(main()))  # 20\n```"
)

add(
    "How do I make a basic HTTP server with the standard library?",
    "```python\nfrom http.server import HTTPServer, BaseHTTPRequestHandler\n\nclass Handler(BaseHTTPRequestHandler):\n    def do_GET(self):\n        self.send_response(200)\n        self.send_header(\"Content-Type\", \"text/plain\")\n        self.end_headers()\n        self.wfile.write(b\"Hello\")\n\nserver = HTTPServer((\"localhost\", 8000), Handler)\nserver.serve_forever()\n```"
)

add(
    "How do I send a GET request and measure response time?",
    "```python\nimport requests\n\nresp = requests.get(\"https://example.com\")\nprint(resp.elapsed.total_seconds())\n```"
)

add(
    "How do I post multipart form data with multiple files?",
    "```python\nimport requests\n\nfiles = [\n    (\"files\", open(\"a.txt\", \"rb\")),\n    (\"files\", open(\"b.txt\", \"rb\")),\n]\nresp = requests.post(\"https://httpbin.org/post\", files=files)\nprint(resp.status_code)\n```"
)

add(
    "How do I make a Flask app return a file download?",
    "```python\nfrom flask import Flask, send_file\n\napp = Flask(__name__)\n\n@app.route(\"/download\")\ndef download():\n    return send_file(\"report.pdf\", as_attachment=True)\n```"
)

add(
    "How do I read JSON in a Flask request safely?",
    "```python\nfrom flask import Flask, request, jsonify\n\napp = Flask(__name__)\n\n@app.route(\"/data\", methods=[\"POST\"])\ndef data():\n    payload = request.get_json(silent=True)\n    if payload is None:\n        return jsonify({\"error\": \"invalid JSON\"}), 400\n    return jsonify(payload)\n```"
)

add(
    "What's the difference between concurrency and parallelism?",
    "Concurrency is dealing with many tasks by interleaving their progress (one core, switching between them), while parallelism is actually executing multiple tasks at the same instant on multiple cores. asyncio and threads give concurrency; multiprocessing gives parallelism in Python."
)

add(
    "When is threading better than asyncio?",
    "Threading is better when you must use blocking libraries that have no async equivalent (e.g. a legacy DB driver or `requests`), since you can run them in threads without rewriting everything. asyncio needs async-aware libraries to actually be non-blocking."
)

add(
    "How do I limit total requests in flight with asyncio and report progress?",
    "```python\nimport asyncio\nimport aiohttp\n\nasync def fetch(session, sem, url, done):\n    async with sem:\n        async with session.get(url) as resp:\n            status = resp.status\n    done[0] += 1\n    print(f\"{done[0]} completed\")\n    return status\n\nasync def main(urls):\n    sem = asyncio.Semaphore(10)\n    done = [0]\n    async with aiohttp.ClientSession() as session:\n        return await asyncio.gather(*(fetch(session, sem, u, done) for u in urls))\n\nasyncio.run(main([\"https://example.com\"] * 30))\n```"
)

add(
    "How do I make an async context manager?",
    "```python\nimport asyncio\n\nclass Resource:\n    async def __aenter__(self):\n        await asyncio.sleep(0.1)\n        print(\"acquired\")\n        return self\n    async def __aexit__(self, *exc):\n        await asyncio.sleep(0.1)\n        print(\"released\")\n\nasync def main():\n    async with Resource() as r:\n        print(\"using resource\")\n\nasyncio.run(main())\n```"
)

add(
    "How do I create a thread subclass?",
    "```python\nimport threading\n\nclass Worker(threading.Thread):\n    def __init__(self, n):\n        super().__init__()\n        self.n = n\n        self.result = None\n    def run(self):\n        self.result = self.n * 2\n\nw = Worker(21)\nw.start()\nw.join()\nprint(w.result)  # 42\n```"
)

add(
    "How do I poll an API until a condition is met asynchronously?",
    "```python\nimport asyncio\nimport aiohttp\n\nasync def poll(url):\n    async with aiohttp.ClientSession() as session:\n        while True:\n            async with session.get(url) as resp:\n                data = await resp.json()\n            if data.get(\"status\") == \"ready\":\n                return data\n            await asyncio.sleep(2)\n\n# result = asyncio.run(poll(\"https://api.example.com/job/1\"))\n```"
)

add(
    "How do I run a Flask app with threaded mode for concurrency?",
    "```python\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route(\"/\")\ndef index():\n    return \"ok\"\n\nif __name__ == \"__main__\":\n    app.run(threaded=True)  # handle requests in separate threads\n```"
)

add(
    "How do I structure a FastAPI app with routers?",
    "Use `APIRouter`, the FastAPI equivalent of Flask blueprints:\n\n```python\n# routers/users.py\nfrom fastapi import APIRouter\n\nrouter = APIRouter(prefix=\"/users\", tags=[\"users\"])\n\n@router.get(\"/\")\ndef list_users():\n    return [\"alice\", \"bob\"]\n\n# main.py\nfrom fastapi import FastAPI\nfrom routers import users\n\napp = FastAPI()\napp.include_router(users.router)\n```"
)

add(
    "How do I send concurrent requests and aggregate JSON results?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(session, url):\n    async with session.get(url) as resp:\n        return await resp.json()\n\nasync def main(urls):\n    async with aiohttp.ClientSession() as session:\n        results = await asyncio.gather(*(fetch(session, u) for u in urls))\n    return [r.get(\"id\") for r in results]\n\nurls = [f\"https://jsonplaceholder.typicode.com/todos/{i}\" for i in range(1, 6)]\nprint(asyncio.run(main(urls)))\n```"
)

add(
    "How do I handle keyboard interrupt cleanly in a threaded program?",
    "Use a `threading.Event` as a stop flag:\n\n```python\nimport threading\nimport time\n\nstop = threading.Event()\n\ndef worker():\n    while not stop.is_set():\n        time.sleep(0.5)\n        print(\"working\")\n\nt = threading.Thread(target=worker)\nt.start()\ntry:\n    while True:\n        time.sleep(1)\nexcept KeyboardInterrupt:\n    stop.set()\n    t.join()\n```"
)

add(
    "How do I set default headers for all requests in a session?",
    "```python\nimport requests\n\nsession = requests.Session()\nsession.headers.update({\n    \"User-Agent\": \"my-app/1.0\",\n    \"Accept\": \"application/json\",\n})\nresp = session.get(\"https://httpbin.org/headers\")\nprint(resp.json())\n```"
)

add(
    "How can I stream a large JSON response line by line?",
    "```python\nimport requests\nimport json\n\nwith requests.get(\"https://example.com/stream\", stream=True) as r:\n    for line in r.iter_lines():\n        if line:\n            obj = json.loads(line)\n            print(obj)\n```"
)

add(
    "How do I time out a whole group of async tasks?",
    "```python\nimport asyncio\n\nasync def work(n):\n    await asyncio.sleep(n)\n    return n\n\nasync def main():\n    try:\n        async with asyncio.timeout(2):\n            return await asyncio.gather(work(1), work(5))\n    except asyncio.TimeoutError:\n        print(\"group timed out\")\n\nasyncio.run(main())\n```"
)

add(
    "How do I make sequential vs concurrent comparison in asyncio?",
    "```python\nimport asyncio\nimport time\n\nasync def task():\n    await asyncio.sleep(1)\n\nasync def sequential():\n    start = time.perf_counter()\n    await task(); await task()\n    print(f\"sequential: {time.perf_counter()-start:.1f}s\")  # ~2s\n\nasync def concurrent():\n    start = time.perf_counter()\n    await asyncio.gather(task(), task())\n    print(f\"concurrent: {time.perf_counter()-start:.1f}s\")  # ~1s\n\nasyncio.run(sequential())\nasyncio.run(concurrent())\n```"
)

add(
    "How do I make a websocket broadcast to all clients?",
    "```python\nimport asyncio\nimport websockets\n\nclients = set()\n\nasync def handler(ws):\n    clients.add(ws)\n    try:\n        async for msg in ws:\n            for client in clients:\n                await client.send(msg)\n    finally:\n        clients.discard(ws)\n\nasync def main():\n    async with websockets.serve(handler, \"localhost\", 8765):\n        await asyncio.Future()\n\nasyncio.run(main())\n```"
)

add(
    "How do I pass path and query params together in FastAPI?",
    "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/users/{user_id}/posts\")\ndef get_posts(user_id: int, limit: int = 10):\n    return {\"user_id\": user_id, \"limit\": limit}\n```"
)

add(
    "How do I handle JSON decode errors from an async response?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def fetch(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as resp:\n            try:\n                return await resp.json()\n            except aiohttp.ContentTypeError:\n                return await resp.text()\n\nprint(asyncio.run(fetch(\"https://example.com\")))\n```"
)

add(
    "How do I limit requests with a connector in aiohttp?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def main(urls):\n    connector = aiohttp.TCPConnector(limit=10)  # max 10 connections\n    async with aiohttp.ClientSession(connector=connector) as session:\n        async def fetch(url):\n            async with session.get(url) as resp:\n                return resp.status\n        return await asyncio.gather(*(fetch(u) for u in urls))\n\nasyncio.run(main([\"https://example.com\"] * 50))\n```"
)

add(
    "How do I do basic auth with requests?",
    "```python\nimport requests\n\nresp = requests.get(\n    \"https://httpbin.org/basic-auth/user/pass\",\n    auth=(\"user\", \"pass\"),\n)\nprint(resp.status_code)\n```"
)

add(
    "How do I read environment-based config for an API key?",
    "```python\nimport os\nimport requests\n\napi_key = os.environ[\"API_KEY\"]\nresp = requests.get(\n    \"https://api.example.com/data\",\n    headers={\"Authorization\": f\"Bearer {api_key}\"},\n)\nprint(resp.status_code)\n```"
)

add(
    "How do I use asyncio.wait with FIRST_COMPLETED?",
    "```python\nimport asyncio\n\nasync def work(n):\n    await asyncio.sleep(n)\n    return n\n\nasync def main():\n    tasks = {asyncio.create_task(work(i)) for i in [3, 1, 2]}\n    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)\n    print(\"first done:\", [t.result() for t in done])\n    for t in pending:\n        t.cancel()\n\nasyncio.run(main())\n```"
)

add(
    "How do I do graceful shutdown of aiohttp ClientSession?",
    "Always use `async with` so the session closes; if you can't, call `await session.close()`:\n\n```python\nimport aiohttp\nimport asyncio\n\nasync def main():\n    session = aiohttp.ClientSession()\n    try:\n        async with session.get(\"https://example.com\") as resp:\n            print(resp.status)\n    finally:\n        await session.close()\n\nasyncio.run(main())\n```"
)

add(
    "How do I serialize a dataclass to JSON for an API response?",
    "```python\nimport json\nfrom dataclasses import dataclass, asdict\n\n@dataclass\nclass User:\n    name: str\n    age: int\n\nuser = User(\"alice\", 30)\nprint(json.dumps(asdict(user)))\n```"
)

add(
    "How do I add middleware in FastAPI to time requests?",
    "```python\nimport time\nfrom fastapi import FastAPI, Request\n\napp = FastAPI()\n\n@app.middleware(\"http\")\nasync def add_timing(request: Request, call_next):\n    start = time.perf_counter()\n    response = await call_next(request)\n    response.headers[\"X-Process-Time\"] = str(time.perf_counter() - start)\n    return response\n```"
)

add(
    "How do I make a long-running asyncio worker that processes a queue forever?",
    "```python\nimport asyncio\n\nasync def worker(queue):\n    while True:\n        job = await queue.get()\n        try:\n            print(\"processing\", job)\n            await asyncio.sleep(0.1)\n        finally:\n            queue.task_done()\n\nasync def main():\n    queue = asyncio.Queue()\n    asyncio.create_task(worker(queue))\n    for i in range(5):\n        await queue.put(i)\n    await queue.join()\n\nasyncio.run(main())\n```"
)

add(
    "How do I make an HTTP request that ignores the proxy?",
    "```python\nimport requests\n\nresp = requests.get(\"https://example.com\", proxies={\"http\": None, \"https\": None})\nprint(resp.status_code)\n```"
)

add(
    "How do I use requests through a proxy?",
    "```python\nimport requests\n\nproxies = {\n    \"http\": \"http://10.0.0.1:8080\",\n    \"https\": \"http://10.0.0.1:8080\",\n}\nresp = requests.get(\"https://example.com\", proxies=proxies)\nprint(resp.status_code)\n```"
)

add(
    "How do I run a coroutine and ignore its result (fire and forget)?",
    "Create a task but keep a reference so it isn't garbage-collected:\n\n```python\nimport asyncio\n\nasync def log_event(msg):\n    await asyncio.sleep(0.1)\n    print(\"logged\", msg)\n\nasync def main():\n    task = asyncio.create_task(log_event(\"hi\"))\n    # keep going; await before exit so it completes\n    await asyncio.sleep(0.2)\n\nasyncio.run(main())\n```"
)

add(
    "How do I retry an async request a few times?",
    "```python\nimport asyncio\nimport aiohttp\n\nasync def fetch(url, retries=3):\n    async with aiohttp.ClientSession() as session:\n        for attempt in range(retries):\n            try:\n                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:\n                    resp.raise_for_status()\n                    return await resp.text()\n            except (aiohttp.ClientError, asyncio.TimeoutError):\n                if attempt == retries - 1:\n                    raise\n                await asyncio.sleep(2 ** attempt)\n\nprint(asyncio.run(fetch(\"https://example.com\"))[:50])\n```"
)

add(
    "How do I make a thread return a value with a future?",
    "```python\nfrom concurrent.futures import ThreadPoolExecutor\n\ndef compute():\n    return 7 * 6\n\nwith ThreadPoolExecutor() as ex:\n    future = ex.submit(compute)\n    print(future.result())  # 42\n```"
)

add(
    "How do I detect if I'm already inside an event loop?",
    "```python\nimport asyncio\n\ntry:\n    asyncio.get_running_loop()\n    print(\"inside a loop\")\nexcept RuntimeError:\n    print(\"no running loop\")\n```"
)

add(
    "How do I run async code in a Jupyter notebook?",
    "Jupyter already runs an event loop, so just `await` directly in a cell instead of calling `asyncio.run()`:\n\n```python\nimport asyncio\n\nasync def fetch():\n    await asyncio.sleep(1)\n    return \"done\"\n\nresult = await fetch()  # works in Jupyter\n```"
)

add(
    "How do I post data and parse the returned id?",
    "```python\nimport requests\n\nresp = requests.post(\"https://jsonplaceholder.typicode.com/posts\", json={\"title\": \"hi\"})\nresp.raise_for_status()\nprint(resp.json()[\"id\"])\n```"
)

add(
    "How do I limit a Flask route to JSON content type?",
    "```python\nfrom flask import Flask, request, jsonify\n\napp = Flask(__name__)\n\n@app.route(\"/api\", methods=[\"POST\"])\ndef api():\n    if not request.is_json:\n        return jsonify({\"error\": \"expected JSON\"}), 415\n    return jsonify(request.get_json())\n```"
)

add(
    "How do I run multiple async HTTP calls with different methods?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def main():\n    async with aiohttp.ClientSession() as session:\n        async def get():\n            async with session.get(\"https://httpbin.org/get\") as r:\n                return await r.json()\n        async def post():\n            async with session.post(\"https://httpbin.org/post\", json={\"a\": 1}) as r:\n                return await r.json()\n        g, p = await asyncio.gather(get(), post())\n        return g[\"url\"], p[\"url\"]\n\nprint(asyncio.run(main()))\n```"
)

add(
    "How do I make a generator that reads a large file lazily?",
    "```python\ndef read_lines(path):\n    with open(path) as f:\n        for line in f:\n            yield line.rstrip(\"\\n\")\n\nfor line in read_lines(\"big.txt\"):\n    process(line)\n```\n\nThis reads one line at a time instead of loading the whole file into memory."
)

add(
    "How do I implement a simple async retry decorator?",
    "```python\nimport asyncio\nimport functools\n\ndef async_retry(retries=3, delay=1):\n    def decorator(func):\n        @functools.wraps(func)\n        async def wrapper(*args, **kwargs):\n            for attempt in range(retries):\n                try:\n                    return await func(*args, **kwargs)\n                except Exception:\n                    if attempt == retries - 1:\n                        raise\n                    await asyncio.sleep(delay)\n        return wrapper\n    return decorator\n\n@async_retry(retries=3)\nasync def unstable():\n    raise ValueError(\"fail\")\n```"
)

add(
    "How do I send concurrent requests with a max and collect failures separately?",
    "```python\nimport asyncio\nimport aiohttp\n\nasync def fetch(session, sem, url):\n    async with sem:\n        try:\n            async with session.get(url) as resp:\n                resp.raise_for_status()\n                return (url, await resp.text())\n        except Exception as e:\n            return (url, e)\n\nasync def main(urls):\n    sem = asyncio.Semaphore(10)\n    async with aiohttp.ClientSession() as session:\n        results = await asyncio.gather(*(fetch(session, sem, u) for u in urls))\n    ok = [(u, r) for u, r in results if not isinstance(r, Exception)]\n    failed = [(u, r) for u, r in results if isinstance(r, Exception)]\n    return ok, failed\n\nasyncio.run(main([\"https://example.com\"] * 10))\n```"
)

add(
    "How do I get the JSON body and headers together from requests?",
    "```python\nimport requests\n\nresp = requests.get(\"https://api.github.com\")\nprint(\"body:\", resp.json())\nprint(\"rate limit:\", resp.headers.get(\"X-RateLimit-Remaining\"))\n```"
)

add(
    "How do I make a coroutine sleep with jitter?",
    "```python\nimport asyncio\nimport random\n\nasync def wait_with_jitter(base):\n    await asyncio.sleep(base + random.uniform(0, 0.5))\n\nasync def main():\n    await wait_with_jitter(1)\n    print(\"done\")\n\nasyncio.run(main())\n```"
)

add(
    "How do I send a request with a connection timeout and read timeout?",
    "Pass a tuple `(connect_timeout, read_timeout)`:\n\n```python\nimport requests\n\nresp = requests.get(\"https://example.com\", timeout=(3.0, 10.0))\nprint(resp.status_code)\n```"
)

add(
    "How do I make a FastAPI endpoint accept a list of Pydantic models?",
    "```python\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass Item(BaseModel):\n    name: str\n\n@app.post(\"/items/bulk\")\ndef bulk(items: list[Item]):\n    return {\"count\": len(items)}\n```"
)

add(
    "How do I return plain text from FastAPI?",
    "```python\nfrom fastapi import FastAPI\nfrom fastapi.responses import PlainTextResponse\n\napp = FastAPI()\n\n@app.get(\"/text\", response_class=PlainTextResponse)\ndef text():\n    return \"hello\"\n```"
)

add(
    "How do I combine threads and a queue for a worker pool manually?",
    "```python\nimport threading\nimport queue\n\nq = queue.Queue()\n\ndef worker():\n    while True:\n        item = q.get()\n        if item is None:\n            break\n        print(\"processed\", item)\n        q.task_done()\n\nthreads = [threading.Thread(target=worker) for _ in range(3)]\nfor t in threads:\n    t.start()\nfor i in range(10):\n    q.put(i)\nq.join()\nfor _ in threads:\n    q.put(None)\nfor t in threads:\n    t.join()\n```"
)

add(
    "How do I make an async HTTP client reusable as a class?",
    "```python\nimport aiohttp\n\nclass ApiClient:\n    def __init__(self, base_url):\n        self.base_url = base_url\n        self.session = None\n    async def __aenter__(self):\n        self.session = aiohttp.ClientSession()\n        return self\n    async def __aexit__(self, *exc):\n        await self.session.close()\n    async def get(self, path):\n        async with self.session.get(self.base_url + path) as resp:\n            return await resp.json()\n\n# async with ApiClient(\"https://api.github.com\") as client:\n#     data = await client.get(\"/\")\n```"
)

add(
    "How do I handle SIGINT to stop an asyncio loop with a flag?",
    "```python\nimport asyncio\nimport signal\n\nstop = asyncio.Event()\n\nasync def main():\n    loop = asyncio.get_running_loop()\n    loop.add_signal_handler(signal.SIGINT, stop.set)\n    print(\"running, press Ctrl+C\")\n    await stop.wait()\n    print(\"stopping\")\n\nasyncio.run(main())\n```"
)

add(
    "How do I measure throughput of concurrent requests?",
    "```python\nimport asyncio\nimport time\nimport aiohttp\n\nasync def fetch(session, url):\n    async with session.get(url) as resp:\n        return resp.status\n\nasync def main(urls):\n    start = time.perf_counter()\n    async with aiohttp.ClientSession() as session:\n        await asyncio.gather(*(fetch(session, u) for u in urls))\n    elapsed = time.perf_counter() - start\n    print(f\"{len(urls)/elapsed:.1f} req/s\")\n\nasyncio.run(main([\"https://example.com\"] * 20))\n```"
)

add(
    "How do I convert a synchronous generator to feed an async consumer?",
    "Wrap iteration in `asyncio.to_thread` or just iterate directly if it's cheap:\n\n```python\nimport asyncio\n\ndef sync_gen():\n    for i in range(5):\n        yield i\n\nasync def main():\n    for item in sync_gen():\n        await asyncio.sleep(0.1)  # async work per item\n        print(item)\n\nasyncio.run(main())\n```"
)

add(
    "How do I make a health check endpoint in FastAPI?",
    "```python\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/health\")\ndef health():\n    return {\"status\": \"healthy\"}\n```"
)

add(
    "How do I make a health check endpoint in Flask?",
    "```python\nfrom flask import Flask, jsonify\n\napp = Flask(__name__)\n\n@app.route(\"/health\")\ndef health():\n    return jsonify({\"status\": \"healthy\"})\n```"
)

add(
    "How do I post and stream a response with aiohttp?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def stream():\n    async with aiohttp.ClientSession() as session:\n        async with session.get(\"https://example.com/stream\") as resp:\n            async for chunk in resp.content.iter_chunked(1024):\n                print(len(chunk))\n\nasyncio.run(stream())\n```"
)

add(
    "How do I share an asyncio.Semaphore across functions cleanly?",
    "Create it once in your entry coroutine and pass it down, or store it on a shared object:\n\n```python\nimport asyncio\n\nasync def limited(sem, n):\n    async with sem:\n        await asyncio.sleep(0.1)\n        return n\n\nasync def main():\n    sem = asyncio.Semaphore(5)\n    return await asyncio.gather(*(limited(sem, i) for i in range(20)))\n\nprint(len(asyncio.run(main())))\n```"
)

add(
    "How do I do a HEAD request asynchronously to check a URL exists?",
    "```python\nimport aiohttp\nimport asyncio\n\nasync def exists(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.head(url) as resp:\n            return resp.status < 400\n\nprint(asyncio.run(exists(\"https://example.com\")))\n```"
)

add(
    "How do I batch a large list of items for processing in asyncio?",
    "```python\nimport asyncio\n\nasync def process(batch):\n    await asyncio.sleep(0.1)\n    return sum(batch)\n\nasync def main(items, size=10):\n    batches = [items[i:i+size] for i in range(0, len(items), size)]\n    return await asyncio.gather(*(process(b) for b in batches))\n\nprint(asyncio.run(main(list(range(100)))))\n```"
)

# Build file
out_path = str(__import__("pathlib").Path(__file__).resolve().parent / "async_web.jsonl")
with open(out_path, "w") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print("wrote", len(examples), "examples to", out_path, file=__import__("sys").stderr)
