from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

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
    "How much does the Pro plan cost?",
    "Does QuickNotes support dark mode?",
    "Explain the refund policy to a customer in 2 sentences.",
]

PROMPT = """<context>
You are a support assistant for QuickNotes, a note-taking app. Your answers
are shown directly to customers.
</context>

<docs>
{docs}
</docs>

<instructions>
Answer the customer's question using the docs above.
</instructions>

<constraints>
- Use ONLY information from the docs. Never guess or add outside knowledge.
- If the docs do not cover the question, reply exactly: Not covered in the docs.
- Keep the answer to 2 sentences at most.
</constraints>

<example>
Question: Do my notes sync between phone and laptop?
Answer: Yes, notes sync across devices automatically when you are online.
Source: "Notes sync across devices automatically when you are online."
</example>

<output_format>
Answer: <your answer>
Source: <the exact line from the docs that supports it, or "none">
</output_format>

<question>
{question}
</question>"""

for q in QUESTIONS:
    prompt = PROMPT.format(docs=DOCS, question=q)
    response = llm.invoke(prompt)
    print("Q:", q)
    print("A:", response.content)
    print("-" * 40)