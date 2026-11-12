from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

system = SystemMessage(content="You are a helpful assistant. Answer in one or two sentences.")
history = [system]   # this list IS the memory

def chat(user_text):
    history.append(HumanMessage(content=user_text))
    reply = model.invoke(history)       # send everything so far
    history.append(reply)               # reply is already an AIMessage, so just store it
    print(f"  (input tokens sent: {reply.usage_metadata['input_tokens']})")
    return reply.content

print("1:", chat("Hi! My name is Sam and I'm learning LangChain."))
print("2:", chat("My favourite programming language is Python."))
print("3:", chat("What is my name and my favourite language?"))

# The experiment: same third question, history dropped
no_history = [system, HumanMessage(content="What is my name and my favourite language?")]
print("3 (NO history):", model.invoke(no_history).content)