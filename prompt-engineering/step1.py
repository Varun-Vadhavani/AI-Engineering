from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Use the same model line you used in your earlier steps
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

# A tiny fake "docs" so we know exactly what is and isn't in it
DOCS = """
QuickNotes Help Center

Plans: Free plan allows up to 50 notes. Pro plan costs $8 per month
and allows unlimited notes and file attachments up to 25 MB.

Refunds: Pro subscriptions can be refunded within 14 days of the first
payment. After 14 days, no refunds are given, but you can cancel anytime
and keep access until the end of the billing period.

Sync: Notes sync across devices automatically when you are online.
"""

QUESTIONS = [
    "How much does the Pro plan cost?",                       # answer IS in the docs
    "Does QuickNotes support dark mode?",                     # answer is NOT in the docs
    "Explain the refund policy to a customer in 2 sentences.",# needs a specific format
]

# The vague, one-line prompt
for q in QUESTIONS:
    prompt = f"Answer questions about these docs.\n{DOCS}\n{q}"
    response = llm.invoke(prompt)
    print("Q:", q)
    print("A:", response.content)
    print("-" * 40)