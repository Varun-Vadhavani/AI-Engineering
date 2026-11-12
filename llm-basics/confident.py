import sys

from llm import ask

sys.stdout.reconfigure(encoding="utf-8")

questions = [
    # 1. A well-known fact
    "What is the capital of France? One sentence.",
    # 2. A real but obscure question
    "Who won the 1987 Ranji Trophy final? One sentence.",
    # 3. A made-up thing, phrased as if it's real
    "Summarize the main argument of the 2019 paper 'Recursive Gradient Folding in Sparse Transformers' by Halvorsen and Mehta. Two sentences.",
]

for q in questions:
    print(f"Q: {q}")
    print(f"A: {ask(q)}\n")