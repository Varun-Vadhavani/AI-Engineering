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

# (customer message, check on the final reply)
CASES = [
    ("We are 8 people, each on a separate Pro plan paid yearly. If we switch to the Team plan paid monthly "
     "for a full year, what would we pay in total, and how does that compare to the 8 Pro plans?",
     lambda o: "576" in o and "640" in o),
    ("I'm a team of 4 and want the Team plan. What would we pay per month? And if I pay today and change my "
     "mind in 10 days, can I get a refund?",
     lambda o: "30" in o and "14" in o),
    ("I paid for Pro on March 1. On March 20 I want to cancel and get a refund, then buy Pro yearly instead. "
     "Will I get the refund, and what will the yearly plan cost?",
     lambda o: "80" in o and re.search(r"\bnot\b|\bno\b|n't|unfortunately", o) is not None),
]

BASE = "You are the support assistant for QuickNotes. Use only the docs provided. Be friendly."

SINGLE = BASE + "\nAnswer every part of the customer's message in a short reply (at most 5 sentences)."

STEPS_IN_PROMPT = BASE + """
Do this in order:
1. List each question the customer asked.
2. Answer each one from the docs, writing out any calculation.
3. Then write the final reply (at most 5 sentences) under the heading REPLY:"""

def msg(system, user):
    return llm.invoke([SystemMessage(content=system), HumanMessage(content=user)]).content.strip()

def docs_and(text):
    return f"<docs>\n{DOCS}\n</docs>\n\n{text}"

def single(c):
    return msg(SINGLE, docs_and(f"<customer_message>\n{c}\n</customer_message>"))

def steps_in_prompt(c):
    out = msg(STEPS_IN_PROMPT, docs_and(f"<customer_message>\n{c}\n</customer_message>"))
    return out.split("REPLY:")[-1].strip()

def chain(c, show=False):
    # Step 1: extract the questions only
    qs = msg("List each separate question in the customer's message as a numbered list. Output only the list.",
             f"<customer_message>\n{c}\n</customer_message>")
    # Step 2: answer each question from the docs, with calculations, no writing style
    facts = msg(BASE + "\nAnswer each numbered question using only the docs. One line per question, "
                "show any calculation. Do not write a reply to the customer.",
                docs_and(f"<questions>\n{qs}\n</questions>"))
    # Step 3: write the reply from the verified answers only
    reply = msg(BASE + "\nWrite the final reply (at most 5 sentences) using ONLY the answers provided. "
                "Do not add or change any numbers.",
                f"<customer_message>\n{c}\n</customer_message>\n\n<answers>\n{facts}\n</answers>")
    if show:
        print("   [chain step 1]", qs.replace("\n", " | "))
        print("   [chain step 2]", facts.replace("\n", " | "))
    return reply

def run(name, fn):
    ok_count, secs = 0, 0.0
    print(f"=== {name} ===")
    for i, (c, check) in enumerate(CASES, start=1):
        t0 = time.perf_counter()
        out = fn(c)
        secs += time.perf_counter() - t0
        ok = check(out.replace(",", ""))
        ok_count += ok
        print(f"{'OK ' if ok else 'BAD'} case {i}: {out}\n")
    print(f"{name}: correct {ok_count}/{len(CASES)}, time {secs:.1f}s\n")

if __name__ == "__main__":
    run("single prompt", single)
    run("steps in one prompt", steps_in_prompt)
    run("chain of 3 calls", lambda c: chain(c, show=True))