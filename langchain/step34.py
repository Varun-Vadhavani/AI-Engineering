import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from errors import get_code

load_dotenv()
logging.basicConfig(filename="errors.log", level=logging.WARNING, format="%(asctime)s %(message)s")

MAX_CHARS = 8000

good = ChatGoogleGenerativeAI(model="gemini-3.6-flash", max_retries=0, timeout=30)
badkey = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key="not-a-real-key", max_retries=0, timeout=30)
slow = ChatGoogleGenerativeAI(model="gemini-3.6-flash", max_retries=0, timeout=0.01)
offline = ChatOllama(model="qwen2.5-coder:7b", base_url="http://localhost:9999")

def friendly_message(e):
    code = get_code(e)
    text = (type(e).__name__ + " " + str(e)).lower()
    if code == 429 or "rate limit" in text or "resource exhausted" in text:
        return "We're getting a lot of requests right now. Please try again in a minute."
    if "timeout" in text or "timed out" in text or "deadline" in text:
        return "That took too long to answer. Please try again."
    if code in (401, 403) or "api key" in text:
        return "The assistant is not set up correctly right now. The team has been notified."
    return "Something went wrong on our side. Please try again later."

def answer(question, model):
    if len(question) > MAX_CHARS:                       # too-long input: reject early
        return "That message is too long. Please shorten it and try again."
    try:
        return model.invoke(question).content
    except Exception as e:
        logging.warning("model call failed: %s: %s", type(e).__name__, e)
        return friendly_message(e)

tests = [
    ("working model",         good,                                   "Say hi in one word."),
    ("bad key",               badkey,                                 "Say hi in one word."),
    ("timeout",               slow,                                   "Say hi in one word."),
    ("primary bad, backup ok", badkey.with_fallbacks([good]),         "Say hi in one word."),
    ("everything down",       badkey.with_fallbacks([offline]),       "Say hi in one word."),
    ("input too long",        good,                                   "x" * 9000),
]

for label, model, q in tests:
    print(f"{label}:\n   USER SEES: {answer(q, model)}\n")