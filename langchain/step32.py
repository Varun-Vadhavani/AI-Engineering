from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()

# ---- Part A: with_retry, using fake steps so the results are predictable ----
calls = {"n": 0}

def flaky(x):
    calls["n"] += 1
    print(f"    flaky call #{calls['n']}")
    if calls["n"] < 3:
        raise ConnectionError("network blip")
    return f"ok: {x}"

def broken(x):
    print("    broken call")
    raise ValueError("bad input")

retry_opts = dict(stop_after_attempt=4,
                  retry_if_exception_type=(ConnectionError,),
                  wait_exponential_jitter=False)   # False = no waiting, just for a fast demo

print("flaky (temporary error):")
print("  ", RunnableLambda(flaky).with_retry(**retry_opts).invoke("hello"))

print("broken (permanent error):")
try:
    RunnableLambda(broken).with_retry(**retry_opts).invoke("x")
except ValueError as e:
    print("   failed immediately:", e)

# ---- Part B: with_fallbacks, using real models ----
backup = ChatOllama(model="qwen2.5-coder:7b")

print("\nfallback when the model name is wrong:")
bad_name = ChatGoogleGenerativeAI(model="gemini-9000", max_retries=0, timeout=20)
r = bad_name.with_fallbacks([backup]).invoke("Say hi in one word.")
print("  ", repr(r.content), "| answered by:", r.response_metadata.get("model_name") or r.response_metadata.get("model"))

print("\nfallback when the call times out:")
too_slow = ChatGoogleGenerativeAI(model="gemini-3.6-flash", max_retries=0, timeout=0.01)
r = too_slow.with_fallbacks([backup]).invoke("Say hi in one word.")
print("  ", repr(r.content), "| answered by:", r.response_metadata.get("model_name") or r.response_metadata.get("model"))