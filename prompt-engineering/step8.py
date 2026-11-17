from langchain_ollama import ChatOllama
from messages import MESSAGES

# temperature=0 makes the model pick its most likely answer every time,
# so reruns give the same results and our counts are comparable
llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

INSTRUCTION = "Classify the urgency of this support message as LOW, MEDIUM or HIGH. Reply with only the label."

correct = 0
for text, expected in MESSAGES:
    raw = llm.invoke(f"{INSTRUCTION}\n\nMessage: {text}").content
    got = raw.strip().upper()
    ok = got == expected
    correct += ok
    print(f"{'OK ' if ok else 'BAD'} expected={expected:6} got={got!r}  | {text[:50]}")

print(f"\nZero-shot score: {correct}/{len(MESSAGES)}")