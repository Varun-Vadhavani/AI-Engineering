import threading
import time
from langchain_core.runnables import RunnableLambda

active = 0
peak = 0
lock = threading.Lock()

def fake_api_call(x):
    global active, peak
    with lock:
        active += 1
        peak = max(peak, active)
    time.sleep(0.5)                 # pretend the API takes half a second
    with lock:
        active -= 1
    return f"done {x}"

step = RunnableLambda(fake_api_call)
inputs = list(range(12))

for limit in (None, 3, 1):
    active = peak = 0
    config = {"max_concurrency": limit} if limit else {}
    start = time.perf_counter()
    step.batch(inputs, config=config)
    secs = time.perf_counter() - start
    print(f"max_concurrency={limit}: peak at once = {peak}, total time = {secs:.1f}s")