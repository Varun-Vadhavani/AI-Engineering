from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {persona}. Answer in at most two sentences."),
    MessagesPlaceholder("history"),     # the whole past conversation goes here
    ("human", "{question}"),
])

chain = prompt | model

history = []   # this list IS the memory

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