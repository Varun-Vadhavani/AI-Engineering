import random
import re
import statistics
import requests
from llm import ask_full

def run(prompt: str, max_tokens: int = 200) -> str:
    return ask_full(prompt, max_tokens=max_tokens)[0]

N = 10
rng = random.Random(1)

# 1. Arithmetic: 6-digit x 4-digit
ok = 0
for _ in range(N):
    a, b = rng.randint(100000, 999999), rng.randint(1000, 9999)
    answer = run(f"What is {a} * {b}? Reply with only the number, no commas.")
    ok += re.sub(r"\D", "", answer) == str(a * b)
print(f"1. big multiplication:       {ok}/{N} correct")

# 2. Letter counting (truth computed by Python's str.count)
cases = [("strawberry", "r"), ("mississippi", "s"), ("bookkeeper", "e"),
         ("onomatopoeia", "o"),
         ("pneumonoultramicroscopicsilicovolcanoconiosis", "i")]
ok = 0
for word, letter in cases:
    answer = run(f"How many times does the letter '{letter}' appear in '{word}'? "
                 "Reply with only the number.")
    ok += re.sub(r"\D", "", answer) == str(word.count(letter))
print(f"2. letter counting:          {ok}/{len(cases)} correct")

# 3. Strict instruction following: exactly 9 words AND no letter 'e'
ok = 0
for _ in range(N):
    sentence = run("Write one sentence about the ocean that has exactly 9 words "
                   "and contains no letter 'e'. Reply with only the sentence.").strip()
    ok += len(sentence.split()) == 9 and "e" not in sentence.lower()
print(f"3. 9 words, no letter 'e':   {ok}/{N} followed both rules")

# 4. Outdated knowledge: latest version of a package
latest = requests.get("https://pypi.org/pypi/requests/json", timeout=15).json()["info"]["version"]
answer = run("What is the latest released version of the Python package 'requests'? "
             "Reply with only the version number.")
print(f"4. latest 'requests' version: model says {answer!r}, PyPI says {latest!r}")

# 5. Fabrication: ask about a function that does not exist
exists = hasattr(statistics, "weighted_median")
print(f"5. statistics.weighted_median exists in your Python? {exists}")
for trial in range(3):
    print(f"   trial {trial + 1}: {run('What does Python statistics.weighted_median() do? Two sentences.')}")