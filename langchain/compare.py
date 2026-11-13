import time
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()

QUESTIONS = [
    "Explain what a REST API is to a beginner.",
    "Write a Python function that checks if a string is a palindrome.",
    "What is the difference between a list and a tuple in Python?",
    "Give me 3 name ideas for a travel app about Gujarat.",
    "Why does 'git push' sometimes get rejected?",
    "Explain what a database index is and when it hurts.",
    "What does the 'async' keyword do in JavaScript?",
    "Summarize the idea of test-driven development.",
    "What is a token in an LLM?",
    "Is 17 * 23 equal to 391? Show your check.",
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer clearly in at most 4 sentences."),
    ("human", "{question}"),
])

models = {
    "gemini": prompt | ChatGoogleGenerativeAI(model="gemini-3.6-flash"),
    "local": prompt | ChatOllama(model="qwen2.5-coder:7b"),
}

# Warm-up: load the local model into memory so load time doesn't distort question 1
models["local"].invoke({"question": "hi"})

lines = ["# Model comparison\n"]
totals = {name: 0.0 for name in models}

for i, q in enumerate(QUESTIONS, 1):
    lines.append(f"## Q{i}: {q}\n")
    for name, chain in models.items():
        start = time.perf_counter()
        try:
            r = chain.invoke({"question": q})
            text, out_tok = r.content, r.usage_metadata["output_tokens"]
        except Exception as e:
            text, out_tok = f"ERROR: {e}", 0
        secs = time.perf_counter() - start
        totals[name] += secs
        lines.append(f"**{name}** ({secs:.1f}s, {out_tok} output tokens)\n\n{text}\n")
        print(f"Q{i} {name}: {secs:.1f}s")

lines.append("## Total time\n")
for name, t in totals.items():
    lines.append(f"- {name}: {t:.1f}s")

with open("results.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("Saved results.md")