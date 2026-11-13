from models import get_model

model = get_model()

pieces = []
for chunk in model.stream("Explain how the internet works in about 80 words."):
    print(chunk.content, end="", flush=True)   # show it live
    pieces.append(chunk.content)               # and keep it

print("\n")
full_text = "".join(pieces)
print("Pieces received:", len(pieces))
print("Full text length:", len(full_text), "characters")

combined = None
for chunk in model.stream("Say hello in five languages."):
    combined = chunk if combined is None else combined + chunk

print(combined.content)
print("USAGE:", combined.usage_metadata)
print("METADATA:", combined.response_metadata)