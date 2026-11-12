import time
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen2.5-coder:7b")

start = time.perf_counter()
response = model.invoke("In one sentence, what is LangChain?")
elapsed = time.perf_counter() - start

print(response.content)
print("USAGE:", response.usage_metadata)
print(f"TIME: {elapsed:.1f}s")