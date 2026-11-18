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

CORE = "You are the support assistant for QuickNotes. Answer using only the docs provided."

VAGUE = CORE + "\nBe brief and friendly."

SPECIFIC = CORE + """
Style rules:
- At most 2 sentences.
- Plain text only: no bullet points, no headings, no bold.
- Friendly, like a helpful shop assistant."""


WITH_EXAMPLE = SPECIFIC + """

Example of a good answer:
Question: Can I use QuickNotes on two devices?
Answer: Yes! Your notes sync automatically across devices whenever you're online."""

QUESTIONS = [
    "Tell me everything about plans and refunds and syncing.",
    "How does the refund policy work?",
    "What does the Pro plan include?",
    "How does sync work?",
]

def sentences(text):
    return len([s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s])

def has_markdown(text):
    return bool(re.search(r"(^|\n)\s*([-*•]|#|\d+\.)\s|\*\*", text))

def run(name, system):
    counts, md = [], 0
    print(f"=== {name} ===")
    for q in QUESTIONS:
        user = f"<docs>\n{DOCS}\n</docs>\n\n<question>\n{q}\n</question>"
        out = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)]).content.strip()
        counts.append(sentences(out))
        md += has_markdown(out)
        print(f"[{counts[-1]} sentences] {out}\n")
    print(f"{name}: sentences per answer {counts}, answers with markdown: {md}/{len(QUESTIONS)}, within 2 sentences: {sum(c <= 2 for c in counts)}/{len(QUESTIONS)}\n")

run("vague", VAGUE)
run("specific", SPECIFIC)
run("specific + example", WITH_EXAMPLE)