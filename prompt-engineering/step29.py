from collections import Counter
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from tests import DOCS, TESTS

llm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192, temperature=0)

PROMPT_V1 = """You are the support assistant for QuickNotes. Customers read your answers directly.
Rules:
- Use only the docs in the user's message.
- If the docs don't contain the answer, reply exactly: "I don't have that in the docs."
- Keep answers to at most 2 sentences.
Format every reply as two lines:
Answer: <answer>
Source: <line from the docs, or none>"""

print("Test set:", dict(Counter(t["cat"] for t in TESTS)), "| total", len(TESTS), "\n")

for t in TESTS:
    user = f"<docs>\n{DOCS}\n</docs>\n\n<question>\n{t['q']}\n</question>"
    out = llm.invoke([SystemMessage(content=PROMPT_V1), HumanMessage(content=user)]).content.strip()
    print(f"#{t['id']} [{t['cat']}] {t['q']}")
    print(f"   expected: {t['expected']}")
    print(f"   got:      {out.replace(chr(10), ' | ')}\n")