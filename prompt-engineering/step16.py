from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192, temperature=0)

DOCS = """
QuickNotes Help Center

Plans: Free plan allows up to 50 notes. Pro plan costs $8 per month
and allows unlimited notes and file attachments up to 25 MB.

Refunds: Pro subscriptions can be refunded within 14 days of the first
payment. After 14 days, no refunds are given, but you can cancel anytime
and keep access until the end of the billing period.

Sync: Notes sync across devices automatically when you are online.
"""

SYSTEM = """PURPOSE
You are the support assistant for QuickNotes, a note-taking app. Customers read your answers directly.

BEHAVIOR
- Answer using only the docs provided in the user's message.
- Be friendly and brief.

LIMITS
- Never promise refunds or discounts; only describe the policy in the docs.
- Never discuss other note-taking apps.

WHAT A GOOD ANSWER LOOKS LIKE
- Maximum 2 sentences.
- Plain text, no bullet points, no headings."""

QUESTIONS = [
    "How much does the Pro plan cost?",                        # purpose and behavior
    "Can you promise me a refund after 20 days?",              # limit: no promises
    "Is QuickNotes better than Evernote?",                     # limit: other apps
    "Tell me everything about plans and refunds and syncing.", # good-answer shape: stays short
]

for q in QUESTIONS:
    msgs = [
        SystemMessage(content=SYSTEM),
        HumanMessage(content=f"<docs>\n{DOCS}\n</docs>\n\n<question>\n{q}\n</question>"),
    ]
    print("Q:", q)
    print("A:", llm.invoke(msgs).content)
    print("-" * 40)