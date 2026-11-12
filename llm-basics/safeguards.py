import json
import re
import requests
from llm import ask_full

# --- Safeguard 1: CHECK the output, retry, then escalate to a human ---
def nine_words_no_e(max_tries: int = 5):
    prompt = ("Write one sentence about the ocean that has exactly 9 words "
              "and contains no letter 'e'. Reply with only the sentence.")
    for attempt in range(1, max_tries + 1):
        s = ask_full(prompt, max_tokens=100)[0].strip()
        if len(s.split()) == 9 and "e" not in s.lower():
            return s, attempt
    return None, max_tries

sentence, tries = nine_words_no_e()
if sentence:
    print(f"1. passed validation on try {tries}: {sentence}")
else:
    print("1. NEEDS HUMAN REVIEW: all attempts failed validation")

# --- Safeguard 2: let CODE do the exact work, the model only parses ---
question = "What is 482915 times 7361?"
raw, _, _ = ask_full(
    f'Extract the two numbers from: "{question}"\n'
    'Reply with only JSON like {"a": 1, "b": 2}.', max_tokens=50)
nums = json.loads(raw.replace("```json", "").replace("```", "").strip())
print(f"2. computed by Python: {nums['a'] * nums['b']}")

# --- Safeguard 3: GIVE it the right document, and permit "not provided" ---
info = requests.get("https://pypi.org/pypi/requests/json", timeout=15).json()["info"]
context = (f"Package: {info['name']}\nLatest version: {info['version']}\n"
           f"Summary: {info['summary']}")

for q in ["What is the latest version of requests?",
          "How many people contribute to requests?"]:
    answer, _, _ = ask_full(
        f"Use ONLY the information below. If the answer is not there, reply 'not provided'.\n\n"
        f"{context}\n\nQuestion: {q}", max_tokens=60)
    print(f"3. {q} -> {answer}")