from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from messages import MESSAGES

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0)

INSTRUCTION = "Classify the urgency of this support message as LOW, MEDIUM or HIGH. Reply with only the label."

# 1) Examples are plain data: a list of dicts, easy to swap or shuffle
EXAMPLES = [
    {"text": "Notifications arrive late on my tablet, though they work fine on my phone.", "label": "MEDIUM"},
    {"text": "PLEASE FIX!!! The settings page has a typo in the word 'preferences'.", "label": "LOW"},
    {"text": "My files from last month are missing after I restored a backup.", "label": "HIGH"},
]

# 2) How ONE example turns into messages
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "Message: {text}"),
    ("ai", "{label}"),
])

# 3) The few-shot block repeats that for every example
few_shot = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=EXAMPLES,
)

# 4) The final prompt: instruction, then examples, then the real input
final_prompt = ChatPromptTemplate.from_messages([
    ("system", INSTRUCTION),
    few_shot,
    ("human", "Message: {text}"),
])

# Look at what the model will receive, without calling it
for m in final_prompt.format_messages(text="How do I change my email address?"):
    print(f"[{m.type}] {m.content}")

chain = final_prompt | llm
correct = 0
wrong = []
for i, (text, expected) in enumerate(MESSAGES, start=1):
    got = chain.invoke({"text": text}).content.strip().upper()
    if got == expected:
        correct += 1
    else:
        wrong.append((i, expected, got))

print(f"\nTemplate score: {correct}/10   wrong: {wrong}")