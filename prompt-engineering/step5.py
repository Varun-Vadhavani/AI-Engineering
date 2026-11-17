from langchain_ollama import ChatOllama

# num_ctx raises the context window; Ollama's default is small and would
# silently cut off our long text
llm = ChatOllama(model="qwen2.5-coder:7b", num_ctx=8192)

FILLER = ("This section describes general background about the product, its "
          "history, and its design philosophy. It contains no policies. ") * 40

DOCS = {
    "pricing.md":  "Pro plan costs $8 per month. " + FILLER,
    "refunds.md":  "Pro subscriptions can be refunded within 14 days of first payment. " + FILLER,
    "security.md": "Account deletion requests are processed within 30 days. " + FILLER,
}

QUESTION = "Which document covers refunds, and what is the refund window?"

# Version A: question and instructions first, docs after, no labels
docs_plain = "\n\n".join(DOCS.values())
prompt_a = f"""Answer using the docs. Be brief.
Question: {QUESTION}

{docs_plain}"""

# Version B: labeled docs first, then instructions, then question last
docs_labeled = "\n".join(
    f'<document name="{name}">\n{text}\n</document>' for name, text in DOCS.items()
)
prompt_b = f"""<documents>
{docs_labeled}
</documents>

<instructions>
Answer using only the documents above. Name the document you used. Be brief.
</instructions>

<question>
{QUESTION}
</question>"""

print("=== A: question first, unlabeled ===")
print(llm.invoke(prompt_a).content)
print("\n=== B: docs first, labeled ===")
print(llm.invoke(prompt_b).content)