import random
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from errors import is_temporary

load_dotenv()

def call_with_retry(fn, max_attempts=3, base_delay=1.0):
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            if not is_temporary(e):
                print(f"  attempt {attempt}: PERMANENT ({type(e).__name__}), not retrying")
                raise
            if attempt == max_attempts:
                print(f"  attempt {attempt}: temporary, but out of attempts, giving up")
                raise
            delay = base_delay * 2 ** (attempt - 1) + random.uniform(0, 0.5)
            print(f"  attempt {attempt}: temporary ({type(e).__name__}), waiting {delay:.1f}s")
            time.sleep(delay)

def test(label, model):
    print(f"\n[{label}]")
    try:
        r = call_with_retry(lambda: model.invoke("Say hi in one word."))
        print("  RESULT:", r.content)
    except Exception as e:
        print("  FINAL FAILURE:", type(e).__name__)

test("good call",        ChatGoogleGenerativeAI(model="gemini-3.6-flash", max_retries=0, timeout=30))
test("wrong model name", ChatGoogleGenerativeAI(model="gemini-9000", max_retries=0, timeout=30))
test("tiny timeout",     ChatGoogleGenerativeAI(model="gemini-3.6-flash", max_retries=0, timeout=0.01))