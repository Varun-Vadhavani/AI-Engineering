import re, time
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from messages import MESSAGES

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

DEFINITIONS = """Urgency definitions:
- HIGH: data loss, money problems (double charge), locked out of the account, or a security problem.
- MEDIUM: something is broken or slow, but there is a workaround or the customer can still use the app.
- LOW: questions, feature requests, cosmetic issues, or thanks. Ignore shouting and exclamation marks; judge by impact."""

DIRECT = f"""Classify the urgency of a support message as LOW, MEDIUM or HIGH.
{DEFINITIONS}
Reply with ONLY one line in this format, with no explanation:
FINAL: <label>"""

REASONING = f"""Classify the urgency of a support message as LOW, MEDIUM or HIGH.
{DEFINITIONS}
First think it through step by step, explaining the impact on the customer.
Then give your answer on the last line, in this format:
FINAL: <label>"""

def get_label(text):
    m = re.findall(r"FINAL:\s*\**\s*(LOW|MEDIUM|HIGH)", text.upper())
    return m[-1] if m else ""

def run(name, system):
    correct, tokens, secs, wrong = 0, 0, 0.0, []
    for i, (text, expected) in enumerate(MESSAGES, start=1):
        t0 = time.perf_counter()
        r = llm.invoke([SystemMessage(content=system), HumanMessage(content=f"Message: {text}")])
        secs += time.perf_counter() - t0
        tokens += (getattr(r, "usage_metadata", None) or {}).get("output_tokens", 0)
        got = get_label(r.content)
        if got == expected:
            correct += 1
        else:
            wrong.append((i, expected, got or "(none)"))
    print(f"{name:16} correct {correct}/10 | output tokens {tokens:5} | time {secs:5.1f}s | wrong: {wrong}")

run("direct", DIRECT)
run("reasoning first", REASONING)