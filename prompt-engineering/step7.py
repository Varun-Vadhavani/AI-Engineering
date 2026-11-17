from langchain_ollama import ChatOllama
from prompts import SUPPORT_PROMPT

llm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192)
chain = SUPPORT_PROMPT | llm

DOCS = """
QuickNotes Help Center

Plans: Free plan allows up to 50 notes. Pro plan costs $8 per month
and allows unlimited notes and file attachments up to 25 MB.

Refunds: Pro subscriptions can be refunded within 14 days of the first
payment. After 14 days, no refunds are given, but you can cancel anytime
and keep access until the end of the billing period.

Sync: Notes sync across devices automatically when you are online.
"""

out = chain.invoke({
    "docs": DOCS,
    "question": "Can I get a refund after 20 days?",
    "max_sentences": 2,
})
print(out.content)