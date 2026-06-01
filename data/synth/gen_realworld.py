#!/usr/bin/env python3
"""Generate real-world practical Python instruction/response training data."""
import json
import textwrap

examples = []


def add(user, silicat):
    examples.append({
        "messages": [
            {"role": "user", "content": user.strip()},
            {"role": "silicat", "content": silicat.strip()},
        ]
    })


def add_multi(turns):
    """turns: list of (role, content)."""
    msgs = [{"role": r, "content": c.strip()} for r, c in turns]
    examples.append({"messages": msgs})


# ---------------------------------------------------------------------------
# FILE I/O
# ---------------------------------------------------------------------------

add("Write a function to read a whole text file and return its contents as a string.",
"""```python
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
```""")

add("How do I read a file line by line into a list?",
"""```python
def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\\n") for line in f]
```""")

add("write a script to write a string to a text file",
"""```python
def write_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


write_text("output.txt", "Hello, world!\\n")
```""")

add("append a line to a log file",
"""```python
def append_line(path, line):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\\n")


append_line("app.log", "Server started")
```""")

add("Write a function that writes a list of strings to a file, one per line.",
"""```python
def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\\n".join(lines) + "\\n")
```""")

add("read a file safely and return an empty string if it does not exist",
"""```python
def safe_read(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
```""")

add("count the number of lines in a text file",
"""```python
def count_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)
```""")

add("Copy the contents of one file to another.",
"""```python
def copy_file(src, dst):
    with open(src, "r", encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        fout.write(fin.read())
```
For binary files use `shutil.copyfile(src, dst)` instead.""")

add("read a large file in chunks of 1024 bytes",
"""```python
def read_chunks(path, size=1024):
    with open(path, "rb") as f:
        while chunk := f.read(size):
            yield chunk
```""")

add("write a program to reverse the lines of a file",
"""```python
def reverse_file(path, out):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(out, "w", encoding="utf-8") as f:
        f.writelines(reversed(lines))
```""")

add("How can I read only the first N lines of a file?",
"""```python
from itertools import islice


def head(path, n=10):
    with open(path, "r", encoding="utf-8") as f:
        return list(islice(f, n))
```""")

add("get the last 10 lines of a file like tail",
"""```python
from collections import deque


def tail(path, n=10):
    with open(path, "r", encoding="utf-8") as f:
        return list(deque(f, maxlen=n))
```
`deque` with `maxlen` keeps only the last n lines while streaming, so memory stays small.""")

add("write text to a file only if it doesn't already exist",
"""```python
def write_if_absent(path, text):
    try:
        with open(path, "x", encoding="utf-8") as f:
            f.write(text)
        return True
    except FileExistsError:
        return False
```
Mode `"x"` fails if the file already exists, avoiding accidental overwrites.""")

add("Read a file and strip trailing whitespace from every line.",
"""```python
def read_stripped(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip() for line in f]
```""")

add("append multiple lines to a file at once",
"""```python
def append_lines(path, lines):
    with open(path, "a", encoding="utf-8") as f:
        f.writelines(line + "\\n" for line in lines)
```""")

# ---------------------------------------------------------------------------
# TEXT PROCESSING
# ---------------------------------------------------------------------------

add("Write a function that counts the words in a string.",
"""```python
def word_count(text):
    return len(text.split())
```""")

add("count how many times each word appears in a text",
"""```python
from collections import Counter


def word_frequencies(text):
    return Counter(text.lower().split())
```""")

add("find and replace all occurrences of a word in a string",
"""```python
def replace_word(text, old, new):
    return text.replace(old, new)
```""")

add("Write a program that reverses a string.",
"""```python
def reverse(s):
    return s[::-1]
```""")

add("check if a string is a palindrome ignoring case and spaces",
"""```python
def is_palindrome(s):
    cleaned = "".join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
```""")

add("convert a string to title case",
"""```python
def to_title(s):
    return s.title()
```""")

add("count the vowels in a string",
"""```python
def count_vowels(s):
    return sum(1 for c in s.lower() if c in "aeiou")
```""")

add("Write a function to capitalize the first letter of each word.",
"""```python
def capitalize_words(s):
    return " ".join(w.capitalize() for w in s.split())
```""")

add("remove all whitespace from a string",
"""```python
def remove_whitespace(s):
    return "".join(s.split())
```""")

add("split a string on commas and strip each part",
"""```python
def split_strip(s, sep=","):
    return [part.strip() for part in s.split(sep)]
```""")

add("count occurrences of a substring in a string",
"""```python
def count_substring(text, sub):
    return text.count(sub)
```""")

add("Write a function to truncate a string to n characters with an ellipsis.",
"""```python
def truncate(s, n):
    return s if len(s) <= n else s[: n - 1] + "\\u2026"
```""")

add("find the longest word in a sentence",
"""```python
def longest_word(sentence):
    return max(sentence.split(), key=len)
```""")

add("remove punctuation from a string",
"""```python
import string


def strip_punctuation(s):
    return s.translate(str.maketrans("", "", string.punctuation))
```""")

add("count the lines, words and characters in a text like wc",
"""```python
def wc(text):
    return {
        "lines": text.count("\\n") + (1 if text and not text.endswith("\\n") else 0),
        "words": len(text.split()),
        "chars": len(text),
    }
```""")

add("Write a function to check if a string contains only digits.",
"""```python
def is_numeric(s):
    return s.isdigit()
```""")

add("turn snake_case into camelCase",
"""```python
def to_camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])
```""")

add("convert camelCase to snake_case",
"""```python
import re


def to_snake(s):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
```""")

add("count unique words in a text",
"""```python
def unique_word_count(text):
    return len(set(text.lower().split()))
```""")

add("Write a function that finds the most common word in a string.",
"""```python
from collections import Counter


def most_common_word(text):
    counts = Counter(text.lower().split())
    return counts.most_common(1)[0][0] if counts else None
```""")

add("wrap text to 40 columns",
"""```python
import textwrap


def wrap_text(text, width=40):
    return textwrap.fill(text, width=width)
```""")

add("remove duplicate lines from a string keeping order",
"""```python
def dedupe_lines(text):
    seen = set()
    out = []
    for line in text.splitlines():
        if line not in seen:
            seen.add(line)
            out.append(line)
    return "\\n".join(out)
```""")

add("Write a function to count how many sentences are in a paragraph.",
"""```python
import re


def count_sentences(text):
    return len([s for s in re.split(r"[.!?]+", text) if s.strip()])
```""")

add("pad a number with leading zeros to width 5",
"""```python
def pad(n, width=5):
    return str(n).zfill(width)
```""")

add("center a string within a field of 30 characters",
"""```python
def center(s, width=30, fill="*"):
    return s.center(width, fill)
```""")

# ---------------------------------------------------------------------------
# DIRECTORIES / FILESYSTEM
# ---------------------------------------------------------------------------

add("List all files in a directory.",
"""```python
import os


def list_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
```""")

add("find all .py files in a directory using pathlib",
"""```python
from pathlib import Path


def find_python_files(directory):
    return list(Path(directory).glob("*.py"))
```""")

add("recursively find all files with a given extension",
"""```python
from pathlib import Path


def find_by_extension(directory, ext):
    return list(Path(directory).rglob(f"*.{ext.lstrip('.')}"))
```""")

add("walk a directory tree and print every file path",
"""```python
import os


def walk_tree(root):
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            print(os.path.join(dirpath, name))
```""")

add("Write a function to get the total size of all files in a folder.",
"""```python
from pathlib import Path


def folder_size(directory):
    return sum(f.stat().st_size for f in Path(directory).rglob("*") if f.is_file())
```""")

add("create a directory if it doesn't exist",
"""```python
from pathlib import Path


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
```""")

add("delete all .tmp files in a directory",
"""```python
from pathlib import Path


def clean_tmp(directory):
    for f in Path(directory).glob("*.tmp"):
        f.unlink()
```""")

add("count files by extension in a folder",
"""```python
from collections import Counter
from pathlib import Path


def count_by_extension(directory):
    return Counter(f.suffix.lower() for f in Path(directory).iterdir() if f.is_file())
```""")

add("Write a function that lists subdirectories of a folder.",
"""```python
from pathlib import Path


def list_subdirs(directory):
    return [p.name for p in Path(directory).iterdir() if p.is_dir()]
```""")

add("find the most recently modified file in a directory",
"""```python
from pathlib import Path


def newest_file(directory):
    files = [f for f in Path(directory).iterdir() if f.is_file()]
    return max(files, key=lambda f: f.stat().st_mtime, default=None)
```""")

add("get the file extension of a path",
"""```python
from pathlib import Path


def extension(path):
    return Path(path).suffix
```""")

add("rename all files in a folder to lowercase",
"""```python
from pathlib import Path


def lowercase_names(directory):
    for f in Path(directory).iterdir():
        if f.is_file():
            f.rename(f.with_name(f.name.lower()))
```""")

add("move all images into an 'images' subfolder",
"""```python
import shutil
from pathlib import Path


def collect_images(directory):
    exts = {".jpg", ".jpeg", ".png", ".gif"}
    dest = Path(directory) / "images"
    dest.mkdir(exist_ok=True)
    for f in Path(directory).iterdir():
        if f.is_file() and f.suffix.lower() in exts:
            shutil.move(str(f), str(dest / f.name))
```""")

# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

add("Read a CSV file into a list of dictionaries.",
"""```python
import csv


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
```""")

add("write a list of dicts to a CSV file",
"""```python
import csv


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
```""")

add("sum a numeric column in a CSV file",
"""```python
import csv


def sum_column(path, column):
    with open(path, newline="", encoding="utf-8") as f:
        return sum(float(row[column]) for row in csv.DictReader(f))
```""")

add("convert a CSV file to JSON",
"""```python
import csv
import json


def csv_to_json(csv_path, json_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
```""")

add("Write a function to filter CSV rows where a column equals a value.",
"""```python
import csv


def filter_rows(path, column, value):
    with open(path, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row[column] == value]
```""")

add("read a tab separated values file",
"""```python
import csv


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\\t"))
```""")

add("count the rows in a CSV file excluding the header",
"""```python
import csv


def row_count(path):
    with open(path, newline="", encoding="utf-8") as f:
        next(f, None)  # skip header
        return sum(1 for _ in f)
```""")

add("Write a program to extract one column from a CSV into a list.",
"""```python
import csv


def get_column(path, column):
    with open(path, newline="", encoding="utf-8") as f:
        return [row[column] for row in csv.DictReader(f)]
```""")

add("sort a CSV file by a column and write it back out",
"""```python
import csv


def sort_csv(in_path, out_path, column):
    with open(in_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = sorted(reader, key=lambda r: r[column])
        fields = reader.fieldnames
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
```""")

add("merge two CSV files with the same columns",
"""```python
import csv


def merge_csv(paths, out_path):
    rows = []
    fields = None
    for p in paths:
        with open(p, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames
            rows.extend(reader)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
```""")

# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------

add("Load a JSON file into a Python object.",
"""```python
import json


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
```""")

add("write a dictionary to a JSON file with pretty printing",
"""```python
import json


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```""")

add("parse a JSON string and handle errors",
"""```python
import json


def parse_json(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return None
```""")

add("pretty print a JSON string",
"""```python
import json


def pretty(s):
    return json.dumps(json.loads(s), indent=2, sort_keys=True)
```""")

add("Write a function to update a value in a JSON file.",
"""```python
import json


def update_json(path, key, value):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data[key] = value
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
```""")

add("merge two JSON objects",
"""```python
def merge(a, b):
    return {**a, **b}
```""")

add("read a JSON lines (jsonl) file into a list",
"""```python
import json


def read_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
```""")

add("write a list of dicts to a JSON lines file",
"""```python
import json


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\\n")
```""")

add("Write a function to flatten a nested JSON dict.",
"""```python
def flatten(d, parent="", sep="."):
    items = {}
    for k, v in d.items():
        key = f"{parent}{sep}{k}" if parent else k
        if isinstance(v, dict):
            items.update(flatten(v, key, sep))
        else:
            items[key] = v
    return items
```""")

# ---------------------------------------------------------------------------
# CLI / argparse
# ---------------------------------------------------------------------------

add("Write a CLI tool that takes a filename argument and prints its line count.",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser(description="Count lines in a file")
    parser.add_argument("filename")
    args = parser.parse_args()
    with open(args.filename, encoding="utf-8") as f:
        print(sum(1 for _ in f))


if __name__ == "__main__":
    main()
```""")

add("make a command line program with a --verbose flag",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()
    if args.verbose:
        print("Verbose mode on")


if __name__ == "__main__":
    main()
```""")

add("argparse program that accepts multiple input files",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="one or more files")
    args = parser.parse_args()
    for f in args.files:
        print(f)


if __name__ == "__main__":
    main()
```""")

add("Write a CLI with an integer option that has a default.",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--count", type=int, default=10)
    args = parser.parse_args()
    print(args.count)


if __name__ == "__main__":
    main()
```""")

add("argparse tool with subcommands add and remove",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    add_p = sub.add_parser("add")
    add_p.add_argument("item")
    rm_p = sub.add_parser("remove")
    rm_p.add_argument("item")
    args = parser.parse_args()
    print(f"{args.command}: {args.item}")


if __name__ == "__main__":
    main()
```""")

add("CLI that reads from stdin if no file is given",
"""```python
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    args = parser.parse_args()
    print(args.file.read())


if __name__ == "__main__":
    main()
```""")

add("argparse with a choice restricted to a few values",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--level", choices=["low", "medium", "high"], default="low")
    args = parser.parse_args()
    print(args.level)


if __name__ == "__main__":
    main()
```""")

# ---------------------------------------------------------------------------
# ENVIRONMENT VARIABLES / CONFIG
# ---------------------------------------------------------------------------

add("read an environment variable with a default value",
"""```python
import os

debug = os.environ.get("DEBUG", "false")
```""")

add("Write a function that requires an env var and raises if missing.",
"""```python
import os


def require_env(name):
    value = os.environ.get(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
```""")

add("load a simple key=value config file into a dict",
"""```python
def load_config(path):
    config = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config
```""")

add("read a config using the configparser module",
"""```python
import configparser


def read_ini(path):
    parser = configparser.ConfigParser()
    parser.read(path)
    return {s: dict(parser.items(s)) for s in parser.sections()}
```""")

add("get a boolean environment variable",
"""```python
import os


def env_bool(name, default=False):
    val = os.environ.get(name)
    if val is None:
        return default
    return val.lower() in ("1", "true", "yes", "on")
```""")

add("Write a function to load a .env file into os.environ.",
"""```python
import os


def load_dotenv(path=".env"):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
```""")

# ---------------------------------------------------------------------------
# DATES / TIMESTAMPS
# ---------------------------------------------------------------------------

add("Get the current date and time as a formatted string.",
"""```python
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```""")

add("parse a date string in the format YYYY-MM-DD",
"""```python
from datetime import datetime


def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()
```""")

add("calculate the number of days between two dates",
"""```python
from datetime import date


def days_between(a, b):
    return abs((b - a).days)
```""")

add("Write a function to add days to a date.",
"""```python
from datetime import date, timedelta


def add_days(d, n):
    return d + timedelta(days=n)
```""")

add("get a unix timestamp for the current time",
"""```python
import time

ts = int(time.time())
```""")

add("convert a unix timestamp to a readable date",
"""```python
from datetime import datetime


def ts_to_str(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
```""")

add("Write a function to get the day of the week for a date.",
"""```python
from datetime import date


def weekday_name(d):
    return d.strftime("%A")
```""")

add("how many days until the new year",
"""```python
from datetime import date


def days_until_new_year():
    today = date.today()
    ny = date(today.year + 1, 1, 1)
    return (ny - today).days
```""")

add("format the current time as an ISO 8601 string in UTC",
"""```python
from datetime import datetime, timezone

iso = datetime.now(timezone.utc).isoformat()
```""")

add("compute someone's age from their birth date",
"""```python
from datetime import date


def age(birth):
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
```""")

add("Write a function that returns the first day of the current month.",
"""```python
from datetime import date


def month_start():
    today = date.today()
    return today.replace(day=1)
```""")

add("measure how long a block of code takes to run",
"""```python
import time

start = time.perf_counter()
# ... work ...
elapsed = time.perf_counter() - start
print(f"Took {elapsed:.3f}s")
```""")

# ---------------------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------------------

add("Write a function to validate an email address.",
"""```python
import re

EMAIL_RE = re.compile(r"^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$")


def is_valid_email(email):
    return bool(EMAIL_RE.match(email))
```""")

add("validate a US phone number",
"""```python
import re

PHONE_RE = re.compile(r"^\\(?\\d{3}\\)?[\\s.-]?\\d{3}[\\s.-]?\\d{4}$")


def is_valid_phone(number):
    return bool(PHONE_RE.match(number.strip()))
```""")

add("check that a password is strong enough",
"""```python
import re


def is_strong(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\\d", password)
        and re.search(r"[^\\w\\s]", password)
    ) is not None
```""")

add("Write a function to validate a URL.",
"""```python
import re

URL_RE = re.compile(r"^https?://[\\w.-]+(?:\\:\\d+)?(?:/[^\\s]*)?$")


def is_valid_url(url):
    return bool(URL_RE.match(url))
```""")

add("validate that a string is a positive integer",
"""```python
def is_positive_int(s):
    return s.isdigit() and int(s) > 0
```""")

add("prompt the user for an integer and keep asking until valid",
"""```python
def ask_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")
```""")

add("validate a date string and return True/False",
"""```python
from datetime import datetime


def is_valid_date(s, fmt="%Y-%m-%d"):
    try:
        datetime.strptime(s, fmt)
        return True
    except ValueError:
        return False
```""")

add("Write a function to check if an IPv4 address is valid.",
"""```python
def is_valid_ipv4(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 and (p == "0" or not p.startswith("0")) for p in parts)
```""")

# ---------------------------------------------------------------------------
# ENCODING / HASHING
# ---------------------------------------------------------------------------

add("base64 encode a string.",
"""```python
import base64


def b64encode(s):
    return base64.b64encode(s.encode("utf-8")).decode("ascii")
```""")

add("decode a base64 string",
"""```python
import base64


def b64decode(s):
    return base64.b64decode(s).decode("utf-8")
```""")

add("compute the md5 hash of a string",
"""```python
import hashlib


def md5(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()
```""")

add("Write a function to compute the SHA-256 hash of a file.",
"""```python
import hashlib


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
```
Reading in chunks keeps memory low for large files.""")

add("url encode a query parameter",
"""```python
from urllib.parse import quote

encoded = quote("hello world & friends")
```""")

add("build a url with query parameters",
"""```python
from urllib.parse import urlencode

params = {"q": "python", "page": 2}
query = urlencode(params)
url = f"https://example.com/search?{query}"
```""")

add("hash a password securely with a salt",
"""```python
import hashlib
import os


def hash_password(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return salt.hex() + ":" + digest.hex()


def verify_password(password, stored):
    salt_hex, digest_hex = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return digest.hex() == digest_hex
```
PBKDF2 with a random salt and many iterations makes brute-forcing far harder than a plain hash.""")

add("Write a function to url-decode a string.",
"""```python
from urllib.parse import unquote


def url_decode(s):
    return unquote(s)
```""")

add("encode bytes as hex and back",
"""```python
data = b"hello"
hex_str = data.hex()
back = bytes.fromhex(hex_str)
```""")

# ---------------------------------------------------------------------------
# SMALL UTILITIES
# ---------------------------------------------------------------------------

add("Write a password generator.",
"""```python
import secrets
import string


def generate_password(length=16):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))
```
`secrets` is used instead of `random` because it is cryptographically secure.""")

add("roll a six sided dice",
"""```python
import random


def roll():
    return random.randint(1, 6)
```""")

add("write a dice roller that rolls N dice with S sides",
"""```python
import random


def roll_dice(count, sides):
    return [random.randint(1, sides) for _ in range(count)]
```""")

add("convert celsius to fahrenheit",
"""```python
def c_to_f(c):
    return c * 9 / 5 + 32
```""")

add("Write a temperature converter for both directions.",
"""```python
def c_to_f(c):
    return c * 9 / 5 + 32


def f_to_c(f):
    return (f - 32) * 5 / 9
```""")

add("calculate BMI",
"""```python
def bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)
```""")

add("Write a BMI calculator that also returns the category.",
"""```python
def bmi_category(weight_kg, height_m):
    value = weight_kg / (height_m ** 2)
    if value < 18.5:
        cat = "underweight"
    elif value < 25:
        cat = "normal"
    elif value < 30:
        cat = "overweight"
    else:
        cat = "obese"
    return round(value, 1), cat
```""")

add("write a simple calculator that evaluates +, -, *, /",
"""```python
def calculate(a, op, b):
    ops = {"+": lambda x, y: x + y, "-": lambda x, y: x - y,
           "*": lambda x, y: x * y, "/": lambda x, y: x / y}
    if op not in ops:
        raise ValueError(f"Unknown operator: {op}")
    return ops[op](a, b)
```""")

add("generate a random hex color",
"""```python
import random


def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
```""")

add("Write a function that picks a random item from a list.",
"""```python
import random


def pick(items):
    return random.choice(items)
```""")

add("shuffle a deck of cards",
"""```python
import random


def make_deck():
    ranks = "2 3 4 5 6 7 8 9 10 J Q K A".split()
    suits = "Hearts Diamonds Clubs Spades".split()
    deck = [f"{r} of {s}" for s in suits for r in ranks]
    random.shuffle(deck)
    return deck
```""")

add("write a number guessing game",
"""```python
import random


def guessing_game():
    secret = random.randint(1, 100)
    while True:
        guess = int(input("Guess (1-100): "))
        if guess < secret:
            print("Too low")
        elif guess > secret:
            print("Too high")
        else:
            print("Correct!")
            return
```""")

add("generate a random token for a URL",
"""```python
import secrets

token = secrets.token_urlsafe(32)
```""")

add("Write a function to generate a UUID.",
"""```python
import uuid


def new_id():
    return str(uuid.uuid4())
```""")

add("convert kilometers to miles",
"""```python
def km_to_miles(km):
    return km * 0.621371
```""")

add("write a function that returns the nth fibonacci number",
"""```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```""")

add("check if a number is prime",
"""```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True
```""")

add("Write a FizzBuzz program.",
"""```python
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
```""")

# ---------------------------------------------------------------------------
# FILE RENAMER / DUPLICATE FINDER
# ---------------------------------------------------------------------------

add("Write a file renamer that adds a prefix to every file in a folder.",
"""```python
from pathlib import Path


def add_prefix(directory, prefix):
    for f in Path(directory).iterdir():
        if f.is_file():
            f.rename(f.with_name(prefix + f.name))
```""")

add("batch rename files to a sequence like img_001.jpg",
"""```python
from pathlib import Path


def sequence_rename(directory, base="img"):
    files = sorted(p for p in Path(directory).iterdir() if p.is_file())
    for i, f in enumerate(files, start=1):
        f.rename(f.with_name(f"{base}_{i:03d}{f.suffix}"))
```""")

add("find duplicate files by content hash",
"""```python
import hashlib
from collections import defaultdict
from pathlib import Path


def find_duplicates(directory):
    hashes = defaultdict(list)
    for f in Path(directory).rglob("*"):
        if f.is_file():
            digest = hashlib.md5(f.read_bytes()).hexdigest()
            hashes[digest].append(str(f))
    return {h: paths for h, paths in hashes.items() if len(paths) > 1}
```""")

add("Write a function to replace spaces with underscores in all filenames.",
"""```python
from pathlib import Path


def despace(directory):
    for f in Path(directory).iterdir():
        if f.is_file() and " " in f.name:
            f.rename(f.with_name(f.name.replace(" ", "_")))
```""")

# ---------------------------------------------------------------------------
# SCRAPERS / REQUESTS
# ---------------------------------------------------------------------------

add("download a file from a URL.",
"""```python
import requests


def download(url, path):
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    with open(path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
```""")

add("fetch JSON from an API endpoint",
"""```python
import requests


def get_json(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()
```""")

add("Write a function to post JSON data to an API.",
"""```python
import requests


def post_json(url, payload):
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()
```""")

add("scrape all the links from a web page",
"""```python
import requests
from bs4 import BeautifulSoup


def get_links(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]
```""")

add("get the title of a web page",
"""```python
import requests
from bs4 import BeautifulSoup


def page_title(url):
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.title.string if soup.title else None
```""")

add("Write a function to check if a website is up.",
"""```python
import requests


def is_up(url):
    try:
        return requests.head(url, timeout=5).status_code < 400
    except requests.RequestException:
        return False
```""")

add("send a GET request with custom headers",
"""```python
import requests


def fetch(url):
    headers = {"User-Agent": "MyBot/1.0", "Accept": "application/json"}
    return requests.get(url, headers=headers, timeout=10)
```""")

# ---------------------------------------------------------------------------
# RETRY / RATE LIMIT
# ---------------------------------------------------------------------------

add("Write a retry decorator that retries on exception.",
"""```python
import functools
import time


def retry(times=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last = None
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last = e
                    time.sleep(delay)
            raise last
        return wrapper
    return decorator
```""")

add("retry an HTTP request with exponential backoff",
"""```python
import time

import requests


def get_with_backoff(url, retries=5):
    delay = 1.0
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
            delay *= 2
```""")

add("write a simple rate limiter that allows N calls per second",
"""```python
import time


class RateLimiter:
    def __init__(self, calls_per_second):
        self.min_interval = 1.0 / calls_per_second
        self.last = 0.0

    def wait(self):
        elapsed = time.monotonic() - self.last
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last = time.monotonic()
```""")

add("Write a token bucket rate limiter.",
"""```python
import time


class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.monotonic()

    def allow(self):
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```""")

# ---------------------------------------------------------------------------
# REPORTS / TEMPLATING
# ---------------------------------------------------------------------------

add("Write a function to format a list of dicts as an aligned table.",
"""```python
def format_table(rows, columns):
    widths = {c: max(len(c), *(len(str(r[c])) for r in rows)) for c in columns}
    header = "  ".join(c.ljust(widths[c]) for c in columns)
    lines = [header, "  ".join("-" * widths[c] for c in columns)]
    for r in rows:
        lines.append("  ".join(str(r[c]).ljust(widths[c]) for c in columns))
    return "\\n".join(lines)
```""")

add("render a template string with named placeholders",
"""```python
from string import Template


def render(template, **values):
    return Template(template).safe_substitute(values)
```""")

add("generate a markdown table from data",
"""```python
def to_markdown_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\\n".join(lines)
```""")

add("Write a function to make a progress bar string.",
"""```python
def progress_bar(current, total, width=30):
    filled = int(width * current / total)
    bar = "#" * filled + "-" * (width - filled)
    pct = 100 * current / total
    return f"[{bar}] {pct:5.1f}%"
```""")

add("format a number with thousands separators",
"""```python
def with_commas(n):
    return f"{n:,}"
```""")

add("format bytes as a human readable size",
"""```python
def human_size(num):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num) < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} PB"
```""")

add("Write a function to format seconds as HH:MM:SS.",
"""```python
def format_duration(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
```""")

# ---------------------------------------------------------------------------
# MISC DATA MUNGING
# ---------------------------------------------------------------------------

add("group a list of dicts by a key",
"""```python
from collections import defaultdict


def group_by(items, key):
    groups = defaultdict(list)
    for item in items:
        groups[item[key]].append(item)
    return dict(groups)
```""")

add("Write a function to chunk a list into groups of n.",
"""```python
def chunk(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]
```""")

add("flatten a list of lists",
"""```python
def flatten(nested):
    return [x for sub in nested for x in sub]
```""")

add("remove duplicates from a list while preserving order",
"""```python
def dedupe(items):
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]
```""")

add("Write a function to find the intersection of two lists.",
"""```python
def intersection(a, b):
    return list(set(a) & set(b))
```""")

add("count items in a list",
"""```python
from collections import Counter


def counts(items):
    return Counter(items)
```""")

add("invert a dictionary",
"""```python
def invert(d):
    return {v: k for k, v in d.items()}
```""")

add("Write a function to sort a dict by its values.",
"""```python
def sort_by_value(d, reverse=False):
    return dict(sorted(d.items(), key=lambda kv: kv[1], reverse=reverse))
```""")

add("merge a list of dicts into one",
"""```python
def merge_dicts(dicts):
    result = {}
    for d in dicts:
        result.update(d)
    return result
```""")

add("find the top 3 most common elements in a list",
"""```python
from collections import Counter


def top_three(items):
    return Counter(items).most_common(3)
```""")

# ---------------------------------------------------------------------------
# MULTI-TURN CONVERSATIONS
# ---------------------------------------------------------------------------

add_multi([
    ("user", "Write a simple todo list in Python that I can add items to."),
    ("silicat", """```python
todos = []


def add_todo(item):
    todos.append(item)


def show_todos():
    for i, item in enumerate(todos, 1):
        print(f"{i}. {item}")
```"""),
    ("user", "Add a way to remove an item by its number."),
    ("silicat", """```python
todos = []


def add_todo(item):
    todos.append(item)


def remove_todo(number):
    if 1 <= number <= len(todos):
        todos.pop(number - 1)


def show_todos():
    for i, item in enumerate(todos, 1):
        print(f"{i}. {item}")
```"""),
    ("user", "Now let me mark items as done instead of just plain strings."),
    ("silicat", """Store each item as a dict with a `done` flag.

```python
todos = []


def add_todo(item):
    todos.append({"text": item, "done": False})


def remove_todo(number):
    if 1 <= number <= len(todos):
        todos.pop(number - 1)


def mark_done(number):
    if 1 <= number <= len(todos):
        todos[number - 1]["done"] = True


def show_todos():
    for i, item in enumerate(todos, 1):
        mark = "x" if item["done"] else " "
        print(f"{i}. [{mark}] {item['text']}")
```"""),
    ("user", "Save the list to a JSON file."),
    ("silicat", """```python
import json

todos = []


def add_todo(item):
    todos.append({"text": item, "done": False})


def remove_todo(number):
    if 1 <= number <= len(todos):
        todos.pop(number - 1)


def mark_done(number):
    if 1 <= number <= len(todos):
        todos[number - 1]["done"] = True


def show_todos():
    for i, item in enumerate(todos, 1):
        mark = "x" if item["done"] else " "
        print(f"{i}. [{mark}] {item['text']}")


def save(path="todos.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)
```"""),
    ("user", "And load it back when the program starts."),
    ("silicat", """```python
import json
import os

todos = []


def load(path="todos.json"):
    global todos
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            todos = json.load(f)


def add_todo(item):
    todos.append({"text": item, "done": False})


def remove_todo(number):
    if 1 <= number <= len(todos):
        todos.pop(number - 1)


def mark_done(number):
    if 1 <= number <= len(todos):
        todos[number - 1]["done"] = True


def show_todos():
    for i, item in enumerate(todos, 1):
        mark = "x" if item["done"] else " "
        print(f"{i}. [{mark}] {item['text']}")


def save(path="todos.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)


if __name__ == "__main__":
    load()
    # ... interact ...
    save()
```
Calling `load()` at startup repopulates `todos`, and `save()` before exit persists changes."""),
])

add_multi([
    ("user", "Write a function that counts words in a file."),
    ("silicat", """```python
def count_words(path):
    with open(path, encoding="utf-8") as f:
        return len(f.read().split())
```"""),
    ("user", "Make it return the count of each unique word too."),
    ("silicat", """```python
from collections import Counter


def count_words(path):
    with open(path, encoding="utf-8") as f:
        words = f.read().lower().split()
    return Counter(words)
```"""),
    ("user", "Strip punctuation so 'word.' and 'word' count as the same."),
    ("silicat", """```python
import string
from collections import Counter


def count_words(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return Counter(text.split())
```"""),
    ("user", "Print the top 10 words."),
    ("silicat", """```python
import string
from collections import Counter


def count_words(path):
    with open(path, encoding="utf-8") as f:
        text = f.read().lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return Counter(text.split())


def print_top(path, n=10):
    for word, count in count_words(path).most_common(n):
        print(f"{count:>5}  {word}")
```"""),
])

add_multi([
    ("user", "I want a CLI tool to convert a CSV file to JSON."),
    ("silicat", """```python
import argparse
import csv
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("json_file")
    args = parser.parse_args()
    with open(args.csv_file, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(args.json_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)


if __name__ == "__main__":
    main()
```"""),
    ("user", "Make the output file optional and print to stdout if not given."),
    ("silicat", """```python
import argparse
import csv
import json
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("json_file", nargs="?")
    args = parser.parse_args()
    with open(args.csv_file, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    text = json.dumps(rows, indent=2)
    if args.json_file:
        with open(args.json_file, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text + "\\n")


if __name__ == "__main__":
    main()
```"""),
    ("user", "Add a --delimiter option for the CSV."),
    ("silicat", """```python
import argparse
import csv
import json
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("json_file", nargs="?")
    parser.add_argument("--delimiter", default=",")
    args = parser.parse_args()
    with open(args.csv_file, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter=args.delimiter))
    text = json.dumps(rows, indent=2)
    if args.json_file:
        with open(args.json_file, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text + "\\n")


if __name__ == "__main__":
    main()
```"""),
])

add_multi([
    ("user", "Write a function to generate a random password."),
    ("silicat", """```python
import secrets
import string


def generate(length=12):
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))
```"""),
    ("user", "Let me include symbols optionally."),
    ("silicat", """```python
import secrets
import string


def generate(length=12, symbols=False):
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += string.punctuation
    return "".join(secrets.choice(chars) for _ in range(length))
```"""),
    ("user", "Guarantee at least one digit and one uppercase letter."),
    ("silicat", """```python
import secrets
import string


def generate(length=12, symbols=False):
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += string.punctuation
    while True:
        pw = "".join(secrets.choice(chars) for _ in range(length))
        if any(c.isdigit() for c in pw) and any(c.isupper() for c in pw):
            return pw
```
Re-rolling until the constraints are met keeps the distribution uniform and the code simple."""),
    ("user", "Turn it into a command line tool."),
    ("silicat", """```python
import argparse
import secrets
import string


def generate(length=12, symbols=False):
    chars = string.ascii_letters + string.digits
    if symbols:
        chars += string.punctuation
    while True:
        pw = "".join(secrets.choice(chars) for _ in range(length))
        if any(c.isdigit() for c in pw) and any(c.isupper() for c in pw):
            return pw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length", type=int, default=12)
    parser.add_argument("-s", "--symbols", action="store_true")
    args = parser.parse_args()
    print(generate(args.length, args.symbols))


if __name__ == "__main__":
    main()
```"""),
])

add_multi([
    ("user", "Help me read a log file and find error lines."),
    ("silicat", """```python
def find_errors(path):
    with open(path, encoding="utf-8") as f:
        return [line.rstrip() for line in f if "ERROR" in line]
```"""),
    ("user", "Count how many errors there are per day. The lines start with a date like 2024-01-15."),
    ("silicat", """```python
from collections import Counter


def errors_per_day(path):
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                date = line[:10]
                counts[date] += 1
    return counts
```"""),
    ("user", "Write the summary to a CSV file."),
    ("silicat", """```python
import csv
from collections import Counter


def errors_per_day(path):
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                counts[line[:10]] += 1
    return counts


def write_summary(log_path, out_path):
    counts = errors_per_day(log_path)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "error_count"])
        for date in sorted(counts):
            writer.writerow([date, counts[date]])
```"""),
])

add_multi([
    ("user", "Write a contact book that stores name and phone in a dict."),
    ("silicat", """```python
contacts = {}


def add_contact(name, phone):
    contacts[name] = phone


def get_contact(name):
    return contacts.get(name)
```"""),
    ("user", "Persist it to a JSON file."),
    ("silicat", """```python
import json

contacts = {}


def add_contact(name, phone):
    contacts[name] = phone


def get_contact(name):
    return contacts.get(name)


def save(path="contacts.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)
```"""),
    ("user", "Load existing contacts on startup."),
    ("silicat", """```python
import json
import os

contacts = {}


def load(path="contacts.json"):
    global contacts
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            contacts = json.load(f)


def add_contact(name, phone):
    contacts[name] = phone


def get_contact(name):
    return contacts.get(name)


def save(path="contacts.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)
```"""),
    ("user", "Add search by partial name match."),
    ("silicat", """```python
import json
import os

contacts = {}


def load(path="contacts.json"):
    global contacts
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            contacts = json.load(f)


def add_contact(name, phone):
    contacts[name] = phone


def get_contact(name):
    return contacts.get(name)


def search(query):
    q = query.lower()
    return {name: phone for name, phone in contacts.items() if q in name.lower()}


def save(path="contacts.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)
```"""),
])

add_multi([
    ("user", "Write something to rename all the files in a folder."),
    ("silicat", """What renaming do you want? Here's a starting point that lowercases every filename:

```python
from pathlib import Path


def rename_all(directory):
    for f in Path(directory).iterdir():
        if f.is_file():
            f.rename(f.with_name(f.name.lower()))
```"""),
    ("user", "Actually I want to add the file's modification date as a prefix."),
    ("silicat", """```python
from datetime import datetime
from pathlib import Path


def prefix_with_date(directory):
    for f in Path(directory).iterdir():
        if f.is_file():
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            prefix = mtime.strftime("%Y-%m-%d_")
            f.rename(f.with_name(prefix + f.name))
```"""),
    ("user", "Do a dry run first that just prints what it would do."),
    ("silicat", """```python
from datetime import datetime
from pathlib import Path


def prefix_with_date(directory, dry_run=False):
    for f in Path(directory).iterdir():
        if f.is_file():
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            new_name = mtime.strftime("%Y-%m-%d_") + f.name
            if dry_run:
                print(f"{f.name} -> {new_name}")
            else:
                f.rename(f.with_name(new_name))
```"""),
])

add_multi([
    ("user", "Make a function to fetch JSON from a URL."),
    ("silicat", """```python
import requests


def fetch(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()
```"""),
    ("user", "Add retries if it fails."),
    ("silicat", """```python
import time

import requests


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
```"""),
    ("user", "Cache the result to disk so repeated calls don't hit the network."),
    ("silicat", """```python
import hashlib
import json
import time
from pathlib import Path

import requests

CACHE_DIR = Path(".cache")


def fetch(url, retries=3):
    CACHE_DIR.mkdir(exist_ok=True)
    key = hashlib.md5(url.encode()).hexdigest()
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            cache_file.write_text(json.dumps(data), encoding="utf-8")
            return data
        except requests.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
```"""),
])

add_multi([
    ("user", "Write a temperature converter function."),
    ("silicat", """```python
def c_to_f(c):
    return c * 9 / 5 + 32
```"""),
    ("user", "Add fahrenheit to celsius and kelvin too."),
    ("silicat", """```python
def c_to_f(c):
    return c * 9 / 5 + 32


def f_to_c(f):
    return (f - 32) * 5 / 9


def c_to_k(c):
    return c + 273.15


def k_to_c(k):
    return k - 273.15
```"""),
    ("user", "Wrap it in an interactive command line menu."),
    ("silicat", """```python
def c_to_f(c):
    return c * 9 / 5 + 32


def f_to_c(f):
    return (f - 32) * 5 / 9


def c_to_k(c):
    return c + 273.15


def k_to_c(k):
    return k - 273.15


CONVERSIONS = {
    "1": ("C to F", c_to_f),
    "2": ("F to C", f_to_c),
    "3": ("C to K", c_to_k),
    "4": ("K to C", k_to_c),
}


def main():
    while True:
        for key, (label, _) in CONVERSIONS.items():
            print(f"{key}. {label}")
        choice = input("Choose (q to quit): ").strip()
        if choice == "q":
            break
        if choice in CONVERSIONS:
            value = float(input("Value: "))
            print(round(CONVERSIONS[choice][1](value), 2))


if __name__ == "__main__":
    main()
```"""),
])

add_multi([
    ("user", "I need to read a CSV of sales and total the revenue."),
    ("silicat", """```python
import csv


def total_revenue(path):
    with open(path, newline="", encoding="utf-8") as f:
        return sum(float(row["amount"]) for row in csv.DictReader(f))
```"""),
    ("user", "Break it down by region."),
    ("silicat", """```python
import csv
from collections import defaultdict


def revenue_by_region(path):
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row["region"]] += float(row["amount"])
    return dict(totals)
```"""),
    ("user", "Print it sorted from highest to lowest."),
    ("silicat", """```python
import csv
from collections import defaultdict


def revenue_by_region(path):
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row["region"]] += float(row["amount"])
    return dict(totals)


def report(path):
    totals = revenue_by_region(path)
    for region, amount in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{region:<15} {amount:>12,.2f}")
```"""),
])

add_multi([
    ("user", "Write a script that backs up a file by copying it with a timestamp."),
    ("silicat", """```python
import shutil
from datetime import datetime
from pathlib import Path


def backup(path):
    src = Path(path)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = src.with_name(f"{src.stem}_{stamp}{src.suffix}")
    shutil.copy2(src, dst)
    return dst
```"""),
    ("user", "Put backups in a 'backups' subfolder instead."),
    ("silicat", """```python
import shutil
from datetime import datetime
from pathlib import Path


def backup(path):
    src = Path(path)
    backup_dir = src.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = backup_dir / f"{src.stem}_{stamp}{src.suffix}"
    shutil.copy2(src, dst)
    return dst
```"""),
    ("user", "Only keep the 5 most recent backups."),
    ("silicat", """```python
import shutil
from datetime import datetime
from pathlib import Path


def backup(path, keep=5):
    src = Path(path)
    backup_dir = src.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = backup_dir / f"{src.stem}_{stamp}{src.suffix}"
    shutil.copy2(src, dst)

    backups = sorted(
        backup_dir.glob(f"{src.stem}_*{src.suffix}"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for old in backups[keep:]:
        old.unlink()
    return dst
```"""),
])

add_multi([
    ("user", "Write a function to validate an email."),
    ("silicat", """```python
import re

EMAIL_RE = re.compile(r"^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$")


def is_valid_email(email):
    return bool(EMAIL_RE.match(email))
```"""),
    ("user", "Read a file of emails, one per line, and split valid from invalid."),
    ("silicat", """```python
import re

EMAIL_RE = re.compile(r"^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$")


def is_valid_email(email):
    return bool(EMAIL_RE.match(email))


def validate_file(path):
    valid, invalid = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            email = line.strip()
            if not email:
                continue
            (valid if is_valid_email(email) else invalid).append(email)
    return valid, invalid
```"""),
    ("user", "Write the valid ones to valid.txt and invalid to invalid.txt."),
    ("silicat", """```python
import re

EMAIL_RE = re.compile(r"^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$")


def is_valid_email(email):
    return bool(EMAIL_RE.match(email))


def validate_file(path):
    valid, invalid = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            email = line.strip()
            if not email:
                continue
            (valid if is_valid_email(email) else invalid).append(email)
    return valid, invalid


def write_results(path):
    valid, invalid = validate_file(path)
    with open("valid.txt", "w", encoding="utf-8") as f:
        f.write("\\n".join(valid) + "\\n")
    with open("invalid.txt", "w", encoding="utf-8") as f:
        f.write("\\n".join(invalid) + "\\n")
```"""),
])

add_multi([
    ("user", "Make a stopwatch I can start and stop."),
    ("silicat", """```python
import time


class Stopwatch:
    def __init__(self):
        self._start = None

    def start(self):
        self._start = time.perf_counter()

    def stop(self):
        return time.perf_counter() - self._start
```"""),
    ("user", "Make it usable as a context manager."),
    ("silicat", """```python
import time


class Stopwatch:
    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self._start
```

```python
with Stopwatch() as sw:
    do_work()
print(sw.elapsed)
```"""),
])

add_multi([
    ("user", "Write a word frequency counter for a text file."),
    ("silicat", """```python
from collections import Counter


def word_freq(path):
    with open(path, encoding="utf-8") as f:
        return Counter(f.read().lower().split())
```"""),
    ("user", "Ignore common stop words like 'the', 'a', 'and'."),
    ("silicat", """```python
from collections import Counter

STOP_WORDS = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "it"}


def word_freq(path):
    with open(path, encoding="utf-8") as f:
        words = f.read().lower().split()
    return Counter(w for w in words if w not in STOP_WORDS)
```"""),
    ("user", "Export the top 20 to a CSV."),
    ("silicat", """```python
import csv
from collections import Counter

STOP_WORDS = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "it"}


def word_freq(path):
    with open(path, encoding="utf-8") as f:
        words = f.read().lower().split()
    return Counter(w for w in words if w not in STOP_WORDS)


def export_top(text_path, csv_path, n=20):
    freq = word_freq(text_path)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        writer.writerows(freq.most_common(n))
```"""),
])

# ---------------------------------------------------------------------------
# MORE SINGLE-TURN, varied phrasing
# ---------------------------------------------------------------------------

add("how do i read a json file in python",
"""```python
import json

with open("data.json", encoding="utf-8") as f:
    data = json.load(f)
```""")

add("script to count empty lines in a file",
"""```python
def count_empty_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if not line.strip())
```""")

add("Write a function that returns the number of files in a directory tree.",
"""```python
import os


def count_files(root):
    return sum(len(files) for _, _, files in os.walk(root))
```""")

add("convert a list of numbers to a comma separated string",
"""```python
def join_numbers(nums):
    return ",".join(str(n) for n in nums)
```""")

add("parse a comma separated string into a list of ints",
"""```python
def parse_ints(s):
    return [int(x) for x in s.split(",") if x.strip()]
```""")

add("Write a function to check if a file is empty.",
"""```python
import os


def is_empty(path):
    return os.path.getsize(path) == 0
```""")

add("read a file and number each line",
"""```python
def numbered(path):
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            print(f"{i}: {line.rstrip()}")
```""")

add("get the absolute path of a file",
"""```python
from pathlib import Path

abs_path = Path("file.txt").resolve()
```""")

add("Write a function to read a CSV and skip blank rows.",
"""```python
import csv


def read_nonblank(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [row for row in csv.reader(f) if any(cell.strip() for cell in row)]
```""")

add("count words from standard input",
"""```python
import sys

text = sys.stdin.read()
print(len(text.split()))
```""")

add("replace tabs with spaces in a file",
"""```python
def detab(path, width=4):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.expandtabs(width))
```""")

add("Write a function to extract all email addresses from text.",
"""```python
import re


def extract_emails(text):
    return re.findall(r"[\\w.+-]+@[\\w-]+\\.[\\w.-]+", text)
```""")

add("extract all numbers from a string",
"""```python
import re


def extract_numbers(text):
    return [float(x) for x in re.findall(r"-?\\d+\\.?\\d*", text)]
```""")

add("count how many times a pattern matches in a file",
"""```python
import re


def count_matches(path, pattern):
    regex = re.compile(pattern)
    with open(path, encoding="utf-8") as f:
        return sum(len(regex.findall(line)) for line in f)
```""")

add("Write a function to slugify a string for a URL.",
"""```python
import re


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\\w\\s-]", "", text)
    return re.sub(r"[\\s_-]+", "-", text).strip("-")
```""")

add("read a file and return the longest line",
"""```python
def longest_line(path):
    with open(path, encoding="utf-8") as f:
        return max(f, key=len, default="").rstrip()
```""")

add("write csv rows from a list of lists",
"""```python
import csv


def write_rows(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
```""")

add("Write a function to pretty print bytes per second as a transfer rate.",
"""```python
def transfer_rate(bytes_, seconds):
    rate = bytes_ / seconds if seconds else 0
    for unit in ["B/s", "KB/s", "MB/s", "GB/s"]:
        if rate < 1024:
            return f"{rate:.1f} {unit}"
        rate /= 1024
    return f"{rate:.1f} TB/s"
```""")

add("zip two lists into a dictionary",
"""```python
def to_dict(keys, values):
    return dict(zip(keys, values))
```""")

add("read environment variable PORT as an int with default 8000",
"""```python
import os

port = int(os.environ.get("PORT", "8000"))
```""")

add("Write a function to compute the average of numbers in a file, one per line.",
"""```python
def average(path):
    with open(path, encoding="utf-8") as f:
        nums = [float(line) for line in f if line.strip()]
    return sum(nums) / len(nums) if nums else 0
```""")

add("create a zip archive of a folder",
"""```python
import shutil


def zip_folder(folder, archive_name):
    shutil.make_archive(archive_name, "zip", folder)
```""")

add("extract a zip file",
"""```python
import zipfile


def unzip(path, dest):
    with zipfile.ZipFile(path) as z:
        z.extractall(dest)
```""")

add("Write a function to list the contents of a zip file.",
"""```python
import zipfile


def list_zip(path):
    with zipfile.ZipFile(path) as z:
        return z.namelist()
```""")

add("gzip compress a text file",
"""```python
import gzip
import shutil


def gzip_file(path):
    with open(path, "rb") as fin, gzip.open(path + ".gz", "wb") as fout:
        shutil.copyfileobj(fin, fout)
```""")

add("read a gzip compressed text file",
"""```python
import gzip


def read_gzip(path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return f.read()
```""")

add("Write a function that returns True if two files have identical content.",
"""```python
import filecmp


def same_content(a, b):
    return filecmp.cmp(a, b, shallow=False)
```""")

add("count distinct lines in a file",
"""```python
def distinct_count(path):
    with open(path, encoding="utf-8") as f:
        return len(set(line.rstrip("\\n") for line in f))
```""")

add("write a function to convert minutes to a human friendly string like '2h 5m'",
"""```python
def humanize_minutes(minutes):
    h, m = divmod(int(minutes), 60)
    parts = []
    if h:
        parts.append(f"{h}h")
    if m or not parts:
        parts.append(f"{m}m")
    return " ".join(parts)
```""")

add("Write a function to roll dice and return the sum.",
"""```python
import random


def roll_sum(count=2, sides=6):
    return sum(random.randint(1, sides) for _ in range(count))
```""")

add("simple coin flip",
"""```python
import random


def flip():
    return random.choice(["heads", "tails"])
```""")

add("generate a list of random numbers",
"""```python
import random


def random_numbers(n, low=0, high=100):
    return [random.randint(low, high) for _ in range(n)]
```""")

add("Write a Caesar cipher encrypt function.",
"""```python
def caesar(text, shift):
    result = []
    for c in text:
        if c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return "".join(result)
```""")

add("rot13 a string",
"""```python
import codecs


def rot13(s):
    return codecs.encode(s, "rot_13")
```""")

add("count characters excluding spaces",
"""```python
def char_count(s):
    return len(s.replace(" ", ""))
```""")

add("Write a function to title-case a headline but keep small words lowercase.",
"""```python
SMALL = {"a", "an", "and", "the", "of", "in", "on", "for", "to", "or"}


def headline(text):
    words = text.lower().split()
    return " ".join(
        w.capitalize() if i == 0 or w not in SMALL else w
        for i, w in enumerate(words)
    )
```""")

add("convert a dict to query string",
"""```python
from urllib.parse import urlencode


def to_query(params):
    return urlencode(params)
```""")

add("parse a query string into a dict",
"""```python
from urllib.parse import parse_qs


def from_query(query):
    return {k: v[0] for k, v in parse_qs(query).items()}
```""")

add("Write a function that returns the file's MIME type by extension.",
"""```python
import mimetypes


def guess_type(path):
    return mimetypes.guess_type(path)[0]
```""")

add("get just the filename without extension",
"""```python
from pathlib import Path


def stem(path):
    return Path(path).stem
```""")

add("read first column of every line split on whitespace",
"""```python
def first_columns(path):
    with open(path, encoding="utf-8") as f:
        return [line.split()[0] for line in f if line.strip()]
```""")

add("Write a function to count lines matching a keyword.",
"""```python
def count_keyword(path, keyword):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if keyword in line)
```""")

add("grep-like search printing matching lines with line numbers",
"""```python
def grep(path, pattern):
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if pattern in line:
                print(f"{i}: {line.rstrip()}")
```""")

add("write a function to merge multiple text files into one",
"""```python
def merge_files(paths, out_path):
    with open(out_path, "w", encoding="utf-8") as out:
        for p in paths:
            with open(p, encoding="utf-8") as f:
                out.write(f.read())
```""")

add("Write a function to split a big file into smaller files of N lines each.",
"""```python
def split_file(path, lines_per_file=1000):
    with open(path, encoding="utf-8") as f:
        chunk = []
        index = 0
        for line in f:
            chunk.append(line)
            if len(chunk) >= lines_per_file:
                with open(f"{path}.part{index}", "w", encoding="utf-8") as out:
                    out.writelines(chunk)
                chunk = []
                index += 1
        if chunk:
            with open(f"{path}.part{index}", "w", encoding="utf-8") as out:
                out.writelines(chunk)
```""")

add("count word occurrences case-insensitively and ignoring punctuation",
"""```python
import re
from collections import Counter


def count_words(text):
    words = re.findall(r"[a-z']+", text.lower())
    return Counter(words)
```""")

add("Write a function to read a properties file like java.",
"""```python
def read_properties(path):
    props = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith(("#", "!")) and "=" in line:
                key, _, value = line.partition("=")
                props[key.strip()] = value.strip()
    return props
```""")

add("get the home directory path",
"""```python
from pathlib import Path

home = Path.home()
```""")

add("expand a path with ~ and environment variables",
"""```python
import os


def expand(path):
    return os.path.expanduser(os.path.expandvars(path))
```""")

add("Write a function to delete a file if it exists.",
"""```python
from pathlib import Path


def remove_if_exists(path):
    p = Path(path)
    if p.exists():
        p.unlink()
```""")

add("check available disk space",
"""```python
import shutil


def free_space_gb(path="/"):
    return shutil.disk_usage(path).free / (1024 ** 3)
```""")

add("write a function to read a fixed-width record file",
"""```python
def parse_fixed_width(line, widths):
    fields = []
    pos = 0
    for w in widths:
        fields.append(line[pos:pos + w].strip())
        pos += w
    return fields
```""")

add("Write a function that returns the most recent log line containing 'ERROR'.",
"""```python
def last_error(path):
    last = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                last = line.rstrip()
    return last
```""")

add("convert a number to words for 0-9",
"""```python
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def digit_to_word(n):
    return WORDS[n] if 0 <= n <= 9 else str(n)
```""")

add("roman numeral converter for integers",
"""```python
def to_roman(n):
    table = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
             (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
             (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    result = []
    for value, symbol in table:
        while n >= value:
            result.append(symbol)
            n -= value
    return "".join(result)
```""")

add("Write a function to count the frequency of each character in a string.",
"""```python
from collections import Counter


def char_freq(s):
    return Counter(s)
```""")

add("compute factorial",
"""```python
import math


def factorial(n):
    return math.factorial(n)
```""")

add("greatest common divisor of two numbers",
"""```python
import math


def gcd(a, b):
    return math.gcd(a, b)
```""")

add("Write a function to check if a year is a leap year.",
"""```python
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```""")

add("convert seconds since midnight to HH:MM",
"""```python
def to_hhmm(seconds):
    h, rem = divmod(seconds, 3600)
    m = rem // 60
    return f"{h:02d}:{m:02d}"
```""")

add("count the number of words longer than n characters",
"""```python
def count_long_words(text, n):
    return sum(1 for w in text.split() if len(w) > n)
```""")

add("Write a function to read a markdown file and extract all headers.",
"""```python
def extract_headers(path):
    headers = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                headers.append((level, line.lstrip("#").strip()))
    return headers
```""")

add("strip HTML tags from a string",
"""```python
import re


def strip_tags(html):
    return re.sub(r"<[^>]+>", "", html)
```""")

add("Write a function to count the number of paragraphs in a text.",
"""```python
def count_paragraphs(text):
    return len([p for p in text.split("\\n\\n") if p.strip()])
```""")

add("read a CSV and convert a column to integers",
"""```python
import csv


def int_column(path, column):
    with open(path, newline="", encoding="utf-8") as f:
        return [int(row[column]) for row in csv.DictReader(f)]
```""")

add("format a phone number as (123) 456-7890",
"""```python
import re


def format_phone(digits):
    d = re.sub(r"\\D", "", digits)
    if len(d) != 10:
        raise ValueError("Need 10 digits")
    return f"({d[:3]}) {d[3:6]}-{d[6:]}"
```""")

add("Write a function to mask a credit card number showing only the last 4 digits.",
"""```python
def mask_card(number):
    digits = number.replace(" ", "")
    return "*" * (len(digits) - 4) + digits[-4:]
```""")

add("normalize whitespace by collapsing runs of spaces",
"""```python
import re


def normalize_ws(s):
    return re.sub(r"\\s+", " ", s).strip()
```""")

add("count syllables roughly by counting vowel groups",
"""```python
import re


def count_syllables(word):
    return max(1, len(re.findall(r"[aeiouy]+", word.lower())))
```""")

add("Write a function to read lines and keep only unique ones, sorted.",
"""```python
def unique_sorted(path):
    with open(path, encoding="utf-8") as f:
        return sorted(set(line.strip() for line in f if line.strip()))
```""")

add("base32 encode some bytes",
"""```python
import base64

encoded = base64.b32encode(b"data").decode("ascii")
```""")

add("compute a CRC32 checksum of a file",
"""```python
import zlib


def crc32(path):
    crc = 0
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            crc = zlib.crc32(chunk, crc)
    return format(crc & 0xFFFFFFFF, "08x")
```""")

add("Write a function to generate an HMAC signature.",
"""```python
import hashlib
import hmac


def sign(message, secret):
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
```""")

add("base64 encode a file's contents",
"""```python
import base64


def encode_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")
```""")

add("Write a function to safely convert a string to float, returning None on failure.",
"""```python
def safe_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None
```""")

add("clamp a number between a min and max",
"""```python
def clamp(value, low, high):
    return max(low, min(value, high))
```""")

add("round a number to the nearest multiple of 5",
"""```python
def round_to_5(n):
    return round(n / 5) * 5
```""")

add("Write a function to convert bytes to a base64 data URI for an image.",
"""```python
import base64


def data_uri(image_bytes, mime="image/png"):
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime};base64,{b64}"
```""")

add("read input until EOF and echo it back uppercase",
"""```python
import sys

for line in sys.stdin:
    print(line.rstrip().upper())
```""")

add("Write a simple key-value store backed by a JSON file.",
"""```python
import json
from pathlib import Path


class JsonStore:
    def __init__(self, path):
        self.path = Path(path)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}

    def set(self, key, value):
        self.data[key] = value
        self.path.write_text(json.dumps(self.data, indent=2))

    def get(self, key, default=None):
        return self.data.get(key, default)
```""")

add("count how many files match a glob pattern",
"""```python
from pathlib import Path


def count_glob(directory, pattern):
    return sum(1 for _ in Path(directory).glob(pattern))
```""")

add("Write a function to read a file's content as bytes.",
"""```python
def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()
```""")

add("write bytes to a file",
"""```python
def write_bytes(path, data):
    with open(path, "wb") as f:
        f.write(data)
```""")

add("Write a function to find files larger than a given size in MB.",
"""```python
from pathlib import Path


def large_files(directory, min_mb):
    limit = min_mb * 1024 * 1024
    return [f for f in Path(directory).rglob("*") if f.is_file() and f.stat().st_size > limit]
```""")

add("get the current working directory",
"""```python
from pathlib import Path

cwd = Path.cwd()
```""")

add("Write a function to read CSV and return a dict keyed by the first column.",
"""```python
import csv


def index_by_first(path):
    result = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            result[row[0]] = dict(zip(header[1:], row[1:]))
    return result
```""")

add("convert a python object to a JSON string",
"""```python
import json

s = json.dumps({"name": "Alice", "age": 30})
```""")

add("Write a function that pretty-prints a dict as indented JSON to the console.",
"""```python
import json


def show(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
```""")

add("write a simple Markdown to plain text by removing common syntax",
"""```python
import re


def md_to_text(md):
    md = re.sub(r"`{1,3}", "", md)
    md = re.sub(r"[*_#>]", "", md)
    md = re.sub(r"\\[([^\\]]+)\\]\\([^)]+\\)", r"\\1", md)
    return md.strip()
```""")

add("Write a function to count the number of code blocks in a markdown file.",
"""```python
def count_code_blocks(path):
    with open(path, encoding="utf-8") as f:
        fences = sum(1 for line in f if line.strip().startswith("```"))
    return fences // 2
```""")

add("compute a running total over a list",
"""```python
import itertools


def running_total(nums):
    return list(itertools.accumulate(nums))
```""")

add("Write a function to find the median of a list.",
"""```python
import statistics


def median(values):
    return statistics.median(values)
```""")

add("compute mean, median and standard deviation of numbers",
"""```python
import statistics


def stats(values):
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0,
    }
```""")

add("read numbers from a file and print min, max, sum",
"""```python
def summarize(path):
    with open(path, encoding="utf-8") as f:
        nums = [float(line) for line in f if line.strip()]
    print(f"min={min(nums)} max={max(nums)} sum={sum(nums)}")
```""")

add("Write a function to deduplicate a CSV file by a key column.",
"""```python
import csv


def dedupe_csv(in_path, out_path, key):
    seen = set()
    with open(in_path, newline="", encoding="utf-8") as fin:
        reader = csv.DictReader(fin)
        rows = []
        for row in reader:
            if row[key] not in seen:
                seen.add(row[key])
                rows.append(row)
        fields = reader.fieldnames
    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
```""")

add("get the size of a file in a human-readable form",
"""```python
import os


def file_size_str(path):
    size = os.path.getsize(path)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
```""")

add("Write a function to count words per line and return the max.",
"""```python
def max_words_per_line(path):
    with open(path, encoding="utf-8") as f:
        return max((len(line.split()) for line in f), default=0)
```""")

add("read a file backwards line by line",
"""```python
def read_reverse(path):
    with open(path, encoding="utf-8") as f:
        return list(reversed(f.readlines()))
```""")

add("Write a function to replace text in a file in place.",
"""```python
def replace_in_file(path, old, new):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.replace(old, new))
```""")

add("create a temporary file and write to it",
"""```python
import tempfile


def write_temp(text):
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as f:
        f.write(text)
        return f.name
```""")

add("Write a function to count lines, words, and bytes of a file like wc.",
"""```python
def wc(path):
    lines = words = 0
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8", errors="replace")
    lines = text.count("\\n")
    words = len(text.split())
    return lines, words, len(data)
```""")

add("read a JSON config and provide defaults for missing keys",
"""```python
import json

DEFAULTS = {"host": "localhost", "port": 8000, "debug": False}


def load_config(path):
    config = dict(DEFAULTS)
    try:
        with open(path, encoding="utf-8") as f:
            config.update(json.load(f))
    except FileNotFoundError:
        pass
    return config
```""")

add("Write a function to tally votes from a list of names.",
"""```python
from collections import Counter


def tally(votes):
    return Counter(votes).most_common()
```""")

add("convert a list of tuples to a CSV file",
"""```python
import csv


def tuples_to_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
```""")

add("Write a function to read a CSV and yield rows lazily.",
"""```python
import csv


def iter_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f)
```""")

add("hash a file with sha1",
"""```python
import hashlib


def sha1_file(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
```""")

add("Write a function to read a file with a given encoding, falling back to latin-1.",
"""```python
def robust_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, encoding="latin-1") as f:
            return f.read()
```""")

add("count the number of true booleans in a list",
"""```python
def count_true(values):
    return sum(bool(v) for v in values)
```""")

add("Write a function to read a 2-column CSV into a dict.",
"""```python
import csv


def csv_to_dict(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {row[0]: row[1] for row in csv.reader(f) if len(row) >= 2}
```""")

add("partition a list into evens and odds",
"""```python
def partition_parity(nums):
    evens = [n for n in nums if n % 2 == 0]
    odds = [n for n in nums if n % 2 != 0]
    return evens, odds
```""")

add("Write a function to read a file and count words starting with each letter.",
"""```python
from collections import Counter


def by_first_letter(path):
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for word in f.read().split():
            if word[0].isalpha():
                counts[word[0].lower()] += 1
    return counts
```""")

add("write a number guessing game with limited attempts",
"""```python
import random


def game(max_attempts=5):
    secret = random.randint(1, 100)
    for attempt in range(1, max_attempts + 1):
        guess = int(input(f"Attempt {attempt}/{max_attempts}: "))
        if guess == secret:
            print("You win!")
            return
        print("Higher" if guess < secret else "Lower")
    print(f"Out of tries. It was {secret}.")
```""")

add("Write a function to convert a duration in seconds to days, hours, minutes.",
"""```python
def breakdown(seconds):
    days, rem = divmod(int(seconds), 86400)
    hours, rem = divmod(rem, 3600)
    minutes, secs = divmod(rem, 60)
    return days, hours, minutes, secs
```""")

add("list all environment variables sorted",
"""```python
import os


def list_env():
    for key in sorted(os.environ):
        print(f"{key}={os.environ[key]}")
```""")

add("Write a function to read the nth line of a file efficiently.",
"""```python
from itertools import islice


def nth_line(path, n):
    with open(path, encoding="utf-8") as f:
        return next(islice(f, n, n + 1), None)
```""")

add("simple unit converter feet to meters",
"""```python
def feet_to_meters(feet):
    return feet * 0.3048
```""")

add("Write a function to count distinct values in a CSV column.",
"""```python
import csv


def distinct_values(path, column):
    with open(path, newline="", encoding="utf-8") as f:
        return {row[column] for row in csv.DictReader(f)}
```""")

add("validate that a username is alphanumeric and 3-16 chars",
"""```python
import re


def valid_username(name):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,16}", name))
```""")

add("Write a function to generate a random PIN code.",
"""```python
import secrets


def generate_pin(digits=4):
    return "".join(str(secrets.randbelow(10)) for _ in range(digits))
```""")

add("convert a hex color to RGB",
"""```python
def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
```""")

add("convert RGB to a hex color string",
"""```python
def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"
```""")

add("Write a function to read a YAML-like simple list file.",
"""```python
def read_list_file(path):
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                items.append(line[2:].strip())
    return items
```""")

add("count the depth of indentation of a line",
"""```python
def indent_level(line, spaces=4):
    stripped = line.lstrip(" ")
    return (len(line) - len(stripped)) // spaces
```""")

add("Write a function to compute word count statistics for a file.",
"""```python
def text_stats(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    return {
        "characters": len(text),
        "words": len(words),
        "lines": text.count("\\n") + 1,
        "avg_word_length": round(sum(len(w) for w in words) / len(words), 2) if words else 0,
    }
```""")

add("read the clipboard? no—just convert tabs in a string to a list",
"""```python
def tabs_to_list(line):
    return line.rstrip("\\n").split("\\t")
```""")

add("Write a function to download multiple URLs and save each.",
"""```python
from pathlib import Path

import requests


def download_all(urls, dest_dir):
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    for url in urls:
        name = url.rstrip("/").split("/")[-1] or "index.html"
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        (Path(dest_dir) / name).write_bytes(resp.content)
```""")

add("parse an ISO datetime string",
"""```python
from datetime import datetime


def parse_iso(s):
    return datetime.fromisoformat(s)
```""")

add("Write a function to get the current month name.",
"""```python
from datetime import date


def current_month():
    return date.today().strftime("%B")
```""")

add("count weekdays between two dates",
"""```python
from datetime import timedelta


def weekdays_between(start, end):
    days = (end - start).days + 1
    return sum(1 for i in range(days) if (start + timedelta(days=i)).weekday() < 5)
```""")

add("Write a function to format a timedelta as a friendly 'ago' string.",
"""```python
from datetime import datetime


def time_ago(then):
    seconds = (datetime.now() - then).total_seconds()
    for unit, size in [("day", 86400), ("hour", 3600), ("minute", 60)]:
        if seconds >= size:
            value = int(seconds // size)
            return f"{value} {unit}{'s' if value != 1 else ''} ago"
    return "just now"
```""")

add("get the quarter of the year for a date",
"""```python
def quarter(date):
    return (date.month - 1) // 3 + 1
```""")

add("Write a function to read a CSV with a header and print as aligned columns.",
"""```python
import csv


def print_csv_table(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        return
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    for row in rows:
        print("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)))
```""")

add("count how many lines end with a period",
"""```python
def lines_ending_period(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if line.rstrip().endswith("."))
```""")

add("Write a function to roll a custom dice expression like 3d6.",
"""```python
import random


def roll(expr):
    count, sides = expr.lower().split("d")
    count = int(count) if count else 1
    return sum(random.randint(1, int(sides)) for _ in range(count))
```""")

add("write a function to merge JSON files into a single list",
"""```python
import json
from pathlib import Path


def merge_json_files(paths, out_path):
    merged = []
    for p in paths:
        data = json.loads(Path(p).read_text(encoding="utf-8"))
        merged.extend(data if isinstance(data, list) else [data])
    Path(out_path).write_text(json.dumps(merged, indent=2), encoding="utf-8")
```""")

add("Write a function to find the longest common prefix of a list of strings.",
"""```python
import os


def common_prefix(strings):
    return os.path.commonprefix(strings)
```""")

add("encode a string to bytes and back",
"""```python
text = "café"
data = text.encode("utf-8")
back = data.decode("utf-8")
```""")

add("Write a function to count tokens separated by any whitespace or punctuation.",
"""```python
import re


def tokenize(text):
    return re.findall(r"\\w+", text)
```""")

add("read a CSV and compute the average of a column ignoring bad rows",
"""```python
import csv


def safe_average(path, column):
    total = count = 0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                total += float(row[column])
                count += 1
            except (ValueError, KeyError):
                continue
    return total / count if count else 0
```""")

add("Write a function to atomically write a file.",
"""```python
import os
import tempfile


def atomic_write(path, text):
    dir_name = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=dir_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        os.unlink(tmp)
        raise
```
Writing to a temp file then `os.replace` guarantees readers never see a half-written file.""")

add("count occurrences of each line in a file",
"""```python
from collections import Counter


def line_counts(path):
    with open(path, encoding="utf-8") as f:
        return Counter(line.rstrip("\\n") for line in f)
```""")

add("Write a function to extract hashtags from text.",
"""```python
import re


def hashtags(text):
    return re.findall(r"#(\\w+)", text)
```""")

add("extract @mentions from text",
"""```python
import re


def mentions(text):
    return re.findall(r"@(\\w+)", text)
```""")

add("Write a function to convert a snake_case dict's keys to camelCase.",
"""```python
def keys_to_camel(d):
    def camel(s):
        parts = s.split("_")
        return parts[0] + "".join(p.capitalize() for p in parts[1:])
    return {camel(k): v for k, v in d.items()}
```""")

add("count positive, negative, and zero values",
"""```python
def sign_counts(nums):
    pos = sum(1 for n in nums if n > 0)
    neg = sum(1 for n in nums if n < 0)
    zero = sum(1 for n in nums if n == 0)
    return pos, neg, zero
```""")

add("Write a function to read a file and return word lengths histogram.",
"""```python
from collections import Counter


def length_histogram(path):
    with open(path, encoding="utf-8") as f:
        return Counter(len(w) for w in f.read().split())
```""")

add("simple BMI CLI tool",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("weight", type=float, help="weight in kg")
    parser.add_argument("height", type=float, help="height in meters")
    args = parser.parse_args()
    print(f"BMI: {args.weight / args.height ** 2:.1f}")


if __name__ == "__main__":
    main()
```""")

add("Write a function to read a CSV and return rows where a numeric column exceeds a threshold.",
"""```python
import csv


def above_threshold(path, column, threshold):
    with open(path, newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if float(row[column]) > threshold]
```""")

add("count vowels and consonants separately",
"""```python
def count_letters(s):
    vowels = sum(1 for c in s.lower() if c in "aeiou")
    consonants = sum(1 for c in s.lower() if c.isalpha() and c not in "aeiou")
    return vowels, consonants
```""")

add("Write a function to safely get a nested key from a dict.",
"""```python
def deep_get(d, *keys, default=None):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d
```""")

add("convert a CSV row count summary to a report string",
"""```python
import csv


def report(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return f"Columns: {len(header)}\\nRows: {len(rows)}\\nHeaders: {', '.join(header)}"
```""")

add("Write a function that retries with a callback on each failure.",
"""```python
import time


def retry(func, attempts=3, on_error=None, delay=1.0):
    for i in range(attempts):
        try:
            return func()
        except Exception as e:
            if on_error:
                on_error(i, e)
            if i == attempts - 1:
                raise
            time.sleep(delay)
```""")

add("limit how often a function can be called using a decorator",
"""```python
import functools
import time


def throttle(seconds):
    def decorator(func):
        last = [0.0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()
            if now - last[0] >= seconds:
                last[0] = now
                return func(*args, **kwargs)
        return wrapper
    return decorator
```""")

add("Write a function to read a numbers file and return a sorted unique list.",
"""```python
def sorted_unique_numbers(path):
    with open(path, encoding="utf-8") as f:
        return sorted({int(line) for line in f if line.strip()})
```""")

add("write a function to count the lines of code in a python file ignoring blanks and comments",
"""```python
def loc(path):
    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                count += 1
    return count
```""")

add("Write a function to read a config file with sections using configparser and return one value.",
"""```python
import configparser


def get_setting(path, section, key):
    parser = configparser.ConfigParser()
    parser.read(path)
    return parser.get(section, key, fallback=None)
```""")

add("normalize a unicode string to NFC form",
"""```python
import unicodedata


def normalize(s):
    return unicodedata.normalize("NFC", s)
```""")

add("Write a function to strip accents from text.",
"""```python
import unicodedata


def strip_accents(s):
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))
```""")

add("count how many files in a folder were modified today",
"""```python
from datetime import date
from pathlib import Path


def modified_today(directory):
    today = date.today()
    count = 0
    for f in Path(directory).iterdir():
        if f.is_file() and date.fromtimestamp(f.stat().st_mtime) == today:
            count += 1
    return count
```""")

add("Write a function to read a file and replace multiple patterns at once.",
"""```python
def multi_replace(text, replacements):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text
```""")

add("split a full name into first and last",
"""```python
def split_name(full_name):
    parts = full_name.strip().split()
    if not parts:
        return "", ""
    return parts[0], " ".join(parts[1:])
```""")

add("Write a function to count duplicate lines across multiple files.",
"""```python
from collections import Counter


def duplicate_lines(paths):
    counts = Counter()
    for p in paths:
        with open(p, encoding="utf-8") as f:
            counts.update(line.rstrip("\\n") for line in f)
    return {line: n for line, n in counts.items() if n > 1}
```""")

add("create an in-memory text buffer with StringIO",
"""```python
import io

buffer = io.StringIO()
buffer.write("hello\\n")
buffer.write("world\\n")
content = buffer.getvalue()
```""")

add("Write a function to capitalize sentences in a paragraph.",
"""```python
import re


def capitalize_sentences(text):
    return re.sub(r"(^|[.!?]\\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), text)
```""")

add("count how many positive integers in a file are prime",
"""```python
def is_prime(n):
    if n < 2:
        return False
    return all(n % i for i in range(2, int(n ** 0.5) + 1))


def count_primes(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for line in f if line.strip().isdigit() and is_prime(int(line)))
```""")

add("Write a function to convert a list of dicts to CSV text in memory.",
"""```python
import csv
import io


def dicts_to_csv_string(rows, fieldnames):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()
```""")

add("get a list of all unique file extensions in a directory tree",
"""```python
from pathlib import Path


def all_extensions(root):
    return {f.suffix.lower() for f in Path(root).rglob("*") if f.is_file() and f.suffix}
```""")

add("Write a function to build a frequency report sorted by count descending.",
"""```python
from collections import Counter


def frequency_report(items):
    counter = Counter(items)
    lines = [f"{item}: {count}" for item, count in counter.most_common()]
    return "\\n".join(lines)
```""")

add("convert a string to a list of its unique characters in order",
"""```python
def unique_chars(s):
    seen = set()
    return [c for c in s if not (c in seen or seen.add(c))]
```""")

add("Write a function to compute the percentage each item makes up of a total.",
"""```python
def percentages(values):
    total = sum(values)
    return [round(v / total * 100, 2) if total else 0 for v in values]
```""")

add("read a file and return a dict of word -> first line number seen",
"""```python
def first_seen(path):
    seen = {}
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            for word in line.split():
                seen.setdefault(word, n)
    return seen
```""")

add("Write a function to convert a dictionary into URL query string sorted by key.",
"""```python
from urllib.parse import urlencode


def stable_query(params):
    return urlencode(sorted(params.items()))
```""")

add("count number of sentences, words, and characters in a file",
"""```python
import re


def analyze(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    sentences = len([s for s in re.split(r"[.!?]+", text) if s.strip()])
    return {"sentences": sentences, "words": len(text.split()), "chars": len(text)}
```""")

add("Write a function to read a file and return a set of all distinct words lowercased.",
"""```python
def vocabulary(path):
    with open(path, encoding="utf-8") as f:
        return set(f.read().lower().split())
```""")

add("simple temperature CLI converting C to F",
"""```python
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("celsius", type=float)
    args = parser.parse_args()
    print(f"{args.celsius * 9 / 5 + 32:.1f}F")


if __name__ == "__main__":
    main()
```""")

add("Write a function to count the number of bytes in a string when UTF-8 encoded.",
"""```python
def byte_length(s):
    return len(s.encode("utf-8"))
```""")

add("read CSV and group sum by a category column",
"""```python
import csv
from collections import defaultdict


def sum_by_category(path, category_col, value_col):
    totals = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row[category_col]] += float(row[value_col])
    return dict(totals)
```""")

add("Write a function to safely parse an int from user input with a default.",
"""```python
def parse_int(s, default=0):
    try:
        return int(s)
    except (ValueError, TypeError):
        return default
```""")

add("rotate a list to the left by n positions",
"""```python
def rotate_left(items, n):
    n %= len(items) if items else 1
    return items[n:] + items[:n]
```""")

add("Write a function to find anagram groups in a word list.",
"""```python
from collections import defaultdict


def anagram_groups(words):
    groups = defaultdict(list)
    for word in words:
        groups["".join(sorted(word.lower()))].append(word)
    return [g for g in groups.values() if len(g) > 1]
```""")

add("count the number of uppercase letters in a string",
"""```python
def count_upper(s):
    return sum(1 for c in s if c.isupper())
```""")

add("Write a function to pad a list to a fixed length with a fill value.",
"""```python
def pad_list(items, length, fill=None):
    return items[:length] + [fill] * max(0, length - len(items))
```""")

add("turn a dict of counts into a bar chart of asterisks",
"""```python
def bar_chart(counts):
    width = max(len(str(k)) for k in counts) if counts else 0
    for key, value in counts.items():
        print(f"{str(key).ljust(width)} | {'*' * value} {value}")
```""")

add("Write a function to read newline-delimited JSON and sum a field.",
"""```python
import json


def sum_field(path, field):
    total = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                total += json.loads(line).get(field, 0)
    return total
```""")

add("validate a hex color string",
"""```python
import re


def is_hex_color(s):
    return bool(re.fullmatch(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", s))
```""")

add("Write a function to compute Levenshtein distance between two strings.",
"""```python
def levenshtein(a, b):
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
```""")

add("count the number of times a value appears in a CSV column",
"""```python
import csv


def count_value(path, column, value):
    with open(path, newline="", encoding="utf-8") as f:
        return sum(1 for row in csv.DictReader(f) if row[column] == value)
```""")

add("Write a function to read a file and yield (line_number, line) pairs.",
"""```python
def enumerate_lines(path):
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            yield i, line.rstrip("\\n")
```""")

add("convert minutes to seconds",
"""```python
def minutes_to_seconds(minutes):
    return minutes * 60
```""")

add("Write a function to validate that a string is valid JSON.",
"""```python
import json


def is_valid_json(s):
    try:
        json.loads(s)
        return True
    except json.JSONDecodeError:
        return False
```""")

add("read a CSV and write only selected columns to a new CSV",
"""```python
import csv


def select_columns(in_path, out_path, columns):
    with open(in_path, newline="", encoding="utf-8") as fin:
        reader = csv.DictReader(fin)
        rows = [{c: row[c] for c in columns} for row in reader]
    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
```""")

add("Write a function to check if a path is a hidden file.",
"""```python
from pathlib import Path


def is_hidden(path):
    return Path(path).name.startswith(".")
```""")

add("compute a simple moving average over a list",
"""```python
def moving_average(values, window):
    return [sum(values[i:i + window]) / window for i in range(len(values) - window + 1)]
```""")

add("Write a function to read a file and return the count of each line length.",
"""```python
from collections import Counter


def line_length_dist(path):
    with open(path, encoding="utf-8") as f:
        return Counter(len(line.rstrip("\\n")) for line in f)
```""")

add("join a directory and filename safely",
"""```python
from pathlib import Path


def join_path(directory, filename):
    return str(Path(directory) / filename)
```""")

add("Write a function to count how many CSV rows have any empty field.",
"""```python
import csv


def rows_with_blanks(path):
    with open(path, newline="", encoding="utf-8") as f:
        return sum(1 for row in csv.DictReader(f) if any(v == "" for v in row.values()))
```""")

add("write a simple ROT-N cipher",
"""```python
def rotn(text, n):
    result = []
    for c in text:
        if c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            result.append(chr((ord(c) - base + n) % 26 + base))
        else:
            result.append(c)
    return "".join(result)
```""")

add("Write a function to summarize a numeric CSV column with count, min, max, mean.",
"""```python
import csv


def summarize_column(path, column):
    values = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                values.append(float(row[column]))
            except ValueError:
                pass
    return {
        "count": len(values),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "mean": sum(values) / len(values) if values else None,
    }
```""")

add("count the number of times a word appears, whole-word only",
"""```python
import re


def whole_word_count(text, word):
    return len(re.findall(rf"\\b{re.escape(word)}\\b", text, re.IGNORECASE))
```""")

add("Write a function to read a file and return lines that match a regex.",
"""```python
import re


def matching_lines(path, pattern):
    regex = re.compile(pattern)
    with open(path, encoding="utf-8") as f:
        return [line.rstrip() for line in f if regex.search(line)]
```""")

add("create nested directories",
"""```python
from pathlib import Path

Path("a/b/c").mkdir(parents=True, exist_ok=True)
```""")

add("Write a function to convert all keys in a dict to lowercase.",
"""```python
def lower_keys(d):
    return {k.lower(): v for k, v in d.items()}
```""")

add("read a text file and write it back with sorted lines",
"""```python
def sort_file(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(sorted(lines))
```""")

add("Write a function to compute a weighted average.",
"""```python
def weighted_average(values, weights):
    total_weight = sum(weights)
    return sum(v * w for v, w in zip(values, weights)) / total_weight if total_weight else 0
```""")

add("escape special characters in a string for use in a regex",
"""```python
import re


def escape(s):
    return re.escape(s)
```""")

add("Write a function to read a CSV with semicolons as delimiter.",
"""```python
import csv


def read_semicolon_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))
```""")

add("count how many words in a sentence are capitalized",
"""```python
def count_capitalized(sentence):
    return sum(1 for w in sentence.split() if w[:1].isupper())
```""")

add("Write a function to print a calendar for a given month.",
"""```python
import calendar


def show_month(year, month):
    print(calendar.month(year, month))
```""")

add("get the number of days in a month",
"""```python
import calendar


def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]
```""")

add("Write a function to read a file of IP addresses and return only valid ones.",
"""```python
import ipaddress


def valid_ips(path):
    result = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            try:
                ipaddress.ip_address(line)
                result.append(line)
            except ValueError:
                pass
    return result
```""")

add("convert bytes to an integer and back",
"""```python
n = int.from_bytes(b"\\x01\\x02", "big")
data = n.to_bytes(2, "big")
```""")

add("Write a function to count the number of distinct file extensions and their totals.",
"""```python
from collections import Counter
from pathlib import Path


def extension_report(root):
    return Counter(f.suffix.lower() or "<none>" for f in Path(root).rglob("*") if f.is_file())
```""")

add("read a file and return the average words per line",
"""```python
def avg_words_per_line(path):
    total = lines = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            total += len(line.split())
            lines += 1
    return total / lines if lines else 0
```""")

add("Write a function to remove blank lines from a file.",
"""```python
def remove_blank_lines(path):
    with open(path, encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
```""")

add("count the number of times a regex group captures across a file",
"""```python
import re
from collections import Counter


def capture_counts(path, pattern):
    regex = re.compile(pattern)
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            counts.update(regex.findall(line))
    return counts
```""")

add("Write a function to convert a flat dict to nested using dotted keys.",
"""```python
def unflatten(flat, sep="."):
    result = {}
    for key, value in flat.items():
        parts = key.split(sep)
        d = result
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = value
    return result
```""")

add("read a file and print only lines that are not duplicates",
"""```python
def print_unique(path):
    seen = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line not in seen:
                seen.add(line)
                print(line, end="")
```""")

add("Write a function to compute the entropy of a string.",
"""```python
import math
from collections import Counter


def entropy(s):
    if not s:
        return 0.0
    counts = Counter(s)
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())
```""")

add("convert a list to a set and report how many duplicates were removed",
"""```python
def count_duplicates(items):
    return len(items) - len(set(items))
```""")

add("Write a function to wrap a long string into lines of max length without breaking words.",
"""```python
import textwrap


def wrap(text, width=80):
    return textwrap.wrap(text, width=width)
```""")

add("count how many numbers in a list are within a range",
"""```python
def count_in_range(nums, low, high):
    return sum(1 for n in nums if low <= n <= high)
```""")

add("Write a function to load a JSON file and pretty-print a specific key.",
"""```python
import json


def show_key(path, key):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(data.get(key), indent=2))
```""")

# A few more multi-turn to reach ~30
add_multi([
    ("user", "Write a function to read a CSV of students with name and grade."),
    ("silicat", """```python
import csv


def read_students(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
```"""),
    ("user", "Compute the average grade."),
    ("silicat", """```python
import csv


def average_grade(path):
    grades = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            grades.append(float(row["grade"]))
    return sum(grades) / len(grades) if grades else 0
```"""),
    ("user", "Find the top student."),
    ("silicat", """```python
import csv


def top_student(path):
    with open(path, newline="", encoding="utf-8") as f:
        return max(csv.DictReader(f), key=lambda r: float(r["grade"]))
```"""),
    ("user", "Assign letter grades and write a new CSV."),
    ("silicat", """```python
import csv


def letter(grade):
    if grade >= 90:
        return "A"
    if grade >= 80:
        return "B"
    if grade >= 70:
        return "C"
    if grade >= 60:
        return "D"
    return "F"


def add_letters(in_path, out_path):
    with open(in_path, newline="", encoding="utf-8") as fin:
        rows = list(csv.DictReader(fin))
    for row in rows:
        row["letter"] = letter(float(row["grade"]))
    fields = list(rows[0].keys()) if rows else ["name", "grade", "letter"]
    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
```"""),
])

add_multi([
    ("user", "I want to track expenses. Start with a function to add an expense."),
    ("silicat", """```python
expenses = []


def add_expense(amount, category):
    expenses.append({"amount": amount, "category": category})
```"""),
    ("user", "Total the expenses."),
    ("silicat", """```python
expenses = []


def add_expense(amount, category):
    expenses.append({"amount": amount, "category": category})


def total():
    return sum(e["amount"] for e in expenses)
```"""),
    ("user", "Break the total down by category."),
    ("silicat", """```python
from collections import defaultdict

expenses = []


def add_expense(amount, category):
    expenses.append({"amount": amount, "category": category})


def total():
    return sum(e["amount"] for e in expenses)


def by_category():
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    return dict(totals)
```"""),
    ("user", "Save and load from a JSON file."),
    ("silicat", """```python
import json
import os
from collections import defaultdict

expenses = []


def load(path="expenses.json"):
    global expenses
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            expenses = json.load(f)


def save(path="expenses.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)


def add_expense(amount, category):
    expenses.append({"amount": amount, "category": category})


def total():
    return sum(e["amount"] for e in expenses)


def by_category():
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    return dict(totals)
```"""),
])

add_multi([
    ("user", "Help me write a URL shortener in memory."),
    ("silicat", """```python
import secrets

store = {}


def shorten(url):
    code = secrets.token_urlsafe(4)
    store[code] = url
    return code


def resolve(code):
    return store.get(code)
```"""),
    ("user", "Make the same URL always return the same code."),
    ("silicat", """```python
import secrets

store = {}
reverse = {}


def shorten(url):
    if url in reverse:
        return reverse[url]
    code = secrets.token_urlsafe(4)
    store[code] = url
    reverse[url] = code
    return code


def resolve(code):
    return store.get(code)
```"""),
    ("user", "Persist the mapping to a JSON file."),
    ("silicat", """```python
import json
import os
import secrets

PATH = "urls.json"
store = {}
reverse = {}


def load():
    global store, reverse
    if os.path.exists(PATH):
        with open(PATH, encoding="utf-8") as f:
            store = json.load(f)
        reverse = {v: k for k, v in store.items()}


def _save():
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=2)


def shorten(url):
    if url in reverse:
        return reverse[url]
    code = secrets.token_urlsafe(4)
    store[code] = url
    reverse[url] = code
    _save()
    return code


def resolve(code):
    return store.get(code)
```"""),
])

add_multi([
    ("user", "Write a function to find files by extension."),
    ("silicat", """```python
from pathlib import Path


def find_by_ext(directory, ext):
    return list(Path(directory).rglob(f"*.{ext.lstrip('.')}"))
```"""),
    ("user", "Now group them by their immediate parent folder."),
    ("silicat", """```python
from collections import defaultdict
from pathlib import Path


def group_by_folder(directory, ext):
    groups = defaultdict(list)
    for f in Path(directory).rglob(f"*.{ext.lstrip('.')}"):
        groups[f.parent.name].append(f.name)
    return dict(groups)
```"""),
    ("user", "Print a summary of counts per folder."),
    ("silicat", """```python
from collections import defaultdict
from pathlib import Path


def summary(directory, ext):
    groups = defaultdict(int)
    for f in Path(directory).rglob(f"*.{ext.lstrip('.')}"):
        groups[f.parent.name] += 1
    for folder, count in sorted(groups.items()):
        print(f"{folder}: {count}")
```"""),
])

add_multi([
    ("user", "Write a function to fetch a web page's HTML."),
    ("silicat", """```python
import requests


def fetch_html(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.text
```"""),
    ("user", "Extract all the image URLs."),
    ("silicat", """```python
import requests
from bs4 import BeautifulSoup


def image_urls(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [img["src"] for img in soup.find_all("img", src=True)]
```"""),
    ("user", "Download them all to a folder."),
    ("silicat", """```python
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def download_images(url, dest):
    Path(dest).mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    for img in soup.find_all("img", src=True):
        img_url = urljoin(url, img["src"])
        name = Path(urlparse(img_url).path).name or "image"
        try:
            data = requests.get(img_url, timeout=10).content
            (Path(dest) / name).write_bytes(data)
        except requests.RequestException:
            continue
```"""),
])

add_multi([
    ("user", "Make a simple note taking function that appends notes to a file."),
    ("silicat", """```python
def add_note(text, path="notes.txt"):
    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\\n")
```"""),
    ("user", "Timestamp each note."),
    ("silicat", """```python
from datetime import datetime


def add_note(text, path="notes.txt"):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {text}\\n")
```"""),
    ("user", "Add a function to search notes for a keyword."),
    ("silicat", """```python
from datetime import datetime


def add_note(text, path="notes.txt"):
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {text}\\n")


def search_notes(keyword, path="notes.txt"):
    try:
        with open(path, encoding="utf-8") as f:
            return [line.rstrip() for line in f if keyword.lower() in line.lower()]
    except FileNotFoundError:
        return []
```"""),
])

add_multi([
    ("user", "Write a function to hash a password."),
    ("silicat", """```python
import hashlib
import os


def hash_password(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return f"{salt.hex()}:{digest.hex()}"
```"""),
    ("user", "Add a verify function."),
    ("silicat", """```python
import hashlib
import hmac
import os


def hash_password(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(password, stored):
    salt_hex, digest_hex = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return hmac.compare_digest(digest.hex(), digest_hex)
```
`hmac.compare_digest` avoids timing attacks when comparing the hashes."""),
])

add_multi([
    ("user", "Write me a basic calculator that takes an expression string."),
    ("silicat", """Use a safe approach rather than `eval`. Here's one that handles two operands:

```python
import operator

OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def calc(expr):
    a, op, b = expr.split()
    return OPS[op](float(a), float(b))
```"""),
    ("user", "Make it a loop that keeps reading expressions until I type quit."),
    ("silicat", """```python
import operator

OPS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def calc(expr):
    a, op, b = expr.split()
    return OPS[op](float(a), float(b))


def main():
    while True:
        line = input("> ").strip()
        if line == "quit":
            break
        try:
            print(calc(line))
        except (ValueError, KeyError, ZeroDivisionError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
```"""),
])

add_multi([
    ("user", "Write a function to read a log file and parse each line into fields."),
    ("silicat", """If lines look like `DATE TIME LEVEL message`:

```python
def parse_log(path):
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip().split(" ", 3)
            if len(parts) == 4:
                date, time, level, message = parts
                entries.append({"date": date, "time": time, "level": level, "message": message})
    return entries
```"""),
    ("user", "Count entries by level."),
    ("silicat", """```python
from collections import Counter


def count_levels(path):
    counts = Counter()
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split(" ", 3)
            if len(parts) >= 3:
                counts[parts[2]] += 1
    return counts
```"""),
    ("user", "Filter to only WARNING and ERROR and write them to a new file."),
    ("silicat", """```python
def filter_severe(in_path, out_path):
    with open(in_path, encoding="utf-8") as fin, open(out_path, "w", encoding="utf-8") as fout:
        for line in fin:
            parts = line.split(" ", 3)
            if len(parts) >= 3 and parts[2] in ("WARNING", "ERROR"):
                fout.write(line)
```"""),
])

add_multi([
    ("user", "Write a Markdown table generator from a list of dicts."),
    ("silicat", """```python
def md_table(rows):
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\\n".join(lines)
```"""),
    ("user", "Write the table to a .md file."),
    ("silicat", """```python
def write_md_table(rows, path):
    table = md_table(rows)
    with open(path, "w", encoding="utf-8") as f:
        f.write(table + "\\n")
```"""),
])

add_multi([
    ("user", "Write a function to count word frequency from stdin."),
    ("silicat", """```python
import sys
from collections import Counter


def main():
    counts = Counter(sys.stdin.read().split())
    for word, n in counts.most_common():
        print(f"{n}\\t{word}")


if __name__ == "__main__":
    main()
```"""),
    ("user", "Add an argument for the top N words to show."),
    ("silicat", """```python
import argparse
import sys
from collections import Counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, default=None, help="show top N words")
    args = parser.parse_args()
    counts = Counter(sys.stdin.read().split())
    for word, n in counts.most_common(args.n):
        print(f"{n}\\t{word}")


if __name__ == "__main__":
    main()
```"""),
])

add_multi([
    ("user", "Make a function to read a CSV into a list of dicts."),
    ("silicat", """```python
import csv


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
```"""),
    ("user", "Sort it by a column."),
    ("silicat", """```python
import csv


def load_sorted(path, column):
    with open(path, newline="", encoding="utf-8") as f:
        return sorted(csv.DictReader(f), key=lambda r: r[column])
```"""),
    ("user", "Handle the column being numeric so it sorts numerically."),
    ("silicat", """```python
import csv


def load_sorted(path, column, numeric=False):
    key = (lambda r: float(r[column])) if numeric else (lambda r: r[column])
    with open(path, newline="", encoding="utf-8") as f:
        return sorted(csv.DictReader(f), key=key)
```"""),
])

add_multi([
    ("user", "Write a function that generates a daily report header with today's date."),
    ("silicat", """```python
from datetime import date


def header():
    return f"Daily Report - {date.today():%B %d, %Y}"
```"""),
    ("user", "Add a section that lists items with bullet points."),
    ("silicat", """```python
from datetime import date


def build_report(items):
    lines = [f"Daily Report - {date.today():%B %d, %Y}", ""]
    for item in items:
        lines.append(f"  - {item}")
    return "\\n".join(lines)
```"""),
    ("user", "Save it to a dated filename."),
    ("silicat", """```python
from datetime import date


def build_report(items):
    lines = [f"Daily Report - {date.today():%B %d, %Y}", ""]
    for item in items:
        lines.append(f"  - {item}")
    return "\\n".join(lines)


def save_report(items):
    filename = f"report_{date.today():%Y%m%d}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(build_report(items) + "\\n")
    return filename
```"""),
])

add_multi([
    ("user", "Write a function to count lines in a file."),
    ("silicat", """```python
def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)
```"""),
    ("user", "Make it work for many files and return a dict."),
    ("silicat", """```python
def count_lines_many(paths):
    return {p: sum(1 for _ in open(p, encoding="utf-8")) for p in paths}
```"""),
    ("user", "Make it a CLI that accepts file arguments and prints a total."),
    ("silicat", """```python
import argparse


def count_lines(path):
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    total = 0
    for path in args.files:
        n = count_lines(path)
        total += n
        print(f"{n:>8}  {path}")
    print(f"{total:>8}  total")


if __name__ == "__main__":
    main()
```"""),
])

add_multi([
    ("user", "Write a function that validates and normalizes phone numbers."),
    ("silicat", """```python
import re


def normalize_phone(raw):
    digits = re.sub(r"\\D", "", raw)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return None
```"""),
    ("user", "Process a whole column from a CSV and add a normalized column."),
    ("silicat", """```python
import csv
import re


def normalize_phone(raw):
    digits = re.sub(r"\\D", "", raw)
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return None


def process(in_path, out_path, phone_col):
    with open(in_path, newline="", encoding="utf-8") as fin:
        rows = list(csv.DictReader(fin))
    for row in rows:
        row["normalized_phone"] = normalize_phone(row[phone_col]) or ""
    fields = list(rows[0].keys()) if rows else [phone_col, "normalized_phone"]
    with open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
```"""),
])

add_multi([
    ("user", "Write a function to compute the hash of a file."),
    ("silicat", """```python
import hashlib


def file_hash(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()
```"""),
    ("user", "Now compare two directories and report files whose hashes differ."),
    ("silicat", """```python
import hashlib
from pathlib import Path


def file_hash(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def diff_dirs(dir_a, dir_b):
    a, b = Path(dir_a), Path(dir_b)
    differing = []
    for fa in a.rglob("*"):
        if fa.is_file():
            rel = fa.relative_to(a)
            fb = b / rel
            if not fb.exists() or file_hash(fa) != file_hash(fb):
                differing.append(str(rel))
    return differing
```"""),
])

add_multi([
    ("user", "Make a function that returns a greeting depending on the time of day."),
    ("silicat", """```python
from datetime import datetime


def greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    if hour < 18:
        return "Good afternoon"
    return "Good evening"
```"""),
    ("user", "Let me pass a name in."),
    ("silicat", """```python
from datetime import datetime


def greeting(name):
    hour = datetime.now().hour
    if hour < 12:
        part = "Good morning"
    elif hour < 18:
        part = "Good afternoon"
    else:
        part = "Good evening"
    return f"{part}, {name}!"
```"""),
])

add_multi([
    ("user", "Write a simple inventory tracker with add and remove quantity."),
    ("silicat", """```python
from collections import defaultdict

inventory = defaultdict(int)


def add(item, qty=1):
    inventory[item] += qty


def remove(item, qty=1):
    inventory[item] = max(0, inventory[item] - qty)
```"""),
    ("user", "Add a low-stock report below a threshold."),
    ("silicat", """```python
from collections import defaultdict

inventory = defaultdict(int)


def add(item, qty=1):
    inventory[item] += qty


def remove(item, qty=1):
    inventory[item] = max(0, inventory[item] - qty)


def low_stock(threshold=5):
    return {item: qty for item, qty in inventory.items() if qty < threshold}
```"""),
    ("user", "Persist the inventory to a JSON file and load it on import."),
    ("silicat", """```python
import json
import os
from collections import defaultdict

PATH = "inventory.json"
inventory = defaultdict(int)


def _load():
    if os.path.exists(PATH):
        with open(PATH, encoding="utf-8") as f:
            inventory.update(json.load(f))


def _save():
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(dict(inventory), f, indent=2)


def add(item, qty=1):
    inventory[item] += qty
    _save()


def remove(item, qty=1):
    inventory[item] = max(0, inventory[item] - qty)
    _save()


def low_stock(threshold=5):
    return {item: qty for item, qty in inventory.items() if qty < threshold}


_load()
```"""),
])

# Write out
out_path = "/home/user/Silicat/data/synth/realworld.jsonl"
with open(out_path, "w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print(f"Wrote {len(examples)} examples to {out_path}")
