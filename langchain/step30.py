import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def attempt(label, model):
    start = time.perf_counter()
    try:
        r = model.invoke("Say hi in one word.")
        print(f"{label}: OK -> {r.content!r}")
    except Exception as e:
        secs = time.perf_counter() - start
        print(f"{label}: FAILED after {secs:.1f}s")
        print("   type:   ", type(e).__module__ + "." + type(e).__name__)
        print("   code:   ", getattr(e, "code", None) or getattr(e, "status_code", None))
        print("   message:", str(e)[:200].replace("\n", " "))
    print()

# max_retries=0 switches off the library's own built-in retrying,
# so each failure shows up immediately and in its raw form
print("=== GEMINI ===\n")
attempt("good call",        ChatGoogleGenerativeAI(model="gemini-3.6-flash", max_retries=0))
attempt("wrong model name", ChatGoogleGenerativeAI(model="gemini-9000", max_retries=0))
attempt("wrong key",        ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key="not-a-real-key", max_retries=0))
attempt("tiny timeout",     ChatGoogleGenerativeAI(model="gemini-3.6-flash", timeout=0.01, max_retries=0))

print("=== LOCAL (Ollama) ===\n")
try:
    from langchain_ollama import ChatOllama
    attempt("wrong model name", ChatOllama(model="no-such-model"))
    attempt("server not reachable", ChatOllama(model="qwen2.5-coder:7b", base_url="http://localhost:9999"))
except ImportError:
    print("langchain-ollama not installed, skipping")