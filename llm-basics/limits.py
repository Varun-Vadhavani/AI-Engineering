from llm import ask_full

prompt = "List 10 fruits, one per line, numbered like '1. Apple'."

# 1. Normal run
text, reason, usage = ask_full(prompt, max_tokens=100)
print(f"NORMAL      stop_reason={reason!r} out_tokens={usage['completion_tokens']}\n{text}\n")

# 2. A max_tokens cap that is too small
text, reason, usage = ask_full(prompt, max_tokens=15)
print(f"TOO SHORT   stop_reason={reason!r} out_tokens={usage['completion_tokens']}\n{text}\n")

# 3. A stop sequence: end the moment the model starts item 4
text, reason, usage = ask_full(prompt, max_tokens=100, stop_sequences=["4."])
print(f"STOP SEQ    stop_reason={reason!r} out_tokens={usage['completion_tokens']}\n{text}\n")