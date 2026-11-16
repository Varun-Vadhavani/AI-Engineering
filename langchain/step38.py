import json
import time
from dotenv import load_dotenv

load_dotenv()

from logger import CallLogger
from app import build

# USD per 1 million tokens: fill from your provider's pricing page (0.0 = unknown)
PRICE_IN, PRICE_OUT = 0.30, 2.50

PARAGRAPH = ("The city council announced a new plan for public transport. "
             "Buses will run more often during rush hour, and a new route will connect "
             "the railway station with the university. ") * 12

QUESTIONS = [
    "How do I reverse a list in Python?",
    "What is 15% of 840?",
    "Why is the sky blue?",
    "Explain in detail, with an example, how a database index works.",
    "What is the difference between a process and a thread?",
    "If a train travels 180 km in 2.5 hours, what is its average speed?",
    "Give me three tips for a first job interview.",
    "Write a Python function that checks whether a number is prime.",
    "Summarize this text in two sentences: " + PARAGRAPH,
    "What is a token in a language model?",
]

chain = build()
logger = CallLogger()
wall = {}

for i, q in enumerate(QUESTIONS, 1):
    start = time.perf_counter()
    try:
        chain.invoke({"question": q}, config={"callbacks": [logger], "metadata": {"q": i}})
    except Exception as e:
        print(f"Q{i} failed: {type(e).__name__}")
    wall[i] = time.perf_counter() - start
    time.sleep(1)

with open("calls.jsonl", "w", encoding="utf-8") as f:
    for c in logger.calls:
        f.write(json.dumps(c) + "\n")

def cost(c):
    return c["in_tokens"] / 1e6 * PRICE_IN + c["out_tokens"] / 1e6 * PRICE_OUT

print(f"\n{'Q':>2} {'calls':>5} {'tok in':>7} {'tok out':>8} {'cost $':>9} {'wall s':>7}  errors")
per_q = {}
for i in range(1, len(QUESTIONS) + 1):
    cs = [c for c in logger.calls if c["q"] == i]
    per_q[i] = dict(
        tokens=sum(c["in_tokens"] + c["out_tokens"] for c in cs),
        cost=sum(cost(c) for c in cs),
    )
    print(f"{i:>2} {len(cs):>5} {sum(c['in_tokens'] for c in cs):>7} "
          f"{sum(c['out_tokens'] for c in cs):>8} {per_q[i]['cost']:>9.5f} "
          f"{wall[i]:>7.1f}  {sum(1 for c in cs if c['error'])}")

total_cost = sum(p["cost"] for p in per_q.values())
total_tokens = sum(p["tokens"] for p in per_q.values())
print(f"\nTOTAL: {total_tokens} tokens, ${total_cost:.5f}")
print(f"Average wall time per question: {sum(wall.values()) / len(wall):.1f}s")

key = "cost" if (PRICE_IN or PRICE_OUT) else "tokens"
worst = max(per_q, key=lambda i: per_q[i][key])
print(f"Most expensive question (by {key}): Q{worst}: {QUESTIONS[worst - 1][:60]}")

print("\nBy step:")
for step in sorted({c["step"] for c in logger.calls}):
    cs = [c for c in logger.calls if c["step"] == step]
    print(f"  {step:<10} calls={len(cs)}  avg {sum(c['secs'] for c in cs) / len(cs):.1f}s  "
          f"avg {sum(c['in_tokens'] + c['out_tokens'] for c in cs) / len(cs):.0f} tokens")