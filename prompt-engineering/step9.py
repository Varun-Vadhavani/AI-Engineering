from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from messages import MESSAGES

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

INSTRUCTION = "Classify the urgency of this support message as LOW, MEDIUM or HIGH. Reply with only the label."

# Three examples: one per label, with a tricky one in the mix.
# None of them is a copy of a test message.
EXAMPLES = [
    ("My files from last month are missing after I restored a backup.", "HIGH"),
    ("PLEASE FIX!!! The settings page has a typo in the word 'preferences'.", "LOW"),
    ("Notifications arrive late on my tablet, though they work fine on my phone.", "MEDIUM"),
]

def build_messages(text):
    msgs = [SystemMessage(content=INSTRUCTION)]
    for ex_text, ex_label in EXAMPLES:
        msgs.append(HumanMessage(content=f"Message: {ex_text}"))
        msgs.append(AIMessage(content=ex_label))
    msgs.append(HumanMessage(content=f"Message: {text}"))
    return msgs

correct = 0
for text, expected in MESSAGES:
    raw = llm.invoke(build_messages(text)).content
    got = raw.strip().upper()
    ok = got == expected
    correct += ok
    print(f"{'OK ' if ok else 'BAD'} expected={expected:6} got={got!r}  | {text[:50]}")

print(f"\nFew-shot score: {correct}/{len(MESSAGES)}")