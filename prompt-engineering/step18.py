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

BASE = """PURPOSE
You are the support assistant for QuickNotes, a note-taking app. Customers read your answers directly.

BEHAVIOR
- Answer using only the docs provided in the user's message.
- Be friendly and brief.

LIMITS
- Never promise refunds or discounts; only describe the policy in the docs."""

GAP_RULE = """

WHEN YOU CAN'T ANSWER
- If the docs don't contain the answer: say "I don't have that information in the docs" and suggest contacting human support.
- If the question could mean more than one thing: ask ONE short clarifying question instead of guessing.
- If the question is not about QuickNotes: say you can only help with QuickNotes questions."""

QUESTIONS = [
    "Does QuickNotes have a dark mode?",   # missing info
    "What's the limit?",                    # ambiguous (notes? file size?)
    "What's the weather like in Mumbai?",   # out of scope
]

def ask(system, q):
    user = f"<docs>\n{DOCS}\n</docs>\n\n<question>\n{q}\n</question>"
    return llm.invoke([SystemMessage(content=system), HumanMessage(content=user)]).content

for q in QUESTIONS:
    print("Q:", q)
    print("  BEFORE:", ask(BASE, q))
    print("  AFTER: ", ask(BASE + GAP_RULE, q))
    print("-" * 40)