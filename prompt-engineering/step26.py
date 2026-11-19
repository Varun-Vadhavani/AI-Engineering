from step25 import CASES, BASE, msg, docs_and

def chain_v2(c):
    # Step 1: extract the questions (unchanged)
    qs = msg("List each separate question in the customer's message as a numbered list. Output only the list.",
             f"<customer_message>\n{c}\n</customer_message>")
    # Step 2: now allowed to work things out; the clean answers come after "ANSWERS:"
    work = msg(BASE + """
Answer each numbered question using only the docs.
First work through each one step by step, writing out every fact and calculation.
Then write ANSWERS: followed by one line per question with the final figures.""",
               docs_and(f"<questions>\n{qs}\n</questions>"))
    facts = work.split("ANSWERS:")[-1].strip()
    # Step 3: write from the verified answers and keep the key figures
    reply = msg(BASE + "\nWrite the final reply (at most 5 sentences) using ONLY the answers provided. "
                "Include every key number and the refund decision from the answers. Do not add or change any facts.",
                f"<customer_message>\n{c}\n</customer_message>\n\n<answers>\n{facts}\n</answers>")
    return qs, facts, reply

clean = lambda t: t.replace(",", "")

for i, (c, check) in enumerate(CASES, start=1):
    qs, facts, reply = chain_v2(c)
    step2_ok = check(clean(facts))
    final_ok = check(clean(reply))
    print(f"case {i}: step 2 facts {'OK ' if step2_ok else 'BAD'} | final reply {'OK ' if final_ok else 'BAD'}")
    print(f"   questions: {qs.replace(chr(10), ' | ')}")
    print(f"   facts:     {facts.replace(chr(10), ' | ')}")
    print(f"   reply:     {reply}\n")