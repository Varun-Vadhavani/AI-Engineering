from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from messages import MESSAGES

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

INSTRUCTION = ("Classify the urgency of this support message as LOW, MEDIUM or HIGH, "
               "then give a short reason. Reply in the format: LABEL | reason")

REPETITIVE = [
    ("Notifications arrive late on my tablet, though they work fine on my phone.",
     "MEDIUM | Customer reports a delay on one device while the other works."),
    ("PLEASE FIX!!! The settings page has a typo in the word 'preferences'.",
     "LOW | Customer reports a cosmetic typo with no effect on use."),
    ("My files from last month are missing after I restored a backup.",
     "HIGH | Customer reports lost data with no workaround."),
]

VARIED = [
    ("Notifications arrive late on my tablet, though they work fine on my phone.",
     "MEDIUM | Delayed on one device only; the other still works."),
    ("PLEASE FIX!!! The settings page has a typo in the word 'preferences'.",
     "LOW | Just a spelling slip, nothing is broken."),
    ("My files from last month are missing after I restored a backup.",
     "HIGH | Lost data and no way to get it back."),
]

def run(name, examples):
    msgs_base = [SystemMessage(content=INSTRUCTION)]
    for q, a in examples:
        msgs_base += [HumanMessage(content=f"Message: {q}"), AIMessage(content=a)]
    correct = copied = 0
    print(f"=== {name} ===")
    for text, expected in MESSAGES:
        out = llm.invoke(msgs_base + [HumanMessage(content=f"Message: {text}")]).content.strip()
        label, _, reason = out.partition("|")
        correct += label.strip().upper() == expected
        starts_same = reason.strip().lower().startswith("customer reports")
        copied += starts_same
        print(f"{'COPY' if starts_same else '    '} {label.strip().upper():6} |{reason}")
    print(f"labels correct: {correct}/10   reasons starting 'Customer reports': {copied}/10\n")

run("repetitive wording", REPETITIVE)
run("varied wording", VARIED)