import json
import sys
import time
from langchain_core.prompts import ChatPromptTemplate
from models import get_model

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 5

# Fill these from your provider's pricing page (USD per 1 million tokens).
# For Google Gemini 2.5 Flash, current paid-tier pricing is:
# - input: $0.30 / 1M tokens
# - output: $2.50 / 1M tokens
INPUT_PER_M = 0.30
OUTPUT_PER_M = 2.50

texts = json.load(open("texts.json", encoding="utf-8"))[:N]
inputs = [{"text": t} for t in texts]

prompt = ChatPromptTemplate.from_template(
    "Summarize this in one short sentence:\n\n{text}"
)
chain = prompt | get_model()

def report(label, results, secs):
    errors = [r for r in results if isinstance(r, Exception)]
    good = [r for r in results if not isinstance(r, Exception)]
    tin = sum((r.usage_metadata or {}).get("input_tokens", 0) for r in good)
    tout = sum((r.usage_metadata or {}).get("output_tokens", 0) for r in good)
    cost = tin / 1e6 * INPUT_PER_M + tout / 1e6 * OUTPUT_PER_M
    print(f"{label}")
    print(f"   time: {secs:.1f}s | ok: {len(good)} | errors: {len(errors)}")
    print(f"   tokens: {tin} in, {tout} out | cost: ${cost:.4f}")
    if errors:
        print(f"   first error: {type(errors[0]).__name__}: {str(errors[0])[:120]}")

# --- One at a time ---
start = time.perf_counter()
sequential = []
for item in inputs:
    try:
        sequential.append(chain.invoke(item))
    except Exception as e:
        sequential.append(e)
report(f"SEQUENTIAL ({N} items)", sequential, time.perf_counter() - start)

# --- Concurrent, with a cap ---
start = time.perf_counter()
concurrent = chain.batch(inputs, config={"max_concurrency": CAP}, return_exceptions=True)
report(f"CONCURRENT ({N} items, max {CAP} at once)", concurrent, time.perf_counter() - start)

print("\nExample summary:", concurrent[0].content if not isinstance(concurrent[0], Exception) else "(first item failed)")