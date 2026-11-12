from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen2.5-coder:7b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {persona}. Answer in at most two sentences."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

chain = prompt | model

history = []

def chat(question, use_history=True):
    reply = chain.invoke({
        "persona": "friendly tutor",
        "history": history if use_history else [],
        "question": question,
    })
    if use_history:
        history.append(HumanMessage(content=question))
        history.append(reply)
    return reply.content

print("1:", chat("Hi, I'm Sam and I'm building a travel app."))
print("2:", chat("It will be for trips around Gujarat."))
print("3:", chat("What am I building and where?"))
print("3 (NO history):", chat("What am I building and where?", use_history=False))