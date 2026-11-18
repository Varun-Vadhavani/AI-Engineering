import json, re
from pydantic import BaseModel, Field
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

class SupportAnswer(BaseModel):
    answer: str = Field(description="Short answer for the customer")
    found_in_docs: bool = Field(description="True only if the docs contain the answer")

# (question, should found_in_docs be True?)
TESTS = [
    ("How much does the Pro plan cost?", True),
    ("Does QuickNotes have a dark mode?", False),
    ("How long do I have to ask for a refund?", True),
    ("What's the weather like in Mumbai?", False),
    ("How does sync work?", True),
    ("Can I use QuickNotes on Linux?", False),
    ("What is the attachment size limit on Pro?", True),
    ("Is there a mobile app?", False),
]

PROMPT_ONLY = """You are the support assistant for QuickNotes. Answer using only the docs provided.
Reply with ONLY a JSON object, no other text:
{"answer": "<string>", "found_in_docs": <true or false>}"""

BASIC = "You are the support assistant for QuickNotes. Answer using only the docs provided."

def user_msg(q):
    return f"<docs>\n{DOCS}\n</docs>\n\n<question>\n{q}\n</question>"

def valid(d):
    return (isinstance(d, dict) and isinstance(d.get("answer"), str)
            and isinstance(d.get("found_in_docs"), bool))

strict_ok = tolerant_ok = structured_ok = 0
flag_ok = {"prompt": 0, "structured": 0}
structured_llm = llm.with_structured_output(SupportAnswer)

for q, expected in TESTS:
    # A) prompt-only, parsed exactly as returned
    raw = llm.invoke([SystemMessage(content=PROMPT_ONLY), HumanMessage(content=user_msg(q))]).content
    try:
        d = json.loads(raw)
        strict = valid(d)
    except Exception:
        d, strict = None, False
    strict_ok += strict

    # B) prompt-only, with the clean-up code you'd have to write
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        d2 = json.loads(cleaned)
        tolerant = valid(d2)
    except Exception:
        d2, tolerant = None, False
    tolerant_ok += tolerant
    if tolerant and d2["found_in_docs"] == expected:
        flag_ok["prompt"] += 1

    # C) structured output with the Pydantic schema
    try:
        res = structured_llm.invoke([SystemMessage(content=BASIC), HumanMessage(content=user_msg(q))])
        ok = isinstance(res, SupportAnswer)
    except Exception as e:
        res, ok = None, False
    structured_ok += ok
    if ok and res.found_in_docs == expected:
        flag_ok["structured"] += 1

    print(f"Q: {q}")
    print(f"  prompt-only strict: {'OK ' if strict else 'FAIL'} | cleaned: {'OK ' if tolerant else 'FAIL'} | structured: {'OK' if ok else 'FAIL'}")
    if not strict:
        print(f"  raw prompt-only output: {raw[:90]!r}")

n = len(TESTS)
print(f"\nUsable output, prompt-only strict: {strict_ok}/{n}")
print(f"Usable output, prompt-only + clean-up code: {tolerant_ok}/{n}")
print(f"Usable output, structured output: {structured_ok}/{n}")
print(f"found_in_docs flag correct: prompt-only {flag_ok['prompt']}/{n}, structured {flag_ok['structured']}/{n}")