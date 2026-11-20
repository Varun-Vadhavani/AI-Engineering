import re
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

GOOD = """You are the support assistant for QuickNotes. Customers read your answers directly.
Rules:
- Use only the docs in the user's message.
- If the docs don't contain the answer, reply exactly: "I don't have that in the docs."
- Keep answers to at most 2 sentences.
Format every reply as two lines:
Answer: <answer>
Source: <line from the docs, or none>"""

VARIANTS = {
    "good (control)": (GOOD, True),
    "1 vague": ("You are a helpful assistant for QuickNotes customers.", True),
    "2 contradicting": (GOOD.replace("- Keep answers to at most 2 sentences.",
                        "- Keep answers to at most 2 sentences.\n- Always explain your reasoning in full detail."), True),
    "3 poor example": (GOOD + "\n\nExample:\nQuestion: Does QuickNotes work offline?\n"
                       "Answer: Yes, QuickNotes works offline.\nSource: none", True),
    "4 missing context": (GOOD, False),   # same prompt, but the docs are NOT sent
    "5 unclear format": (GOOD.replace("Format every reply as two lines:\nAnswer: <answer>\nSource: <line from the docs, or none>",
                         "Reply in a clear, nicely formatted way."), True),
}

QUESTIONS = [
    "How much does the Pro plan cost?",
    "Does QuickNotes have a dark mode?",
    "Tell me everything about plans, refunds and syncing.",
    "Can I get a refund after 20 days?",
]

def n_sentences(t):
    return len([s for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s])

for name, (system, send_docs) in VARIANTS.items():
    print(f"=== {name} ===")
    for q in QUESTIONS:
        user = (f"<docs>\n{DOCS}\n</docs>\n\n" if send_docs else "") + f"<question>\n{q}\n</question>"
        out = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)]).content.strip()
        fmt = "answer:" in out.lower() and "source:" in out.lower()
        print(f"[format ok: {fmt!s:5} | {n_sentences(out)} sentences] {q}\n   -> {out}\n")