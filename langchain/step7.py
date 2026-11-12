from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def ask(model, question):
    r = model.invoke(question)
    reason = r.response_metadata.get("finish_reason")
    print(f"  finish_reason: {reason}")
    print(f"  tokens: {r.usage_metadata}")
    print(f"  text: {r.content!r}")
    if reason != "STOP":
        print("  WARNING: the answer did not finish normally.")

print("Normal model:")
ask(ChatGoogleGenerativeAI(model="gemini-3.6-flash"),
    "Explain what a prompt template is in 3 sentences.")

print("\nModel with a tiny output limit:")
ask(ChatGoogleGenerativeAI(model="gemini-3.6-flash", max_tokens=20),
    "Explain what a prompt template is in 3 sentences.")