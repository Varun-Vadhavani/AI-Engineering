from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from messages import MESSAGES

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

INSTRUCTION = "Classify the urgency of this support message as LOW, MEDIUM or HIGH. Reply with only the label."

def build_messages(examples, text):
    msgs = [SystemMessage(content=INSTRUCTION)]
    for ex_text, ex_label in examples:
        msgs.append(HumanMessage(content=f"Message: {ex_text}"))
        msgs.append(AIMessage(content=ex_label))
    msgs.append(HumanMessage(content=f"Message: {text}"))
    return msgs

def score(examples):
    """Return (number correct, list of (message number, expected, got) for the wrong ones)."""
    wrong = []
    for i, (text, expected) in enumerate(MESSAGES, start=1):
        got = llm.invoke(build_messages(examples, text)).content.strip().upper()
        if got != expected:
            wrong.append((i, expected, got))
    return len(MESSAGES) - len(wrong), wrong