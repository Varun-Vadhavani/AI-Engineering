from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

INSTRUCTION = "Classify the sentiment of this message as POSITIVE, NEGATIVE or NEUTRAL. Reply with only the label."

SENTIMENT = [
    ("I love the new update, everything feels faster.", "POSITIVE"),
    ("This is the worst app I have ever used.", "NEGATIVE"),
    ("What time does support open on Monday?", "NEUTRAL"),
    ("Thanks so much, the issue is finally fixed!", "POSITIVE"),
    ("The app crashed again and I lost my work. Very disappointing.", "NEGATIVE"),
    ("I am writing to ask how to export my notes.", "NEUTRAL"),
    ("Great, another crash. Just what I needed today.", "NEGATIVE"),  # sarcasm
    ("The tag feature is useful, but search is still slow.", "NEUTRAL"),  # mixed
]

correct = 0
for text, expected in SENTIMENT:
    got = llm.invoke(f"{INSTRUCTION}\n\nMessage: {text}").content.strip().upper()
    ok = got == expected
    correct += ok
    print(f"{'OK ' if ok else 'BAD'} expected={expected:8} got={got!r}  | {text[:50]}")

print(f"\nZero-shot sentiment: {correct}/{len(SENTIMENT)}")