import time
from models import get_model

model = get_model()
question = "Write a detailed 300-word explanation of how the internet works."

# Without streaming
start = time.perf_counter()
full = model.invoke(question)
invoke_total = time.perf_counter() - start
print(f"invoke:  first word visible after {invoke_total:.1f}s (total {invoke_total:.1f}s)")

# With streaming
start = time.perf_counter()
first = None
for chunk in model.stream(question):
    if first is None and chunk.content:        # first NON-EMPTY piece
        first = time.perf_counter() - start
stream_total = time.perf_counter() - start
print(f"stream:  first word visible after {first:.1f}s (total {stream_total:.1f}s)")