from models import get_model

model = get_model()

for chunk in model.stream("Explain how the internet works in about 100 words."):
    print(chunk.content, end="", flush=True)

print()  # final newline