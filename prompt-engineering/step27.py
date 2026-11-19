import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from step25 import DOCS, docs_and

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)  # a reasoning model

CASES = [
    ("We are 8 people, each on a separate Pro plan paid yearly. If we switch to the Team plan paid monthly "
     "for a full year, what would we pay in total, and how does that compare to the 8 Pro plans?",
     lambda o: "576" in o and "640" in o),
    ("I'm a team of 4 and want the Team plan. What would we pay per month? And if I pay today and change my "
     "mind in 10 days, can I get a refund?",
     lambda o: "30" in o and re.search(r"\byes\b|can get a refund|eligible", o) is not None),
    ("I paid for Pro on March 1. On March 20 I want to cancel and get a refund, then buy Pro yearly instead. "
     "Will I get the refund, and what will the yearly plan cost?",
     lambda o: "80" in o and re.search(r"\bnot\b|\bno\b|n't|unfortunately", o) is not None),
]

SCAFFOLDED = """You are the support assistant for QuickNotes. Use only the docs provided. Be friendly.
Think step by step:
1. List each question the customer asked.
2. For each one, quote the relevant line from the docs.
3. Do any calculations one at a time.
4. Check your numbers again.
5. Write the final reply in at most 5 sentences."""

GOAL_BASED = """GOAL
Reply to a customer's multi-part question about QuickNotes accurately.

CONTEXT
You are the support assistant. The docs in the user's message are the only source of truth; they list prices, minimums and the refund window.

CONSTRAINTS
- Use only the docs. Apply every rule in them, including minimums and time limits.
- Friendly tone, at most 5 sentences, plain text.

A GOOD ANSWER
Addresses every part of the customer's message, states the final totals and the refund decision, and does not show the working."""

def run(name, system):
    ok_count, out_tokens, reasoning_tokens = 0, 0, 0
    print(f"=== {name} ===")
    for i, (c, check) in enumerate(CASES, start=1):
        r = llm.invoke([SystemMessage(content=system),
                        HumanMessage(content=docs_and(f"<customer_message>\n{c}\n</customer_message>"))])
        text = r.content if isinstance(r.content, str) else str(r.content)
        meta = getattr(r, "usage_metadata", None) or {}
        out_tokens += meta.get("output_tokens", 0)
        reasoning_tokens += (meta.get("output_token_details") or {}).get("reasoning", 0)
        ok = check(text.replace(",", "").lower())
        ok_count += ok
        print(f"{'OK ' if ok else 'BAD'} case {i}: {text.strip()}\n")
    print(f"{name}: correct {ok_count}/{len(CASES)}, output tokens {out_tokens}, of which hidden reasoning {reasoning_tokens}\n")

run("scaffolded", SCAFFOLDED)
run("goal-based", GOAL_BASED)