import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from models import get_model

model = get_model()

def make(instruction):
    prompt = ChatPromptTemplate.from_template(instruction + "\n\nText:\n{text}")
    return prompt | model | StrOutputParser()

summary   = make("Summarize this text in one sentence.")
tone      = make("Describe the tone of this text in 1 to 3 words only.")
questions = make("Write 2 quiz questions about this text, one per line.")

# Run the three branches at once
parallel = RunnableParallel(summary=summary, tone=tone, questions=questions)

# Combine step: its placeholders match the dict keys exactly
combine = (
    ChatPromptTemplate.from_template(
        "Write a short study card using these parts. Keep it under 80 words.\n\n"
        "Summary: {summary}\nTone: {tone}\nQuiz questions:\n{questions}"
    )
    | model
    | StrOutputParser()
)

full = parallel | combine

text = """Streaming sends a model's answer piece by piece instead of waiting for the
whole thing. It does not make the model faster, but users see the first words almost
immediately, so the app feels much quicker. Developers still need to collect the pieces
into a full answer to save it, and must handle cancelled or broken streams."""

# Timing: one after another
start = time.perf_counter()
s = summary.invoke({"text": text})
t = tone.invoke({"text": text})
q = questions.invoke({"text": text})
sequential_time = time.perf_counter() - start

# Timing: all at once
start = time.perf_counter()
parts = parallel.invoke({"text": text})
parallel_time = time.perf_counter() - start

print("PARTS:", parts, "\n")
print(f"sequential: {sequential_time:.1f}s   parallel: {parallel_time:.1f}s\n")
print("STUDY CARD:\n", full.invoke({"text": text}))