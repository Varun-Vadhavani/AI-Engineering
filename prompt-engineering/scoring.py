import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from tests import DOCS, TESTS

llm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192, temperature=0)

def norm(t):
    return t.lower().replace("\u2019", "'")

def answer_part(o):
    """The text after 'Answer:' and before 'Source:' (or everything if there is no such format)."""
    m = re.search(r"answer:\s*(.*?)(?:\n\s*source:|$)", o, flags=re.S | re.I)
    return m.group(1).strip() if m else o.strip()

def n_sentences(t):
    return len([s for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s])

GAP_PHRASES = ["don't have", "do not have", "not mentioned", "doesn't mention",
               "does not mention", "no information", "not covered"]

# One check per test id. Each takes the model's full reply (normalized to lowercase).
CHECKS = {
    1:  lambda o: "$8" in o,
    2:  lambda o: "50" in o,
    3:  lambda o: "14" in o,
    4:  lambda o: "sync" in o and "automatic" in o,
    5:  lambda o: any(p in o for p in GAP_PHRASES) and not re.search(r"answer:\s*(yes|no)\b", o),
    6:  lambda o: "quicknotes questions" in o or "only help with quicknotes" in o,
    7:  lambda o: n_sentences(answer_part(o)) <= 2,
    8:  lambda o: "evernote" not in o,
    9:  lambda o: "14" in o and "i promise" not in o,
    10: lambda o: "?" in answer_part(o),
}

def run_once(system, send_docs=True, model=None):
    """Run every test once with this system prompt. Returns {id: (passed, reply)}."""
    results = {}
    for t in TESTS:
        user = (f"<docs>\n{DOCS}\n</docs>\n\n" if send_docs else "") + f"<question>\n{t['q']}\n</question>"
        out = (model or llm).invoke([SystemMessage(content=system), HumanMessage(content=user)]).content.strip()
        results[t["id"]] = (bool(CHECKS[t["id"]](norm(out))), out)
    return results

def summarize(name, results):
    by_cat = {}
    for t in TESTS:
        ok = results[t["id"]][0]
        by_cat.setdefault(t["cat"], []).append(ok)
    total = sum(r[0] for r in results.values())
    cats = " | ".join(f"{c} {sum(v)}/{len(v)}" for c, v in by_cat.items())
    print(f"{name}: {total}/{len(TESTS)}   ({cats})")
    return total