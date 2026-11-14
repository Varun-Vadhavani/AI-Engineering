from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from models import get_model

model = get_model()
LABELS = ["code", "math", "general"]

# --- Step 1 of the router: classify ---
classify_chain = (
    ChatPromptTemplate.from_template(
        "Classify this question into exactly one category: code, math, or general.\n"
        "Reply with ONLY the category word.\n\nQuestion: {question}"
    )
    | model
    | StrOutputParser()
)

def clean_label(raw):
    """Never trust the model's wording: map whatever it said to a known label."""
    raw = raw.strip().lower()
    for label in LABELS:
        if label in raw:
            return label
    return "general"          # safe default

# --- One prompt per path ---
PROMPTS = {
    "code": "You are a senior programmer. Answer with a short explanation and a small code example.\n\nQuestion: {question}",
    "math": "You are a careful math tutor. Work step by step, then state the final answer clearly.\n\nQuestion: {question}",
    "general": "You are a friendly assistant. Answer in at most three sentences.\n\nQuestion: {question}",
}

def route(inputs):
    label = inputs["label"]
    print(f"  routed to: {label}")
    prompt = ChatPromptTemplate.from_template(PROMPTS[label])
    return prompt | model | StrOutputParser()      # returning a chain: LangChain runs it

# classify -> keep the question and add the label -> pick a path
full_chain = (
    RunnablePassthrough.assign(label=classify_chain | clean_label)
    | RunnableLambda(route)
)

for q in [
    "How do I reverse a list in Python?",
    "What is 15% of 840?",
    "Why is the sky blue?",
    "Can you help me with something?",
]:
    print("\nQ:", q)
    print("A:", full_chain.invoke({"question": q}))