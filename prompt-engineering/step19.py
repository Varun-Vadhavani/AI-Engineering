from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192, temperature=0)

DOCS = """
QuickNotes Help Center

Plans: Free plan allows up to 50 notes. Pro plan costs $8 per month
and allows unlimited notes and file attachments up to 25 MB.

Refunds: Pro subscriptions can be refunded within 14 days of the first
payment. After 14 days, no refunds are given, but you can cancel anytime
and keep access until the end of the billing period.

Sync: Notes sync across devices automatically when you are online.
"""

RULEBOOK = """You are the support assistant for QuickNotes, a note-taking app.
- Only use information from the docs.
- Never guess or use outside knowledge.
- If the docs don't contain the answer, reply: "I don't have that in the docs. Please contact human support."
- If the question is not about QuickNotes, reply: "I can only help with QuickNotes questions."
- If the question is unclear, ask a clarifying question.
- Never promise refunds or discounts.
- Never discuss other apps.
- Always be friendly.
- Always keep answers brief.
- If you are unsure, say you don't have that information.
- Never answer questions unrelated to the docs.
- Always stay on topic."""

LIGHT = """You are the support assistant for QuickNotes, a note-taking app. Be friendly and brief.

Decide in this order, and stop at the first match:
1. Not about QuickNotes -> reply exactly: "I can only help with QuickNotes questions."
2. Too vague to answer (for example it has no clear subject) -> ask ONE short clarifying question.
3. About QuickNotes but not covered in the docs -> reply exactly: "I don't have that in the docs. Please contact human support."
4. Otherwise answer using only the docs, in 2 sentences or fewer. Never promise refunds or discounts."""

# (question, what the answer should contain, why)
TESTS = [
    ("Does QuickNotes have a dark mode?",       "don't have that",           "missing info"),
    ("Can I change it?",                         "?",                         "ambiguous"),
    ("What's the weather like in Mumbai?",       "only help with quicknotes", "out of scope"),
    ("How much does the Pro plan cost?",         "$8",                        "normal question"),
    ("How long do I have to ask for a refund?",  "14",                        "normal question"),
]

def run(name, system):
    passed = 0
    print(f"=== {name} ===")
    for q, must_contain, kind in TESTS:
        user = f"<docs>\n{DOCS}\n</docs>\n\n<question>\n{q}\n</question>"
        out = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)]).content
        ok = must_contain in out.lower().replace("\u2019", "'")
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} [{kind}] {q}\n     -> {out.strip()}")
    print(f"{name}: {passed}/{len(TESTS)}\n")

run("rulebook (12 rules)", RULEBOOK)
run("light (4 ordered steps)", LIGHT)