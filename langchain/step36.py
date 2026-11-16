import json
import sys
import time
from langchain_core.prompts import ChatPromptTemplate
from models import get_model

TOTAL = int(sys.argv[1]) if len(sys.argv) > 1 else 200   # size of the real job
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 5       # planned concurrency
SAMPLE = 5


# USD per 1 million tokens: fill from your provider's pricing page (0.0 = unknown)
INPUT_PER_M = 0.30
OUTPUT_PER_M = 2.50

texts = json.load(open("texts.json", encoding="utf-8"))
chain = ChatPromptTemplate.from_template(
    "Summarize this in one short sentence:\n\n{text}"
) | get_model()

tin = tout = 0
start = time.perf_counter()
for t in texts[:SAMPLE]:
    r = chain.invoke({"text": t})
    tin += (r.usage_metadata or {}).get("input_tokens", 0)
    tout += (r.usage_metadata or {}).get("output_tokens", 0)
secs_per_call = (time.perf_counter() - start) / SAMPLE

est_in = tin / SAMPLE * TOTAL
est_out = tout / SAMPLE * TOTAL
est_cost = est_in / 1e6 * INPUT_PER_M + est_out / 1e6 * OUTPUT_PER_M
est_time = secs_per_call * TOTAL / CAP

print(f"Sample of {SAMPLE}: avg {tin/SAMPLE:.0f} tokens in, {tout/SAMPLE:.0f} out, {secs_per_call:.1f}s per call")
print(f"\nEstimate for {TOTAL} items:")
print(f"  requests: {TOTAL}")
print(f"  tokens:   ~{est_in:,.0f} in, ~{est_out:,.0f} out")
print(f"  cost:     ~${est_cost:.4f} (0 means you haven't filled in the prices)")
print(f"  time:     ~{est_time/60:.1f} min at best with {CAP} at once")
print("  Add a safety margin of about 20-30%.")