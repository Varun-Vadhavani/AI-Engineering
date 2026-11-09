import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

texts = [
    "Hello world",
    "unbelievable",
    "Strawberry",
    "2026 + 17 = 2043",
    "    indented_code()",
    "Hello, how are you?",
    "नमस्ते, आप कैसे हैं?",
]

for t in texts:
    ids = enc.encode(t)
    pieces = [enc.decode([i]) for i in ids]
    print(f"{len(ids):>3} tokens | {t!r}")
    print(f"      ids:    {ids}")
    print(f"      pieces: {pieces}\n")