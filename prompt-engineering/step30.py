from tests import TESTS
from scoring import run_once, summarize

PROMPT_V1 = """You are the support assistant for QuickNotes. Customers read your answers directly.
Rules:
- Use only the docs in the user's message.
- If the docs don't contain the answer, reply exactly: "I don't have that in the docs."
- Keep answers to at most 2 sentences.
Format every reply as two lines:
Answer: <answer>
Source: <line from the docs, or none>"""

results = run_once(PROMPT_V1)

for t in TESTS:
    ok, reply = results[t["id"]]
    print(f"{'PASS' if ok else 'FAIL'} #{t['id']} [{t['cat']}] {t['q']}")
    if not ok:
        print(f"      expected: {t['expected']}")
        print(f"      got:      {reply.replace(chr(10), ' | ')}")

print()
summarize("PROMPT_V1", results)