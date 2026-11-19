import re, time
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192, temperature=0)

DOCS = """
QuickNotes Help Center

Plans:
- Free: up to 50 notes.
- Pro: $8 per month, or $80 per year. Unlimited notes, attachments up to 25 MB.
- Team: $6 per user per month, with a minimum of 5 users.

Refunds: Pro and Team subscriptions can be refunded within 14 days of the
first payment. After 14 days, no refunds are given.
"""

# (question, how to check the FINAL line)
TESTS = [
    ("A team of 8 people wants the Team plan, paid monthly, for a full year. What is the total cost for the year?",
     lambda f: "576" in f),
    ("How much money does one person save by paying for Pro yearly instead of monthly for a full year?",
     lambda f: "16" in f),
    ("A team of 3 people wants the Team plan. How much do they pay per month?",
     lambda f: "30" in f),
    ("I made my first Pro payment on March 1 and asked for a refund on March 20. Do I qualify for a refund?",
     lambda f: re.search(r"\bno\b", f) is not None),
]

DIRECT = """You are a QuickNotes support assistant. Answer using only the docs provided.
Reply with ONLY one line in this format, with no explanation:
FINAL: <answer>"""

REASONING = """You are a QuickNotes support assistant. Answer using only the docs provided.
First work through the problem step by step, writing out each fact you use and each calculation.
Then give your answer on the last line, in this format:
FINAL: <answer>"""

def final_line(text):
    lines = [l for l in text.splitlines() if l.strip().upper().startswith("FINAL:")]
    return lines[-1].replace(",", "").lower() if lines else ""

def run(name, system):
    ok_count, tokens, secs = 0, 0, 0.0
    print(f"=== {name} ===")
    for q, check in TESTS:
        user = f"<docs>\n{DOCS}\n</docs>\n\n<question>\n{q}\n</question>"
        t0 = time.perf_counter()
        r = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
        dt = time.perf_counter() - t0
        out_tokens = (getattr(r, "usage_metadata", None) or {}).get("output_tokens", 0)
        f = final_line(r.content)
        ok = bool(f) and check(f)
        ok_count += ok
        tokens += out_tokens
        secs += dt
        print(f"{'OK ' if ok else 'BAD'} {out_tokens:4} tokens {dt:5.1f}s | {f or '(no FINAL line)'}")
    print(f"{name}: correct {ok_count}/{len(TESTS)}, output tokens {tokens}, time {secs:.1f}s\n")

run("direct", DIRECT)
run("reasoning first", REASONING)